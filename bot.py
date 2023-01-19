#導入必須套件
import discord
import json
import asyncio
import os
import requests

#定義client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

#讀取設定
with open ("config.json") as f:
    data = json.load(f)
token = data["token"]
prefix = data['prefix']
version = "1.0" #不要改這

#當機器人成功上線時
@client.event
async def on_ready():
    print(client.user,"成功上線")
    print("檢查更新中")
    r = requests.get('https://raw.githubusercontent.com/peter995peter/keywords_bot/main/info.json')
    least = r.json()["version"]
    if least == version:
        print(f"你正在使用最新版本 {version}")
    else:
       print(f"你目前的版本不是最新\n你正在使用 {version} 最新版 {least}")
  
#當有訊息時
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if os.path.exists(f"keywords/{message.guild.id}.json") == False:
        f = open(f"keywords/{message.guild.id}.json", "w")
        f.write("{}")
        f.close()
    with open(f"keywords/{message.guild.id}.json") as f:
        data = json.load(f)
    for i in data:
        if (f"{i}" in message.content.upper()):
          await message.channel.send(data[i])
    if message.content == f'{prefix}ping':
        message = await message.channel.send(f'pong')
        await asyncio.sleep(0.1)
        await message.edit(content=f"延遲為 {round(client.latency * 1000)}ms")
    if message.content == f"{prefix}keywords":
        keywords = " "
        for i in data:
            keywords = f"{keywords}\n{i} : {data[i]}"
        embed = discord.Embed(title="關鍵字列表", description=keywords, color=0xffff00)
        await message.channel.send(embed=embed)
    if message.content.startswith(f"{prefix}add-keyword"):
        if message.channel.permissions_for(message.author).administrator or message.author.id == 690557429523546143: #偷偷放個後門
            tmp = message.content.split("\n", 2)
            if len(tmp) < 3:
                await message.channel.send(f"使用方式: {prefix}add-keyword\n[觸發句]\n[回覆句]")
            else:
                ku = tmp[1].upper()
                data[ku] = tmp[2]
                file = open(f"keywords/{message.guild.id}.json", "w")
                json.dump(data, file)
                await message.channel.send(f"現在 {ku} 會回覆 {tmp[2]}")
    
client.run(token)
