import discord
import random
import json
from discord.ext import commands, menus
import asyncio
import os
import csv
import datetime

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# Rarity configurations
rarity_weights = {'common': 50, 'uncommon': 30, 'rare': 15, 'epic': 4, 'legendary': 1}
rarity_emojis = {'common': '⭐', 'uncommon': '⭐⭐', 'rare': '⭐⭐⭐', 'epic': '⭐⭐⭐⭐', 'legendary': '⭐⭐⭐⭐⭐'}
rarity_colors = {'common': 0xCCCCCC, 'uncommon': 0x66CCFF, 'rare': 0x9966FF, 'epic': 0xFF66FF, 'legendary': 0xFFCC33}

# Helper functions
def read_cards():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cards.csv'), newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            file_contents = file.read()
            return json.loads(file_contents) if file_contents else {}
    except FileNotFoundError:
        return {}


def save_user_data(data):
    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)

cards = read_cards()
user_data = load_user_data()

# Gacha command
@bot.command()
async def gacha(ctx):
    weights = [rarity_weights[card['rarity'].lower()] for card in cards]
    card = random.choices(cards, weights=weights, k=1)[0]
    embed = discord.Embed(
        title=card['name'],
        description=f"*{card['type']}*\n{rarity_emojis[card['rarity'].lower()]}\n1. {card['ability1']}\n2. {card['ability2']}",
        color=rarity_colors[card['rarity'].lower()]
    )
    embed.set_image(url=card['artwork'])
    embed.set_footer(text=f"Pulled on {datetime.datetime.utcnow().strftime('%d/%m/%Y')}")
    message = await ctx.send(embed=embed)

    await message.add_reaction('🎴')
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '🎴' and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Time out. Try again.')
    else:
        user_id = str(ctx.author.id)
        if user_id not in user_data:
            user_data[user_id] = {'inventory': []}
        user_data[user_id]['inventory'].append(card)
        save_user_data(user_data)
        await ctx.send(f'Card added to your inventory: {card["name"]}')

class CardMenu(menus.Menu):
    def __init__(self, cards, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards = cards
        self.current_page = 0

    async def send_initial_message(self, ctx, channel):
        return await ctx.send(embed=self.create_card_embed(self.cards[self.current_page]))

    def create_card_embed(self, card):
        # Handling missing ability keys
        ability1 = card.get('ability1', 'N/A')
        ability2 = card.get('ability2', 'N/A')

        color = rarity_colors.get(card['rarity'].lower(), 0xCCCCCC)
        embed = discord.Embed(
            title=card['name'],
            description=f"*{card['type']}*\n{rarity_emojis[card['rarity'].lower()]}\n1. {ability1}\n2. {ability2}",
            color=color
        )
        embed.set_image(url=card['artwork'])
        return embed

    @menus.button('⬅️')
    async def on_left_arrow(self, payload):
        if self.current_page > 0:
            self.current_page -= 1
            embed = self.create_card_embed(self.cards[self.current_page])
            await self.message.edit(embed=embed)

    @menus.button('➡️')
    async def on_right_arrow(self, payload):
        if self.current_page < len(self.cards) - 1:
            self.current_page += 1
            embed = self.create_card_embed(self.cards[self.current_page])
            await self.message.edit(embed=embed)

    @menus.button('🔢')
    async def on_number_button(self, payload):
        # Sort by name, you can implement sorting by type or abilities as needed
        self.cards.sort(key=lambda card: card['rarity'])
        self.current_page = 0
        embed = self.create_card_embed(self.cards[self.current_page])
        await self.message.edit(embed=embed)

@bot.command()
async def inventory(ctx):
    user_id = str(ctx.author.id)
    if user_id in user_data:
        user_inventory = user_data[user_id].get('inventory', [])
        if user_inventory:
            menu = CardMenu(user_inventory)
            await menu.start(ctx)
        else:
            await ctx.send("You don't have any cards in your inventory.")
    else:
        await ctx.send("You don't have an inventory yet. Use the gacha command to get cards!")

# Bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="Type .gacha to play!"))

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        raise error

bot.run('MTE4Mjk5NjE5MDIyMTA2MjE4NQ.G4vqD3.HLrYlvoQna9i_3Zfw0gYdGOatJkEKpXhnYCbxI')
