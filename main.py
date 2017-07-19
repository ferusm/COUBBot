import discord
import re
import requests
r = requests.get("http://example.com/foo/bar")

emoji_list = {
    "0⃣":0, "1⃣":1, "2⃣":2, "3⃣":3, "4⃣":4, "5⃣":5, "6⃣":6, "7⃣":7, "8⃣":8, "9⃣":9, "🔟":10
}

coub_pattern = re.compile("[\s\S]*coub.com/view/[\s\S]+", re.IGNORECASE)


client = discord.Client(max_messages=100000)


@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name + "; " + client.user.id)
    print('Start loading messages from chanel named COUB')
    for channel in client.get_all_channels():
        if channel.name == "COUB" or channel.name == "coub":
            async for message in client.logs_from(channel=channel, limit=10000):
                client.messages.append(message)
                await on_message(message)
            return
    raise ValueError("Can't find COUB channel")

@client.event
async def on_message(message):
    count = 0
    for message_iterator in client.messages:
        if message.content == message_iterator.content:
            count = count + 1
    if count > 1:
        await client.delete_message(message)
        return
    if not message.author.bot:
        if coub_pattern.match(message.content):
            try:
                req = requests.get(message.content)
            except:
                await client.delete_message(message)
                print("404")
                return
            if req.status_code != 404:
                bot_content = "Прислал: " + message.author.name + "\nОценка: 0.0/10\n" + message.content
                bot_message = await client.send_message(message.channel, content=bot_content)
                await client.delete_message(message)
                for emoji in emoji_list.keys():
                    await client.add_reaction(message=bot_message, emoji=emoji)
            else:
                await client.delete_message(message)

@client.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        rating = 0
        count = 0
        for reaction_iterator in reaction.message.reactions:
            reaction_rating = emoji_list.get(reaction_iterator.emoji)
            if reaction_iterator.count > 1 and reaction_rating is not None:
                rating = rating + reaction_rating * reaction_iterator.count
                count = count + reaction_iterator.count
        if count == 0:
            rating = 0
        else:
            rating = rating / count
        new_content = reaction.message.content
        new_content = re.sub(r"Оценка: -*\d+\.*\d*/10", "Оценка: " + str(rating) + "/10", new_content)
        await client.edit_message(reaction.message, new_content=new_content)


@client.event
async def on_reaction_remove(reaction, user):
    if not user.bot:
        rating = 0
        count = 0
        for reaction_iterator in reaction.message.reactions:
            reaction_rating = emoji_list.get(reaction_iterator.emoji)
            if reaction_iterator.count > 1 and reaction_rating is not None:
                rating = rating + reaction_rating * reaction_iterator.count
                count = count + reaction_iterator.count
        if count == 0:
            rating = 0
        else:
            rating = rating / count
        new_content = reaction.message.content
        new_content = re.sub(r"Оценка: \d+\.*\d*/10", "Оценка: " + str(rating) + "/10", new_content)
        await client.edit_message(reaction.message, new_content=new_content)

client.run('MzExNjIwMzMzNjA4MTA4MDM1.C_PK2g.D9ubmt5EOZ3hi9SW6-hXhUoABHE')