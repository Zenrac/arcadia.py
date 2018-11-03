# -*- coding: utf-8 -*-

import aiohttp
import asyncio

from .errors import NotFound, Forbidden

try:
    import discord
except ImportError:
    _discord = False
else:
    if discord.__version__ != '1.0.0a':
        _discord = False
    else:
        _discord = True


class Client:
    def __init__(self, token: str = '', bot=None, loop=None):
        self._headers = {
            "User-Agent": "Arcadia.py (GitHub: Zenrac)",
            "Authorization": token
        }

        self.url = "https://arcadia-api.xyz/api/v1"
        self._loop = loop or asyncio.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.loop)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @classmethod
    def pluggable(cls, bot, token: str = "", *args, **kwargs):
        """
        Pluggable version of Client. Inserts Client directly into your Bot client.
        Called by using `bot.arcadia`

        Parameters

        bot: discord.ext.commands.Bot or discord.ext.commands.AutoShardedBot
            Your Bot client from discord.py

        token: str
            Your token from arcadia-api.xyz
        """

        if hasattr(bot, 'arcadia'):
            return bot.arcadia
        bot.arcadia = cls(token, bot=bot, *args, **kwargs)
        return bot.arcadia

    async def get_image(self, image_type: str, url: str, type: int = 0, discordfile: bool = True, generate: bool = False):
        """
        Basic get_image function using aiohttp

        Parameters

        image_type: str
            A valid image type from the list of available endpoints in the documentation : https://arcadia-api.xyz/

        url : str
            The image url parameter

        type : int, default to 0
            Some endpoint have multiple variants to the same image, type allows to get a specific one.

        discordfile : bool, default to True
            If enabled, try to return a discord.File object

        generate : bool, default to False
            If enabled, the parameters called 'url' becomes 'text', allows to get generated image from an endpoint.

        """
        async with self.session.get('{}/{}{}{}{}'.format(self.url, image_type.lower(), '?text=' if generate else '?url=', url,
                                                         '&type={}'.format(type) if type else ''), headers=self._headers) as response:
            if response.status != 200 and response.status != 403:
                raise NotFound('This resource does not exist or you are not allowed to access.')
            elif response.status == 403:
                raise Forbidden('You are not allowed to access this resource.')
            ext = response.content_type.split('/')[-1]
            img = await response.read()
        if _discord and discordfile:
            return discord.File(img, filename=f"image.{ext}")

        return img