import os
from dotenv import load_dotenv
import math
import random
from PIL import Image, ImageDraw
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext

load_dotenv()

token = os.getenv('EPIC_BOT_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True


bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
print("Bot object created...")
slash = SlashCommand(bot, sync_commands=True)
print("SlashCommand object created...")


# Conversion Functions
def hsl_to_rgb(h, s, l):
    h = h % 1
    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue2rgb(p, q, h + 1 / 3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1 / 3)
    return [round(r * 255), round(g * 255), round(b * 255)]


def hue2rgb(p, q, t):
    if t < 0: t += 1
    if t > 1: t -= 1
    if t < 1 / 6: return p + (q - p) * 6 * t
    if t < 1 / 2: return q
    if t < 2 / 3: return p + (q - p) * (2 / 3 - t) * 6
    return p


# Drawing and Palette Generation Function
def generate_palette(color_count, palette_type="random"):
    img = Image.new('RGB', (color_count * 50, 150), color='white')
    draw = ImageDraw.Draw(img)

    h = random.random()  # Random value between 0 and 1 for hue
    s = random.uniform(0.4, 0.6)  # Random saturation between 0.4 and 0.6
    l = random.uniform(0.4, 0.6)  # Random lightness between 0.4 and 0.6
    
    for i in range(color_count):
        if palette_type == "complementary":
            if i == color_count // 2:  # Change to complementary hue at halfway point
                h = (h + 0.5) % 1
            s = random.uniform(0.4, 0.6)  # Vary saturation
            l = random.uniform(0.4, 0.6)  # Vary lightness
        elif palette_type == "monochromatic":
            l = random.uniform(0.3, 0.7)  # Vary lightness
            s = random.uniform(0.3, 0.7)  # Vary saturation

        color = hsl_to_rgb(h, s, l)
        draw.rectangle([i * 50, 0, (i + 1) * 50, 150], fill=tuple(color))

    return img




@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@slash.slash(name="generate_palette", 
             description="Generate a color palette", 
             options=[
                 {
                     "name": "color_count",
                     "description": "Number of colors in the palette",
                     "type": 4,  # 4 is TYPE_INTEGER
                     "required": False,
                     "choices": [{"name": str(i), "value": i} for i in range(1, 11)]
                 },
                 {
                     "name": "palette_type",
                     "description": "Type of color palette",
                     "type": 3,  # 3 is TYPE_STRING
                     "required": False,
                     "choices": [{"name": "random", "value": "random"}, 
                                 {"name": "complementary", "value": "complementary"}, 
                                 {"name": "monochromatic", "value": "monochromatic"}]
                 }
             ])
async def _generate_palette(ctx: SlashContext, color_count: int = 5, palette_type: str = "random"):
    img = generate_palette(color_count, palette_type)
    img.save("palette.png")
    await ctx.send(file=discord.File("palette.png"), content=f"Generated a {palette_type} palette with {color_count} colors!")


print("Running bot...")
bot.run(token)
