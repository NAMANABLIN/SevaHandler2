from discord import Message, Intents, RawReactionActionEvent
from discord.ext import commands
from db_func import update_data, get_data, create_data
from asyncio import sleep

from config import *

nums = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

intents = Intents.default()
intents.reactions = True
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='!', intents=intents)

data = dict()


@bot.event
async def on_ready():
    global data
    print('START')
    # create_data()  # if you start first time
    await bot.tree.sync()  # Синхронизация слэш-команд с Discord
    data = get_data()


async def shutdown(msg):
    await msg.channel.send("Shutting down...")
    update_data(data)
    await sleep(5)
    await bot.close()


@bot.event
async def on_message(msg: Message):
    global data
    if msg.author.id == idPasha:
        if msg.content == 'shutdown':
            await shutdown(msg)
    if msg.channel.id in data['stickers'].keys() and not msg.author.bot:
        if len(msg.stickers) != 0 and msg.stickers[0].id == id2Sticker:
            data['stickers'][msg.channel.id] += 1
        else:
            if data['stickers'][msg.channel.id] >= 2:
                channel = bot.get_channel(msg.channel.id)
                stickers = data['stickers'][msg.channel.id]
                word = ''
                if 11 <= stickers <= 14:
                    word = "стикеров"
                elif stickers % 10 == 1:
                    word = "стикер"
                elif stickers % 10 >= 5 or stickers % 10 <= 9 and stickers % 10 == 0:
                    word = "стикеров"
                elif stickers % 10 >= 2 or stickers % 10 <= 4:
                    word = "стикера"
                await (channel.send(
                    f'Последовательность Di dance прекращена, подряд было отправлено {data["stickers"][msg.channel.id]} {word}.'))
                data['stickers'][msg.channel.id] = 0
    else:
        if len(msg.stickers) != 0 and msg.stickers[0].id == id2Sticker:
            data['stickers'][msg.channel.id] = 1


@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    global data
    channelid = payload.channel_id
    messageid = payload.message_id

    channel = bot.get_channel(channelid)
    msg = await channel.fetch_message(messageid)

    if ((msg.channel.id == idAnounsments or msg.channel.id == idObjee)
            and msg.author.id == idPasha and not payload.member.bot):
        if payload.emoji.name in nums:
            user = payload.member
            if channelid == idObjee:
                await msg.remove_reaction(payload.emoji, user)
        else:
            unique_users = set()
            for reaction in msg.reactions:
                async for user in reaction.users():
                    if not user.bot:
                        unique_users.add(user.id)
            a = len(unique_users)
            if msg.id in data['reactions']:
                if a != data['reactions'][msg.id]:
                    data['reactions'][msg.id] = a
            else:
                data['reactions'][msg.id] = a
            await prikol(msg, a)


@bot.event
async def on_raw_reaction_remove(payload: RawReactionActionEvent):
    global data
    channelid = payload.channel_id
    messageid = payload.message_id

    channel = bot.get_channel(channelid)
    msg = await channel.fetch_message(messageid)

    if ((msg.channel.id == idAnounsments or msg.channel.id == idObjee)
            and msg.author.id == idPasha):
        unique_users = set()
        data['reactions'][msg.id] = 1

        for reaction in msg.reactions:
            async for user in reaction.users():
                if not user.bot:
                    unique_users.add(user.id)
        a = len(unique_users)
        if a != data['reactions'][msg.id]:
            data['reactions'][msg.id] = a
            await prikol(msg, a)


async def prikol(msg: Message, count: int) -> None:
    for reaction in msg.reactions:
        async for user in reaction.users():
            if user.id == bot.user.id:
                await msg.clear_reaction(reaction.emoji)
    if count <= 9:
        await msg.add_reaction(nums[count])
    else:
        for x in str(count):
            await msg.add_reaction(nums[int(x)])


bot.run(API)
