import discord
import time
import subprocess
from win32gui import GetWindowText, GetForegroundWindow
from discord.ext import commands
import pymem
import pymem.process
import re
from datetime import datetime

client = commands.Bot(command_prefix = '+') #Bot Prefix

version = "1.0"

def get_sig(modname, pattern, extra = 0, offset = 0, relative = True): #Get_Sig Function that will let us pattern scan for offsets
    pm = pymem.Pymem("csgo.exe")
    if offset == 0:
        module = pymem.process.module_from_name( pm.process_handle, modulename )
        bytes = pm.read_bytes( module.lpBaseOfDll, module.SizeOfImage )
        match = re.search( pattern, bytes ).start()
        res = match + extra
        return res
    module = pymem.process.module_from_name(pm.process_handle, modname)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)

@client.event
async def on_ready():
    print(f'DiscordDumperBot is ready. Version:', version) #When discord bot is ready, it will print Dumperbot is ready.
    await client.change_presence(status=discord.Status.online, activity=discord.Game('+helplist'))

@client.command()
async def helplist(ctx):
    embedVar = discord.Embed(title="Help", description="Command List", color=0x00ECFF)
    embedVar.add_field(name="+dumpoffsets", value="Dumps all major offsets from bot host PC", inline=False)
    embedVar.add_field(name="+dwLocalPlayer", value="Retrieves dwLocalPlayer Offset from bot host PC", inline=False)
    await ctx.channel.send(embed=embedVar)

@client.command()
async def dumpoffsets(ctx): #Command that will dump most major offsets
    if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive": #Check to see if csgo is not open
        await ctx.send("Opening Process: csgo.exe")
        subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 730") #If csgo is not open we will launch it with steam's appID system
        time.sleep(12) #Wait for csgo to get into main menu to dump offset

    await ctx.send("Scanning for Offsets...")

    dwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3) #Dumping offsets
    dwLocalPlayerInt = int(dwLocalPlayer, 0) #Converting our offsets to an integer

    dwEntityList = get_sig('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1)
    dwEntityListInt = int(dwEntityList, 0)

    dwViewMatrix = get_sig('client.dll', rb'\x0F\x10\x05....\x8D\x85....\xB9', 176, 3)
    dwViewMatrixInt = int(dwViewMatrix, 0)

    dwClientState = get_sig('engine.dll', rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0', 0, 1)
    dwClientStateInt = int(dwClientState, 0)

    dwClientState_ViewAngles = get_sig('engine.dll', rb'\xF3\x0F\x11\x80....\xD9\x46\x04\xD9\x05', 0, 4, False)
    dwClientState_ViewAnglesInt = int(dwClientState_ViewAngles, 0)

    m_bDormant = get_sig('client.dll', rb'\x8A\x81....\xC3\x32\xC0', 8, 2, False)
    m_bDormantInt = int(m_bDormant, 0)

    dwForceJump = get_sig('client.dll', rb'\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02', 0, 2)
    dwForceJumpInt = int(dwForceJump, 0)

    model_ambient_min = get_sig('engine.dll', rb'\xF3\x0F\x10\x0D....\xF3\x0F\x11\x4C\x24.\x8B\x44\x24\x20\x35....\x89\x44\x24\x0C', 0, 4)
    model_ambient_minInt = int(model_ambient_min, 0)

    dwGlowObjectManager = get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1)
    dwGlowObjectManagerInt = int(dwGlowObjectManager, 0)

    now = datetime.now() #Using the datetime module we are setting the time to when the embed was created
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S %p") #Formatting the time to be month,day,year, hour,minute,second, AM/PM
    embedVar = discord.Embed(title=f"Offset Dump", description=f"{date_time}", color=0x58D68D) #Titling and coloring the embed
    embedVar.add_field(name="dwLocalPlayer", value=f"{dwLocalPlayer} | Integer Value: {dwLocalPlayerInt}", inline=False) #Adding fields that show the name of the offset, the value and also the integer value

    embedVar.add_field(name="dwEntityList", value=f"{dwEntityList} | Integer Value: {dwEntityListInt}", inline=False)

    embedVar.add_field(name="dwViewMatrix", value=f"{dwViewMatrix} | Integer Value: {dwViewMatrixInt}", inline=False)

    embedVar.add_field(name="dwClientState", value=f"{dwClientState} | Integer Value: {dwClientStateInt}", inline=False)

    embedVar.add_field(name="dwClientState_ViewAngles", value=f"{dwClientState_ViewAngles} | Integer Value: {dwClientState_ViewAnglesInt}", inline=False)

    embedVar.add_field(name="m_bDormant", value=f"{m_bDormant} | Integer Value: {m_bDormantInt}", inline=False)

    embedVar.add_field(name="dwForceJump", value=f"{dwForceJump} | Integer Value: {dwForceJumpInt}", inline=False)

    embedVar.add_field(name="model_ambient_min", value=f"{model_ambient_min} | Integer Value: {model_ambient_minInt}", inline=False)

    embedVar.add_field(name="dwGlowObjectManager", value=f"{dwGlowObjectManager} | Integer Value: {dwGlowObjectManagerInt}", inline=False)

    await ctx.channel.send(embed=embedVar) #Sending the embed to the channel where the command was typed

    time.sleep(2)
    await ctx.send("Closing Process: csgo.exe")
    subprocess.call(["taskkill","/F","/IM","csgo.exe"]) #Closing the process

@client.command()
async def dwLocalPlayer(ctx): #Command that will dump just dwLocalPlayer
    if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive": #Check to see if csgo is not open
        await ctx.send("Opening Process: csgo.exe")
        subprocess.call(r"C:\Program Files (x86)\Steam\Steam.exe -applaunch 730") #If csgo is not open we will launch it with steam's appID system
        time.sleep(12) #Wait for csgo to get into main menu to dump offset

    await ctx.send("Scanning for dwLocalPlayer Offset...")
    dwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3) #Dumping Offset with out get_sig pattern scan function
    dwLocalPlayerInt = int(dwLocalPlayer, 0) #Converting our dwLocalPlayer string to an Integer

    embedVar = discord.Embed(title=f"dwLocalPlayer", description=f"{dwLocalPlayer}", color=0xFF2D00) #Creating an embed and displaying offset data
    embedVar.add_field(name="Integer Value", value=f"{dwLocalPlayerInt}", inline=True)

    now = datetime.now() #Using the datetime module, we are setting our time to now, so that the time recorded wil be when the embed is created
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S%p") #Setting our time to be displayed as month, day,year then hour,minute,seconds, then AM/PM
    embedVar.add_field(name="Time Dumped", value=f"{date_time}", inline=False)
    await ctx.channel.send(embed=embedVar) #Sending the embed

    time.sleep(2) #Waits for the pattern scanner
    await ctx.send("Closing Process: csgo.exe")
    subprocess.call(["taskkill","/F","/IM","csgo.exe"]) #Closes csgo to ensure when command is typed again, the offsets do not go out of date in case of an update.

client.run(' ') #Put in your own discord token here
