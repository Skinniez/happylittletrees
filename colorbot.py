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
    rgb_values = []

    h = random.random()  
    s = random.uniform(0.4, 0.6)  
    l = random.uniform(0.4, 0.6)  

    for i in range(color_count):
        if palette_type == "random":
            h = random.random()  
            s = random.uniform(0.3, 0.7)  
            l = random.uniform(0.3, 0.7)  
        elif palette_type == "complementary":
            if i == color_count // 2:  
                h = (h + 0.5) % 1
            s = random.uniform(0.4, 0.6)  
            l = random.uniform(0.4, 0.6)  
        elif palette_type == "monochromatic":
            l = random.uniform(0.3, 0.7)  
            s = random.uniform(0.3, 0.7)  
        elif palette_type == "neon":
            h = random.random()
            s = random.uniform(0.8, 1.0)  
            l = random.uniform(0.5, 0.7)  
        elif palette_type == "pastel":
            h = random.random()
            s = random.uniform(0.2, 0.4)  
            l = random.uniform(0.7, 0.9)  
        elif palette_type == "analogous":
            h = (h + 1 / max(1, color_count - 1)) % 1  
            s = random.uniform(0.4, 0.6)
            l = random.uniform(0.4, 0.6)
        elif palette_type == "split_complementary":
            if i == 0:
                h = random.random()
            else:
                h = (h + 0.5 + (-1) ** i * 1 / 12) % 1  
        elif palette_type == "square":
            h = (h + 0.25) % 1   
        elif palette_type == "rectangle":
            h = (h + 0.25 + i % 2 * 0.25) % 1  
        elif palette_type == "triadic":
            h = (h + 1 / 3) % 1  



        color = hsl_to_rgb(h, s, l)
        draw.rectangle([i * 50, 0, (i + 1) * 50, 150], fill=tuple(color))
        rgb_values.append(color)

    return img, rgb_values




@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@slash.slash(name="colors", 
             description="Generate a color palette", 
             options=[
                 {
                     "name": "quantity",
                     "description": "Number of colors in the palette",
                     "type": 4,  # 4 is TYPE_INTEGER
                     "required": False,
                     "choices": [{"name": str(i), "value": i} for i in range(1, 11)]
                 },
                 {
                     "name": "type",
                     "description": "Type of color palette",
                     "type": 3,  # 3 is TYPE_STRING
                     "required": False,
                     "choices": [{"name": "random", "value": "random"}, 
                                 {"name": "complementary", "value": "complementary"}, 
                                 {"name": "monochromatic", "value": "monochromatic"},
                                 {"name": "neon", "value": "neon"},
                                 {"name": "pastel", "value": "pastel"},
                                 {"name": "analogous", "value": "analogous"},
                                 {"name": "split_complementary", "value": "split_complementary"},
                                 {"name": "square", "value": "square"},
                                 {"name": "rectangle", "value": "rectangle"},
                                 {"name": "triadic", "value": "triadic"}
                                ]
                 }
             ])
async def _generate_palette(ctx: SlashContext, quantity: int = 5, type: str = "random"):
    img, rgb_values = generate_palette(quantity, type)
    img.save("palette.png")
    rgb_string = "\n".join([f"Color {i+1}: RGB({r}, {g}, {b})" for i, (r, g, b) in enumerate(rgb_values)])
    
    # Send the image and the RGB values
    await ctx.send(file=discord.File("palette.png"), content=f"Generated a {type} palette with {quantity} colors!\n{rgb_string}")



print("Running bot...")
bot.run(token)
