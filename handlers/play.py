import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(title, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 60)
    draw.text((40, 550), "Playing here...", (0, 0, 0), font=font)
    draw.text((40, 630), f"{title}", (0, 0, 0), font=font)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("☠️ 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...𝐑𝐮𝐤𝐨 𝐍𝐚😘.**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Sanki"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "𝐀𝐝𝐝 𝐌𝐞 𝐀𝐬 𝐀𝐝𝐦𝐢𝐧 𝐅𝐢𝐫𝐬𝐭😋.")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐉𝐨𝐢𝐧𝐞𝐝 ..𝐇𝐮𝐫𝐫𝐚𝐲𝐲𝐲💋💋.")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🛑 𝐅𝐥𝐨𝐨𝐝 𝐞𝐫𝐫𝐨𝐫 🛑</b> \n\𝐇𝐞𝐥𝐥𝐨, {user.first_name}, 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐂𝐨𝐮𝐥𝐝'𝐧𝐭 𝐉𝐨𝐢𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩. 𝐌𝐚𝐲 𝐁𝐞 𝐈𝐭𝐬 𝐁𝐚𝐧𝐧𝐞𝐝 𝐎𝐫 𝐎𝐭𝐡𝐞𝐫 𝐈𝐬𝐬𝐮𝐞.")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>𝐇𝐞𝐲, {user.first_name}, 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐍𝐨𝐭 𝐇𝐞𝐫𝐞 :( 𝐒𝐞𝐧𝐝 /play 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐅𝐢𝐫𝐬𝐭 𝐓𝐨 𝐀𝐝𝐝 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭.</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"𝐕𝐢𝐝𝐞𝐨 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧🥺 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬."
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/ab2865486ab04269fb706-ef319dc2d2a2043d24.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🥱 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                        url="https://t.me/shivamdemon")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❣️𝐎𝐰𝐧𝐞𝐫",
                            url=f"https://t.me/shivamdemon"),
                        InlineKeyboardButton(
                            text="✌️𝐁𝐡𝐚𝐢",
                            url=f"https://t.me/alone_boy_xd_01")

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/ab2865486ab04269fb706-ef319dc2d2a2043d24.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🥱 𝐒𝐮𝐩𝐩𝐨𝐫𝐭",
                                url=f"https://t.me/shivamdemon")

                        ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"𝐕𝐢𝐝𝐞𝐨 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧🥺 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("🧐 **𝐖𝐡𝐢𝐜𝐡 𝐒𝐨𝐧𝐠 𝐔 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲??**")
        await lel.edit("☠️ 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...𝐑𝐮𝐤𝐨 𝐧𝐚😘")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("☠️ 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...𝐑𝐮𝐤𝐨 𝐧𝐚😘")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "𝐒𝐨𝐧𝐠 𝐍𝐨𝐭 𝐅𝐨𝐮𝐧𝐝 ☹ ️𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧 𝐖𝐢𝐭𝐡 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠..."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❣️𝐎𝐰𝐧𝐞𝐫",
                            url=f"https://t.me/Shivamdemon"),
                        InlineKeyboardButton(
                            text="✌️𝐁𝐡𝐚𝐢",
                            url=f"https://t.me/Alone_boy_xd_01")

                    ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"𝐕𝐢𝐝𝐞𝐨 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧🥺 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption = f"🔥 **𝐓𝐫𝐚𝐜𝐤 𝐀𝐝𝐝𝐞𝐝 𝐓𝐨 𝐐𝐮𝐞𝐮 »** `{position}`\n\n🎵 **𝐍𝐚𝐦𝐞 :** [{title[:50]}]({url})\n🕛 **𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 :** `{duration}`\n🎧 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {message.from_user.mention}",
        ),
        reply_markup=keyboard
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption = f"🎵**𝐍𝐚𝐦𝐞 :** [{title[:50]}]({url})\n🕛 **𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 :** `{duration}`\n" \
                    + f"🎧 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲 :** {message.from_user.mention}",
        ), )
        os.remove("final.png")
        return await lel.delete()
