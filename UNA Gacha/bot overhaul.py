import discord
import random
import json
from discord.ext import commands, menus
import os
import csv

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

# Rarity configurations
rarity_weights = {'common': 50, 'uncommon': 30, 'rare': 15, 'epic': 4, 'legendary': 1}
rarity_colors = {'common': 0xCCCCCC, 'uncommon': 0x66CCFF, 'rare': 0x9966FF, 'epic': 0xFF66FF, 'legendary': 0xFFCC33}
rarity_emojis = {'common': '⭐', 'uncommon': '⭐⭐', 'rare': '⭐⭐⭐', 'epic': '⭐⭐⭐⭐', 'legendary': '⭐⭐⭐⭐⭐'}

# Helper functions
def read_cards():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cards.csv'), newline='', encoding='utf-8') as csvfile:
        return {row['name']: row for row in csv.DictReader(csvfile)}

def load_user_data():
    try:
        with open('user_data.json', 'r') as file:
            return json.load(file) if (contents := file.read()) else {}
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
    # Select a card based on rarity weights
    card_names, weights = zip(*[(name, rarity_weights[card['rarity'].lower()]) for name, card in cards.items()])
    card_name = random.choices(card_names, weights=weights, k=1)[0]
    card = cards[card_name]

    embed = discord.Embed(
        title=card['name'],
        description=f"*{card['type']}*\n{rarity_emojis[card['rarity'].lower()]}\n{card['ability1']}\n{card['ability2']}",
        color=rarity_colors[card['rarity'].lower()]
    )
    embed.set_image(url=card['artwork'])
    embed.set_footer(text="Pulled on {}".format(datetime.now().strftime('%d/%m/%Y')))
    message = await ctx.send(embed=embed)
    
    # React to the message with an emoji
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


# Import datetime module
from datetime import datetime

# CardMenu class for browsing user inventory
class CardMenu(menus.Menu):
    def __init__(self, card_names, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_names = card_names
        self.current_page = 0

    async def send_initial_message(self, ctx, channel):
        card = cards[self.card_names[self.current_page]]
        return await ctx.send(embed=self.create_card_embed(card))

    def create_card_embed(self, card):
        embed = discord.Embed(
            title=card['name'],
            description=f"*{card['type']}*\n{rarity_emojis[card['rarity'].lower()]}\n{card['ability1']}\n{card['ability2']}",
            color=rarity_colors[card['rarity'].lower()]
        )
        embed.set_image(url=card['artwork'])
        return embed

    @menus.button('⬅️')
    async def on_left_arrow(self, payload):
        if self.current_page > 0:
            self.current_page -= 1
            card = cards[self.card_names[self.current_page]]
            embed = self.create_card_embed(card)
            await self.message.edit(embed=embed)

    @menus.button('➡️')
    async def on_right_arrow(self, payload):
        if self.current_page < len(self.card_names) - 1:
            self.current_page += 1
            card = cards[self.card_names[self.current_page]]
            embed = self.create_card_embed(card)
            await self.message.edit(embed=embed)

    @menus.button('🔄')
    async def on_refresh_button(self, payload):
        # Refresh card data from CSV
        global cards
        cards = read_cards()
        card = cards[self.card_names[self.current_page]]
        embed = self.create_card_embed(card)
        await self.message.edit(embed=embed)

# Inventory command
@bot.command()
async def inventory(ctx):
    user_id = str(ctx.author.id)
    if user_id in user_data and 'inventory' in user_data[user_id]:
        if user_data[user_id]['inventory']:
            menu = CardMenu(user_data[user_id]['inventory'])
            await menu.start(ctx)
        else:
            await ctx.send("You don't have any cards in your inventory.")
    else:
        await ctx.send("You don't have an inventory yet. Use the gacha command to get cards!")


bot.run('MTE4Mjk5NjE5MDIyMTA2MjE4NQ.Gdu_ku.xb8Gelx2l428UQiIeiUKhlX0_6C5UdfTnrSt-w')
