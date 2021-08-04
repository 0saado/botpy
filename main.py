import discord
from discord.ext import commands, tasks
from discord.utils import async_all
import youtube_dl
import asyncio
import os
import colorama
from colorama import Fore

bot = commands.Bot(command_prefix="sudu ", description="Coded by Saado")
musics = {}
ytdl = youtube_dl.YoutubeDL()


@bot.event
async def on_ready():
    print(f"{Fore.LIGHTYELLOW_EX}Status: {Fore.MAGENTA}On!")
    print(f"{Fore.LIGHTYELLOW_EX}User: {Fore.MAGENTA}{bot.user} \n")
    status.start()


@bot.command()
async def ping(ctx):
    await ctx.send(f":ping_pong:  `{round(bot.latency*1000)}ms`")

@bot.command()
async def hi(ctx):
    await ctx.send("Hi!")

@bot.command()
async def saado(ctx):
    mesaado = "Saado is the owner of this server and the creator of the Soodo team."
    await ctx.send(mesaado)

@bot.command()
async def servinfo(ctx):
    server = ctx.guild
    notc = len(server.text_channels)
    novc = len(server.voice_channels)
    sd = server.description
    mn = server.member_count
    sn = server.name
    message = f"Server name: **{sn}**. \nMember count **{mn}**. \nText Channels count: **{notc}**. \nVoice Channels count: **{novc}**."
    await ctx.send(message)

@bot.command()
async def say(ctx, *text):
    print(text)
    await ctx.send(" ".join(text))

@bot.command()
async def cook(ctx, *text):
    
    text = " ".join(text)
    message = await ctx.send(f"Wtf? I'm not gonna cook a '{text}' for you, I'M A BOT!! ")

@bot.command()
async def command(ctx):
    embed = discord.Embed(title = "**Commands**", color = 0xffdb00)
    embed.add_field(name = "**Useless commands**",value = "/hi \n/say *+ something to say* \n/cook *+ something to cook*")
    embed.add_field(name = "**Useful commands**", value = "/servinfo")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members = True)
async def adcommand(ctx):
    embed = discord.Embed(Title = "**Admin Commands**", color = 0xffdb00)
    embed.add_field(name = "**Admin Commands**", value = "/clear *+ number of messages to delete* \n/mute *+ mention someone* \n/unmute *+ mention muted person*\n/kick *+ mention someone* \n /ban *+ mention someone*\n /unban *+ full username and tag of the banned person*")
    await ctx.send(embed = embed)

#---------------------------------------------------------------------------------------------------------------------------------------------------------

@bot.command()
@commands.has_permissions(ban_members = True)
async def clear(ctx, n : int):
    msgs = await ctx.channel.history(limit= n + 1).flatten()
    for msg in msgs:
        await msg.delete()

@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason = reason)
    embed = discord.Embed(title = "**Kick**", description = f"{user} has been kicked!", color = 0xffdb00)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://instagram.com/0saado")
    embed.set_thumbnail(url = "https://cdn0.iconfinder.com/data/icons/everyday-objects-2/128/ban-hammer-512.png")
    embed.add_field(name = "Kicked Member", value = user.name, inline = True)
    embed.add_field(name = "Reason", value = reason, inline = True)
    embed.add_field(name = "Admin", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Please respect the rules.")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason = reason)
    embed = discord.Embed(title = "**Ban**", description = f"{user} has been banned!", color = 0xffdb00)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://instagram.com/0saado")
    embed.set_thumbnail(url = "https://cdn0.iconfinder.com/data/icons/everyday-objects-2/128/ban-hammer-512.png")
    embed.add_field(name = "Banned Member", value = user.name, inline = True)
    embed.add_field(name = "Reason", value = reason, inline = True)
    embed.add_field(name = "Admin", value = ctx.author.name, inline = True)
    embed.set_footer(text = "Please respect the rules.")
    await ctx.send(embed = embed)

async def createmutedrole(ctx):
    mutedrole = await ctx.guild.create_role(name = "Muted", permissions = discord.Permissions(send_messages = False, speak = False))
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedrole, send_messages = False, speak = False)
        return mutedrole

async def getmutedrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    await createmutedrole(ctx)


@bot.command()
@commands.has_permissions(ban_members = True)
async def mute(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    mutedrole = await getmutedrole(ctx)
    await user.add_roles(mutedrole , reason = reason)
    embed = discord.Embed(title = "**Mute**", description = f"{user} has been muted!", color = 0xffdb00)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://instagram.com/0saado")
    embed.set_thumbnail(url = "https://cdn0.iconfinder.com/data/icons/everyday-objects-2/128/ban-hammer-512.png")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members = True)
async def unmute(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    mutedrole = await getmutedrole(ctx)
    await user.remove_roles(mutedrole, reason = reason)
    embed = discord.Embed(title = "**Unmute**", description = f"{user} has been un  muted!", color = 0xffdb00)
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url, url = "https://instagram.com/0saado")
    embed.set_thumbnail(url = "https://cdn0.iconfinder.com/data/icons/everyday-objects-2/128/ban-hammer-512.png")
    await ctx.send(embed = embed)

