import urllib.request
from pymongo import ReturnDocument
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from shivu import application, sudo_users, collection, db, CHARA_CHANNEL_ID, SUPPORT_CHAT

WRONG_FORMAT_TEXT = """Wrong ❌️ format...  eg. /upload Img_url muzan-kibutsuji Demon-slayer 3

img_url character-name anime-name rarity-number

Use rarity number accordingly rarity Map

rarity_map = 1 (⚪️ Common), 2 (🟣 Rare), 3 (🟡 Legendary), 4 (🟢 Medium)"""

async def get_next_sequence_number(sequence_name):
    sequence_collection = db.sequences
    sequence_document = await sequence_collection.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=ReturnDocument.AFTER
    )
    if not sequence_document:
        # Initialize sequence if not found
        await sequence_collection.insert_one({'_id': sequence_name, 'sequence_value': 1})
        return 1
    return sequence_document['sequence_value']

async def upload(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 4:
            await update.message.reply_text(WRONG_FORMAT_TEXT)
            return

        img_url = args[0]
        character_name = args[1].replace('-', ' ').title()
        anime = args[2].replace('-', ' ').title()

        # Validate image URL
        try:
            urllib.request.urlopen(img_url)
        except Exception:
            await update.message.reply_text('Invalid image URL. Please provide a valid one.')
            return

        # Map rarity
        rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium"}
        try:
            rarity = rarity_map[int(args[3])]
        except (KeyError, ValueError):
            await update.message.reply_text('Invalid rarity. Please use 1, 2, 3, or 4.')
            return

        char_id = str(await get_next_sequence_number('character_id')).zfill(2)

        character = {
            'img_url': img_url,
            'name': character_name,
            'anime': anime,
            'rarity': rarity,
            'id': char_id
        }

        try:
            message = await context.bot.send_photo(
                chat_id=CHARA_CHANNEL_ID,
                photo=img_url,
                caption=f'<b>Character Name:</b> {character_name}\n<b>Anime Name:</b> {anime}\n<b>Rarity:</b> {rarity}\n<b>ID:</b> {char_id}\nAdded by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )
            character['message_id'] = message.message_id
            await collection.insert_one(character)
            await update.message.reply_text('Character added successfully.')
        except Exception:
            await update.message.reply_text("Character added to the database but couldn't be uploaded to the channel.")
            await collection.insert_one(character)

    except Exception as e:
        await update.message.reply_text(f'Upload failed: {str(e)}. Contact {SUPPORT_CHAT} if the issue persists.')

async def delete(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 1:
            await update.message.reply_text('Incorrect format. Use: /delete ID')
            return

        char_id = args[0]
        character = await collection.find_one_and_delete({'id': char_id})

        if character:
            try:
                await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
            except Exception:
                pass
            await update.message.reply_text('Character deleted successfully.')
        else:
            await update.message.reply_text('Character not found.')
    except Exception as e:
        await update.message.reply_text(f'Deletion failed: {str(e)}')

async def update(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in sudo_users:
        await update.message.reply_text('You do not have permission to use this command.')
        return

    try:
        args = context.args
        if len(args) != 3:
            await update.message.reply_text('Incorrect format. Use: /update id field new_value')
            return

        char_id = args[0]
        field = args[1]
        new_value = args[2]

        character = await collection.find_one({'id': char_id})
        if not character:
            await update.message.reply_text('Character not found.')
            return

        valid_fields = ['img_url', 'name', 'anime', 'rarity']
        if field not in valid_fields:
            await update.message.reply_text(f'Invalid field. Choose from: {", ".join(valid_fields)}.')
            return

        if field in ['name', 'anime']:
            new_value = new_value.replace('-', ' ').title()
        elif field == 'rarity':
            rarity_map = {1: "⚪ Common", 2: "🟣 Rare", 3: "🟡 Legendary", 4: "🟢 Medium"}
            try:
                new_value = rarity_map[int(new_value)]
            except (KeyError, ValueError):
                await update.message.reply_text('Invalid rarity. Use 1, 2, 3, or 4.')
                return

        await collection.find_one_and_update({'id': char_id}, {'$set': {field: new_value}})

        if field == 'img_url':
            try:
                await context.bot.delete_message(chat_id=CHARA_CHANNEL_ID, message_id=character['message_id'])
                message = await context.bot.send_photo(
                    chat_id=CHARA_CHANNEL_ID,
                    photo=new_value,
                    caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                    parse_mode='HTML'
                )
                await collection.find_one_and_update({'id': char_id}, {'$set': {'message_id': message.message_id}})
            except Exception:
                pass
        else:
            await context.bot.edit_message_caption(
                chat_id=CHARA_CHANNEL_ID,
                message_id=character['message_id'],
                caption=f'<b>Character Name:</b> {character["name"]}\n<b>Anime Name:</b> {character["anime"]}\n<b>Rarity:</b> {character["rarity"]}\n<b>ID:</b> {character["id"]}\nUpdated by <a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>',
                parse_mode='HTML'
            )

        await update.message.reply_text('Character updated successfully.')
    except Exception as e:
        await update.message.reply_text(f'Update failed: {str(e)}')

UPLOAD_HANDLER = CommandHandler('upload', upload, block=False)
DELETE_HANDLER = CommandHandler('delete', delete, block=False)
UPDATE_HANDLER = CommandHandler('update', update, block=False)

application.add_handler(UPLOAD_HANDLER)
application.add_handler(DELETE_HANDLER)
application.add_handler(UPDATE_HANDLER)
