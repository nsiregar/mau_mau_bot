#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import logging
from functools import wraps

from flufl.i18n import registry
from flufl.i18n import PackageStrategy

from telegram import Emoji
from telegram.ext.dispatcher import run_async
import locales
from database import db_session
from user_setting import UserSetting

strategy = PackageStrategy('unobot', locales)
application = registry.register(strategy)
_ = application._
logger = logging.getLogger(__name__)

TIMEOUT = 2.5


def __(string):
    """Translates text into all locales on the stack"""
    translations = list()
    locales = list()

    while True:
        translation = _(string)

        if translation not in translations:
            translations.append(translation)

        l = _.code
        _.pop()

        if l is None:
            break
        else:
            locales.append(l)

    for l in reversed(locales):
        _.push(l)

    return '\n'.join(translations)  # TODO


def list_subtract(list1, list2):
    """ Helper function to subtract two lists and return the sorted result """
    list1 = list1.copy()

    for x in list2:
        list1.remove(x)

    return list(sorted(list1))


def display_name(user):
    """ Get the current players name including their username, if possible """
    user_name = user.first_name
    if user.username:
        user_name += ' (@' + user.username + ')'
    return user_name


def display_color(color):
    """ Convert a color code to actual color name """
    if color == "r":
        return Emoji.HEAVY_BLACK_HEART + " Red"
    if color == "b":
        return Emoji.BLUE_HEART + " Blue"
    if color == "g":
        return Emoji.GREEN_HEART + " Green"
    if color == "y":
        return Emoji.YELLOW_HEART + " Yellow"


def error(bot, update, error):
    """Simple error handler"""
    logger.exception(error)


@run_async
def send_async(bot, *args, **kwargs):
    """Send a message asynchronously"""
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    try:
        bot.sendMessage(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


@run_async
def answer_async(bot, *args, **kwargs):
    """Answer an inline query asynchronously"""
    if 'timeout' not in kwargs:
        kwargs['timeout'] = TIMEOUT

    try:
        bot.answerInlineQuery(*args, **kwargs)
    except Exception as e:
        error(None, None, e)


def user_locale(func):
    @wraps(func)
    @db_session
    def wrapped(bot, update, *pargs, **kwargs):
        with db_session:
            us = UserSetting.get(id=update.message.from_user.id)
            if us:
                _.push(us.lang)
            else:
                _.push('en_US')
        result = func(bot, update, *pargs, **kwargs)
        _.pop()
        return result
    return wrapped


def game_locales(func):
    @wraps(func)
    @db_session
    def wrapped(*pargs, **kwargs):
        num_locales = 0
        for loc in ('en_US', 'de_DE'):  # TODO: Get user locales from Database
            _.push(loc)
            num_locales += 1

        result = func(*pargs, **kwargs)

        for i in range(num_locales):
            _.pop()
        return result
    return wrapped