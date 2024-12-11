from telethon import TelegramClient, events
from kafka_data.db.servic import insert_to_mongo
from config_kafka import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_CHANNELS,KAFKA_TOPIC


client = TelegramClient('telegram_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)

@client.on(events.NewMessage(chats=TELEGRAM_CHANNELS))
async def handle_new_message(event):
    message_text = event.message.message or ""
    print(f"New message received: {message_text}")

    if event.message.media:
        file_path = await event.message.download_media()
        print(f"Media downloaded: {file_path}")
    else:
        file_path = None

    message_data = {
        'channel': event.chat.title if hasattr(event.chat, 'title') else "Unknown",
        'message': message_text,
        'date': str(event.message.date),
        'media': file_path
    }
    insert_to_mongo(message_data)
    print(f"Inserted message to MongoDB: {message_data}")

if __name__ == "__main__":
    with client:
        print("Listening for financial updates...")
        client.run_until_disconnected()
