import asyncio
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import MessageNotModified
from Zaid.main import Test, bot as Client



from Zaid.Database.dbusers import add_served_user
from config import START_PIC, UPDATES_CHANNEL, GROUP_SUPPORT


ALIVE_PIC = START_PIC

HOME_TEXT = """
HEY! 🌼 {} 🌼
➖➖➖➖➖➖➖➖➖➖➖
 ** 🎼ɪ'ᴍ ᴊᴜꜱᴛ ɴᴏᴛ ᴀ ᴍᴜꜱɪᴄ ʙᴏᴛ 🎼 
 ɪ ʜᴀᴠᴇ ʟᴏᴛꜱ ᴏꜰ ꜰᴇᴀᴛᴜʀᴇꜱ ᴡʜɪᴄʜ ʏᴏᴜ ʟɪᴋᴇꜱ ᴛʜᴀᴛ**.
‣ **ɪ ᴄᴀɴ ᴘʟᴀʏ ᴀᴜᴅɪᴏ+ᴠɪᴅᴇᴏ ʙᴏᴛʜ 🎬**.
‣ **ɪ ʜᴀᴠᴇ ᴀʟᴍᴏꜱᴛ ᴀʟʟ ꜰᴇᴀᴛᴜʀᴇꜱ ᴡʜɪᴄʜ ɴᴇᴇᴅꜱ ᴀ ᴍᴜꜱɪᴄ ʙᴏᴛ**
➖➖➖➖➖➖➖➖➖➖➖
🌸 **ᴄʟɪᴄᴋ ᴏɴ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ 🌸**.
"""
HELP_TEXT = """
🌸 **ʜᴏᴡ ᴛᴏ ꜱᴇᴛᴜᴘ?**

‣ ꜱᴛᴀʀᴛ ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.⚡️
‣ ᴀᴅᴅ ʙᴏᴛ `{}` ᴀɴᴅ ᴜꜱᴇʀ ᴀᴄᴄᴏᴜɴᴛ ɪɴ ᴄʜᴀᴛ ᴡɪᴛʜ ᴀᴅᴍɪɴ ʀɪɢʜᴛꜱ.⚡️
‣ ᴅᴏɴᴇ ꜱᴇᴛᴜᴘ ᴘʀᴏᴄᴇꜱꜱ ʀᴇᴀᴅ ᴄᴏᴍᴍᴀɴᴅꜱ ʙᴇʟᴏᴡ 👇.
"""



USER_TEXT = """
🌸 **ᴜꜱᴇʀꜱ ᴄᴏᴍᴍᴀɴᴅꜱ** 

‣ /play <Qᴜᴇʀʏ> ᴛᴏ ᴘʟᴀʏ ᴀ ꜱᴏɴɢ.
‣ /vplay <Qᴜᴇʀʏ> ᴛᴏ ᴘʟᴀʏ ᴠɪᴅᴇᴏ.
‣ /stream <ʟɪᴠᴇ ᴜʀʟ> ᴛᴏ ᴘʟᴀʏ ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍꜱ.
‣ /song ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴀ ᴀᴜᴅɪᴏ ꜰɪʟᴇ ꜰʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ. 
‣ /video ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ꜰʀᴏᴍ ʏᴏᴜᴛᴜʙᴇ.
‣ /lyric ᴛᴏ ꜰɪɴᴅ ʟʏʀɪᴄꜱ.
"""

SPAM_TEXT = """
🌸 **ꜱᴘᴀᴍ ᴄᴏᴍᴍᴀɴᴅꜱ (ꜱᴜᴅᴏ_ᴜꜱᴇʀꜱ)** :

‣ /spam <ᴄᴏᴜɴᴛ> ᴛᴇxᴛ ᴛᴏ ꜱᴘᴀᴍ ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ.
‣ /fspam <ᴄᴏᴜɴᴛ> ᴛᴇxᴛ ꜰᴏʀ ꜱᴘᴀᴍᴍɪɴɢ.
‣ /delayspam <ᴄᴏᴜɴᴛ> ᴛᴇxᴛ ꜰᴏʀ ꜱᴘᴀᴍᴍɪɴɢ.
"""

RAID_TEXT = """
🌸 **ʀᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅꜱ (ꜱᴜᴅᴏ_ᴜꜱᴇʀꜱ)** :

‣ /vcraid <ᴄʜᴀᴛɪᴅ> - ɢɪᴠᴇ ᴀ ᴄʜᴀᴛ ɪᴅ ᴇʟꜱᴇ ᴜꜱᴇʀɴᴀᴍᴇ ᴛᴏ ᴠᴏɪᴄᴇ ʀᴀɪᴅ.
‣ /vraid <ᴄʜᴀᴛɪᴅ + ʀᴇᴘʟʏ ᴛᴏ ᴠɪᴅᴇᴏ ꜰɪʟᴇ> - ᴛᴏ ʀᴀɪᴅ ᴠɪᴅᴇᴏ.
‣ /raidpause - ᴛᴏ ᴘᴀᴜꜱᴇ ʀᴀɪᴅ.
‣ /raidresume ᴛᴏ ʀᴇꜱᴜᴍᴇ ʀᴀɪᴅ.
‣ /raidend <ᴄʜᴀᴛɪᴅ> ᴛᴏ ᴇɴᴅ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ʀᴀɪᴅ.
"""

