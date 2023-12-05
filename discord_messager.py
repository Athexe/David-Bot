import yaml
import sys
import discord
import os
from dotenv import load_dotenv

# Loading configuration
load_dotenv()
with open('config.yml', 'rb') as f:
  config = yaml.safe_load(f)

# Discord initialization
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

# Get our data from argument
message = sys.argv[1] 
data = message.split("%!@")

@discord_client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(discord_client))

  # Channel id's
  channels_cybersport = ["-1001421655869"]
  channels_lviv = ["-1001254374439"]
  channels_ukraine = ["-1001483876482","-1001308491047"]
  channels_halyava = ["-1001374759118"]
  
  # Get channel to send message
  channel_trash = discord_client.get_channel(int(os.getenv("DISCORD_TRASH_CHANNEL")))
  if data[0] in channels_cybersport:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_CYBERSPORT_CHANNEL")))
  elif data[0] in channels_lviv and "Львівич | Підписатися" in data[1]:
    data[1] = data[1].replace("Львівич | Підписатися","")
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_LVIV_CHANNEL")))
  elif data[0] in channels_ukraine and ("ЦЕНТР" in data[1] or "Інформує Україна" in data[1]):
    data[1] = data[1].replace("ЦЕНТР","").replace("Інформує Україна","")
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_UKRAINE_CHANNEL")))
  elif data[0] in channels_halyava and "Получить игру можно бесплатно" in data[1]:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_HALYAVA_CHANNEL")))
  else:
    channel_send = channel_trash
  
  # Sending messages
  embed = discord.Embed(description=data[1])
  if data[2] != "":
    image = discord.File(data[2])
    if data[2].lower().endswith(".mp4"):
      embed.set_image(url="attachment://"+data[2])
      await channel_send.send(embed=embed, file=discord.File(data[2]))
    else:
      uploaded_image = await channel_trash.send(file=image)
      image_url = uploaded_image.attachments[0].url
      embed.set_image(url=image_url)
      await channel_send.send(embed=embed)
  else:
    await channel_send.send(embed=embed)
    
  if len(data)>3:
    for i in range (3,len(data)):
      embed = discord.Embed()
      embed.set_image(url="attachment://"+data[i])
      await channel_send.send(embed=embed, file=discord.File(data[i]))
  
  # Exit Bot
  quit()

discord_client.run(os.getenv("TOKEN"))