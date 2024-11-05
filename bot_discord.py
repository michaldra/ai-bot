import discord
import bot_logic
import random
import requests
import os
import ai_thing
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Zalogowaliśmy się jako {bot.user}')

@bot.command()
async def all(ctx):
    await ctx.send('Wszystkie komendy:\n')
    await ctx.send('**$hello** - Wita się\n')
    await ctx.send('**$bye** - Żegna się\n')
    await ctx.send('**$hehe #** - Pisze "he" # razy\n')
    await ctx.send('**$password #** - Generuje hasło o długości #\n')
    await ctx.send('**$h #** - Pisze "h " # razy\n')
    await ctx.send('**$coin** - Rzuca monetą\n')
    await ctx.send('**$emoji** - Generuje losową emotkę\n')
    await ctx.send('**$dice #** - Rzuca kostką o # ścianach\n')
    await ctx.send('**$guess #** - Zaczyna grę w zgadywanie od 1 do #\n')
    await ctx.send('**$joined** - Pisze kiedy użytkownik dołączył do serwera')
    await ctx.send('**$meme** - Wysyła losowy mem o programowaniu\n')
    await ctx.send('**$dog** - Wysyła losowy obrazek z pieskami\n')
    await ctx.send('**$eko** - Pisze losowy pomysł na zrobienie czegoś ze śmieci\n')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Cześć, jestem {bot.user}!')

@bot.command()
async def bye(ctx):
    await ctx.send(f'👋')

@bot.command()
async def hehe(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def password(ctx, pass_chars = 12):
    await ctx.send(bot_logic.gen_pass(pass_chars))

@bot.command()
async def h(ctx, count_h = random.randint(3,13)):
    await ctx.send("h " * count_h)

@bot.command()
async def coin(ctx):
    await ctx.send(bot_logic.coin())

@bot.command()
async def emoji(ctx):
    await ctx.send(bot_logic.gen_emoji())

@bot.command()
async def dice(ctx, dice_sides = 6):
    await ctx.send(bot_logic.kostka(dice_sides))

@bot.command()
async def guess(ctx, max_guess = 10):
    await ctx.send(f'Myślę o liczbie od 1 do {max_guess}')

@bot.command()
async def joined(ctx, member = discord.Member):
    await ctx.send(f'{(member.name)} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def meme(ctx):
    rng = random.randint(0,999)
    if rng < 500:
        img_name = random.choice(os.listdir('images/common'))
        with open(f'images/common/{img_name}', 'rb') as f:
                picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('Popularny (50%)')
    elif rng < 750:
        img_name = random.choice(os.listdir('images/uncommon'))
        with open(f'images/uncommon/{img_name}', 'rb') as f:
                picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('Niepopularny (25%)')
    elif rng < 900:
        img_name = random.choice(os.listdir('images/rare'))
        with open(f'images/rare/{img_name}', 'rb') as f:
                picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('Rzadki (15%)')
    elif rng < 980:
        img_name = random.choice(os.listdir('images/epic'))
        with open(f'images/epic/{img_name}', 'rb') as f:
                picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('Epicki (8%)')
    elif rng < 999:
        img_name = random.choice(os.listdir('images/legendary'))
        with open(f'images/legendary/{img_name}', 'rb') as f:
                picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('Legendarny (1.9%)')
    else:
        with open(f'images/mine/meme31', 'rb') as f:
                picture = discord.File(f)
        await ctx.send(file=picture)
        await ctx.send('Mój mem! (0.1%)')

def get_dog_image_url():    
    url = 'https://random.dog/woof.json'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command()
async def dog(ctx):
    image_url = get_dog_image_url()
    await ctx.send(image_url)

@bot.command()
async def eko(ctx):
    await ctx.send(bot_logic.ekologia())

@bot.command()
async def ai(ctx):
    if len(ctx.message.attachments) == 0:
        await ctx.send("Nie wykryto załączonego obrazka")
    else:
        for attachment in ctx.message.attachments:
            await(attachment.save(f"ai_imgs/{attachment.filename}"))
            await ctx.send(ai_thing.detect_bird(f"ai_imgs/{attachment.filename}", "keras_model.h5", "labels.txt"))
         

bot.run("amogus")