@bot.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user, *reason):
    reason = " ".join(reason)
    usern, useri = user.split("#")
    bannedusers = await ctx.guild.bans()
    for i in bannedusers:
        if i.user.name == usern and i.user.discriminator == useri:
            await ctx.guild.unban(i.user, reason = reason)
            await ctx.send(f"{user} has been unbanned.")
            return
        else: 
         await ctx.send(f"{user} is not banned from this server, baka.")

#-----------------------------------------------------------------------------------------------------------------------------------------------

#@bot.event
#async def on_message_delete(message):
#   await message.channel.send(f"{message.author}'s message has been delted. \n **Message: ** *'{message.content}'*")
#   await bot.process_commands(message)

#@bot.event
#async def on_message_edit(before, after):
#    await before.channel.send(f"{before.author} edited his message.\n **Before ->** *'{before.content}'*\n **After ->** *'{after.content}'*")

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(849614923546099723)
    await channel.send(f"Welcome to {member.mention}. ❤")

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(849615010967060490)
    await channel.send(f"{member.mention} left the server. 👋")

#----------------------------------------------------------------------------------------------------------------------------------------------------

@bot.event
async def on_reaction_add(reaction, user):
    await reaction.message.add_reaction(reaction.emoji)
#----------------------------------------------------------------------------------------------------------------------------------------------------

@tasks.loop(seconds = 5)
async def status():
    game = discord.Game("sudu help")
    await bot.change_presence(status = discord.Status.idle, activity = game)



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------


@bot.command()
@commands.has_permissions(ban_members = True)
async def hanae(ctx):
    embed = discord.Embed(title = "Role commands", color = 0xffdb00)
    embed.add_field(name = "**Members**", value = "/mmbr *+mention*", inline = True)
    embed.add_field(name = "**She/Her**", value = "/hershe *+mention*", inline = True)
    embed.add_field(name = "**He/Him**", value = "/heh *+mention*", inline = True)
    embed.add_field(name = "**They/Them**", value = "/theyt *+mention*", inline = True)
    embed.add_field(name = "**She/Them**", value = "/shet *+mention*", inline = True)
    embed.add_field(name = "**He/Them**", value = "/het *+mention*", inline = True)
    await ctx.send(embed = embed)


async def getmembersrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "members":
            return role


@bot.command()
@commands.has_permissions(ban_members = True)
async def mmbr(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    membersrole = await getmembersrole(ctx)
    await user.add_roles(membersrole , reason = reason)
    embed = discord.Embed(title = "**Role**", description = f"{user} got **Members** role", color = 0xffdb00)
    await ctx.send(embed = embed)

async def gethersherole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "she / her":
            return role


@bot.command()
@commands.has_permissions(ban_members = True)
async def hershe(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    hersherole = await gethersherole(ctx)
    await user.add_roles(hersherole , reason = reason)
    embed = discord.Embed(title = "**Role**", description = f"{user} got **She/Her** role", color = 0xffdb00)
    await ctx.send(embed = embed)




async def gethehrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "he /him":
            return role


@bot.command()
@commands.has_permissions(ban_members = True)
async def heh(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    hehrole = await gethehrole(ctx)
    await user.add_roles(hehrole , reason = reason)
    embed = discord.Embed(title = "**Role**", description = f"{user} got **He/Him** role", color = 0xffdb00)
    await ctx.send(embed = embed)




async def gettheytrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "they /them":
            return role


@bot.command()
@commands.has_permissions(ban_members = True)
async def theyt(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    theytrole = await gettheytrole(ctx)
    await user.add_roles(theytrole , reason = reason)
    embed = discord.Embed(title = "**Role**", description = f"{user} got **They/Them** role", color = 0xffdb00)
    await ctx.send(embed = embed)




async def getshetrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "she /them":
            return role


@bot.command()
@commands.has_permissions(ban_members = True)
async def shet(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    shetrole = await getshetrole(ctx)
    await user.add_roles(shetrole , reason = reason)
    embed = discord.Embed(title = "**Role**", description = f"{user} got **She/Them** role", color = 0xffdb00)
    await ctx.send(embed = embed)




async def gethetrole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "he /them":
            return role


@bot.command()
@commands.has_permissions(ban_members = True)
async def het(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    hetrole = await gethetrole(ctx)
    await user.add_roles(hetrole , reason = reason)
    embed = discord.Embed(title = "**Role**", description = f"{user} got **He/Them** role", color = 0xffdb00)
    await ctx.send(embed = embed)


#---------------------------------------------------------------------------------------------------------------------------------------------------------


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download = False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []
    await ctx.send("Disconnected.")


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()
    await ctx.send("Paused.")


@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()
    await ctx.send("Resume.")


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()
    await ctx.send("Skipped.")


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url, before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after =next)


@bot.command()
async def play(ctx, url):
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Play: {video.url}")
        play_song(client, musics[ctx.guild], video)


bot.run(getenv('TOKEN'))
