from telethon import TelegramClient, events
from telethon.tl.types import InputChannel
import yaml
import sys
import os
from dotenv import load_dotenv
from webserver import keep_alive
import subprocess

# Loading configuration
load_dotenv()

def start(config):
  # Telegram Client Init
  client = TelegramClient(os.getenv("SESSION_NAME"), os.getenv("API_ID"), os.getenv("API_HASH"))
  client.start()

  # Input Messages Telegram Channels will be stored in these empty Entities
  input_channels_entities = []
  output_channel_entities = []

  # Iterating over dialogs and finding new entities and pushing them to our empty entities list above
  for d in client.iter_dialogs():
    if d.name in config["input_channel_names"] or d.entity.id in config[
        "input_channel_ids"]:
      input_channels_entities.append(
        InputChannel(d.entity.id, d.entity.access_hash))
    if d.name in config["output_channel_names"] or d.entity.id in config[
        "output_channel_ids"]:
      output_channel_entities.append(
        InputChannel(d.entity.id, d.entity.access_hash))

  # TELEGRAM NEW MESSAGE - When new message triggers, come here
  @client.on(events.NewMessage(chats=input_channels_entities))
  async def handler(event):
    for output_channel in output_channel_entities:
      message = event.message
      folder = ""
      if event.message.media:
        if message.file.size<8000000 :
          folder = await message.download_media("downloads/")
          
      #if folder.endswith("mp4") or folder.endswith("MP4"):
      #  from_path   = os.path.join("downloads/", old_filename[1])
      #  to_path     = os.path.join("downloadsMP4", old_filename[1].rsplit('.', 1)[0]) + '.' + "mp4"
      #  clip = mp.VideoFileClip(from_path)
      #  clip.write_videofile(to_path)
      #  folder = to_path

      parsed_response = str(message.chat_id)+"%!@"+message.message +"%!@"+folder
      #print(parsed_response)
      
      subprocess.call(["python", "discord_messager.py", parsed_response])
      await client.forward_messages(output_channel, message)

      try:
        os.remove(folder)
      except:
        print("")

  keep_alive()
  client.run_until_disconnected()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} {{CONFIG_PATH}}")
    sys.exit(1)
  with open(sys.argv[1], 'rb') as f:
    config = yaml.safe_load(f)
  start(config)