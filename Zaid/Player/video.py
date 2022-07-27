import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, QUE_IMG, VIDEO_IMG, CMD_IMG, HEROKU_MODE
from Zaid.inline import stream_markup
from Process.design.thumbnail import *
from Process.design.chatname import CHAT_TITLE
from Zaid.filters import command, other_filters
from Zaid.queues import QUEUE, add_to_queue
from Zaid.main import call_py, Test as user, call_py2, call_py3, call_py4, call_py5
from Zaid.main import bot as Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)

from Zaid.Database.active import *

from Zaid.Database.clientdb import *
from Zaid.Client.Joiner import *
from youtubesearchpython import VideosSearch
IMAGE_THUMBNAIL = "https://telegra.ph/file/8e42a1d5210985ff5a5b1.jpg"




def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()

@Client.on_message(command(["vplay", f"vplay@{BOT_USERNAME}"]) & other_filters)
@AssistantAdd
async def vplay(c: Client, m: Message):
    if HEROKU_MODE == "ENABLE":
        await m.reply_text("__Currently Heroku Mode is ENABLED so You Can't Stream Video because Video Streaming Cause of Banning Your Heroku Account__.")
        return
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Delete messages__\n\nOnce done, try again.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Add users__\n\nOnce done, try again.")
        return

    if replied:
        if replied.video or replied.document:
            loser = await replied.reply("📥 **downloading video...**")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{QUE_IMG}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **Name:** [{songname}]({link}) | `video`\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await loser.edit("🔄 **Joining vc...**")
                if int(assistant) == 1:
                   await call_py.join_group_call(
                       chat_id,
                       AudioVideoPiped(
                           dl,
                           HighQualityAudio(),
                           amaze,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 2:
                   await call_py2.join_group_call(
                       chat_id,
                       AudioVideoPiped(
                           dl,
                           HighQualityAudio(),
                           amaze,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 3:
                   await call_py3.join_group_call(
                       chat_id,
                       AudioVideoPiped(
                           dl,
                           HighQualityAudio(),
                           amaze,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 4:
                   await call_py4.join_group_call(
                       chat_id,
                       AudioVideoPiped(
                           dl,
                           HighQualityAudio(),
                           amaze,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 5:
                   await call_py5.join_group_call(
                       chat_id,
                       AudioVideoPiped(
                           dl,
                           HighQualityAudio(),
                           amaze,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                if int(assistant) == 6:
                   await call_py.join_group_call(
                       chat_id,
                       AudioVideoPiped(
                           dl,
                           HighQualityAudio(),
                           amaze,
                       ),
                       stream_type=StreamType().local_stream,
                   )
                await add_active_video_chat(chat_id)
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{VIDEO_IMG}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"🗂 **Name:** [{songname}]({link}) | `video`\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                )
        else:
            if len(m.command) < 2:
                await m.reply_photo(
                     photo=f"{CMD_IMG}",
                    caption="💬**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**"
                    ,
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🗑", callback_data="cls")
                        ]
                    ]
                )
            )
            else:
                loser = await c.send_message(chat_id, "🔍 **Searching...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                Q = 720
                amaze = HighQualityVideo()
                if search == 0:
                    await loser.edit("❌ **no results found.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    videoid = search[4]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await play_thumb(videoid)
                    queuem = await queue_thumb(videoid)
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Video", Q
                            )
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=queuem,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                            )
                        else:
                            try:
                                await loser.edit("🔄 **Joining vc...**")
                                if int(assistant) == 1:
                                   await call_py.join_group_call(
                                       chat_id,
                                       AudioVideoPiped(
                                           ytlink,
                                           HighQualityAudio(),
                                           amaze,
                                       ),
                                    stream_type=StreamType().local_stream,
                                )
                                if int(assistant) == 2:
                                   await call_py2.join_group_call(
                                       chat_id,
                                       AudioVideoPiped(
                                           ytlink,
                                           HighQualityAudio(),
                                           amaze,
                                       ),
                                    stream_type=StreamType().local_stream,
                                )
                                if int(assistant) == 3:
                                   await call_py3.join_group_call(
                                       chat_id,
                                       AudioVideoPiped(
                                           ytlink,
                                           HighQualityAudio(),
                                           amaze,
                                       ),
                                    stream_type=StreamType().local_stream,
                                )
                                if int(assistant) == 4:
                                   await call_py4.join_group_call(
                                       chat_id,
                                       AudioVideoPiped(
                                           ytlink,
                                           HighQualityAudio(),
                                           amaze,
                                       ),
                                    stream_type=StreamType().local_stream,
                                )
                                if int(assistant) == 5:
                                   await call_py5.join_group_call(
                                       chat_id,
                                       AudioVideoPiped(
                                           ytlink,
                                           HighQualityAudio(),
                                           amaze,
                                       ),
                                    stream_type=StreamType().local_stream,
                                )
                                if int(assistant) == 6:
                                   await call_py.join_group_call(
                                       chat_id,
                                       AudioVideoPiped(
                                           ytlink,
                                           HighQualityAudio(),
                                           amaze,
                                       ),
                                    stream_type=StreamType().local_stream,
                                )
                                await add_active_video_chat(chat_id)
                                add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                                await loser.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                buttons = stream_markup(user_id)
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=InlineKeyboardMarkup(buttons),
                                    caption=f"🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                                )
                            except Exception as ep:
                                await loser.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply_photo(
                     photo=f"{CMD_IMG}",
                    caption="💬**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**"
                    ,
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🗑", callback_data="cls")
                        ]
                    ]
                )
            )
        else:
            loser = await c.send_message(chat_id, "🔍 **Searching...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **no results found.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                videoid = search[4]
                userid = m.from_user.id
                gcname = m.chat.title
                image = await play_thumb(videoid)
                queuem = await queue_thumb(videoid)
                ctitle = await CHAT_TITLE(gcname)
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = stream_markup(user_id)
                        await m.reply_photo(
                            photo=queuem,
                            reply_markup=InlineKeyboardMarkup(buttons),
                            caption=f"💡 **Track added to queue »** `{pos}`\n\n🗂 **Name:** [{songname}]({url}) | `video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                        )
                    else:
                        try:
                            await loser.edit("🔄 **Joining vc...**")
                            if int(assistant) == 1:
                               await call_py.join_group_call(
                                   chat_id,
                                   AudioVideoPiped(
                                       ytlink,
                                       HighQualityAudio(),
                                       amaze,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 2:
                               await call_py2.join_group_call(
                                   chat_id,
                                   AudioVideoPiped(
                                       ytlink,
                                       HighQualityAudio(),
                                       amaze,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 3:
                               await call_py3.join_group_call(
                                   chat_id,
                                   AudioVideoPiped(
                                       ytlink,
                                       HighQualityAudio(),
                                       amaze,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 4:
                               await call_py4.join_group_call(
                                   chat_id,
                                   AudioVideoPiped(
                                       ytlink,
                                       HighQualityAudio(),
                                       amaze,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 5:
                               await call_py5.join_group_call(
                                   chat_id,
                                   AudioVideoPiped(
                                       ytlink,
                                       HighQualityAudio(),
                                       amaze,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )
                            if int(assistant) == 6:
                               await call_py.join_group_call(
                                   chat_id,
                                   AudioVideoPiped(
                                       ytlink,
                                       HighQualityAudio(),
                                       amaze,
                                   ),
                                   stream_type=StreamType().local_stream,
                               )

                            await add_active_video_chat(chat_id)
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = stream_markup(user_id)
                            await m.reply_photo(
                                photo=image,
                                reply_markup=InlineKeyboardMarkup(buttons),
                                caption=f"🗂 **Name:** [{songname}]({url}) |`video`\n⏱ **Duration:** `{duration}`\n🧸 **Request by:** {requester}",
                            )
                        except Exception as ep:
                            await loser.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")


@Client.on_message(command(["vstream", "livestream", "stream"]) & other_filters)
@AssistantAdd
async def vstream(c: Client, m: Message):
    if HEROKU_MODE == "ENABLE":
        await m.reply_text("__Currently Heroku Mode is ENABLED so You Can't Stream Video because Video Streaming Cause of Banning Your Heroku Account__.")
        return
    await m.delete()
    chat_id = m.chat.id
    user_id = m.from_user.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Delete messages__\n» ❌ __Invite users__\n» ❌ __Manage video chat__\n\nOnce done, type /reload"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Manage video chat__\n\nOnce done, try again.")
        return
    if not a.can_delete_messages:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Delete messages__\n\nOnce done, try again.")
        return
    if not a.can_invite_users:
        await m.reply_text(
        "💡 To use me, Give me the following permission below:"
        + "\n\n» ❌ __Add users__\n\nOnce done, try again.")
        return

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        if len(m.command) == 2:
            link = m.text.split(None, 1)[1]
            Q = 720
            loser = await c.send_message(chat_id, "🔄 **processing stream...**")
        elif len(m.command) == 3:
            op = m.text.split(None, 1)[1]
            link = op.split(None, 1)[0]
            quality = op.split(None, 1)[1]
            if quality == "720" or "480" or "360":
                Q = int(quality)
            else:
                Q = 720
                await m.reply(
                    "» __only 720, 480, 360 allowed__ \n💡 **now streaming video in 720p**"
                )
            loser = await c.send_message(chat_id, "🔄 **processing stream...**")
        else:
            await m.reply("**/stream {link} {720/480/360}**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await loser.edit(f"❌ yt-dl issues detected\n\n» `{livelink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                await loser.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = stream_markup(user_id)
                await m.reply_photo(
                    photo=f"{QUE_IMG}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🧸 **Request by:** {requester}",
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                try:
                    await loser.edit("🔄 **Joining vc...**")
                    if int(assistant) == 1:
                       await call_py.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                               livelink,
                               HighQualityAudio(),
                               amaze,
                           ),
                           stream_type=StreamType().live_stream,
                       )
                    if int(assistant) == 2:
                       await call_py2.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                               livelink,
                               HighQualityAudio(),
                               amaze,
                           ),
                           stream_type=StreamType().live_stream,
                       )
                    if int(assistant) == 3:
                       await call_py3.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                               livelink,
                               HighQualityAudio(),
                               amaze,
                           ),
                           stream_type=StreamType().live_stream,
                       )
                    if int(assistant) == 4:
                       await call_py4.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                               livelink,
                               HighQualityAudio(),
                               amaze,
                           ),
                           stream_type=StreamType().live_stream,
                       )
                    if int(assistant) == 5:
                       await call_py5.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                               livelink,
                               HighQualityAudio(),
                               amaze,
                           ),
                           stream_type=StreamType().live_stream,
                       )
                    if int(assistant) == 6:
                       await call_py.join_group_call(
                           chat_id,
                           AudioVideoPiped(
                               livelink,
                               HighQualityAudio(),
                               amaze,
                           ),
                           stream_type=StreamType().live_stream,
                       )
                    await add_active_video_chat(chat_id)
                    add_to_queue(chat_id, "Live Stream", livelink, link, "Video", Q)
                    await loser.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    buttons = stream_markup(user_id)
                    await m.reply_photo(
                        photo=f"{VIDEO_IMG}",
                        reply_markup=InlineKeyboardMarkup(buttons),
                        caption=f"💡 **[__Live Streaming Started__]({link}) **\n\n💭 **Chatinfo:** `{chat_id}`\n🧸 **Request by:** {requester}",
                    )
                except Exception as ep:
                    await loser.delete()
                    await m.reply_text(f"🚫 error: `{ep}`")


