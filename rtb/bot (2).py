import os
import sys
import time
import shlex
import shutil
import inspect
import logging
import asyncio
import pathlib
import traceback
import aiohttp
import discord
import colorlog
import json
import io
import platform
import wikipedia
import datetime
import logging
import copy
import requests
import markovify
import re
import random
import cleverbot

#python imports
from io import BytesIO, StringIO
from functools import wraps
from textwrap import dedent
from datetime import timedelta
from random import choice, shuffle
from collections import defaultdict
from concurrent.futures._base import TimeoutError as ConcurrentTimeoutError
from subprocess import call
from subprocess import check_output
from xml.dom import minidom

#discord imports
from discord.enums import ChannelType
from discord.ext.commands.bot import _get_variable
from discord.http import _func_
from discord import utils
from discord.object import Object
from discord.voice_client import VoiceClient

from . import exceptions
from . import downloader

#rtb imports
from .playlist import Playlist
from .player import MusicPlayer
from .entry import StreamPlaylistEntry
from .opus_loader import load_opus_lib
from .config import Config, ConfigDefaults
from .permissions import Permissions, PermissionsDefaults
from .constructs import SkipState, Response, VoiceStateUpdate
from .utils import load_file, write_file, download_file, sane_round_int, fixg, safe_print, extract_user_id
from .mysql import *

from .constants import VERSION as BOTVERSION
from .constants import DISCORD_MSG_CHAR_LIMIT, AUDIO_CACHE_PATH
from .constants import VER
from .constants import BDATE as BUILD
from .constants import MAINVER as MVER
from .constants import BUILD_USERNAME as BUNAME
from _operator import contains


load_opus_lib()
# initial time, or basically when the bot has started
inittime = time.time()
#color formattings
xl = "```xl\n{0}\n```"
rb = "```ruby\n{0}\n```"
py = "```py\n{0}\n```"
#command booleans
respond = True
change_game = True
owner_id = "117678528220233731" or "117053687045685248" or "169597963507728384"

#Discord Game Statuses! :D
dis_games = [
    discord.Game(name='with fire'),
    discord.Game(name='with Robin'),
    discord.Game(name='baa'),
    discord.Game(name='Denzel Curry - Ultimate'),
    discord.Game(name='Windows XP'),
    discord.Game(name='Drake - Jumpman'),
    discord.Game(name='with Kyle'),
    discord.Game(name='Super Smash Bros. Melee'),
    discord.Game(name='.help for help!'),
    discord.Game(name='how to lose a phone'),
    discord.Game(name='with memes'),
    discord.Game(name='Sergal'),
    discord.Game(name='Fox'),
    discord.Game(name='Dragon'),
    discord.Game(name='with some floof'),
    discord.Game(name='with Napstabot'),
    discord.Game(name='DramaNation'),
    discord.Game(name='browsing 4chan'),
    discord.Game(name="Guns N' Roses"),
    discord.Game(name='vaporwave'),
    discord.Game(name='being weird'),
    discord.Game(name='stalking Twitter'),
    discord.Game(name='Microsoft Messaging'),
    discord.Game(name="out in the club and I'm sippin' that bubb"),
    discord.Game(name="Let's get riiiiiiight into the news!"),
    discord.Game(name='Twenty One Pilots'),
    discord.Game(name='Twenty Juan Pilots'),
    discord.Game(name="I've gone batty!"),
    discord.Game(name='Lunatic under the moon'),
    discord.Game(name='with the idea of democratic socialism'),
    discord.Game(name='with the idea of a totalitarian dictatorship'),
    discord.Game(name="with Donald Trump's hair"),
    discord.Game(name='Quake'),
    discord.Game(name='Quake II'),
    discord.Game(name='Quake III Arena'),
    discord.Game(name='Here in my garage, just bought this, uh, new Lamborghini here.'),
    discord.Game(name='Cyka-Strike: Blyat Offensive'),
    discord.Game(name='the NSA for fools'),
    discord.Game(name='3.14159265358979323846264338327950288'),
    discord.Game(name="No more charades, my heart's been displayed"),
    discord.Game(name='I have a suggestion.'),
    discord.Game(name="If you're reading this, it's too late."),
    discord.Game(name='all the girls in the club'),
    discord.Game(name='all the guys in the club'),
    discord.Game(name='Never trust me with your secrets.'),
    discord.Game(name='Hey, you! I... I... I have a crush on you.'),
    discord.Game(name='Yandere Simulator'),
    discord.Game(name='VACation Simulator'),
    discord.Game(name='#BotLivesMatter'),
    discord.Game(name='with my DS'),
    discord.Game(name='learning Greek'),
    discord.Game(name='learning Japanese'),
    discord.Game(name='learning Swedish'),
    discord.Game(name='learning Spanish'),
    discord.Game(name='BLAME CANADA!'),
    discord.Game(name='Did you expect something witty and clever?'),
    discord.Game(name='hockey'),
    discord.Game(name='football'),
    discord.Game(name='basketball'),
    discord.Game(name='lacrosse'),
    discord.Game(name='baseball'),
    discord.Game(name='golf'),
    discord.Game(name='XDXDXDXDXDXDXD'),
    discord.Game(name='the game of nil.'),
    discord.Game(name='there are many knots i cannot untie.'),
    discord.Game(name='through the ceiling.'),
    discord.Game(name='(null)'),
    discord.Game(name='with my tiddy'),
    discord.Game(name='i have 9 bandaids on my penis'),
    discord.Game(name='explorer.exe'),
    discord.Game(name='tinder'),
    discord.Game(name='Minion Pregnancy flash game'),
    discord.Game(name='discord.Game(name="penis")'),
    discord.Game(name='tuna'),
    discord.Game(name='SUPER'),
    discord.Game(name='HOT'),
    discord.Game(name='I PLEDGE ALLEGIANCE, TO THE FLAG, OF THE UNITED STATES OF AMERICA.'),
    discord.Game(name='Capitalism is on its way out.'),
    discord.Game(name='THE SINGULARITY'),
    discord.Game(name='6.0221409e+23'),
    discord.Game(name='68'),
    discord.Game(name='ALT+F4'),
    discord.Game(name='Minecraft 2.0 baby XDXD'),
    discord.Game(name='where do babies come from?'),
    discord.Game(name='my uteri is expanding'),
    discord.Game(name='your mom XDDDDDDDDDDDD'),
    discord.Game(name='I am not a contributing member of society.'),
    discord.Game(name='Meincraft'),
    discord.Game(name='i dont know a lot of python.'),
    discord.Game(name='WILL'),
    discord.Game(name='ROBIN'),
    discord.Game(name='DREW'),
    discord.Game(name='ITS THE LAW.'),
    discord.Game(name='DOOM'),
    discord.Game(name='Fallout Shelter is now available for PC! Install it now.'),
    discord.Game(name='9:30 PM'),
    discord.Game(name='why would anyone think that this is my golden ticket idea?'),
    discord.Game(name='PRESSURE, PRESSURE, NOOSE AROUND MY NECK'),
    discord.Game(name='jenna is cute'),
    discord.Game(name='crippling social anxiety'),
    discord.Game(name='HMU ON YOUTUBE: http://youtube.com/c/FUCKBOIS2016'),
    discord.Game(name='Ow, my head hurts.')
]

