from disnake import Message, Intents, RawReactionActionEvent, Reaction, Member
from disnake.ext import commands
from db_func import update_data, get_data, create_data

from config import *

nums = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

nums_add = ['0️⃣', ':zero:', '2️⃣ ', '3️⃣ ', '4️⃣ ', '5️⃣ ', '6️⃣ ', '7️⃣ ', '8️⃣ ', '9️⃣ ', '🔟']

intents = Intents()
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='.', intents=intents.all())

data = dict()


@bot.event
async def on_message(msg: Message):
    global data
    if msg.channel.id in data['stickers'].keys():

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
        update_data(data)
    else:
        if len(msg.stickers) != 0 and msg.stickers[0].id == id2Sticker:
            data['stickers'][msg.channel.id] = 1
            update_data(data)


async def prikol(msg: Message, count: int) -> None:
    for x in msg.reactions:
        if x in nums:
            await msg.remove_reaction(x, bot.user)
    print('lox')
    if count <= 9:
        await msg.add_reaction(nums[count])
    else:
        for x in str(count):
            await msg.add_reaction(nums[int(x)])


@bot.event
async def on_ready():
    global data
    print('START')
    create_data()  # if you start first time
    data = get_data()


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
            if payload.message_id in data['reactions'].keys():
                if payload.member.id not in data['reactions'][payload.message_id]:
                    data['reactions'][payload.message_id].append(payload.member.id)
            else:
                data['reactions'][payload.message_id] = [payload.member.id]
            update_data(data)

        await prikol(msg, len(data['reactions'][payload.message_id]))
    update_data(data)


bot.run(API)
