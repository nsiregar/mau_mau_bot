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

# Modify this file if you want a different startup sequence, for example using
# a Webhook

from credentials import TOKEN

def start_bot(updater):
    #updater.start_polling()
    updater.start_webhook(listen = '0.0.0.0',
                          port = '8443',
                          url_path = 'TOKEN',
                          key = 'private.key',
                          cert = 'cert.pem',
                          webhook_url = 'https://IP_ADDRESS:8443/TOKEN')