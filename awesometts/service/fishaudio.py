# -*- coding: utf-8 -*-

# AwesomeTTS text-to-speech add-on for Anki
# Copyright (C) 2010-Present  Anki AwesomeTTS Development Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Service implementation for the Fish Audio service
https://fish.audio
"""

import requests
from .base import Service

__all__ = ['FishAudio']


VOICE_LIST = [
    ('b545c585f631496c914815291da4e893', 'English, Friendly Woman'),
    ('802e3bc2b27e49c2995d23ef70e6ac89', 'English, Energetic Male'),
    ('4ac32dd8d3304f5f8357acb1efb8d414', 'Chinese, 一只战鱼'),
    ('44bf01002da540c190df681410576aea', 'Chinese, 翔宇-硬朗风格广告配音'),
    ('b85f3ec7e48b4abfaa723d95c1cdaff5', 'Japanese, 草薙宁宁【nene】'),
]


class FishAudio(Service):
    """
    Provides a Service-compliant implementation for Fish Audio.
    """

    __slots__ = []

    NAME = "Fish Audio"

    # Although FIsh Audio is an Internet service, we do not mark it with
    # Trait.INTERNET, as it is a paid-for-by-the-user API, and we do not want
    # to rate-limit it or trigger error caching behavior
    TRAITS = []

    def desc(self):
        """Returns name with a voice count."""

        return "Fish Audio API (%d voices)" % len(VOICE_LIST)

    def extras(self):
        """The Fish Audio API requires an API key."""
        return [dict(key='key', label="API Key", required=True)]

    def options(self):
        """Provides access to voice only."""

        result = [
            dict(key='voice',
                 label="Voice",
                 values=VOICE_LIST,
                 transform=lambda value: value),
        ]

        return result

    def run(self, text, options, path):
        """Downloads from Fish Audio API directly to an MP3."""

        subscription_key = options['key']

        url = 'https://api.fish.audio/v1/tts'
        headers = {
            'Authorization': 'Bearer ' + subscription_key,
            'Content-Type': 'application/json',
        }

        payload = {
            "reference_id": options['voice'],
            "text": text,
            "format": "mp3"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            with open(path, 'wb') as audio:
                audio.write(response.content)
        else:
            error_message = f"Status code: {response.status_code} reason: {response.reason} voice: [{options['voice']}] " + \
            f"subscription key: [{subscription_key}]]"
            raise ValueError(error_message)
