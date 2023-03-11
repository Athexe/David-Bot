import yaml
import sys
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)
with open('config.yml', 'rb') as f:
  config = yaml.safe_load(f)

message = sys.argv[1] # Get our argument with message and media urls

@discord_client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(discord_client))

  channel_trash = discord_client.get_channel(int(os.getenv("DISCORD_TRASH_CHANNEL")))

  data = message.split("@")
  print("!!!"+data[0]+"!!!")
  channels_cybersport = ["-1001421655869"]
  channels_lviv = ["-1001254374439"]
  channels_ukraine = ["-1001483876482","-1001308491047"]
  channels_halyava = ["-1001374759118"]
  #channels_steam = []
  
  
  if data[0] in channels_cybersport:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_CYBERSPORT_CHANNEL")))
  elif data[0] in channels_lviv:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_LVIV_CHANNEL")))
  elif data[0] in channels_ukraine:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_UKRAINE_CHANNEL")))
  elif data[0] in channels_halyava:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_HALYAVA_CHANNEL")))
  else:
    channel_send = discord_client.get_channel(int(os.getenv("DISCORD_TRASH_CHANNEL")))
  
  embed = discord.Embed(description=data[1])

  if data[2] != "":
    image = discord.File(data[2])
    if data[2].endswith(".mp4") == False:
      uploaded_image = await channel_trash.send(file=image)
      image_url = uploaded_image.attachments[0].url
      embed.set_image(url=image_url)
      await channel_send.send(embed=embed)
    else:
      embed.set_image(url="attachment://"+data[2])
      await channel_send.send(embed=embed, file=discord.File(data[2]))
    
  if len(data)>3:
    for i in range (3,len(data)):
      embed = discord.Embed()
      embed.set_image(url="attachment://"+data[i])
      await channel_send.send(embed=embed, file=discord.File(data[i]))
    
  quit()

discord_client.run(os.getenv("TOKEN"))
