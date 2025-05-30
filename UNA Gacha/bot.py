import discord
import random
import json
import os
import csv
import datetime
import asyncio
from discord.ext import commands, menus

# Set up intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

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
            return json.load(file)
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
    weights = [rarity_weights.get(card['rarity'].lower(), 0) for card in cards]
    card = random.choices(cards, weights=weights, k=1)[0]
    
    # Ensure card attributes exist
    embed = discord.Embed(
        title=card['name'],
        description=f"*{card['type']}*\n{rarity_emojis.get(card['rarity'].lower(), '')}\n1. {card.get('ability1', 'N/A')}\n2. {card.get('ability2', 'N/A')}",
        color=rarity_colors.get(card['rarity'].lower(), 0xCCCCCC)
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
        user_data.setdefault(user_id, {'inventory': []})['inventory'].append(card)
        save_user_data(user_data)
        embed = discord.Embed(
            title="Card Added!",
            description=f"✅ Card added to your inventory: **{card['name']}**",
            color=rarity_colors.get(card['rarity'].lower(), 0xCCCCCC)
        )
        await ctx.send(embed=embed)

class CardMenu(menus.Menu):
    def __init__(self, cards, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cards = cards
        self.current_page = 0

    async def send_initial_message(self, ctx, channel):
        return await ctx.send(embed=self.create_card_embed(self.cards[self.current_page]))

    def create_card_embed(self, card):
        ability1 = card.get('ability1', 'N/A')
        ability2 = card.get('ability2', 'N/A')
        color = rarity_colors.get(card['rarity'].lower(), 0xCCCCCC)
        embed = discord.Embed(
            title=card['name'],
            description=f"*{card['type']}*\n{rarity_emojis.get(card['rarity'].lower(), '')}\n1. {ability1}\n2. {ability2}",
            color=color
        )
        embed.set_image(url=card['artwork'])
        embed.set_footer(text=f"Page {self.current_page + 1} of {len(self.cards)}")  # {{ edit_1 }}
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
        self.cards.sort(key=lambda card: card['rarity'])
        self.current_page = 0
        embed = self.create_card_embed(self.cards[self.current_page])
        await self.message.edit(embed=embed)

@bot.command()
async def inventory(ctx):
    user_id = str(ctx.author.id)
    user_inventory = user_data.get(user_id, {}).get('inventory', [])
    if user_inventory:
        menu = CardMenu(user_inventory)
        await menu.start(ctx)
    else:
        await ctx.send("You don't have any cards in your inventory. Use the gacha command to get cards!")

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

# New reset command
@bot.command()
async def reset(ctx):
    user_id = str(ctx.author.id)
    user_inventory = user_data.get(user_id, {}).get('inventory', [])
    
    if not user_inventory:
        await ctx.send("Your inventory is already empty.")
        return

    embed = discord.Embed(
        title="Confirm Reset",
        description="Are you sure you want to clear your inventory?",
        color=0xFFCC33
    )
    message = await ctx.send(embed=embed)

    await message.add_reaction('✅')
    await message.add_reaction('❌')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Time out. Reset cancelled.')
    else:
        if str(reaction.emoji) == '✅':
            user_data[user_id]['inventory'] = []
            save_user_data(user_data)
            await ctx.send(embed=discord.Embed(
                title="Inventory Cleared!",
                description="Your inventory has been successfully cleared.",
                color=0xFF0000
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Reset Cancelled",
                description="Your inventory remains unchanged.",
                color=0xFFCC33
            ))

# Custom help command
@bot.command(name='help', aliases=['commands'])
async def help_command(ctx):
    embed = discord.Embed(
        title="Available Commands",
        description="Here are the commands you can use:",
        color=0x66CCFF
    )
    embed.add_field(name=".gacha", value="Pull a card from the gacha.", inline=False)
    embed.add_field(name=".inventory", value="View your card inventory.", inline=False)
    embed.add_field(name=".reset", value="Clear your inventory after confirmation.", inline=False)
    embed.set_footer(text="Use the commands wisely!")
    
    await ctx.send(embed=embed)

# MTE4Mjk5NjE5MDIyMTA2MjE4NQ.GYNBFs.UbPEh3zECZ1RK7EXSdm2FMAi_Ee-dm3PrxPvWg
bot.run('MTE4Mjk5NjE5MDIyMTA2MjE4NQ.GYNBFs.UbPEh3zECZ1RK7EXSdm2FMAi_Ee-dm3PrxPvWg')
