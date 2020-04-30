# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from platform import python_version, uname
from shutil import which
from os import remove
from telethon import version

from userbot import CMD_HELP, ALIVE_NAME
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
# ============================================


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    #Prevent Channel Bug to run sysd commad
    if sysd.is_channel and not sysd.is_group:
        await sysd.edit("`sysd Commad isn't permitted on channels`")
        return
    """ For .sysd command, get system info using neofetch. """
    try:
        neo = "neofetch --stdout"
        fetch = await asyncrunapp(
            neo,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await fetch.communicate()
        result = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await sysd.edit("`" + result + "`")
    except FileNotFoundError:
        await sysd.edit("`Install neofetch first !!`")


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
     #Prevent Channel Bug to run botver commad
    if event.is_channel and not event.is_group:
        await event.edit("`botver Commad isn't permitted on channels`")
        return
    """ For .botver command, get the bot version. """
    if which("git") is not None:
        invokever = "git describe --all --long"
        ver = await asyncrunapp(
            invokever,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        invokerev = "git rev-list --all --count"
        rev = await asyncrunapp(
            invokerev,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        await event.edit("`Userbot Version: "
                         f"{verout}"
                         "` \n"
                         "`Revision: "
                         f"{revout}"
                         "`")
    else:
        await event.edit(
            "Shame that you don't have git, You're running 9.0 - 'Extended' anyway"
        )


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
      #Prevent Channel Bug to run pip commad
    if pip.is_channel and not pip.is_group:
        await pip.edit("`pip Commad isn't permitted on channels`")
        return
    """ For .pip command, do a pip search. """
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("`Searching . . .`")
        invokepip = f"pip3 search {pipmodule}"
        pipc = await asyncrunapp(
            invokepip,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) \
            + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("`Output too large, sending as file`")
                file = open("output.txt", "w+")
                file.write(pipout)
                file.close()
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit("**Query: **\n`"
                           f"{invokepip}"
                           "`\n**Result: **\n`"
                           f"{pipout}"
                           "`")
        else:
            await pip.edit("**Query: **\n`"
                           f"{invokepip}"
                           "`\n**Result: **\n`No Result Returned/False`")
    else:
        await pip.edit("`Use .help pip to see an example`")


@register(outgoing=True, pattern=r"^\.(?:alive|on)\s?(.)?")
async def amireallyalive(alive):
    #Prevent Channel Bug to run alive commad
    if alive.is_channel and not alive.is_group:
        await alive.edit("`alive Commad isn't permitted on channels`")
        return
    """ For .alive command, check if the bot is running.  """
    await alive.edit("`"
                     f"••••••••••••••••••••••••••••••• \n"
                     "Aone-Kangbot is running, Enjoy! \n\n"
                     f"=============================== \n"
                     f"Telethon version: {version.__version__} \n"
                     f"Python: {python_version()} \n"
                     f"=============================== \n\n"
                     f"User: {DEFAULTUSER} \n"
                     f"••••••••••••••••••••••••••••••• \n"
                     " \n\n"
                     "`")    



@register(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(username):
    #Prevent Channel Bug to run aliveu commad
    if username.is_channel and not username.is_group:
        await username.edit("`aliveu Commad isn't permitted on channels`")
        return
    """ For .aliveu command, change the username in the .alive command. """
    message = username.text
    output = '.aliveu [new user without brackets] nor can it be empty'
    if not (message == '.aliveu' or message[7:8] != ' '):
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
        output = 'Successfully changed user to ' + newuser + '!'
    await username.edit("`" f"{output}" "`")


@register(outgoing=True, pattern="^.resetalive$")
async def amireallyalivereset(ureset):
    #Prevent Channel Bug to run resetalive commad
    if ureset.is_channel and not ureset.is_group:
        await ureset.edit("`resetalive Commad isn't permitted on channels`")
        return
    """ For .resetalive command, reset the username in the .alive command. """
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update(
    {"sysd": ".sysd\
    \nUsage: Shows system information using neofetch."})
CMD_HELP.update({"botver": ".botver\
    \nUsage: Shows the userbot version."})
CMD_HELP.update(
    {"pip": ".pip <module(s)>\
    \nUsage: Does a search of pip modules(s)."})
CMD_HELP.update({
    "alive":
    ".alive | .on\
    \nUsage: Type .alive to see wether your bot is working or not.\
    \n\n.aliveu <text>\
    \nUsage: Changes the 'user' in alive to the text you want.\
    \n\n.resetalive\
    \nUsage: Resets the user to default."
})