ADMIN = """
🌸 **ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ** :

‣ /changeassistant <1,2,3,4,5> ᴛᴏ ᴄʜᴀɴɢᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ (ɪꜰ 2 ᴏʀ ᴍᴏʀᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ<ᴍᴜʟᴛɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ>).
‣ /checkassistant ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜɪᴄʜ ᴀꜱꜱɪꜱᴛᴀɴᴛ ᴘʀᴇꜱᴇɴᴛ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
‣ /end ᴛᴏ ᴇɴᴅ ꜱᴛʀᴇᴀᴍɪɴɢ.
‣ /pause ᴛᴏ ᴘᴀᴜꜱᴇ ꜱᴛʀᴇᴀᴍ.
‣ /resume ᴛᴏ ʀᴇꜱᴜᴍᴇ ꜱᴛʀᴇᴀᴍ.
‣ /volume ᴛᴏ ꜱᴇᴛ ᴠᴏʟᴜᴍᴇ.
‣ /skip ᴛᴏ ꜱᴋɪᴘ ᴛʀᴀᴄᴋꜱ.
"""

SUDO_TEXT = """
🌸 **ꜱᴏᴍᴇ ᴍᴏʀᴇ ᴇxᴛʀᴀ ᴄᴏᴍᴍᴀɴᴅꜱ ꜰᴏʀ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ**

‣ /gban ᴛᴏ ʙᴀɴ ꜱᴏᴍᴇᴏɴᴇ ɢʟᴏʙᴀʟʟʏ.
‣ /ungban ᴛᴏ ᴜɴʙᴀɴ  ɢʟᴏʙᴀʟʟʏ ɪꜰ ɢʙᴀɴɴᴇᴅ.
‣ /broadcast ᴛᴏ ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴡʜɪᴄʜ ᴘʀᴇꜱᴇɴᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀꜱᴇ.
‣ /activevoice ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛꜱ.
‣ /activevideo ᴛᴏ ᴄʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛꜱ.
"""

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data=="help":
        get_me = await client.get_me()
        USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("🍁 ᴀᴅᴍɪɴꜱ 🍁 ", callback_data="azminss"),
                InlineKeyboardButton("🍁 ᴜꜱᴇʀꜱ 🍁 ", callback_data="users"),
            ],
            [
                InlineKeyboardButton(" 👮🏻 ᴠᴄ ʀᴀɪᴅ ⚡️ ", callback_data="raid"),
                InlineKeyboardButton("👮🏻 ꜱᴘᴀᴍ ⚡️", callback_data="spam"),
            ],
            [
                InlineKeyboardButton("☘️ ꜱᴜᴅᴏꜱ ☘️", callback_data="sudouser"),
            ],
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙 ", callback_data="home"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌ ", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT.format(USERNAME),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="home":
        get_me = await client.get_me()
        USERNAME = get_me.username
        buttons = [
            [
                InlineKeyboardButton("⚡️ ADD ME IN YOUR FAMILY ❤️", url=f"https://t.me/{USERNAME}?startgroup=true"),
            ],
            [
                InlineKeyboardButton("🤝🏻 GROUP 🤝🏻 ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton("🤝🏻 CHANNEL 🤝🏻", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ],
            [
                InlineKeyboardButton("  YM 💟 ", url="https://telegra.ph/file/c422fdf4bc9a1128b64b4.jpg"),
            ],
            [
                InlineKeyboardButton("⚙️ ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅꜱ ⚙️", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="users":
        buttons = [
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙", callback_data="help"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                USER_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="sudouser":
        buttons = [
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙 ", callback_data="help"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                SUDO_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="azminss":
        buttons = [
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙", callback_data="help"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                ADMIN,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="raid":
        buttons = [
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙", callback_data="help"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌ ", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                RAID_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="spam":
        buttons = [
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙 ", callback_data="help"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                SPAM_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data=="close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

    elif query.data=="cls":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass


@Client.on_message(filters.command(["start"]) & filters.private)
async def start(client: Client, message: Message):
    get_me = await client.get_me()
    user_id = message.from_user.id
    await add_served_user(user_id)
    USERNAME = get_me.username
    buttons = [
            [
                InlineKeyboardButton("❤️ ADD ME IN YOUR FAMILY ❤️", url='https://t.me/{USERNAME}?startgroup=true'),
            ],
            [
                InlineKeyboardButton("🤝🏻 GROUP 🤝🏻", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton("🤝🏻CHANNEL 🤝🏻", url=f"https://t.me/{UPDATES_CHANNEL}"),
            ],
            [
                InlineKeyboardButton(" YM 💟", url="https://telegra.ph/file/c422fdf4bc9a1128b64b4.jpg"),
            ],
            [
                InlineKeyboardButton("⚙️ ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅꜱ ⚙️", callback_data="help"),
            ]
            ]     
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(photo=f"{ALIVE_PIC}", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)

@Client.on_message(filters.command(["help"]) & filters.private)
async def help(client: Client, message: Message):
    get_me = await client.get_me()
    self.username = get_me.username
    buttons = [
           [
                InlineKeyboardButton("🍁 ᴀᴅᴍɪɴꜱ 🍁", call_back_data="azminss"),
                InlineKeyboardButton("🍁 ᴜꜱᴇʀꜱ 🍁", callback_data="users"),
            ],
            [
                InlineKeyboardButton("👮🏻 ᴠᴄ ʀᴀɪᴅ 👮", callback_data="raid"),
                InlineKeyboardButton("👮 ꜱᴘᴀᴍ 👮", callback_data="spam"),
            ],
            [
                InlineKeyboardButton("☘️ ꜱᴜᴅᴏꜱ ☘️", callback_data="sudouser"),
            ],
            [
                InlineKeyboardButton("🌼 Bᴀᴄᴋ 🔙 ", callback_data="home"),
                InlineKeyboardButton("🌼 Cʟᴏꜱᴇ ❌ ", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(photo=f"{ALIVE_PIC}", caption=f"{HELP_TEXT}", reply_markup=reply_markup)
