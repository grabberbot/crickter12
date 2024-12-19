import aiohttp
from pymongo import ReturnDocument
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

WRONG_FORMAT_TEXT = """Wrong ❌️ format... eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

Use rarity number accordingly rarity Map:
1 (⚪️ Common), 2 (🟣 Rare), 3 (🟡 Legendary), 4 (🟢 Medium)"""


async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 0})
        return 0
    return sequence_document['sequence_value']


async def validate_url(url: str) -> bool:
    """Validate the given URL using aiohttp."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as response:
                return response.status == 200
    except Exception:
        return False


async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You are not authorized to use this command. Contact the owner.')
        return

    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        image_url, character_name, anime_name, rarity_number = args[0], args[1], args[2], args[3]

        # Validate URL
        if not await validate_url(image_url):
            await update.message.reply_text('Invalid URL. Please provide a valid image URL.')
            return

        # Parse and format character details
        character_name = character_name.replace('-', ' ').title()
        anime_name = anime_name.replace('-', ' ').title()

        # Validate rarity
        rarity_map = {1: "⚪️ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium"}
        try:
            rarity = rarity_map[int(rarity_number)]
        except KeyError:
            await update.message.reply_text('Invalid rarity. Use 1, 2, 3, or 4.')
            return

        # Get next ID
        character_id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': image_url,
            'name': character_name,
            'anime': anime_name,
            'rarity': rarity,
            'id': character_id
        }

        # Send photo to the channel
        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=image_url,
                caption=f"<b>Character Name:</b> {character_name}\n"
                        f"<b>Anime Name:</b> {anime_name}\n"
                        f"<b>Rarity:</b> {rarity}\n"
                        f"<b>ID:</b> {character_id}\n"
                        f"Added by <a href='tg://user?id={update.effective_user.id}'>{update.effective_user.first_name}</a>",
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('Character added successfully!')
        except Exception as e:
            await update.message.reply_text(f"Error while uploading character: {str(e)}. Please try again.")
    except Exception as e:
        await update.message.reply_text(f"An unexpected error occurred: {str(e)}")


UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
application.add_handler(UPLOAD_HANDLER)