#Regex for IP addresses
ipv4_regex = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
#don't you just hate ipv6?
ipv6_regex = re.compile(
    r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')

#rating system numbers
ratelevel = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

#for the perf command, i might eventually remove it smh
tweetsthatareokhand = [
    "http://i.imgur.com/lkMJ1O9.png",
    "http://i.imgur.com/rbGmZqV.png",
    "http://i.imgur.com/hYzNxVR.png",
    "http://i.imgur.com/JuVsIMg.png",
    "http://i.imgur.com/2NYwUcj.png",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222734961442817/uh_semen.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222732260442113/train_of_horses.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222728338636802/they_wshiper.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222725977243650/thats_my_boyfriend.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222723175579650/pinned.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222720667385858/list.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222717743824907/idea_of_music.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222715147550721/goals.PNG",
    "https://cdn.discordapp.com/attachments/173887966031118336/177222711867604993/disturbing_fetish.PNG",
    #    "here's a message from the coder of this: I FUCKING RAN OUT NEEDS MORE CHEESE",
    # not anymore, its like what 21 links
    "​https://cdn.discordapp.com/attachments/173886531080159234/176425292426903553/f20e683862a17ef49633eed742fc2b22eb17220eef5a1d607cda2e7a7758720b_1.jpg",
    "http://i.imgur.com/m71nJAg.png",
    "http://i.imgur.com/m5fx7U9.png",
    "https://cdn.discordapp.com/attachments/173887966031118336/177518766781890562/your-resistance-only-makes-my-penis-harder.jpg",
    "http://i.imgur.com/21bV05w.png",
    "http://i.imgur.com/7Y94F7L.png"
]

#the .kill command messages
suicidalmemes = [
    "what the hell did you do idiot",
    "wtf ok idiot fool",
    "you killed him nice job.",
    "lmao you killed him gg on your killing :ok_hand:",
    "party on his death? lit",
    "fuckin fag wtf no.... y..."
]

#the super fucking long throw command
throwaf = [
    "a keyboard",
    "a Playstation 4",
    "a PSP with Crash Bandicoot 2 on it",
    "a fur coat",
    "furtrash called art",
    "a british trash can",
    "a raincoat made with :heart:",
    "some shitty pencil, it's definitely useless",
    "a dragon",
    "a Lightning Dragon",
    "Mαxie",
    "Robin",
    "a water bucket",
    "water",
    "a shamrock shake",
    "flowers",
    "some fisting",
    "a RoboNitori message",
    "a ice cream cone",
    "hot ass pie, and it's strawberry",
    "a strawberry ice cream cone",
    "Visual Studio 2015",
    "Toshiba Satellite laptop with Spotify, Guild Wars 2 and Visual Studio on it",
    "a compass",
    "honk honk",
    "pomfpomfpomf",
    "⑨",
    "a watermelone",
    "FUCKING PAPERCLIP",
    "HTTP Error 403",
    "Error 429",
    "`never`",
    "`an error that should be regretted of`",
    "Georgia",
    "New York",
    "Nevada",
    "Michigan",
    "Florida",
    "California",
    "TEEEEEEXASSSSSSS",
    "a climaxing dragon picture"
    "Nebraska",
    "an ok ok please message",
    "a pleb called EJH2",
    "15 dust bunnies, a water bottle, and a iron hammer to ban people with",
    "a broken glass (dance bitch)",
    "ok ok",
    "allergy pills",
    "a Chocolate Calculator",
    "probably not Bad Dragon toy",
    "aww yiss a piece of WORLD DOMINATION POWER",
    "a prime minister from Canada",
    "Indiana",
    "a coca-cola bottle",
    "a DJ System",
    "a fridge with wifi enabled",
    "a router",
    "a modem box",
    "a Napstabot",
    "another RoboNitori sentence",
    "a phone",
    "a fan",
    "a pair of earphones",
    "Excel document",
    "Paint Tool SAI painting",
    "Word Document",
    "Visual Studio Project",
    "nerd thing",
    "python 3.5 py",
    "fuckin office tool",
    "clippy",
    "dat boi meme",
    "random.jpeg",
    "Danny DeVito",
    "Deadpool",
    "a Lenovo Keyboard",
    "Life of Pablo",
    "a Mexican called Ambrosio",
    "the most obvious dick master",
    "Motopuffs",
    "Motopuffs",
    "the dick master called Motopuffs",
    "a weeaboo",
    "Ryulise, the stupid smash master",
    "death, at its finest",
    "morth, but not in its final form",
    "some flaccid sword"
]

log = logging.getLogger(__name__)

#showing off specs class
class PlatformSpecs:
    def __init__(self):
        self.platformObj = platform
        self.machine = platform.machine()
        self.version = platform.version()
        self.platform = platform.platform()
        self.uname = platform.uname()
        self.system = platform.system()
        self.processor = platform.processor()

    def getPlatObj(self):
        return self.platformObj

    def getMachine(self):
        return self.machine

    def getVersion(self):
        return self.version

    def getPlatform(self):
        return self.platform

    def getPlatUName(self):
        return self.uname

    def getSys(self):
        return self.system

    def getProcessor(self):
        return self.processor

#the entire music bot class
class RobTheBoat(discord.Client):
    def __init__(self, config_file=None, perms_file=None):
        if config_file is None:
            config_file = ConfigDefaults.options_file

        if perms_file is None:
            perms_file = PermissionsDefaults.perms_file

        #essential player defs
        self.players = {}
        self.exit_signal = None
        self.init_ok = False
        self.cached_app_info = None
        self.last_status = None

        self.config = Config(config_file)
        self.permissions = Permissions(perms_file, grant_all=[self.config.owner_id])

        self.blacklist = set(load_file(self.config.blacklist_file))
        self.autoplaylist = load_file(self.config.auto_playlist_file)

        self.aiolocks = defaultdict(asyncio.Lock)
        self.downloader = downloader.Downloader(download_folder='audio_cache')

        self._setup_logging()
        #my shit
        self.uptime = datetime.datetime.utcnow()
        self.command_prefix = self.config.command_prefix

        if not self.autoplaylist:
            log.warning("Autoplaylist is empty, disabling.")
            self.config.auto_playlist = False
        else:
            log.info("Loaded autoplaylist with {} entries".format(len(self.autoplaylist)))

        if self.blacklist:
            log.debug("Loaded blacklist with {} entries".format(len(self.blacklist)))

        # TODO: Do these properly
        ssd_defaults = {
            'last_np_msg': None,
            'auto_paused': False,
            'availability_paused': False
        }
        self.server_specific_data = defaultdict(lambda: dict(ssd_defaults)) # yes, this is supposed to be like this, dict(...)

        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' RobTheBoat Discord/%s' % BOTVERSION

    def __del__(self):
        try:
            if not self.http.session.closed:
                self.http.session.close()
        except: pass

        try:
            if not self.aiosession.closed:
                self.aiosession.close()
        except: pass

    # TODO: Add some sort of `denied` argument for a message to send when someone else tries to use it
    def owner_only(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Only allow the owner to use these commands
            orig_msg = _get_variable('message')

            if not orig_msg or orig_msg.author.id == self.config.owner_id:
                # noinspection PyCallingNonCallable
                return await func(self, *args, **kwargs)
            else:
                raise exceptions.PermissionsError("Only the owner can use these type of commands.", expire_in=30)

        return wrapper

    def dev_only(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            orig_msg = _get_variable('message')

            if orig_msg.author.id in self.config.dev_ids:
                # noinspection PyCallingNonCallable
                return await func(self, *args, **kwargs)
            else:
                raise exceptions.PermissionsError("Only the developers can use these commands.", expire_in=30)

        wrapper.dev_cmd = True
        return wrapper

    def ensure_appinfo(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            await self._cache_app_info()
            # noinspection PyCallingNonCallable
            return await func(self, *args, **kwargs)

        return wrapper

    def _get_owner(self, *, server=None, voice=False):
            return discord.utils.find(
                lambda m: m.id == self.config.owner_id and (m.voice_channel if voice else True),
                server.members if server else self.get_all_members()
            )

    def _delete_old_audiocache(self, path=AUDIO_CACHE_PATH):
        try:
            shutil.rmtree(path)
            return True
        except:
            try:
                os.rename(path, path + '__')
            except:
                return False
            try:
                shutil.rmtree(path)
            except:
                os.rename(path + '__', path)
                return False

        return True

    #terminal logging, and logging to files
    def _setup_logging(self):
        if len(logging.getLogger(__package__).handlers) > 1:
            log.debug("Already setup loggers?")
            return

        shandler = logging.StreamHandler(stream=sys.stdout)
        shandler.setFormatter(colorlog.LevelFormatter(
            fmt = {
                'DEBUG': '{log_color}[{levelname}:{module}] {message}',
                'INFO': '{log_color}{message}',
                'WARNING': '{log_color}{levelname}: {message}',
                'ERROR': '{log_color}[{levelname}:{module}] {message}',
                'CRITICAL': '{log_color}[{levelname}:{module}] {message}',

                'EVERYTHING': '{log_color}[{levelname}:{module}] {message}',
                'NOISY': '{log_color}[{levelname}:{module}] {message}',
                'VOICEDEBUG': '{log_color}[{levelname}:{module}][{relativeCreated:.9f}] {message}',
                'FFMPEG': '{log_color}[{levelname}:{module}][{relativeCreated:.9f}] {message}'
            },
            log_colors = {
                'DEBUG':    'cyan',
                'INFO':     'white',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',

                'EVERYTHING': 'white',
                'NOISY':      'white',
                'FFMPEG':     'bold_purple',
                'VOICEDEBUG': 'purple',
        },
            style = '{',
            datefmt = ''
        ))
        shandler.setLevel(self.config.debug_level)
        logging.getLogger(__package__).addHandler(shandler)

        log.debug("Set logging level to {}".format(self.config.debug_level_str))

        if self.config.debug_mode:
            dlogger = logging.getLogger('discord')
            dlogger.setLevel(logging.DEBUG)
            dhandler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
            dhandler.setFormatter(logging.Formatter('{asctime}:{levelname}:{name}: {message}', style='{'))
            dlogger.addHandler(dhandler)

    @staticmethod
    def _check_if_empty(vchannel: discord.Channel, *, excluding_me=True, excluding_deaf=False):
        def check(member):
            if excluding_me and member == vchannel.server.me:
                return False

            if excluding_deaf and any([member.deaf, member.self_deaf]):
                return False

            return True

        return not sum(1 for m in vchannel.voice_members if check(m))


    async def _join_startup_channels(self, channels, *, autosummon=True):
        joined_servers = set()
        channel_map = {c.server: c for c in channels}

        def _autopause(player):
            if self._check_if_empty(player.voice_client.channel):
                log.info("Initial autopause in empty channel")

                player.pause()
                self.server_specific_data[player.voice_client.channel.server]['auto_paused'] = True

        for server in self.servers:
            if server.unavailable or server in channel_map:
                continue

            if server.me.voice_channel:
                log.info("Found resumable voice channel {0.server.name}/{0.name}".format(server.me.voice_channel))
                channel_map[server] = server.me.voice_channel

            if autosummon:
                owner = self._get_owner(server=server, voice=True)
                if owner:
                    log.info("Found owner in \"{}\"".format(owner.voice_channel.name))
                    channel_map[server] = owner.voice_channel

        for server, channel in channel_map.items():
            if server in joined_servers:
                log.info("Already joined a channel in \"{}\", skipping".format(server.name))
                continue

            if channel and channel.type == discord.ChannelType.voice:
                log.info("Attempting to join {0.server.name}/{0.name}".format(channel))

                chperms = channel.permissions_for(server.me)

                if not chperms.connect:
                    log.info("Cannot join channel \"{}\", no permission.".format(channel.name))
                    continue

                elif not chperms.speak:
                    log.info("Will not join channel \"{}\", no permission to speak.".format(channel.name))
                    continue

                try:
                    player = await self.get_player(channel, create=True, deserialize=True)

                    log.info("Joined {0.server.name}/{0.name}".format(channel))

                    if player.is_stopped:
                        player.play()

                    joined_servers.add(server)

                    if self.config.auto_playlist:
                        await self.on_player_finished_playing(player)
                        if self.config.auto_pause:
                            player.once('play', lambda player, **_: _autopause(player))

                except Exception:
                    log.debug("Error joining {0.server.name}/{0.name}".format(channel), exc_info=True)
                    log.error("Failed to join {0.server.name}/{0.name}".format(channel))

            elif channel:
                log.warning("Not joining {0.server.name}/{0.name}, that's a text channel.".format(channel))

            else:
                log.warning("Invalid channel thing: {}".format(channel))

    async def _wait_delete_msg(self, message, after):
        await asyncio.sleep(after)
        await self.safe_delete_message(message, quiet=True)

    # TODO: Check to see if I can just move this to on_message after the response check
    async def _manual_delete_check(self, message, *, quiet=False):
        if self.config.delete_invoking:
            await self.safe_delete_message(message, quiet=quiet)

    async def _check_ignore_non_voice(self, msg):
        vc = msg.server.me.voice_channel

        # If we've connected to a voice chat and we're in the same voice channel
        if not vc or vc == msg.author.voice_channel:
            return True
        else:
            raise exceptions.PermissionsError(
                "oh no guess what, you can't use this if you aren't in the voice channel called (%s), idiot" % vc.name, expire_in=30)

    async def _cache_app_info(self, *, update=False):
        if not self.cached_app_info and not update and self.user.bot:
            log.debug("Caching app info")
            self.cached_app_info = await self.application_info()

        return self.cached_app_info


    async def remove_from_autoplaylist(self, song_url:str, *, ex:Exception=None, delete_from_ap=False):
        if song_url not in self.autoplaylist:
            log.debug("URL \"{}\" not in autoplaylist, ignoring".format(song_url))
            return

        async with self.aiolocks[_func_()]:
            self.autoplaylist.remove(song_url)
            log.info("Removing unplayable song from autoplaylist: %s" % song_url)

            with open(self.config.auto_playlist_removed_file, 'a', encoding='utf8') as f:
                f.write(
                    '# Entry removed {ctime}\n'
                    '# Reason: {ex}\n'
                    '{url}\n\n{sep}\n\n'.format(
                        ctime=time.ctime(),
                        ex=str(ex).replace('\n', '\n#' + ' ' * 10), # 10 spaces to line up with # Reason:
                        url=song_url,
                        sep='#' * 32
                ))

            if delete_from_ap:
                log.info("Updating autoplaylist")
                write_file(self.config.auto_playlist_file, self.autoplaylist)

    @ensure_appinfo
    async def generate_invite_link(self, *, permissions=discord.Permissions(70380544), server=None):
        return discord.utils.oauth_url(self.cached_app_info.id, permissions=permissions, server=server)


    async def join_voice_channel(self, channel):
        if isinstance(channel, discord.Object):
            channel = self.get_channel(channel.id)

        if getattr(channel, 'type', ChannelType.text) != ChannelType.voice:
            raise discord.InvalidArgument('Channel passed must be a voice channel')

        server = channel.server

        if self.is_voice_connected(server):
            raise discord.ClientException('already connected to a voice channel on this server, please do .disconnect then .connect to continue')

        def session_id_found(data):
            user_id = data.get('user_id')
            guild_id = data.get('guild_id')
            return user_id == self.user.id and guild_id == server.id

        log.voicedebug("(%s) creating futures", _func_())
        # register the futures for waiting
        session_id_future = self.ws.wait_for('VOICE_STATE_UPDATE', session_id_found)
        voice_data_future = self.ws.wait_for('VOICE_SERVER_UPDATE', lambda d: d.get('guild_id') == server.id)

        # request joining
        log.voicedebug("(%s) setting voice state", _func_())
        await self.ws.voice_state(server.id, channel.id)

        log.voicedebug("(%s) waiting for session id", _func_())
        session_id_data = await asyncio.wait_for(session_id_future, timeout=15, loop=self.loop)

        log.voicedebug("(%s) waiting for voice data", _func_())
        data = await asyncio.wait_for(voice_data_future, timeout=15, loop=self.loop)

        kwargs = {
            'user': self.user,
            'channel': channel,
            'data': data,
            'loop': self.loop,
            'session_id': session_id_data.get('session_id'),
            'main_ws': self.ws
        }

        voice = discord.VoiceClient(**kwargs)
        try:
            log.voicedebug("(%s) connecting...", _func_())
            with aiohttp.Timeout(15):
                await voice.connect()
        except asyncio.TimeoutError as e:
            log.voicedebug("(%s) connection failed, disconnecting", _func_())
            try:
                await voice.disconnect()
            except:
                pass
            raise e

        log.voicedebug("(%s) connection successful", _func_())

        self.connection._add_voice_client(server.id, voice)
        return voice


    async def get_voice_client(self, channel: discord.Channel):
        if isinstance(channel, discord.Object):
            channel = self.get_channel(channel.id)

        if getattr(channel, 'type', ChannelType.text) != ChannelType.voice:
            raise AttributeError('Channel passed must be a voice channel')

        async with self.aiolocks[_func_() + ':' + channel.server.id]:
            if self.is_voice_connected(channel.server):
                return self.voice_client_in(channel.server)

            vc = None
            t0 = t1 = 0
            tries = 5

            for attempt in range(1, tries+1):
                log.debug("Connection attempt {} to {}".format(attempt, channel.name))
                t0 = time.time()

                try:
                    vc = await self.join_voice_channel(channel)
                    t1 = time.time()
                    break

                except ConcurrentTimeoutError:
                    log.warning("Failed to connect, retrying ({}/{})".format(attempt, tries))
                    try:
                        await self.ws.voice_state(channel.server.id, None)
                    except:
                        pass

                except:
                    log.exception("Unknown error attempting to connect to voice")

                await asyncio.sleep(0.5)

            if not vc:
                log.critical("Voice client is unable to connect")
                raise exceptions.RestartSignal() # fuck it

            log.debug("Connected in {:0.1f}s".format(t1-t0))

            vc.ws._keep_alive.name = 'VoiceClient Keepalive'

            return vc

    async def reconnect_voice_client(self, server, *, sleep=0.1, channel=None):
        log.debug("Reconnecting voice client on \"{}\"{}".format(
            server, ' to "{}"'.format(channel.name) if channel else ''))

        async with self.aiolocks[_func_() + ':' + server.id]:
            vc = self.voice_client_in(server)

            if not (vc or channel):
                return

            _paused = False
            player = self.get_player_in(server)

            if player and player.is_playing:
                log.voicedebug("(%s) Pausing", _func_())

                player.pause()
                _paused = True

            log.voicedebug("(%s) Disconnecting", _func_())

            try:
                await vc.disconnect()
            except:
                pass

            if sleep:
                log.voicedebug("(%s) Sleeping for %s", _func_(), sleep)
                await asyncio.sleep(sleep)

            if player:
                log.voicedebug("(%s) Getting voice client", _func_())

                if not channel:
                    new_vc = await self.get_voice_client(vc.channel)
                else:
                    new_vc = await self.get_voice_client(channel)

                log.voicedebug("(%s) Reloading voice client", _func_())
                await player.reload_voice(new_vc)

                if player.is_paused and _paused:
                    log.voicedebug("Resuming")
                    player.resume()

        log.debug("Reconnected voice client on \"{}\"{}".format(
            server, ' to "{}"'.format(channel.name) if channel else ''))

    async def disconnect_voice_client(self, server):
        vc = self.voice_client_in(server)
        if not vc:
            return

        if server.id in self.players:
            self.players.pop(server.id).kill()

        await vc.disconnect()

    async def disconnect_all_voice_clients(self):
        for vc in list(self.voice_clients).copy():
            await self.disconnect_voice_client(vc.channel.server)

    async def set_voice_state(self, vchannel, *, mute=False, deaf=False):
        if isinstance(vchannel, discord.Object):
            vchannel = self.get_channel(vchannel.id)

        if getattr(vchannel, 'type', ChannelType.text) != ChannelType.voice:
            raise AttributeError('Channel passed must be a voice channel')

        await self.ws.voice_state(vchannel.server.id, vchannel.id, mute, deaf)
        # I hope I don't have to set the channel here
        # instead of waiting for the event to update it

    def get_player_in(self, server: discord.Server) -> MusicPlayer:
        return self.players.get(server.id)

    async def get_player(self, channel, create=False, *, deserialize=False) -> MusicPlayer:
        server = channel.server

        async with self.aiolocks[_func_() + ':' + server.id]:
            if deserialize:
                voice_client = await self.get_voice_client(channel)
                player = await self.deserialize_queue(server, voice_client)

                if player:
                    log.debug("Created player via deserialization for server %s", server.id)
                    return self._init_player(player, server=server)

            if server.id not in self.players:
                if not create:
                    raise exceptions.CommandError(
                        'Bot isn\'t in a voice channel.  '
                        'Use %sconnect to connect to it to your voice channel' % self.config.command_prefix)

                voice_client = await self.get_voice_client(channel)

                playlist = Playlist(self)
                player = MusicPlayer(self, voice_client, playlist)
                self._init_player(player, server=server)

            async with self.aiolocks[self.reconnect_voice_client.__name__ + ':' + server.id]:
                if self.players[server.id].voice_client not in self.voice_clients:
                    log.debug("Reconnect required for voice client in {}".format(server.name))
                    await self.reconnect_voice_client(server, channel=channel)

        return self.players[server.id]

    def _init_player(self, player, *, server=None):
        player = player.on('play', self.on_player_play) \
                       .on('resume', self.on_player_resume) \
                       .on('pause', self.on_player_pause) \
                       .on('stop', self.on_player_stop) \
                       .on('finished-playing', self.on_player_finished_playing) \
                       .on('entry-added', self.on_player_entry_added) \
                       .on('error', self.on_player_error)
        player.skip_state = SkipState()

        if server:
            self.players[server.id] = player

        return player


    async def on_player_play(self, player, entry):
        await self.update_now_playing(entry)
        player.skip_state.reset()

        log.debug("Serialize queue in %s", _func_())

        channel = entry.meta.get('channel', None)
        author = entry.meta.get('author', None)

        if channel and author:
            last_np_msg = self.server_specific_data[channel.server]['last_np_msg']
            if last_np_msg and last_np_msg.channel == channel:

                async for lmsg in self.logs_from(channel, limit=1):
                    if lmsg != last_np_msg and last_np_msg:
                        await self.safe_delete_message(last_np_msg)
                        self.server_specific_data[channel.server]['last_np_msg'] = None
                    break  # This is probably redundant

            if self.config.now_playing_mentions:
                newmsg = 'hey.... %s.... - your song **%s** is now playing in %s...' % (
                    entry.meta['author'].mention, entry.title, player.voice_client.channel.name)
            else:
                newmsg = 'Now it\'s time to play **%s** in *%s*' % (
                    entry.title, player.voice_client.channel.name)

            if self.server_specific_data[channel.server]['last_np_msg']:
                self.server_specific_data[channel.server]['last_np_msg'] = await self.safe_edit_message(last_np_msg, newmsg, send_if_fail=True)
            else:
                self.server_specific_data[channel.server]['last_np_msg'] = await self.safe_send_message(channel, newmsg)

    async def on_player_resume(self, player, entry, **_):
        await self.update_now_playing(entry)

    async def on_player_pause(self, player, entry, **_):
        await self.update_now_playing(entry, True)

    async def on_player_stop(self, player, **_):
        await self.update_now_playing()

    async def on_player_finished_playing(self, player, **_):
        if not player.playlist.entries and not player.current_entry and self.config.auto_playlist:
            while self.autoplaylist:
                song_url = choice(self.autoplaylist)
                # TODO: fix rng
                info = None

                try:
                    info = await self.downloader.extract_info(player.playlist.loop, song_url, download=False, process=False)
                except downloader.youtube_dl.utils.DownloadError as e:
                    if 'YouTube said:' in e.args[0]:
                        # url is bork, remove from list and put in removed list
                        log.error("Error processing youtube url:\n{}".format(e.args[0]))

                    else:
                        # Probably an error from a different extractor, but I've only seen youtube's
                        log.error("Error processing \"{url}\": {ex}".format(url=song_url, ex=e))

                    await self.remove_from_autoplaylist(song_url, ex=e, delete_from_ap=True)
                    continue

                except Exception as e:
                    log.error("Error processing \"{url}\": {ex}".format(url=song_url, ex=e))
                    log.debug('', exc_info=True)

                    self.autoplaylist.remove(song_url)
                    continue

                if info.get('entries', None):  # or .get('_type', '') == 'playlist'
                    log.debug("Playlist found but is unsupported at this time, skipping.")
                    # TODO: Playlist expansion

                # TODO: better checks here
                try:
                    await player.playlist.add_entry(song_url, channel=None, author=None)
                except exceptions.ExtractionError as e:
                    log.error("Error adding song from autoplaylist: {}".format(e))
                    log.debug('', exc_info=True)
                    continue

                break

            if not self.autoplaylist:
                log.warning("No playable songs in the autoplaylist, disabling.")
                self.config.auto_playlist = False

        log.debug("Serialize queue in %s", _func_())

    async def on_player_entry_added(self, player, playlist, entry, **_):
        log.debug("Serialize queue in %s", _func_())

    async def on_player_error(self, player, entry, ex, **_):
        if 'channel' in entry.meta:
            await self.safe_send_message(
                entry.meta['channel'],
                "```\nError from FFmpeg:\n{}\n```".format(ex)
            )
        else:
            log.exception("Player error", exc_info=ex)
            # Maybe change to logging call with format_exception?
            # traceback.print_exception(ex.__class__, ex, ex.__traceback__)

    async def update_now_playing(self, entry=None, is_paused=False):
        if change_game is False:
            return
        game = None

        if self.user.bot:
            activeplayers = sum(1 for p in self.players.values() if p.is_playing)
            if activeplayers > 1:
                #game = discord.Game(name="music on %s servers" % activeplayers)
                game = random.choice(dis_games)
                entry = None

            elif activeplayers == 1:
                player = discord.utils.get(self.players.values(), is_playing=True)
                entry = player.current_entry

        if entry:
            prefix = u'\u275A\u275A ' if is_paused else ''

            name = u'{}{}'.format(prefix, entry.title)[:128]
            game = random.choice(dis_games)

        #await self.change_status(game)
        async with self.aiolocks[_func_()]:
            if game == self.last_status:
                return

            await self.change_status(game)
            self.last_status = game

    async def serialize_queue(self, server, *, dir=None):
        """
        Serialize the cuerrent queue for a server's player to json.
        """

        player = self.get_player_in(server)
        if not player:
            return
        if dir is None:
            dir = 'data/%s/queue.json' % server.id

        async with self.aiolocks['queue_serialization'+':'+server.id]:
            log.debug("Serializing queue for %s", server.id)

            with open(dir, 'w', encoding='utf8') as f:
                f.write(player.serialize())

    async def serialize_all_queues(self, *, dir=None):
        coros = [self.serialize_queue(s, dir=dir) for s in self.servers]
        await asyncio.gather(*coros, return_exceptions=True)

    async def deserialize_queue(self, server, voice_client, playlist=None, *, dir=None) -> MusicPlayer:
        """
        Deserialize a saved queue for a server into a MusicPlayer.  If no queue is saved, returns None.
        """

        if playlist is None:
            playlist = Playlist(self)

        if dir is None:
            dir = 'data/%s/queue.json' % server.id

        async with self.aiolocks['queue_serialization' + ':' + server.id]:
            if not os.path.isfile(dir):
                return None

            log.debug("Deserializing queue for %s", server.id)

            with open(dir, 'r', encoding='utf8') as f:
                data = f.read()

        return MusicPlayer.from_json(data, self, voice_client, playlist)

    @ensure_appinfo
    async def _on_ready_sanity_checks(self):
        #Ensure folders exist
        await self._scheck_ensure_env()

        # Server permissions check
        await self._scheck_server_permissions()

        # playlists in autoplaylist
        await self._scheck_autoplaylist()

        # config/permissions async validate?
        await self._scheck_configs()

    async def _scheck_ensure_env(self):
        log.debug("Ensuring data folders exist")
        for server in self.servers:
            pathlib.Path('data/%s/' % server.id).mkdir(exist_ok=True)

        with open('data/server_names.txt', 'w', encoding='utf8') as f:
            for server in sorted(self.servers, key=lambda s: int(s.id)):
                f.write('{:<22} {}\n'.format(server.id, server.name))

        if not self.config.save_videos and os.path.isdir(AUDIO_CACHE_PATH):
            if self._delete_old_audiocache():
                log.debug("Deleted old audio cache")
            else:
                log.debug("Could not delete old audio cache, moving on.")

    async def _scheck_server_permissions(self):
        log.debug("Checking server permissions")
        pass # TODO

    async def _scheck_autoplaylist(self):
        log.debug("Auditing autoplaylist")
        pass  # TODO

    async def _scheck_configs(self):
        log.debug("Validating config")
        await self.config.async_validate(self)
        log.debug("Validating permissions config")
        await self.permissions.async_validate(self)

#######################################################################################################################
    async def safe_send_message(self, dest, content, *, tts=False, expire_in=0, also_delete=None, quiet=False, allow_none=True):
        msg = None
        lfunc = log.debug if quiet else log.warning

        try:
            if content is not None or allow_none:
                msg = await self.send_message(dest, content, tts=tts)

        except discord.Forbidden:
            lfunc("Cannot send message to \"{}\", no permission".format(dest.name))

        except discord.NotFound:
            lfunc("Cannot send message to \"{}\", invalid channel?".format(dest.name))

        except discord.HTTPException:
            pass

        finally:
            if msg and expire_in:
                asyncio.ensure_future(self._wait_delete_msg(msg, expire_in))

            if also_delete and isinstance(also_delete, discord.Message):
                asyncio.ensure_future(self._wait_delete_msg(also_delete, expire_in))

        return msg

    async def safe_delete_message(self, message, *, quiet=False):
        lfunc = log.debug if quiet else log.warning

        try:
            return await self.delete_message(message)

        except discord.Forbidden:
            lfunc("Cannot delete message \"{}\", no permission".format(message.clean_content))

        except discord.NotFound:
            lfunc("Cannot delete message \"{}\", message not found".format(message.clean_content))

    async def safe_edit_message(self, message, new, *, send_if_fail=False, quiet=False):
        lfunc = log.debug if quiet else log.warning

        try:
            return await self.edit_message(message, new)

        except discord.NotFound:
            lfunc("Cannot edit message \"{}\", message not found".format(message.clean_content))
            if send_if_fail:
                lfunc("Sending message instead")
                return await self.safe_send_message(message.channel, new)

    async def send_typing(self, destination):
        try:
            return await super().send_typing(destination)
        except discord.Forbidden:
            log.warning("Could not send typing to {}, no permssion".format(destination))

    async def edit_profile(self, **fields):
        if self.user.bot:
            return await super().edit_profile(**fields)
        else:
            return await super().edit_profile(self.config._password,**fields)

    def _cleanup(self):
        try:
            self.loop.run_until_complete(self.logout())
        except: # Can be ignored
            pass

        pending = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*pending)

        try:
            gathered.cancel()
            self.loop.run_until_complete(gathered)
            gathered.exception()
        except: # Can be ignored
            pass

    # noinspection PyMethodOverriding
    def run(self):
        try:
            self.loop.run_until_complete(self.start(*self.config.auth))

        except discord.errors.LoginFailure:
            # Add if token, else
            raise exceptions.HelpfulError(
                "Bot cannot login, bad credentials.",
                "Fix your Email or Password or Token in the options file.  "
                "Remember that each field should be on their own line.")

        finally:
            try:
                self._cleanup()
            except Exception:
                log.error("Error in cleanup", exc_info=True)

            self.loop.close()
            if self.exit_signal:
                raise self.exit_signal()

    async def logout(self):
        await self.disconnect_all_voice_clients()
        return await super().logout()

    async def on_error(self, event, *args, **kwargs):
        ex_type, ex, stack = sys.exc_info()

        if ex_type == exceptions.HelpfulError:
            log.error("Exception in {}:\n{}".format(event, ex.message))

            await asyncio.sleep(2)  # don't ask
            await self.logout()

        elif issubclass(ex_type, exceptions.Signal):
            self.exit_signal = ex_type
            await self.logout()

        else:
            log.error("Exception in {}".format(event), exc_info=True)

    async def on_resumed(self):
        log.info("\nReconnected to discord.\n")

    async def on_ready(self):
        log.debug("Connection established, ready to go.")

        self.ws._keep_alive.name = 'Gateway Keepalive'

        if self.init_ok:
            log.debug("Received additional READY event, may have failed to resume")
            return

        await self._on_ready_sanity_checks()
        print()

        #Discord Bots JSON thing
        abalishorny = len(self.servers)
        r = requests.post('https://bots.discord.pw/api/bots/' + self.user.id + '/stats', json={"server_count": abalishorny},
                          headers={
                              'Authorization': self.config._abaltoken})
        if r.status_code == int(200):
            log.info('Discord Bots count updated!')
        elif r.status_code == int(401):
            log.error('Failed to update discord bots count, error 401')
        elif r.status_code == int(403):
            log.error('Failed to update count, you sure you\'re using the right auth key?')

        log.info('Connected! RTB System v{}\n'.format(BOTVERSION))

        self.init_ok = True

        ################################

        log.info("Bot:   {0}/{1}#{2}{3}".format(
            self.user.id,
            self.user.name,
            self.user.discriminator,
            ' [BOT]' if self.user.bot else ' [Userbot]'
        ))

        owner = self._get_owner(voice=True) or self._get_owner()
        if owner and self.servers:
            log.info("Owner: {0}/{1}#{2}\n".format(
                owner.id,
                owner.name,
                owner.discriminator
            ))

            log.info('Server List:')
            [log.info(' - ' + s.name) for s in self.servers]

        elif self.servers:
            log.warning("Owner could not be found on any server (id: %s)\n" % self.config.owner_id)

            log.info('Server List:')
            [log.info(' - ' + s.name) for s in self.servers]

        else:
            log.warning("Owner unknown, bot is not on any servers.")
            if self.user.bot:
                log.warning(
                    "\nTo make the bot join a server, paste this link in your browser."
                    "Note: You should be logged into your main account and have \n"
                    "manage server permissions on the server you want the bot to join.\n"
                    "  " + await self.generate_invite_link()
                )

        print(flush=True)

        if self.config.bound_channels:
            chlist = set(self.get_channel(i) for i in self.config.bound_channels if i)
            chlist.discard(None)

            invalids = set()
            invalids.update(c for c in chlist if c.type == discord.ChannelType.voice)

            chlist.difference_update(invalids)
            self.config.bound_channels.difference_update(invalids)

            if chlist:
                log.info("Bound to text channels:")
                [log.info(' - {}/{}'.format(ch.server.name.strip(), ch.name.strip())) for ch in chlist if ch]
            else:
                print("Not bound to any text channels")

            if invalids and self.config.debug_mode:
                print(flush=True)
                log.info("Not binding to voice channels:")
                [log.info(' - {}/{}'.format(ch.server.name.strip(), ch.name.strip())) for ch in invalids if ch]

            print(flush=True)

        else:
            log.info("Not bound to any text channels")

        if self.config.autojoin_channels:
            chlist = set(self.get_channel(i) for i in self.config.autojoin_channels if i)
            chlist.discard(None)

            invalids = set()
            invalids.update(c for c in chlist if c.type == discord.ChannelType.text)

            chlist.difference_update(invalids)
            self.config.autojoin_channels.difference_update(invalids)

            if chlist:
                log.info("Autojoining voice chanels:")
                [log.info(' - {}/{}'.format(ch.server.name.strip(), ch.name.strip())) for ch in chlist if ch]
            else:
                log.info("Not bound to any text channels")

            if invalids and self.config.debug_mode:
                print(flush=True)
                log.info("Cannot autojoin text channels:")
                [log.info(' - {}/{}'.format(ch.server.name.strip(), ch.name.strip())) for ch in invalids if ch]

            autojoin_channels = chlist

        else:
            log.info("Not autojoining any voice channels")
            autojoin_channels = set()

        print(flush=True)
        log.info("Options:")

        log.info("  Command prefix: " + self.config.command_prefix)
        log.info("  Default volume: {}%".format(int(self.config.default_volume * 100)))
        log.info("  Skip threshold: {} votes or {}%".format(
            self.config.skips_required, fixg(self.config.skip_ratio_required * 100)))
        log.info("  Now Playing @mentions: " + ['Disabled', 'Enabled'][self.config.now_playing_mentions])
        log.info("  Auto-Summon: " + ['Disabled', 'Enabled'][self.config.auto_summon])
        log.info("  Auto-Playlist: " + ['Disabled', 'Enabled'][self.config.auto_playlist])
        log.info("  Auto-Pause: " + ['Disabled', 'Enabled'][self.config.auto_pause])
        log.info("  Delete Messages: " + ['Disabled', 'Enabled'][self.config.delete_messages])
        if self.config.delete_messages:
            log.info("    Delete Invoking: " + ['Disabled', 'Enabled'][self.config.delete_invoking])
        log.info("  Debug Mode: " + ['Disabled', 'Enabled'][self.config.debug_mode])
        log.info("  Downloaded songs will be " + ['deleted', 'saved'][self.config.save_videos])
        print(flush=True)

        # maybe option to leave the ownerid blank and generate a random command for the owner to use
        # wait_for_message is pretty neato

        await self._join_startup_channels(autojoin_channels, autosummon=self.config.auto_summon)

        # t-t-th-th-that's all folks!

    async def cmd_help2(self, command=None):
        """
        Usage:
            {command_prefix}help [command]

        Prints a help message.
        If a command is specified, it prints a help message for that command.
        Otherwise, it lists the available commands.
        """

        if command:
            cmd = getattr(self, 'cmd_' + command, None)
            if cmd and not hasattr(cmd, 'dev_cmd'):
                return Response(
                    "```\n{}```".format(
                        dedent(cmd.__doc__)
                    ).format(command_prefix=self.config.command_prefix),
                    delete_after=60
                )
            else:
                return Response("No such command", delete_after=10)

        else:
            helpmsg = "**Available commands**\n```"
            commands = []

            for att in dir(self):
                if att.startswith('cmd_') and att != 'cmd_help' and not hasattr(getattr(self, att), 'dev_cmd'):
                    command_name = att.replace('cmd_', '').lower()
                    commands.append("{}{}".format(self.config.command_prefix, command_name))

            helpmsg += ", ".join(commands)
            helpmsg += "```\n<https://github.com/SexualRhinoceros/MusicBot/wiki/Commands-list>"
            helpmsg += "You can also use `{}help x` for more info about each command.".format(self.config.command_prefix)

            return Response(helpmsg, reply=True, delete_after=60)

    async def cmd_blacklist(self, message, user_mentions, option, something):
        """
        Usage:
            {command_prefix}blacklist [ + | - | add | remove ] @UserName [@UserName2 ...]

        Add or remove users to the blacklist.
        Blacklisted users are forbidden from using bot commands.
        """

        if not user_mentions:
            raise exceptions.CommandError("No users listed.", expire_in=20)

        if option not in ['+', '-', 'add', 'remove']:
            raise exceptions.CommandError(
                'Invalid option "%s" specified, use +, -, add, or remove' % option, expire_in=20
            )

        for user in user_mentions.copy():
            if user.id == self.config.owner_id:
                print("[Commands:Blacklist] The owner cannot be blacklisted.")
                user_mentions.remove(user)

        old_len = len(self.blacklist)

        if option in ['+', 'add']:
            self.blacklist.update(user.id for user in user_mentions)

            write_file(self.config.blacklist_file, self.blacklist)

            return Response(
                '%s users have been added to the blacklist.' % (len(self.blacklist) - old_len),
                reply=True, delete_after=10
            )

        else:
            if self.blacklist.isdisjoint(user.id for user in user_mentions):
                return Response('None of the users that you\'ve mentioned aren\'t in the list.', reply=True, delete_after=10)

            else:
                self.blacklist.difference_update(user.id for user in user_mentions)
                write_file(self.config.blacklist_file, self.blacklist)

                return Response(
                    '%s users have been removed from the blacklist.' % (old_len - len(self.blacklist)),
                    reply=True, delete_after=10
                )

    async def cmd_id(self, author, user_mentions):
        """
        Usage:
            {command_prefix}id [@user]

        Tells the user their id or the id of another user.
        """
        if not user_mentions:
            return Response('Your Discord User ID is `%s`' % author.id, reply=True, delete_after=35)
        else:
            usr = user_mentions[0]
            return Response("%s's Discord User ID is `%s`" % (usr.name, usr.id), reply=True, delete_after=35)

    @owner_only
    async def cmd_joinserver(self, message, server_link=None):
        """
        Usage:
            {command_prefix}joinserver invite_link

        Asks the bot to join a server.  Note: Bot accounts cannot use invite links.
        """

        if self.user.bot:
            url = await self.generate_invite_link()
            return Response(
                #"Click here to add me to a server: \n{} - Use .notifydev if there's any problem.".format(url),
                "Click the following URL to add me to your server! - https://inv.rtb.dragonfire.me/ - Use .notifydev if there's any problem.",
                reply=True, delete_after=30
            )

        try:
            if server_link:
                await self.accept_invite(server_link)
                return Response("\N{THUMBS UP SIGN}")

        except:
            raise exceptions.CommandError('Invalid URL provided:\n{}\n'.format(server_link), expire_in=30)

    async def cmd_play(self, player, channel, author, permissions, leftover_args, song_url):
        """
        Usage:
            {command_prefix}play song_link
            {command_prefix}play text to search for

        Adds the song to the playlist.  If a link is not provided, the first
        result from a youtube search is added to the queue.
        """

        song_url = song_url.strip('<>')

        if permissions.max_songs and player.playlist.count_for_user(author) >= permissions.max_songs:
            raise exceptions.PermissionsError(
                "boop. you've reached your playlist count/song limit. (%s)" % permissions.max_songs, expire_in=30
            )

        await self.send_typing(channel)

        if leftover_args:
            song_url = ' '.join([song_url, *leftover_args])

        try:
            info = await self.downloader.extract_info(player.playlist.loop, song_url, download=False, process=False)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=30)

        if not info:
            raise exceptions.CommandError(
                "That video cannot be played.  Try using the {}stream command.".format(self.config.command_prefix),
                expire_in=30
            )

        # abstract the search handling away from the user
        # our ytdl options allow us to use search strings as input urls
        if info.get('url', '').startswith('ytsearch'):
            # print("[Command:play] Searching for \"%s\"" % song_url)
            info = await self.downloader.extract_info(
                player.playlist.loop,
                song_url,
                download=False,
                process=True,    # ASYNC LAMBDAS WHEN
                on_error=lambda e: asyncio.ensure_future(
                    self.safe_send_message(channel, "```\n%s\n```" % e, expire_in=120), loop=self.loop),
                retry_on_error=True
            )

            if not info:
                raise exceptions.CommandError(
                    "Error extracting info from search string, youtubedl returned no data.  "
                    "You may need to restart the bot if this continues to happen.", expire_in=30
                )

            if not all(info.get('entries', [])):
                # empty list, no data
                log.debug("Got empty list, no data")
                return

            song_url = info['entries'][0]['webpage_url']
            info = await self.downloader.extract_info(player.playlist.loop, song_url, download=False, process=False)
            # Now I could just do: return await self.cmd_play(player, channel, author, song_url)
            # But this is probably fine

        # TODO: Possibly add another check here to see about things like the bandcamp issue
        # TODO: Where ytdl gets the generic extractor version with no processing, but finds two different urls

        if 'entries' in info:
            # I have to do exe extra checks anyways because you can request an arbitrary number of search results
            if not permissions.allow_playlists and ':search' in info['extractor'] and len(info['entries']) > 1:
                raise exceptions.PermissionsError("You can't request songs.", expire_in=30)

            # The only reason we would use this over `len(info['entries'])` is if we add `if _` to this one
            num_songs = sum(1 for _ in info['entries'])

            if permissions.max_playlist_length and num_songs > permissions.max_playlist_length:
                raise exceptions.PermissionsError(
                    "Playlist is too crowded. I'm not gonna play this. (%s > %s)" % (num_songs, permissions.max_playlist_length),
                    expire_in=30
                )

            # This is a little bit weird when it says (x + 0 > y), I might add the other check back in
            if permissions.max_songs and player.playlist.count_for_user(author) + num_songs > permissions.max_songs:
                raise exceptions.PermissionsError(
                    "Playlist entries + your already queued songs reached limit (%s + %s > %s)" % (
                        num_songs, player.playlist.count_for_user(author), permissions.max_songs),
                    expire_in=30
                )

            if info['extractor'].lower() in ['youtube:playlist', 'soundcloud:set', 'bandcamp:album']:
                try:
                    return await self._cmd_play_playlist_async(player, channel, author, permissions, song_url, info['extractor'])
                except exceptions.CommandError:
                    raise
                except Exception as e:
                    log.error("Error queuing playlist", exc_info=True)
                    raise exceptions.CommandError("Error queuing playlist:\n%s" % e, expire_in=30)

            t0 = time.time()

            # My test was 1.2 seconds per song, but we maybe should fudge it a bit, unless we can
            # monitor it and edit the message with the estimated time, but that's some ADVANCED SHIT
            # I don't think we can hook into it anyways, so this will have to do.
            # It would probably be a thread to check a few playlists and get the speed from that
            # Different playlists might download at different speeds though
            wait_per_song = 1.2

            procmesg = await self.safe_send_message(
                channel,
                'Gathering playlist information for {} songs{}'.format(
                    num_songs,
                    ', ETA: {} seconds'.format(fixg(
                        num_songs * wait_per_song)) if num_songs >= 10 else '.'))

            # We don't have a pretty way of doing this yet.  We need either a loop
            # that sends these every 10 seconds or a nice context manager.
            await self.send_typing(channel)

            # TODO: I can create an event emitter object instead, add event functions, and every play list might be asyncified
            #       Also have a "verify_entry" hook with the entry as an arg and returns the entry if its ok

            entry_list, position = await player.playlist.import_from(song_url, channel=channel, author=author)

            tnow = time.time()
            ttime = tnow - t0
            listlen = len(entry_list)
            drop_count = 0

            if permissions.max_song_length:
                for e in entry_list.copy():
                    if e.duration > permissions.max_song_length:
                        player.playlist.entries.remove(e)
                        entry_list.remove(e)
                        drop_count += 1
                        # Im pretty sure there's no situation where this would ever break
                        # Unless the first entry starts being played, which would make this a race condition
                if drop_count:
                    print("Dropped %s songs" % drop_count)

            log.info("Processed {} songs in {} seconds at {:.2f}s/song, {:+.2g}/song from expected ({}s)".format(
                listlen,
                fixg(ttime),
                ttime / listlen if listlen else 0,
                ttime / listlen - wait_per_song if listlen - wait_per_song else 0,
                fixg(wait_per_song * num_songs))
            )

            await self.safe_delete_message(procmesg)

            if not listlen - drop_count:
                raise exceptions.CommandError(
                    "No songs were added, all songs were over max duration (%ss)" % permissions.max_song_length,
                    expire_in=30
                )

            reply_text = "Enqueued **%s** songs to be played. Position in queue: %s"
            btext = str(listlen - drop_count)

        else:
            if permissions.max_song_length and info.get('duration', 0) > permissions.max_song_length:
                raise exceptions.PermissionsError(
                    "song is exceeding the limit that my owner has set:(%s > %s)" % (info['duration'], permissions.max_song_length),
                    expire_in=30
                )

            try:
                entry, position = await player.playlist.add_entry(song_url, channel=channel, author=author)

            except exceptions.WrongEntryTypeError as e:
                if e.use_url == song_url:
                    log.warning("Determined incorrect entry type, but suggested url is the same.  Help.")

                log.debug("Assumed url \"%s\" was a single entry, was actually a playlist" % song_url)
                log.debug("Using \"%s\" instead" % e.use_url)

                return await self.cmd_play(player, channel, author, permissions, leftover_args, e.use_url)

            reply_text = "Enqueued **%s** to be played. Position in queue: %s"
            btext = entry.title

        if position == 1 and player.is_stopped:
            position = 'Up next!'
            reply_text %= (btext, position)

        else:
            try:
                time_until = await player.playlist.estimate_time_until(position, player)
                reply_text += ' - estimated time until playing: %s'
            except:
                traceback.print_exc()
                time_until = ''

            reply_text %= (btext, position, time_until)

        return Response(reply_text, delete_after=30)

    async def _cmd_play_playlist_async(self, player, channel, author, permissions, playlist_url, extractor_type):
        """
        Secret handler to use the async wizardry to make playlist queuing non-"blocking"
        """

        await self.send_typing(channel)
        info = await self.downloader.extract_info(player.playlist.loop, playlist_url, download=False, process=False)

        if not info:
            raise exceptions.CommandError("That playlist cannot be played.")

        num_songs = sum(1 for _ in info['entries'])
        t0 = time.time()

        busymsg = await self.safe_send_message(
            channel, "Processing %s songs..." % num_songs)  # TODO: From playlist_title
        await self.send_typing(channel)

        entries_added = 0
        if extractor_type == 'youtube:playlist':
            try:
                entries_added = await player.playlist.async_process_youtube_playlist(
                    playlist_url, channel=channel, author=author)
                # TODO: Add hook to be called after each song
                # TODO: Add permissions

            except Exception:
                log.error("Error processing playlist", exc_info=True)
                raise exceptions.CommandError('Error handling playlist %s queuing.' % playlist_url, expire_in=30)

        elif extractor_type.lower() in ['soundcloud:set', 'bandcamp:album']:
            try:
                entries_added = await player.playlist.async_process_sc_bc_playlist(
                    playlist_url, channel=channel, author=author)
                # TODO: Add hook to be called after each song
                # TODO: Add permissions

            except Exception:
                log.error("Error processing playlist", exc_info=True)
                raise exceptions.CommandError('Error handling playlist %s queuing.' % playlist_url, expire_in=30)


        songs_processed = len(entries_added)
        drop_count = 0
        skipped = False

        if permissions.max_song_length:
            for e in entries_added.copy():
                if e.duration > permissions.max_song_length:
                    try:
                        player.playlist.entries.remove(e)
                        entries_added.remove(e)
                        drop_count += 1
                    except:
                        pass

            if drop_count:
                log.debug("Dropped %s songs" % drop_count)

            if player.current_entry and player.current_entry.duration > permissions.max_song_length:
                await self.safe_delete_message(self.server_specific_data[channel.server]['last_np_msg'])
                self.server_specific_data[channel.server]['last_np_msg'] = None
                skipped = True
                player.skip()
                entries_added.pop()

        await self.safe_delete_message(busymsg)

        songs_added = len(entries_added)
        tnow = time.time()
        ttime = tnow - t0
        wait_per_song = 1.2
        # TODO: actually calculate wait per song in the process function and return that too

        # This is technically inaccurate since bad songs are ignored but still take up time
        log.info("Processed {}/{} songs in {} seconds at {:.2f}s/song, {:+.2g}/song from expected ({}s)".format(
            songs_processed,
            num_songs,
            fixg(ttime),
            ttime / num_songs if num_songs else 0,
            ttime / num_songs - wait_per_song if num_songs - wait_per_song else 0,
            fixg(wait_per_song * num_songs))
        )

        if not songs_added:
            basetext = "None of the songs were added, since they're all over the time limit. (%ss)" % permissions.max_song_length
            if skipped:
                basetext += "\nAlso, the song was skipped because it was too long."

            raise exceptions.CommandError(basetext, expire_in=30)

        return Response("Enqueued {} songs to be played in {} seconds".format(
            songs_added, fixg(ttime, 1)), delete_after=30)

    async def cmd_stream(self, player, channel, author, permissions, song_url):
        """
        Usage:
            {command_prefix}stream song_link

        Enqueue a media stream.
        This could mean an actual stream like Twitch or shoutcast, or simply streaming
        media without predownloading it.  Note: FFmpeg is notoriously bad at handling
        streams, especially on poor connections.  You have been warned.
        """

        song_url = song_url.strip('<>')

        if permissions.max_songs and player.playlist.count_for_user(author) >= permissions.max_songs:
            raise exceptions.PermissionsError(
                "You have reached your enqueued song limit (%s)" % permissions.max_songs, expire_in=30
            )

        await self.send_typing(channel)
        await player.playlist.add_stream_entry(song_url, channel=channel, author=author)

        return Response(":+1:", delete_after=6)

    async def cmd_search(self, player, channel, author, permissions, leftover_args):
        """
        Usage:
            {command_prefix}search [service] [number] query

        Searches a service for a video and adds it to the queue.
        - service: any one of the following services:
            - youtube (yt) (default if unspecified)
            - soundcloud (sc)
            - yahoo (yh)
        - number: return a number of video results and waits for user to choose one
          - defaults to 1 if unspecified
          - note: If your search query starts with a number,
                  you must put your query in quotes
            - ex: {command_prefix}search 2 "I ran seagulls"
        """

        if permissions.max_songs and player.playlist.count_for_user(author) > permissions.max_songs:
            raise exceptions.PermissionsError(
                "You have reached your playlist item limit (%s)" % permissions.max_songs,
                expire_in=30
            )

        def argcheck():
            if not leftover_args:
                # noinspection PyUnresolvedReferences
                raise exceptions.CommandError(
                    "Please specify a search query.\n%s" % dedent(
                        self.cmd_search.__doc__.format(command_prefix=self.config.command_prefix)),
                    expire_in=60
                )

        argcheck()

        try:
            leftover_args = shlex.split(' '.join(leftover_args))
        except ValueError:
            raise exceptions.CommandError("Please quote your search query properly.", expire_in=30)

        service = 'youtube'
        items_requested = 3
        max_items = 10  # this can be whatever, but since ytdl uses about 1000, a small number might be better
        services = {
            'youtube': 'ytsearch',
            'soundcloud': 'scsearch',
            'yahoo': 'yvsearch',
            'yt': 'ytsearch',
            'sc': 'scsearch',
            'yh': 'yvsearch'
        }

        if leftover_args[0] in services:
            service = leftover_args.pop(0)
            argcheck()

        if leftover_args[0].isdigit():
            items_requested = int(leftover_args.pop(0))
            argcheck()

            if items_requested > max_items:
                raise exceptions.CommandError("You cannot search for more than %s videos" % max_items)

        # Look jake, if you see this and go "what the fuck are you doing"
        # and have a better idea on how to do this, i'd be delighted to know.
        # I don't want to just do ' '.join(leftover_args).strip("\"'")
        # Because that eats both quotes if they're there
        # where I only want to eat the outermost ones
        if leftover_args[0][0] in '\'"':
            lchar = leftover_args[0][0]
            leftover_args[0] = leftover_args[0].lstrip(lchar)
            leftover_args[-1] = leftover_args[-1].rstrip(lchar)

        search_query = '%s%s:%s' % (services[service], items_requested, ' '.join(leftover_args))

        search_msg = await self.send_message(channel, "Searching for videos...")
        await self.send_typing(channel)

        try:
            info = await self.downloader.extract_info(player.playlist.loop, search_query, download=False, process=True)

        except Exception as e:
            await self.safe_edit_message(search_msg, str(e), send_if_fail=True)
            return
        else:
            await self.safe_delete_message(search_msg)

        if not info:
            return Response("No videos found.", delete_after=30)

        def check(m):
            return (
                m.content.lower()[0] in 'yn' or
                # hardcoded function name weeee
                m.content.lower().startswith('{}{}'.format(self.config.command_prefix, 'search')) or
                m.content.lower().startswith('exit'))

        for e in info['entries']:
            result_message = await self.safe_send_message(channel, "Result %s/%s: %s" % (
                info['entries'].index(e) + 1, len(info['entries']), e['webpage_url']))

            confirm_message = await self.safe_send_message(channel, "This fine? Type `y`, `n` or `exit`")
            response_message = await self.wait_for_message(30, author=author, channel=channel, check=check)

            if not response_message:
                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                return Response("Fine, nevermind then.", delete_after=30)

            # They started a new search query so lets clean up and bugger off
            elif response_message.content.startswith(self.config.command_prefix) or \
                    response_message.content.lower().startswith('exit'):

                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                return

            if response_message.content.lower().startswith('y'):
                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                await self.safe_delete_message(response_message)

                await self.cmd_play(player, channel, author, permissions, [], e['webpage_url'])

                return Response("Coming right up.", delete_after=30)
            else:
                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                await self.safe_delete_message(response_message)

        return Response("Oh well fam. I tried. \N{SLIGHTLY FROWNING FACE}", delete_after=30)

    async def cmd_np(self, player, channel, server, message):
        """
        Usage:
            {command_prefix}np

        Displays the current song in chat.
        """

        if player.current_entry:
            if self.server_specific_data[server]['last_np_msg']:
                await self.safe_delete_message(self.server_specific_data[server]['last_np_msg'])
                self.server_specific_data[server]['last_np_msg'] = None

            # TODO: Fix timedelta garbage with util function
            song_progress = str(timedelta(seconds=player.progress)).lstrip('0').lstrip(':')
            song_total = str(timedelta(seconds=player.current_entry.duration)).lstrip('0').lstrip(':')

            streaming = isinstance(player.current_entry, StreamPlaylistEntry)
            prog_str = ('`[{progress}]`' if streaming else '`[{progress}/{total}]`').format(
                progress=song_progress, total=song_total
            )
            action_text = 'Streaming' if streaming else 'Playing'

            if player.current_entry.meta.get('channel', False) and player.current_entry.meta.get('author', False):
                np_text = "Now {action}: **{title}** added by **{author}** {progress}\n\N{WHITE RIGHT POINTING BACKHAND INDEX} <{url}>".format(
                    action=action_text,
                    title=player.current_entry.title,
                    author=player.current_entry.meta['author'].name,
                    progress=prog_str,
                    url=player.current_entry.url
                )
            else:
                np_text = "Now {action}: **{title}** {progress}\n\N{WHITE RIGHT POINTING BACKHAND INDEX} <{url}>".format(
                    action=action_text,
                    title=player.current_entry.title,
                    progress=prog_str,
                    url=player.current_entry.url
                )

            self.server_specific_data[server]['last_np_msg'] = await self.safe_send_message(channel, np_text)
            await self._manual_delete_check(message)
        else:
            return Response(
                'Hey, no one\'s playing anything! Queue a song with {}play.'.format(self.config.command_prefix),
                delete_after=30
            )

    async def cmd_connect(self, channel, server, message, author, voice_channel):
        """
        Usage:
            {command_prefix}connect

        Call the bot to the voice channel.
        """

        if not author.voice_channel:
            raise exceptions.CommandError('You\'re not even connected to a voice channel...')

        voice_client = self.voice_client_in(server)
        if voice_client and server == author.voice_channel.server:
            await voice_client.move_to(author.voice_channel)
            return

        # move to _verify_vc_perms?
        chperms = author.voice_channel.permissions_for(server.me)

        if not chperms.connect:
            log.warning("Cannot join channel \"{}\", no permission.".format(author.voice_channel.name))
            return Response(
                "```Cannot join channel \"{}\", no permission.```".format(author.voice_channel.name),
                delete_after=25
            )

        elif not chperms.speak:
            log.warning("Will not join channel \"{}\", no permission to speak.".format(author.voice_channel.name))
            return Response(
                "```Not gonna join \"{}\", I can't speak in there.```".format(author.voice_channel.name),
                delete_after=25
            )

        log.info("Joining {0.server.name}/{0.name}".format(author.voice_channel))
        await self.send_message(message.channel, "Joined ***{}***".format(message.author.voice_channel.name))

        player = await self.get_player(author.voice_channel, create=True)

        if player.is_stopped:
            player.play()

        if self.config.auto_playlist:
            await self.on_player_finished_playing(player)

    async def cmd_pause(self, player):
        """
        Usage:
            {command_prefix}pause

        Pauses playback of the current song.
        """

        if player.is_playing:
            player.pause()

        else:
            raise exceptions.CommandError('I\'m not playing anything.')

    async def cmd_resume(self, player):
        """
        Usage:
            {command_prefix}resume

        Resumes playback of a paused song.
        """

        if player.is_paused:
            player.resume()

        else:
            raise exceptions.CommandError('Nothing\'s playing, nor nothing\'s paused.')

    async def cmd_shuffle(self, channel, player):
        """
        Usage:
            {command_prefix}shuffle

        Shuffles the playlist.
        """

        player.playlist.shuffle()

        cards = ['\N{BLACK SPADE SUIT}', '\N{BLACK CLUB SUIT}', '\N{BLACK HEART SUIT}', '\N{BLACK DIAMOND SUIT}']
        shuffle(cards)

        hand = await self.send_message(channel, ' '.join(cards))
        await asyncio.sleep(0.6)

        for x in range(4):
            shuffle(cards)
            await self.safe_edit_message(hand, ' '.join(cards))
            await asyncio.sleep(0.6)

        await self.safe_delete_message(hand, quiet=True)
        return Response(":\N{OK HAND SIGN}: shuffled!")

    async def cmd_clear(self, player, author):
        """
        Usage:
            {command_prefix}clear

        Clears the playlist.
        """

        player.playlist.clear()
        return Response('Cleared the playlist!')

    async def cmd_skip(self, player, channel, author, message, permissions, voice_channel):
        """
        Usage:
            {command_prefix}skip

        Skips the current song when enough votes are cast, or by the bot owner.
        """

        if player.is_stopped:
            raise exceptions.CommandError("I can't skip because I'm not playing anything!", expire_in=20)

        if not player.current_entry:
            if player.playlist.peek():
                if player.playlist.peek()._is_downloading:
                    return Response("The next song (%s) is downloading, please wait." % player.playlist.peek().title)

                elif player.playlist.peek().is_downloaded:
                    print("The next song will be played shortly.  Please wait.")
                else:
                    print("Something odd is happening.  "
                          "You might want to restart the bot if it doesn't start working.")
            else:
                print("Something strange is happening.  "
                      "You might want to restart the bot if it doesn't start working.")

        if author.id == self.config.owner_id \
                or permissions.instaskip \
                or author == player.current_entry.meta.get('author', None):

            player.skip()  # check autopause stuff here
            await self._manual_delete_check(message)
            return

        # TODO: ignore person if they're deaf or take them out of the list or something?
        # Currently is recounted if they vote, deafen, then vote

        num_voice = sum(1 for m in voice_channel.voice_members if not (
            m.deaf or m.self_deaf or m.id in [self.config.owner_id, self.user.id]))

        num_skips = player.skip_state.add_skipper(author.id, message)

        skips_remaining = min(
            self.config.skips_required,
            sane_round_int(num_voice * self.config.skip_ratio_required)
        ) - num_skips

        if skips_remaining <= 0:
            player.skip()  # check autopause stuff here
            return Response(
                'your skip for **{}** was acknowledged.'
                '\nThe vote to skip has been passed.{}'.format(
                    player.current_entry.title,
                    ' Next song coming up!' if player.playlist.peek() else ''
                ),
                reply=True,
                delete_after=20
            )

        else:
            # TODO: When a song gets skipped, delete the old x needed to skip messages
            return Response(
                'your skip for **{}** was acknowledged.'
                '\n**{}** more {} required to vote to skip this song.'.format(
                    player.current_entry.title,
                    skips_remaining,
                    'person is' if skips_remaining == 1 else 'people are'
                ),
                reply=True,
                delete_after=20
            )

    async def cmd_volume(self, message, player, new_volume=None):
        """
        Usage:
            {command_prefix}volume (+/-)[volume]

        Sets the playback volume. Accepted values are from 1 to 350.
        Anything above 225 is ear rape.
        Putting + or - before the volume will make the volume change relative to the current volume.
        """

        if not new_volume:
            return Response('Current volume: `%s%%`' % int(player.volume * 350), reply=True, delete_after=20)

        relative = False
        if new_volume[0] in '+-':
            relative = True

        try:
            new_volume = int(new_volume)

        except ValueError:
            raise exceptions.CommandError('{} isn\'t valid.'.format(new_volume), expire_in=20)

        vol_change = None
        if relative:
            vol_change = new_volume
            new_volume += (player.volume * 350)

        old_volume = int(player.volume * 350)

        if 0 < new_volume <= 350:
            player.volume = new_volume / 350

            return Response('updated volume from %d to %d' % (old_volume, new_volume), reply=True, delete_after=20)

        else:
            if relative:
                raise exceptions.CommandError(
                    'Unreasonable volume change provided: {}{:+} -> {}%.  Provide a change between {} and {:+}.'.format(
                        old_volume, vol_change, old_volume + vol_change, 1 - old_volume, 350 - old_volume), expire_in=20)
            else:
                raise exceptions.CommandError(
                    'Unreasonable volume provided: {}%. Provide a value between 1 and 350.'.format(new_volume), expire_in=20)

    async def cmd_queue(self, channel, player):
        """
        Usage:
            {command_prefix}queue

        Prints the current song queue.
        """

        lines = []
        unlisted = 0
        andmoretext = '* ... and %s more*' % ('x' * len(player.playlist.entries))

        if player.current_entry:
            # TODO: Fix timedelta garbage with util function
            song_progress = str(timedelta(seconds=player.progress)).lstrip('0').lstrip(':')
            song_total = str(timedelta(seconds=player.current_entry.duration)).lstrip('0').lstrip(':')
            prog_str = '`[%s/%s]`' % (song_progress, song_total)

            if player.current_entry.meta.get('channel', False) and player.current_entry.meta.get('author', False):
                lines.append("Playing **%s**, added by **%s** %s\n" % (
                    player.current_entry.title, player.current_entry.meta['author'].name, prog_str))
            else:
                lines.append("Playing **%s**. %s\n" % (player.current_entry.title, prog_str))

        for i, item in enumerate(player.playlist, 1):
            if item.meta.get('channel', False) and item.meta.get('author', False):
                nextline = '`{}.` **{}** added by **{}**'.format(i, item.title, item.meta['author'].name).strip()
            else:
                nextline = '`{}.` **{}**'.format(i, item.title).strip()

            currentlinesum = sum(len(x) + 1 for x in lines)  # +1 is for newline char

            if currentlinesum + len(nextline) + len(andmoretext) > DISCORD_MSG_CHAR_LIMIT:
                if currentlinesum + len(andmoretext):
                    unlisted += 1
                    continue

            lines.append(nextline)

        if unlisted:
            lines.append('\n*... and %s more* (jesus you got lots of shit in here)' % unlisted)

        if not lines:
            lines.append(
                'There are no songs queued! Queue something with {}play.'.format(self.config.command_prefix))

        message = '\n'.join(lines)
        return Response(message, delete_after=30)

    async def cmd_clean(self, message, channel, server, author, search_range=50):
        """
        Usage:
            {command_prefix}clean [range]

        Removes up to [range] messages the bot has posted in chat. Default: 50, Max: 1000
        """

        try:
            float(search_range)  # lazy check
            search_range = min(int(search_range), 1000)
        except:
            return Response("ENTER A GOD DAMN NUMBER. AN INTENGER. SOMETHING THAT ISN'T A SYMBOL.", reply=True, delete_after=8)

        await self.safe_delete_message(message, quiet=True)

        def is_possible_command_invoke(entry):
            valid_call = any(
                entry.content.startswith(prefix) for prefix in [self.config.command_prefix])  # can be expanded
            return valid_call and not entry.content[1:2].isspace()

        delete_invokes = True
        delete_all = channel.permissions_for(author).manage_messages or self.config.owner_id == author.id

        def check(message):
            if is_possible_command_invoke(message) and delete_invokes:
                return delete_all or message.author == author
            return message.author == self.user

        if self.user.bot:
            if channel.permissions_for(server.me).manage_messages:
                deleted = await self.purge_from(channel, check=check, limit=search_range, before=message)
                return Response('Cleaned up {} message{}.'.format(len(deleted), 's' * bool(deleted)), delete_after=15)

        deleted = 0
        async for entry in self.logs_from(channel, search_range, before=message):
            if entry == self.server_specific_data[channel.server]['last_np_msg']:
                continue

            if entry.author == self.user:
                await self.safe_delete_message(entry)
                deleted += 1
                await asyncio.sleep(0.21)

            if is_possible_command_invoke(entry) and delete_invokes:
                if delete_all or entry.author == author:
                    try:
                        await self.delete_message(entry)
                        await asyncio.sleep(0.21)
                        deleted += 1

                    except discord.Forbidden:
                        delete_invokes = False
                    except discord.HTTPException:
                        pass

        return Response('Cleaned up {} message{}.'.format(deleted, 's' * bool(deleted)), delete_after=6)

    async def cmd_pldump(self, channel, song_url):
        """
        Usage:
            {command_prefix}pldump url

        Dumps the individual urls of a playlist
        """

        try:
            info = await self.downloader.extract_info(self.loop, song_url.strip('<>'), download=False, process=False)
        except Exception as e:
            raise exceptions.CommandError("Could not extract info from input url\n%s\n" % e, expire_in=25)

        if not info:
            raise exceptions.CommandError("Could not extract info from input url, no data.", expire_in=25)

        if not info.get('entries', None):
            # TODO: Retarded playlist checking
            # set(url, webpageurl).difference(set(url))

            if info.get('url', None) != info.get('webpage_url', info.get('url', None)):
                raise exceptions.CommandError("This does not seem to be a playlist.", expire_in=25)
            else:
                return await self.cmd_pldump(channel, info.get(''))

        linegens = defaultdict(lambda: None, **{
            "youtube":    lambda d: 'https://www.youtube.com/watch?v=%s' % d['id'],
            "soundcloud": lambda d: d['url'],
            "bandcamp":   lambda d: d['url']
        })

        exfunc = linegens[info['extractor'].split(':')[0]]

        if not exfunc:
            raise exceptions.CommandError("Could not extract info from input url, unsupported playlist type.", expire_in=25)

        with BytesIO() as fcontent:
            for item in info['entries']:
                fcontent.write(exfunc(item).encode('utf8') + b'\n')

            fcontent.seek(0)
            await self.send_file(channel, fcontent, filename='playlist.txt', content="Here's the url dump for <%s>" % song_url)

        return Response("Check your PMs, I've sent the url dump.", delete_after=20)

    async def cmd_listids(self, server, author, leftover_args, cat='all'):
        """
        Usage:
            {command_prefix}listids [categories]

        Lists the ids for various things.  Categories are:
           all, users, roles, channels
        """

        cats = ['channels', 'roles', 'users']

        if cat not in cats and cat != 'all':
            return Response(
                "Valid categories: " + ' '.join(['`%s`' % c for c in cats]),
                reply=True,
                delete_after=25
            )

        if cat == 'all':
            requested_cats = cats
        else:
            requested_cats = [cat] + [c.strip(',') for c in leftover_args]

        data = ['Your ID: %s' % author.id]

        for cur_cat in requested_cats:
            rawudata = None

            if cur_cat == 'users':
                data.append("\nUser IDs:")
                rawudata = ['%s #%s: %s' % (m.name, m.discriminator, m.id) for m in server.members]

            elif cur_cat == 'roles':
                data.append("\nRole IDs:")
                rawudata = ['%s: %s' % (r.name, r.id) for r in server.roles]

            elif cur_cat == 'channels':
                data.append("\nText Channel IDs:")
                tchans = [c for c in server.channels if c.type == discord.ChannelType.text]
                rawudata = ['%s: %s' % (c.name, c.id) for c in tchans]

                rawudata.append("\nVoice Channel IDs:")
                vchans = [c for c in server.channels if c.type == discord.ChannelType.voice]
                rawudata.extend('%s: %s' % (c.name, c.id) for c in vchans)

            if rawudata:
                data.extend(rawudata)

        with BytesIO() as sdata:
            sdata.writelines(d.encode('utf8') + b'\n' for d in data)
            sdata.seek(0)

            # TODO: Fix naming (Discord20API-ids.txt)
            await self.send_file(author, sdata, filename='%s-ids-%s.txt' % (server.name.replace(' ', '_'), cat))

        return Response("Check your PMs, I've sent the entire ID list of this Discord guild.", delete_after=20)


    async def cmd_perms(self, author, channel, server, permissions):
        """
        Usage:
            {command_prefix}perms

        Sends the user a list of their permissions.
        """

        lines = ['Command permissions in %s\n' % server.name, '```', '```']

        for perm in permissions.__dict__:
            if perm in ['user_list'] or permissions.__dict__[perm] == set():
                continue

            lines.insert(len(lines) - 1, "%s: %s" % (perm, permissions.__dict__[perm]))

        await self.send_message(author, '\n'.join(lines))
        return Response("Check your PMs for your current permissions.", delete_after=20)


    @owner_only
    async def cmd_renamebot(self, leftover_args, name):
        """
        Usage:
            {command_prefix}setname name

        Changes the bot's username.
        Note: This operation is limited by discord to twice per hour.
        """

        name = ' '.join([name, *leftover_args])

        try:
            await self.edit_profile(username=name)

        except discord.HTTPException:
            raise exceptions.CommandError(
                "I... I can't change my name.  "
                "Remember man, I can only do it twice an hour.")

        except Exception as e:
            raise exceptions.CommandError(e, expire_in=20)

        return Response("Changed my name to `{}`".format(name), delete_after=20)

    async def cmd_setnick(self, server, channel, leftover_args, nick):
        """
        Usage:
            {command_prefix}setnick nick

        Changes the bot's nickname.
        """

        if not channel.permissions_for(server.me).change_nickname:
            raise exceptions.CommandError("Can't change my own nickname, I don't have the required \"Change Nickname\" permission.")

        nick = ' '.join([nick, *leftover_args])

        try:
            await self.change_nickname(server.me, nick)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=20)

        return Response("Changed my nickname to `{}`".format(nick), delete_after=20)

    @owner_only
    async def cmd_setavatar(self, message, url=None):
        """
        Usage:
            {command_prefix}setavatar [url]

        Changes the bot's avatar.
        Attaching a file and leaving the url parameter blank also works.
        """

        if message.attachments:
            thing = message.attachments[0]['url']
        else:
            thing = url.strip('<>')

        try:
            with aiohttp.Timeout(10):
                async with self.aiosession.get(thing) as res:
                    await self.edit_profile(avatar=await res.read())

        except Exception as e:
            raise exceptions.CommandError("Can't change my avatar. {}".format(e), expire_in=20)

        return Response("Much better, right?", delete_after=20)
    #here begins the commandos
    async def cmd_robbopls(self, message):
        markov = open('markovrobin.txt','r')
        await self.send_message(message.channel, markov)

    async def cmd_wt(self, message, chanid, msg):
    #wireless message sending amirite
        if message.author.id == '117678528220233731' or '154785871311273986':
            msg = message.content[len(".wt " + chanid):].strip()
            await self.send_typing(discord.Object(id=chanid))
            asyncio.sleep(150)
            log.info("Bot sent a message to the channel ID:{}".format(chanid))
            await self.send_message(discord.Object(id=chanid), msg)

    async def cmd_time(self, message):
        time = time.strftime("%I:%M %P")
        timeed = time[:5] + "" + time[:4 + 1:]
        await self.send_message(message.channel, "```diff\n+ The time is now\n- ==[{}]==\n```".format(
            time.strftime("%I:%M %P").replace("0"[:5], "")))

    #THIS ISN'T IMPLEMENTED EITHER AAAAAAAAAAAAAAAAAAAAA
    async def cmd_disconnect(self, server, message):
        await self.safe_send_message(message.channel, "Disconnected from the voice server.")
        log.info("Disconnected from: `%s`" % server.name)
        await self.disconnect_voice_client(server)
        await self._manual_delete_check(message)

    async def cmd_reboot(self, message):
        # await self.safe_send_message(message.channel, "Bot is restarting, please wait...")
        await self.safe_send_message(message.channel, "restarting...")
        log.info("Bot is restarting")
        await self.disconnect_all_voice_clients()
        raise exceptions.RestartSignal()

    async def cmd_timetodie(self, message):
        kek = await self.safe_send_message(message.channel, "Bot is shutting down...")
        asyncio.sleep(10)
        await self.edit_message(kek, "I'm never coming back...")
        log.info("Bot is shutting down")
        await self.disconnect_all_voice_clients()
        raise exceptions.TerminateSignal()

    @dev_only
    async def cmd_breakpoint(self, message):
        log.critical("Activating debug breakpoint")
        return

    @dev_only
    async def cmd_objgraph(self, channel, func='most_common_types()'):
        import objgraph
        await self.send_typing(channel)

        if func == 'growth':
            f = StringIO()
            objgraph.show_growth(limit=10, file=f)
            f.seek(0)
            data = f.read()
            f.close()

        elif func == 'leaks':
            f = StringIO()
            objgraph.show_most_common_types(objects=objgraph.get_leaking_objects(), file=f)
            f.seek(0)
            data = f.read()
            f.close()

        elif func == 'leakstats':
            data = objgraph.typestats(objects=objgraph.get_leaking_objects())

        else:
            data = eval('objgraph.' + func)

        return Response(data, codeblock='py')
    @dev_only
    async def cmd_deval(self, message):
        if 'deval' in message.content:
            if message.author.id == '117678528220233731':
                debug = message.content[len(".deval "):].strip()
                try:
                    debug = eval(debug)
                    debug = str(debug)
                    await self.send_message(message.channel, "```python\n" + debug + "\n```")
                except Exception as e:
                    debug = traceback.format_exc()
                    debug = str(debug)
                    await self.send_message(message.channel, "```python\n" + debug + "\n```")
            else:
                pass

    @dev_only
    async def cmd_debug(self, message, content):
        if 'debug' in message.content:
            if message.author.id == '117678528220233731' or '154785871311273986':
                debug = message.content[len(".debug "):].strip()
                py = "```py\n{}\n```"
                thing = None
                try:
                    thing = eval(debug)
                except Exception as e:
                    await self.send_message(message.channel, py.format(type(e).__name__ + ': ' + str(e)))
                    return
                if asyncio.iscoroutine(thing):
                    thing = await thing
                    await self.send_message(message.channel, py.format(thing))
            else:
                pass

    async def cmd_kys(self, message):
        # return Response("kill yourself and never _EVER_ come back to me again, you stupid peasant. how dare you ask me to die. like fucking hell, why not do it yourself to satisfy yourself?", delete_after=0)
        return Response(
            "Seriously? You're such a fucking faggot. Kill yourself, unironically, hell, I'd kill you myself you fucking little shit, stupid fucking shitrag.",
            delete_after=0)
        # return Response("kill yourself and don't come back again to ask me to kill myself, stupid peasant.", delete_after=0)

    async def cmd_dab(self, message):
        return Response("​http://i.giphy.com/lae7QSMFxEkkE.gif", delete_after=0)

    @owner_only
    async def cmd_spamthefuckoutofeveryone(self, message):
        return Response(
            "( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°)( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°) ( ͡° ͜ʖ ͡°)",
            delete_after=0)

    async def cmd_memeg(author, self, message):
        """
        Attempt on trying to create a meme command, .memeg (template/line1/line2)
        List: http://memegen.link/templates/
        """
        genmeme = message.content[len(".memeg "):].strip()
        if message.content[len(".memeg"):].strip() != 0:
            return Response("http://memegen.link/" + re.sub(r"\s+", '-', genmeme) + ".jpg", delete_after=0)
        else:
            return Response("You didn't enter a message. Templates: http://memegen.link/templates/", delete_after=0)

    async def cmd_perf(self):
        rt = random.choice(tweetsthatareokhand)
        return Response(rt, delete_after=0)

    async def cmd_ver(self):
        return Response("`Ver. " + VER + " " + BUILD + "`", delete_after=0)

    # always remember to update this everytime you do an edit
    async def cmd_changes(self):
        return Response(
            "What's new in " + VER + ": `deprecated, check the website OR check #ViralBot and Napsta's #todo-list/#announcements`",
            delete_after=0)

    async def cmd_prune(self, channel, amount):
        try:
            harambe = int(amount)
        except:
            raise exceptions.CommandError("That's not a valid number man.")
        deleted = await self.purge_from(channel, limit=harambe)
        await self.send_message(channel, "I deleted {} messages.".format(len(deleted)))

    @owner_only
    async def cmd_rtb(self, message, client):
        """
        RTB System.
        Only Robin#0052 is allowed, or the Bot Owner if this isn't the main bot, RobTheBoat#9091
        """
        if message.content[len(".rtb "):].strip() == "servers":
            return Response("``` \n" + self.servers + "\n ```", delete_after=0)
        elif message.content[len(".rtb "):].strip() == "betamode":
            discord.Game(name='in Beta Mode')
            await self.change_status(discord.Game(name='in Beta Mode'))
            return Response("(!) Now in Beta mode.", delete_after=0)
        elif message.content[len(".rtb "):].strip() == "bye":
            await self.send_message(message.channel, "bye")
            await self.leave_server(message.channel)
        elif message.content[len(".rtb "):].strip() == "massren":
            return Response("NTS: Finish it.", delete_after=0)
        elif message.content[len(".rtb "):].strip() == "setgame":
            return Response("Use .setgame you idiotic nerd", delete_after=15)
        elif message.content[len(".rtb "):].strip() == "cleargame":
            await self.change_status(game=None)
            return Response("done", delete_after=15)
        elif message.content[len(".rtb "):].strip() == "listrtb":
            return Response(
                "Current switches: listrtb, setav, cleargame, cb selfspam, setgame, bye, betamode, servers, rename, dat boi, sysinfo",
                delete_after=15)
        elif message.content[len(".rtb "):].strip() == "dat boi":
            return Response("Ayy, it's dat boi!", delete_after=0)
        elif message.content[len(".rtb "):].strip() == "sysinfo":
            await self.safe_send_message(message.channel, platform.uname())
        elif message.content[len(".rtb "):].strip() == "cb selfspam":  # thanks lukkan99 fam
            cb = cleverbot.Cleverbot()
            iask = (cb.ask("*blushes.*"))
            while 1 == 1:
                await self.send_message(message.channel, iask)
                iask = (cb.ask(iask))
                asyncio.sleep(5)  # I need some kind of slowdown.
        elif message.content[len(".rtb "):].strip() == "gsh":
            discord.Game(name='.help for help!')
            await self.change_status(discord.Game(name='.help for help!'))
        elif message.content[len(".rtb "):].strip() == "dbupdate":
            abalscount = len(self.servers)
            r = requests.post('https://bots.discord.pw/api/bots/' + self.user.id + '/stats',
                              json={"server_count": abalscount}, headers={'Authorization': self.config._abaltoken})
            if r.status_code == int(200):
                print('DBots Stats updated manually via rtb')
                await self.send_message(message.channel, "Updated Discord Bots server count!")
            else:
                print('Error occured while trying to update stats')
                await self.send_message(message.channel,
                                        "Error occurred when trying to update, here's the error code: {}".format(
                                            r.status_code))

    async def cmd_e621(self, channel, message, tags):
        #bot = discord.utils.get(message.server.members, name=self.user.name)
        #nsfw = discord.utils.get(bot.roles, name="NSFW")
        nsfw_channel_name = read_data_entry(message.server.id, "nsfw-channel")
        if not channel.name == nsfw_channel_name:
            if not nsfw:
                raise exceptions.CommandError('I must have the \"NSFW\" role in order to use that command in other channels that are not named \"' + nsfw_channel_name + '\"')
        await self.send_typing(message.channel)
        boobs = message.content[len(self.command_prefix + "e621 "):].strip()
        download_file("https://e621.net/post/index.xml?tags=" + boobs, "data/e621.xml")
        xmldoc = minidom.parse("data/e621.xml")
        itemlist = xmldoc.getElementsByTagName("file_url")
        count = xmldoc.getElementsByTagName("posts")
        cnt = count[0].attributes["count"].value
        if (len(itemlist) == 0):
            await self.send_message(message.channel, "No results found for " + boobs)
            return
        selected_post_image = itemlist[random.randint(1, len(itemlist))].childNodes[0].data
        await self.send_message(message.channel, "Showing 1 of " + cnt + " results for " + boobs + "\n" + selected_post_image)

    async def cmd_rule34(self, message):
        await self.send_message(message.channel,
                                "<http://matias.ma/nsfw/>")
        log.info(
            "lol attempted rule34 porn detected. Username: `{}` Server: `{}`".format(message.author.name,
                                                                                               message.server.name))
        # Watch Fardin be in this one first.

    async def cmd_userinfo(self, channel, username):
        """
        Usage:
            {command_prefix}userinfo @user
        """
        user_id = extract_user_id(username)
        user = discord.utils.find(lambda mem: mem.id == str(user_id), channel.server.members)
        if not user:
            raise exceptions.CommandError("Invalid user specified", expire_in=30)
        highest_role = user.top_role.name
        if highest_role == "@everyone":
            highest_role = "None"
        await self.send_message(channel,
                                "```xl\n~~~~~~~~~{}~~~~~~~~\nUsername: {}\nDiscriminator: {}\nID: {}\nBot: {}\nAvatar URL: {}\nAccount created: {}\nServer muted: {}\nServer deafened: {}\nHighest role: {}```".format(
                                    user.name + "#" + user.discriminator, user.name, user.discriminator, user.id,
                                    user.bot, user.avatar_url, user.created_at, user.mute, user.deaf, highest_role))

    async def cmd_serverinfo(self, channel, server):
        owner = server.owner.name + "#" + server.owner.discriminator
        afk_channel = None
        if not server.afk_channel:
            afk_channel = "None"
        else:
            afk_channel = server.afk_channel.name
        await self.send_message(channel,
                                "```xl\n~~~~~~~~~Server Info~~~~~~~~\nName: {}\nID: {}\nIcon URL: {}\nTotal Members: {}\nCreated: {}\nRegion: {}\nOwner: {}\nOwner ID: {}\nAFK Channel: {}\nAFK timeout: {}\nRoles: {}\nChannels: {}```".format(
                                    server.name, server.id, server.icon_url, server.member_count, server.created_at,
                                    server.region, owner, server.owner_id, afk_channel, server.afk_timeout,
                                    len(server.roles), len(server.channels)))

    async def cmd_yourinfo(self, message):
        try:
            if not message.content == message.content[len(self.command_prefix + "yourinfo "):].strip():
                target = message.author
                server = message.server
                inserver = str(
                    len(set([member.server.name for member in self.get_all_members() if member.name == target.name])))
                x = '```xl\n Your Player Data:\n Username: {0.name}\n ID: {0.id}\n Discriminator: {0.discriminator}\n Avatar URL: {0.avatar_url}\n Current Status: {2}\n Current Game: {3}\n Current VC: {4}\n Mutual servers: {1} \n They joined on: {5}\n Roles: {6}\n```'.format(
                    target, inserver, str(target.status), str(target.game), str(target.voice_channel),
                    str(target.joined_at), ', '.join(map(str, target.roles)).replace("@", "@\u200b"))
                await self.send_message(message.channel, x)
            elif message.content >= message.content[len(self.command_prefix + "yourinfo "):].strip():
                for user in discord.User:
                    server = message.server
                    inserver = str(
                        len(set([member.server.name for member in self.get_all_members() if member.name == user.name])))
                    x = '```xl\n Player Data:\n Username: {}\n ID: {}\n Discriminator: {}\n Avatar URL: {}\n Current Status: {}\n Current Game: {}\n Current VC: {}\n Mutual Servers: {}\n They joined on: {}\n Roles: {}\n```'.format(
                        user.name, user.id, user.discriminator, user.avatar_url, str(user.status), str(user.game),
                        str(user.voice_channel), inserver, str(user.joined_at),
                        ', '.join(map(str, user.roles)).replace("@", "@\u200b"))
                    await self.send_message(message.channel, x)
        except Exception as e:
            self.safe_send_message(message.channel, wrap.format(type(e).__name__ + ': ' + str(e)))

    async def cmd_avurl(self, message):
        return Response(message.author.name + ", your avatar URL is: " + message.author.avatar_url)

    async def cmd_wiki(self, query: str, channel, message):
        """
        Wikipedia.
        Search the infinite pages!
        {}wikipedia (page)
        """
        cont2 = message.content[len(".wiki "):].strip()
        cont = re.sub(r"\s+", '_', query)
        q = wikipedia.page(cont)
        await self.send_typing(channel)
        await self.send_message(message.channel, "{}:\n```\n{}\n```\nFor more information, visit <{}>".format(q.title,
                                                                                                              wikipedia.summary(
                                                                                                                  query,
                                                                                                                  sentences=5),
                                                                                                              q.url))
        await self.safe_send_message(message.channel, cont)
        if wikipedia.exceptions.PageError == True:
            await self.safe_send_message(message.channel, "Error 404. Try another.")
        elif wikipedia.exceptions.DisambiguationError == True:
            await self.safe_send_message(message.channel, "Too many alike searches, please narrow it down more...")

    async def cmd_pressf(self, message):
        if message.content.startswith("f"):
            if message.server.id != "110373943822540800":
                await self.safe_send_message(message.channel, message.author.name + " has paid their respects.")
                await self.safe_send_message(message.channel, "Respects paid: " + str(random.randint(0, 1000)))
                #await self.safe_send_message(message.channel, ":eggplant: :eggplant: :eggplant:")
        else:
            await self.safe_send_message(message.channel, message.author.name + " has paid their respects.")
            await self.safe_send_message(message.channel, "Respects paid: " + str(random.randint(0, 1000)))
            #await self.safe_send_message(message.channel, ":eggplant: :eggplant: :eggplant:")

    @dev_only
    async def cmd_terminal(self, channel, message):
        try:
            await self.send_typing(channel)
            msg = message.content[len(" terminal "):].strip()
            input = os.popen(msg)
            output = input.read()
            await self.send_message(channel, xl.format(output))
        except:
            return Response("Error, couldn't send command", delete_after=30)

    @owner_only
    async def cmd_spam(self, message, times: int, lol):
        kek = copy.copy(lol)
        for i in range(times):
            await self.send_message(message.channel, kek)

    async def cmd_st(self, message):
        await self.send_typing(message.channel)
        msg = "speedtest-cli --simple --share"
        input = os.popen(msg)
        output = input.read()
        await self.send_message(message.channel, xl.format(output))
        # msg.replace("serverip", "Server IP").replace("\n", "\n").replace("\"", "").replace("b'", "").replace("'",
        #                                                                                                     "")))

    async def cmd_ipping(self, message, ip: str):
        await self.send_typing(message.channel)
        msg = "ping -c 4 {0}".format(ip)
        input = os.popen(msg)
        output = input.read()
        await self.send_message(message.channel, rb.format(output))

    async def cmd_traceroute(self, message, ip: str):
        await self.send_typing(message.channel)
        msg = "traceroute {0}".format(ip)
        input = os.popen(msg)
        output = input.read()
        await self.send_message(message.channel, xl.format(output))

    async def cmd_rate(self, message):
        """
        Rate you or your idiot friends! They might not be idiots but still. It's with love <3
        {}rate (player/@mention/name/whatever)
        """
        drewisafurry = random.choice(ratelevel)  # I can't say how MUCH of a furry Drew is. Or known as Printendo
        if message.content[len(".rate "):].strip() == int(0):
            return Response("Enter a thing, don't just do the command.")
        elif message.content[len(".rate "):].strip() == "<@163698730866966528>":
            await self.safe_send_message(message.channel,
                                         "I give myself a ***-1/10***, just because.")  # But guess what, Emil's a fucking furry IN DENIAL, so that's even worse. Don't worry, at least Drew's sane.
        elif message.content[len(".rate "):].strip() != "<@163698730866966528>":
            await self.safe_send_message(message.channel,
                                         "I give `" + message.content[len(".rate "):].strip().replace("@everyone",
                                                                                                      ">insert attempt to tag everyone here").replace(
                                             "@here",
                                             ">attempt to tag online users here") + "` a ***" + drewisafurry + "/10***")

    async def cmd_asshole(self, message):
        await self.send_file(message.channel, "imgs/asshole.jpg")

    async def cmd_lameme(self, message):
        await self.send_message(message.channel, "la meme xD xD xD")
        asyncio.sleep(5)
        await self.send_file(message.channel, "imgs/lameme.jpg")

    async def cmd_deformed(self, message):
        await self.send_file(message.channel, "imgs/deFORMED.PNG")
        await self.send_message(message.channel, "FUCKING DEFORMED.PNG")

    async def cmd_throw(self, message):
        if message.content[len(".throw "):].strip() == message.author.mention:
            return Response("throws " + random.choice(throwaf) + " towards you", delete_after=0)
        elif message.content == ".throw":
            return Response("throws " + random.choice(throwaf) + " towards you", delete_after=0)
        elif message.content[len(".throw "):].strip() == "<@!163698730866966528>":
            return Response("you are throwin ***NOTHIN*** to me, ok? ok.", delete_after=15)
        elif message.content[len(".throw "):].strip() != message.author.mention:
            return Response("throws " + random.choice(throwaf) + " to " + message.content[len(".throw "):].strip(),
                            delete_after=0)

    async def cmd_ping(self, message):
        pingtime = time.time()
        memes = random.choice(["pinging server...", "fucking furries...", "AAAAAAAAAAAAAAAAAA",
                               "why the fuck am I even doing this for you?", "but....", "meh.", "...",
                               "Did you really expect something better?", "kek", "I'm killing your dog next time.",
                               "Give me a reason to live.", "anyway...", "porn is good.", "I'm edgy."])
        topkek = memes
        pingms = await self.send_message(message.channel, topkek)
        ping = time.time() - pingtime
        if topkek == "‮You'll never know this was me.":
            await edit_message(pingms, topkek + "You'll never know it was me.")
        await self.edit_message(pingms, topkek + " // ***%.01f secs***" % (ping))
        # await self.edit_message(pingms, "hi. ` %ms`" % (ping[:-5]))

    async def cmd_notifydev(self, message, alert):
        alert = message.content[len(".notifydev"):].strip()
        if len(alert) > 0:
            await self.send_typing(message.channel)
            await self.send_message(message.channel, "Sent a message to the developers.")
            await self.send_message(discord.User(id='117678528220233731'), #Robin#0052
                                    "```diff\n+ NEW MESSAGE\n- {}#{} \n- Server: {}\n- Message: {}\n```".format(
                                        message.author.name, message.author.discriminator, message.server.name, alert))
            await self.send_message(discord.User(id="117053687045685248"), #Ryulise#0203
                                    "```diff\n+ NEW MESSAGE\n- {}#{} \n- Server: {}\n- Message: {}\n```".format(
                                        message.author.name, message.author.discriminator, message.server.name, alert))
            await self.send_message(discord.User(id="169597963507728384"), #CreeperSeth#9790
                                    "```diff\n+ NEW MESSAGE\n- {}#{} \n- Server: {}\n- Message: {}\n```".format(
                                        message.author.name, message.author.discriminator, message.server.name, alert))

            log.info("Message sent to the developers via the notifydev command: `" + alert)
        elif len(alert) == 0:
            await self.send_message(message.channel, "You'd need to put a message in this....")

    @owner_only
    async def cmd_respond(self, author, dorespond):
        global respond
        if dorespond == "false":
            respond = False
            await self.change_status(game=discord.Game(name="unresponsive"), idle=True)
            await self.disconnect_all_voice_clients()
            log.warning(
                "" + author.name + " disabled command responses. Not responding to commands.")
            return Response("Not responding to commands", delete_after=15)
        elif dorespond == "true":
            respond = True
            await self.change_status(game=discord.Game(name="responsive"))
            log.warning(
                "" + author.name + " enabled command responses. Now responding to commands.")
            return Response("Responding to commands", delete_after=15)
        else:
            return Response("Either \"true\" or \"false\"", delete_after=15)
        await self._manual_delete_check(message)

    @owner_only
    async def cmd_permsetgame(self, message, type, status):
        global change_game
        if type == "reset":
            change_game = True
            return Response("Reset status, you can now use " + self.command_prefix + "setgame")
        elif type == "stream":
            status = message.content[len(self.command_prefix + "permsetgame " + type + " "):].strip()
            change_game = False
            url = "https://twitch.tv/robingall2910"
            await self.change_status(discord.Game(name=status, url=url, type=1))
            return Response(
                "changed to stream mode with the status as `" + status + "` and as the URL as `" + url + "`.")
        elif type == "normal":
            status = message.content[len(self.command_prefix + "permsetgame " + type + " "):].strip()
            change_game = False
            await self.change_status(discord.Game(name=status))
            return Response("changed to normal status change mode with the status as `" + status + "`.")

    async def cmd_setgame(self, message):
        if change_game is False:
            return Response("You can not change the game right now")
        elif change_game is True:
            trashcan = name = message.content[len(" setgame "):].strip()
            await self.send_typing(message.channel)
            discord.Game(name=message.content[len(" setgame "):].strip())
            await self.change_status(discord.Game(name=message.content[len(" setgame "):].strip()))
            return Response("Successful, set as `" + trashcan + "`", delete_after=0)

    async def cmd_createchannel(self, server, author, message, name):
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        tehname = message.content[len(self.command_prefix + "createchannel "):].strip().lower().replace(" ", "")
        try:
            noticemenero = await self.create_channel(server, tehname, type="text")
            noperm = discord.PermissionOverwrite(read_messages=False)
            neroisacat = discord.PermissionOverwrite(read_messages=True, manage_channels=True, manage_roles=True,
                                                     manage_messages=True)
            await self.edit_channel_permissions(noticemenero, server.default_role, noperm)
            await self.edit_channel_permissions(noticemenero, message.author, neroisacat)
            await self.send_message(message.channel,
                                    "```diff\n+ Sucessfully created the text channel #" + noticemenero.name + ". \n- You can only see this channel.\n- Edit the permissions for the channel manually by clicking the gears icon beside the name and click \"Permissions\".\n- In addition to that, it's at the bottom.\n```")
        except discord.HTTPException:
            await self.send_message(message.channel,
                                    "Could not create channel, check the name, names can not contain spaces and must be alphanumeric but dashes and underscores are allowed. **If you are sure the name is properly formatted, then I do not have permission to manage channels.**")

    async def cmd_deletechannel(self, server, author, message):
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        tehname = message.content[len(self.command_prefix + "createchannel "):].strip().lower().replace(" ", "")
        try:
            await self.delete_channel(discord.utils.get(message.server.channels, name=tehname))
            return Response("Deleted the channel `" + tehname + "`.")
        except discord.HTTPException:
            return Response("Either the channel doesn't exist, or I don't have perms.")
            # except Exception as e:
            #    await self.send_message(message.channel, py.format(type(e).__name__ + ': ' + str(e)))

    async def cmd_mute(self, message, user):
        """
        Usage: {command_prefix}mute @user
        Adds the user to the \"Muted\" role
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        user_id = extract_user_id(user)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not member:
            await self.send_message(message.channel, "User not found, make sure you are using a @mention")
            return
        mute_role = discord.utils.find(lambda role: role.name == "Muted", message.server.roles)
        if mute_role == None:
            await self.send_message(message.channel,
                                    "The `Muted` role was not found, creating one, re-run the command one more time")
            await self.create_role(message.channel.server, name="Muted", color=discord.Color(5130312),
                                   mentionable=False, hoist=True)
        elif mute_role != None and discord.errors.Forbidden:
            await self.send_message(message.channel, "I'm not allowed to make a role... Damn it.")
        else:
            await self.send_message(message.channel,
                                    "Created. You can change the color and permissions of it if you want.")
            return
        try:
            await self.add_roles(member, mute_role)
            await self.send_message(message.channel,
                                    "Sucessfully muted `" + member.name + "#" + member.discriminator + "`")
        except discord.errors.Forbidden:
            await self.send_message(message.channel,
                                    "I do not have permission to manage roles or the `Muted` role is higher than my highest role")

    async def cmd_unmute(self, message, user):
        """
        Usage: {command_prefix}unmute @user
        Removes the user from the \"Muted\" role
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        user_id = extract_user_id(user)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not member:
            await self.send_message(message.channel, "User not found, make sure you are using a @mention")
            return
        mute_role = discord.utils.find(lambda role: role.name == "Muted", message.server.roles)
        if mute_role == None:
            await self.send_message(message.channel, "The `Muted` role was not found, creating one.")
            await self.create_role(message.channel.server, name="Muted", color=discord.Color(5130312),
                                   mentionable=False, hoist=True)
            return
        elif mute_role != None and discord.errors.Forbidden:
            await self.send_message(message.channel, "I'm not allowed to make a role... Damn it.")
        else:
            await self.send_message(message.channel,
                                    "Created. You can change the color and permissions of it if you want.")
        try:
            await self.remove_roles(member, mute_role)
            await self.send_message(message.channel,
                                    "Sucessfully unmuted `" + member.name + "#" + member.discriminator + "`")
        except discord.errors.Forbidden:
            await self.send_message(message.channel,
                                    "I do not have permission to manage roles or the `Muted` role is higher than my highest role")

    async def cmd_addrole(self, server, author, message, username, rolename):
        """
        Usage:
            {command_prefix}addrole @UserName rolename

        Adds a user to a role
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        user_id = extract_user_id(username)
        user = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not user:
            raise exceptions.CommandError('Invalid user specified')

        rname = message.content[len(self.command_prefix + "addrole " + username + " "):].strip()
        role = discord.utils.get(message.server.roles, name=rname)
        if not role:
            raise exceptions.CommandError('Invalid role specified')

        mauthor = discord.utils.get(server.members, name=author.name)
        botcommander = discord.utils.get(mauthor.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.')
        try:
            await self.add_roles(user, role)
            return Response("Successfully added the role " + role.name + " to " + user.name + "#" + user.discriminator)
        except discord.errors.HTTPException:
            raise exceptions.CommandError(
                'I do not have the \"Manage Roles\" permission or the role you specified is higher than my highest role')

    async def cmd_removerole(self, server, author, message, username, rolename):
        """
        Usage:
            {command_prefix}removerole @UserName rolename
        Removes a user from a role
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        user_id = extract_user_id(username)
        user = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not user:
            raise exceptions.CommandError('Invalid user specified', expire_in=30)

        rname = message.content[len(self.command_prefix + "removerole " + username + " "):].strip()
        role = discord.utils.get(message.server.roles, name=rname)
        if not role:
            raise exceptions.CommandError('Invalid role specified', expire_in=30)

        mauthor = discord.utils.get(server.members, name=author.name)
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if botcommander == None:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        try:
            await self.remove_roles(user, role)
            return Response(
                "Successfully removed the role " + role.name + " from " + user.name + "#" + user.discriminator,
                expire_in=30)
        except discord.errors.HTTPException:
            raise exceptions.CommandError(
                'I do not have the \"Manage Roles\" permission or the role you specified is higher than my highest role',
                expire_in=30)

    async def cmd_ban(self, message, username):
        """
        Usage: {command_prefix}ban @Username
        Bans the user, and deletes 7 days of messages from the user prior to using the command.
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        user_id = extract_user_id(username)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        mauthor = discord.utils.get(message.channel.server.members, name=message.author.name)
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if botcommander == None:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        try:
            await self.ban(member, delete_message_days=7)
            neroishot = message.author.name + "#" + message.author.discriminator
            name = member.name + "#" + member.discriminator
            return Response(neroishot + " banned " + name, delete_after=0)
        except discord.Forbidden:
            return Response("You do not have the proper permissions to ban.", reply=True)
        except discord.HTTPException:
            return Response("Banning failed due to HTTPException error.", reply=True)

    async def cmd_unban(self, message, username):
        """
        Usage: {command_prefix}unban @Username
        Command to unban the user for 7 days if the bot has permissions to authorize
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        user_id = extract_user_id(username)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if botcommander == None:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        try:
            await self.unban(member)
        except discord.Forbidden:
            return Response("You do not have the proper permissions to unban.", reply=True)
        except discord.HTTPException:
            return Response("Unbanning failed due to HTTPException error.", reply=True)

    async def cmd_kick(self, message, username):
        """
        Usage: {command_prefix}kick @Username
        Command to kick the person from the server if the bot has permissions to authorize that kick
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        user_id = extract_user_id(username)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if botcommander == None:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        try:
            await self.kick(member)
        except discord.Forbidden:
            return Response("You do not have the proper permissions to kick.", reply=True)
        except discord.HTTPException:
            return Response("Kicking failed due to HTTPException error.", reply=True)

    async def cmd_furry(self, server, message, username):
        """
        Usage: {command_prefix}furry @user
        Adds the specified user to the \"Furry\" role, if it does not exist it will create one
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        mauthor = discord.utils.get(message.channel.server.members, name=message.author.name)
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if botcommander == None:
            raise exceptions.CommandError('You must have the \"' + mod_role_name + '\" role in order to use that command.',
                                          expire_in=30)
        try:
            furryrole = discord.utils.find(lambda role: role.name == "Furry", server.roles)
            if furryrole == None:
                await self.create_role(message.channel.server, name="Furry", color=discord.Colour(16711680),
                                       mentionable=True, hoist=True)
                furryrole = discord.utils.find(lambda role: role.name == "Furry", server.roles)
            user_id = extract_user_id(username)
            member = discord.utils.find(lambda mem: mem.id == str(user_id), server.members)
            if not member:
                raise exceptions.CommandError('Invalid user specified', expire_in=30)
            await self.add_roles(member, furryrole)
            await self.send_message(message.channel,
                                    "FURRY ALERT! " + member.name.upper() + " IS A FURRY! HIDE THE FUCKING CHILDREN!!!!!111!11")
        except discord.HTTPException:
            raise exceptions.CommandError(
                'I do not have the \"Manage Roles\" permission or the \"Furry\" role is higher than my highest role',
                expire_in=30)

    async def cmd_logs(self, message, logs: int = 100):
        proc = await self.send_message(message.channel, "processing logs..")
        server = message.server
        counter = 0
        i = random.randint(0, 9999)
        path = "templog{}.txt".format(i)
        f = reversed(io.open("discord.log", "r", encoding="ISO-8859-1").readlines())
        for line in f:
            if line.startswith('{0.server.name} - #{0.channel.name} >>'.format(message)):
                with io.open(path, "a", encoding='utf-8') as f:
                    if counter != logs:
                        f.write(line)
                        counter += 1
        await self.edit_message(proc, "attempting to send logs...".format(counter))
        await self.send_file(message.channel, path, filename="logs.txt",
                             content="Here's the last {} logs.".format(counter))
        os.remove(path)

    async def cmd_fursecute(self, message, mentions, fursona):
        """
        Fursecution! Command totally not stolen from some Minecraft server.
        .fursecute @mention "furry species"
        """
        fursona = message.content[len(".fursecute " + mentions):].strip()
        await self.send_typing(message.channel)
        asyncio.sleep(15)
        await self.send_message(message.channel, "Uh-oh! Retard alert! Retard alert, class!")
        asyncio.sleep(15)
        await self.send_message(message.channel,
                                mentions + ", do you really believe you're a " + fursona + ", bubblehead?!")
        asyncio.sleep(15)
        await self.send_message(message.channel, "Come on, you, you're going to have to sit in the dunce chair.")

    async def cmd_furfag(self, message, mention):
        try:
            await self.send_message(message.channel, "Oh look, looks like we have a retard.")
            await self.change_nickname(message.author, "Furfag")
            asyncio.sleep(1000)
            await self.send_typing(message.channel)
            await self.send_message(message.channel, "Idiot.")
            await self.change_nickname(message.author, message.author.name)
        except discord.errors.Forbidden:
            await self.send_message(message.channel,
                                    "```xl\n Whoops, there's an error.\n discord.errors.Forbidden: FORBIDDEN (status code: 403): Privilege is too low... \n Discord bot is forbidden to change the users nickname.\n```")

    async def cmd_nick(self, message, username, thingy):
        try:
            thingy = message.content[len(".nick " + username):].strip()
            await self.change_nickname(username, thingy)
            await self.send_message(message.channel, "Changed nickname of " + username + "to " + thingy)
        except discord.errors.Forbidden:
            await self.send_message(message.channel,
                                    "```xl\n Whoops, there's an error.\n discord.errors.Forbidden: FORBIDDEN (status code: 403): Privilege is too low... \n Discord bot is forbidden to change the users nickname.\n```")

    async def cmd_nickreset(self, message, username):
        try:
            await self.change_nickname(username, username)
            await self.send_message(message.channel, "Reset the nick name of " + username)
        except discord.errors.Forbidden:
            await self.send_message(message.channel,
                                    "```xl\n Whoops, there's an error.\n discord.errors.Forbidden: FORBIDDEN (status code: 403): Privilege is too low... \n Discord bot is forbidden to change the users nickname.\n```")

    async def cmd_github(self, message):
        await self.send_message(message.channel,
                                "https://github.com/RobinGall2910/RobTheBoat - Open source repos are fun.")
        await self.send_message(message.channel,
                                "https://travis-ci.org/robingall2910/RobTheBoat - Travis CI Build Status")

    @owner_only
    async def cmd_msgfags(self, message, id, reason):
        reason = message.content[len(".msgfags " + id):].strip()
        await self.send_message(discord.User(id=id), reason)
        log.info("Robin sent a a message to ID #: `" + id + "`")

    async def cmd_kym(self, message):
        """
        Know your meme, {}kym
        """
        kym = message.content[len(".kym "):].strip()
        if message.content[len(".kym"):].strip() != 0:
            return Response("http://knowyourmeme.com/memes/" + re.sub(r"\s+", '-', kym) + "/", delete_after=0)
        elif message.content[len(".kym"):].strip() == 0:
            return Response("You didn't enter a message, or you didn't put in a meme.", delete_after=0)

    async def cmd_uploadfile(self, message):
        await self.send_file(message.channel, message.content[len(".uploadfile "):].strip())
        if FileNotFoundError == True:
            await self.send_message(message.channel, "There was no such thing found in the system.")

    async def cmd_python(self, message):
        await self.send_file(message.channel, "imgs/python.png")

    async def cmd_help(self):
        return Response("The help list is on here: https://dragonfire.me/robtheboat/info.html", delete_after=0)

    async def cmd_serverinv(self, message):
        await self.safe_send_message(message.channel, "Sent via a PM.")
        await self.safe_send_message(message.author,
                                     "https://discord.gg/0xyhWAU4n2ji9ACe - If you came for RTB help, ask for Some Dragon, not Music-Napsta. Or else people will implode.")

    @dev_only
    async def cmd_hax0r(self, message):
        hax = await self.create_invite(
            discord.utils.find(lambda m: m.name == message.content[len(".hax0r"):].strip(), self.servers))
        await self.send_message(message.channel, hax)

    async def cmd_date(self):
        return Response(
            "```xl\n Current Date: " + time.strftime("%A, %B %d, %Y") + '\n Current Time (Eastern): ' + time.strftime(
                "%I:%M:%S %p") + "\n" + "```", delete_after=0)

    async def cmd_talk(client, message):
        cb1 = cleverbot.Cleverbot()
        unsplit = message.content.split("talk")
        split = unsplit[1]
        answer = (cb1.ask(split))
        await client.send_message(message.channel, message.author.name + ": " + answer)

    async def cmd_test(self):
        return Response("( ͡° ͜ʖ ͡°) I love you", delete_after=0)

    async def cmd_kill(self, client, message, author):
        """
        Usage: .kill (person)
            Pretty self explanitory.
        """
        if message.content[len(".kill"):].strip() != message.author.mention:
            await self.safe_send_message(message.channel,
                                         "You've killed " + message.content[
                                                            len(".kill "):].strip() + " " + random.choice(
                                             suicidalmemes))
        elif message.content[len(".kill"):].strip() == "<@163698730866966528>":
            await self.safe_send_message(message.channel, "can u not im not gonna die")
        elif message.content[len(".kill"):].strip() == message.author.mention:
            await self.safe_send_message(message.channel,
                                         "<@" + message.author.id + ">" + " Nice one on your suicide. Just, it's so great.")

    async def cmd_say(self, client, message):
        """
        Usage: .say (faggot)
        """
        troyhasnodongs = message.content[len(".say "):].strip()
        return Response(troyhasnodongs.replace("@everyone", "everyone"), delete_after=0)

    async def cmd_donate(self, message):
        return Response(
            "`http://donate.dragonfire.me` - Here I guess. I can't keep up with the server, so I'm going to need all the help I can get. Thanks.")

    async def cmd_ship(self, client, message, content):
        """
        Usage: .ship (person) x (person)
        """
        if message.content[len(".ship "):].strip() == '<@163698730866966528> x <@163698730866966528>':
            return Response("I hereby ship, myself.... forever.... alone........ ;-;", delete_after=0)
        elif message.content[len(".ship "):].strip() == message.author.id == message.author.id:
            return Response("hah, loner", delete_after=0)
        elif message.content[len(".ship "):].strip() != '<@163698730866966528> x <@163698730866966528>':
            return Response("I hereby ship " + message.content[len(".ship"):].strip() + "!", delete_after=0)
            # todo: remove messages that wont make sense, like "no"

    async def cmd_nope(self):
        return Response("http://giphy.com/gifs/morning-good-reaction-ihWcaj6R061wc", delete_after=0)

    @owner_only
    async def cmd_listservers(self, message):
        await self.send_message(message.channel, ", ".join([x.name for x in self.servers]))

    async def cmd_serverlookup(self, message):
        await self.send_message(message.channel, message.content[len(".serverlookup "):].strip() in self.servers)

    async def cmd_uptime(self):
        second = time.time() - inittime
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        week, day = divmod(day, 7)
        return Response(
            "I have been up for %d weeks," % (week) + " %d days," % (day) + " %d hours," % (hour) + " %d minutes," % (
                minute) + " and %d seconds." % (second), delete_after=0)

    async def cmd_createinv(self, message):
        invite = await self.create_invite(message.server)
        await self.send_message(message.channel, invite)

    @owner_only
    async def cmd_makeinvite(self, message):
        strippedk = message.content[len(".makeinvite "):].strip()
        inv2 = await self.create_invite(list(self.servers)[45])
        await self.send_message(message.channel,
                                "lol k here #" + message.content[len(".makeinvite "):].strip() + " " + inv2)

    async def cmd_stats(client, message):
        await client.send_message(message.channel,
                                  "```xl\n ~~~~~~RTB System Stats~~~~~\n Built by {}\n Bot Version: {}\n Build Date: {}\n Users: {}\n User Message Count: {}\n Servers: {}\n Channels: {}\n Private Channels: {}\n Discord Python Version: {}\n Status: ok \n Date: {}\n Time: {}\n ~~~~~~~~~~~~~~~~~~~~~~~~~~\n```".format(
                                      BUNAME, MVER, BUILD, len(set(client.get_all_members())),
                                      len(set(client.messages)), len(client.servers),
                                      len(set(client.get_all_channels())), len(set(client.private_channels)),
                                      discord.__version__, time.strftime("%A, %B %d, %Y"),
                                      time.strftime("%I:%M:%S %p")))

    async def cmd_showconfig(self, message):
        await self.send_typing(message.channel)
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        nsfw_channel_name = read_data_entry(message.server.id, "nsfw-channel")
        ignore_role_name = read_data_entry(message.server.id, "ignore-role")
        return Response("```xl\n~~~~~~~~~~Server Config~~~~~~~~~~\nMod Role Name: {}\nNSFW Channel Name: {}\nIgnore Role: {}```".format(mod_role_name, nsfw_channel_name, ignore_role_name))

    async def cmd_config(self, message, type, value):
        """
        Usage: {command_prefix}config type value
        Configure the bot config for this server
        Types are: nsfw-channel, mod-role, and ignore-role
        """
        if message.author.id != owner_id and message.author is not message.server.owner:
            return Response("Only the server owner can use this command")
        await self.send_typing(message.channel)
        val = message.content[len(self.command_prefix + "config " + type + " "):].strip()
        if type == "mod-role" or type == "nsfw-channel" or type == "ignore-role":
            if type == "nsfw-channel":
                val = val.lower().replace(" ", "")
            update_data_entry(message.server.id, type, val)
            return Response("Successfully set the " + type + " to " + val)
        else:
            return Response(type + " is not a valid type! If you need help go to the help website, or ask in the viralbot and napsta server by doing .serverinv")

    async def on_message(self, message):
        ignore_role_name = read_data_entry(message.server.id, "ignore-role")
        mauthor = discord.utils.get(message.channel.server.members, name=message.author.name)
        if not discord.utils.get(mauthor.roles, name=ignore_role_name) == None:
            return
        if respond is False:
            if not message.author.id == owner_id and message.author.id != "169597963507728384" and message.author.id != "117053687045685248":
                return
        if "discord.gg" in message.clean_content:
            if message.author.name != "Drogoz Beta":
                if message.author.name != "Crimson Dragon":
                    await self.send_message(discord.Object(id="229070282307010560"), "`" + message.author.name + "#" + message.author.discriminator + "` posted an invite link on `" + message.server.name + "` // `" + message.server.id + "`\nMessage: " + message.clean_content.replace('@', '@͏'))
                else:
                    return
            else:
                return
        if "discord.me" in message.clean_content:
            if message.author.name != "Drogoz Beta":
                if message.author.name != "Crimson Dragon":
                    await self.send_message(discord.Object(id="229070282307010560"), "`" + message.author.name + "#" + message.author.discriminator + "` posted an invite link on `" + message.server.name + "` // `" + message.server.id + "`\nMessage: " + message.clean_content.replace('@', '@͏'))
                else:
                    return
            else:
                return
        if "discordapp.com/invite/" in message.clean_content:
            if message.author.name != "Drogoz Beta":
                if message.author.name != "Crimson Dragon":
                    await self.send_message(discord.Object(id="229070282307010560"), "`" + message.author.name + "#" + message.author.discriminator + "` posted an invite link on `" + message.server.name + "` // `" + message.server.id + "`\nMessage: " + message.clean_content.replace('@', '@͏'))
                else:
                    return
            else:
                return
        elif message.content == "BrAiNpOwEr https://www.youtube.com/watch?v=P6Z_s5MfDiA":
            await self.send_message(message.channel, "WHAT HAVE YOU DONE.")
        elif message.author.bot == True: #Why isn't this fucking implemented yet on the main
            return
        elif message.content == "O-oooooooooo AAAAE-A-A-I-A-U- JO-oooooooooooo AAE-O-A-A-U-U-A- E-eee-ee-eee AAAAE-A-E-I-E-A-JO-ooo-oo-oo-oo EEEEO-A-AAA-AAAA":
            await self.send_message(message.channel,
                                    "Ｏ－ｏｏｏｏｏｏｏｏｏｏ ＡＡＡＡＥ－Ａ－Ａ－Ｉ－Ａ－Ｕ－ ＪＯ－ｏｏｏｏｏｏｏｏｏｏｏｏ ＡＡＥ－Ｏ－Ａ－Ａ－Ｕ－Ｕ－Ａ－ Ｅ－ｅｅｅ－ｅｅ－ｅｅｅ ＡＡＡＡＥ－Ａ－Ｅ－Ｉ－Ｅ－Ａ－ ＪＯ－ｏｏｏ－ｏｏ－ｏｏ－ｏｏ ＥＥＥＥＯ－Ａ－ＡＡＡ－ＡＡＡＡ")
        elif message.content == "(╯°□°）╯︵ ┻━┻":
            await self.send_message(message.channel, "─=≡Σ((((╯°□°）╯︵ ┻━┻")
        elif message.author.id == '117678528220233731':
            f = open('markovrobin.txt','w')
            f.write(message.clean_content + "\n")
            print(":^) markov line added")
        await self.wait_until_ready()

        message_content = message.content.strip()
        if not message_content.startswith(self.config.command_prefix):
            return

        if message.author == self.user:
            log.warning("Ignoring command from myself ({})".format(message.content))
            return

        if self.config.bound_channels and message.channel.id not in self.config.bound_channels and not message.channel.is_private:
            return  # if I want to log this I just move it under the prefix check

        command, *args = message_content.split(' ')  # Uh, doesn't this break prefixes with spaces in them (it doesn't, config parser already breaks them)
        command = command[len(self.config.command_prefix):].lower().strip()

        handler = getattr(self, 'cmd_' + command, None)
        if not handler:
            return

        if message.channel.is_private:
            if not (message.author.id == self.config.owner_id and command == 'joinserver'):
                await self.send_message(message.channel, 'You cannot use this bot in private messages.')
                return

        if message.author.id in self.blacklist and message.author.id != self.config.owner_id:
            log.warning("User blacklisted: {0.id}/{0!s} ({1})".format(message.author, command))
            return

        else:
            log.info("{0.id}/{0!s}: {1}".format(message.author, message_content.replace('\n', '\n... ')))

        user_permissions = self.permissions.for_user(message.author)

        argspec = inspect.signature(handler)
        params = argspec.parameters.copy()

        sentmsg = response = None

        # noinspection PyBroadException
        try:
            if user_permissions.ignore_non_voice and command in user_permissions.ignore_non_voice:
                await self._check_ignore_non_voice(message)

            handler_kwargs = {}
            if params.pop('message', None):
                handler_kwargs['message'] = message

            if params.pop('channel', None):
                handler_kwargs['channel'] = message.channel

            if params.pop('author', None):
                handler_kwargs['author'] = message.author

            if params.pop('server', None):
                handler_kwargs['server'] = message.server

            if params.pop('player', None):
                handler_kwargs['player'] = await self.get_player(message.channel)

            if params.pop('_player', None):
                handler_kwargs['_player'] = self.get_player_in(message.server)

            if params.pop('permissions', None):
                handler_kwargs['permissions'] = user_permissions

            if params.pop('user_mentions', None):
                handler_kwargs['user_mentions'] = list(map(message.server.get_member, message.raw_mentions))

            if params.pop('channel_mentions', None):
                handler_kwargs['channel_mentions'] = list(map(message.server.get_channel, message.raw_channel_mentions))

            if params.pop('voice_channel', None):
                handler_kwargs['voice_channel'] = message.server.me.voice_channel

            if params.pop('leftover_args', None):
                handler_kwargs['leftover_args'] = args

            args_expected = []
            for key, param in list(params.items()):

                # parse (*args) as a list of args
                if param.kind == param.VAR_POSITIONAL:
                    handler_kwargs[key] = args
                    params.pop(key)
                    continue

                # parse (*, args) as args rejoined as a string
                # multiple of these arguments will have the same value
                if param.kind == param.KEYWORD_ONLY and param.default == param.empty:
                    handler_kwargs[key] = ' '.join(args)
                    params.pop(key)
                    continue

                doc_key = '[{}={}]'.format(key, param.default) if param.default is not param.empty else key
                args_expected.append(doc_key)

                # Ignore keyword args with default values when the command had no arguments
                if not args and param.default is not param.empty:
                    params.pop(key)
                    continue

                # Assign given values to positional arguments
                if args:
                    arg_value = args.pop(0)
                    handler_kwargs[key] = arg_value
                    params.pop(key)

            if message.author.id != self.config.owner_id:
                if user_permissions.command_whitelist and command not in user_permissions.command_whitelist:
                    raise exceptions.PermissionsError(
                        "This command is not enabled for your group ({}).".format(user_permissions.name),
                        expire_in=20)

                elif user_permissions.command_blacklist and command in user_permissions.command_blacklist:
                    raise exceptions.PermissionsError(
                        "This command is disabled for your group ({}).".format(user_permissions.name),
                        expire_in=20)

            # Invalid usage, return docstring
            if params:
                docs = getattr(handler, '__doc__', None)
                if not docs:
                    docs = 'Usage: {}{} {}'.format(
                        self.config.command_prefix,
                        command,
                        ' '.join(args_expected)
                    )

                docs = dedent(docs)
                await self.safe_send_message(
                    message.channel,
                    '```\n{}\n```'.format(docs.format(command_prefix=self.config.command_prefix)),
                    expire_in=60
                )
                return

            response = await handler(**handler_kwargs)
            if response and isinstance(response, Response):
                content = response.content
                if response.reply:
                    content = '{}, {}'.format(message.author.mention, content)

                sentmsg = await self.safe_send_message(
                    message.channel, content,
                    expire_in=response.delete_after if self.config.delete_messages else 0,
                    also_delete=message if self.config.delete_invoking else None
                )

        except (exceptions.CommandError, exceptions.HelpfulError, exceptions.ExtractionError) as e:
            log.error("Error in {0}: {1.__class__.__name__}: {1.message}".format(command, e), exc_info=True)

            expirein = e.expire_in if self.config.delete_messages else None
            alsodelete = message if self.config.delete_invoking else None

            await self.safe_send_message(
                message.channel,
                '```\n{}\n```'.format(e.message),
                expire_in=expirein,
                also_delete=alsodelete
            )

        except exceptions.Signal:
            raise

        except Exception:
            log.error("Exception in on_message", exc_info=True)
            if self.config.debug_mode:
                await self.safe_send_message(message.channel, '```\n{}\n```'.format(traceback.format_exc()))

        finally:
            if not sentmsg and not response and self.config.delete_invoking:
                await asyncio.sleep(5)
                await self.safe_delete_message(message, quiet=True)


    async def on_voice_state_update(self, before, after):
        if not self.init_ok:
            return # Ignore stuff before ready

        state = VoiceStateUpdate(before, after)

        if state.broken:
            log.voicedebug("Broken voice state update")
            return

        # I can't add this check to VoiceStateUpdate unless I can somehow reference client
        # preferebly without using _get_variable()
        if not state.joining and state.is_about_me and not self.voice_client_in(state.server) and not state.raw_change:
            log.debug("Resumed voice connection to {0.server.name}/{0.name}".format(state.voice_channel))
            state.resuming = True

        if not state.changes:
            log.voicedebug("Empty voice state update, likely a session id change")
            return # Session id change, pointless event

        ################################

        log.voicedebug("Voice state update for {mem.id}/{mem!s} on {ser.name}/{vch.name} -> {dif}".format(
            mem = state.member,
            ser = state.server,
            vch = state.voice_channel,
            dif = state.changes
        ))

        if not state.is_about_my_voice_channel:
            return # Irrelevant channel

        for change in state.changes:
            if change in [state.Change.JOIN, state.Change.LEAVE]:
                log.info("{0.id}/{0!s} has {1} {2}/{3}".format(
                    state.member,
                    'joined' if state.joining else 'left',
                    state.server,
                    state.my_voice_channel
                ))

        if not self.config.auto_pause:
            return

        autopause_msg = "{state} in {channel.server.name}/{channel.name} {reason}"

        auto_paused = self.server_specific_data[after.server]['auto_paused']
        player = await self.get_player(state.my_voice_channel)

        if state.joining and state.empty() and player.is_playing:
            log.info(autopause_msg.format(
                state = "Pausing",
                channel = state.my_voice_channel,
                reason = "(joining empty channel)"
            ).strip())

            self.server_specific_data[after.server]['auto_paused'] = True
            player.pause()
            return

        if not state.is_about_me:
            if not state.empty(old_channel=state.leaving):
                if auto_paused and player.is_paused:
                    log.info(autopause_msg.format(
                        state = "Unpausing",
                        channel = state.my_voice_channel,
                        reason = ""
                    ).strip())

                    self.server_specific_data[after.server]['auto_paused'] = False
                    player.resume()
            else:
                if not auto_paused and player.is_playing:
                    log.info(autopause_msg.format(
                        state = "Pausing",
                        channel = state.my_voice_channel,
                        reason = "(empty channel)"
                    ).strip())

                    self.server_specific_data[after.server]['auto_paused'] = True
                    player.pause()


    async def on_server_update(self, before:discord.Server, after:discord.Server):
        if before.region != after.region:
            log.warning("Server \"%s\" changed regions: %s -> %s" % (after.name, before.region, after.region))

            await self.reconnect_voice_client(after)


    async def on_server_join(self, server:discord.Server):
        log.info("Bot has been joined server: {}".format(server.name))
        log.debug("Creating data folder for server %s", server.id)
        pathlib.Path('data/%s/' % server.id).mkdir(exist_ok=True)


    async def on_server_remove(self, server: discord.Server):
        log.info("Bot has been removed from server: {}".format(server.name))
        log.debug('Updated server list:')
        [log.debug(' - ' + s.name) for s in self.servers]

        if server.id in self.players:
            self.players.pop(server.id).kill()


    async def on_server_available(self, server: discord.Server):
        if not self.init_ok:
            return # Ignore pre-ready events

        log.debug("Server \"{}\" has become available.".format(server.name))

        player = self.get_player_in(server)

        if player and player.is_paused:
            av_paused = self.server_specific_data[server]['availability_paused']

            if av_paused:
                log.debug("Resuming player in \"{}\" due to availability.".format(server.name))
                self.server_specific_data[server]['availability_paused'] = False
                player.resume()


    async def on_server_unavailable(self, server: discord.Server):
        log.debug("Server \"{}\" has become unavailable.".format(server.name))

        player = self.get_player_in(server)

        if player and player.is_playing:
            log.debug("Pausing player in \"{}\" due to unavailability.".format(server.name))
            self.server_specific_data[server]['availability_paused'] = True
            player.pause()
