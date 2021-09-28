from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_sticker("CAACAgUAAxkBAAEC-i1hUo0LvMtL0C5wqi329nCa4esnHgACTQMAAs10QVSA3vFI6MOLwSEE")
    await message.reply_text(
        f"""** `Hᴇʏᴀ!! Aᴍ` {bn} 🎧,

`I Cᴀɴ Pʟᴀʏ Mᴜsɪᴄ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ Vᴏɪᴄᴇ Cᴀʟʟ. Pᴏᴡᴇʀᴇᴅ Bʏ` [<𝗡𝗶𝘁𝗿𝗶𝗰'𝗫𝗱/>](https://t.me/Sanki_Manager) 💛.

`Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Pʟᴀʏ Mᴜsɪᴄ Fʀᴇᴇʟʏ 🎧`**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🛠 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 🛠", url="https://t.me/Sanki_Manager")
                  ],[
                    InlineKeyboardButton(
                        "💬 Gʀᴏᴜᴘ", url="https://t.me/worldwidechatsXd"
                    ),
                    InlineKeyboardButton(
                        "📣 Cʜᴀɴɴᴇʟ", url="https://t.me/Sanki_BOTs"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "➕ Summon Me ➕", url="https://t.me/MusicXdRobot?startgroup=true"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""**Pʟᴀʏᴇʀ Is Oɴʟɪɴᴇ ✅**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📣 Cʜᴀɴɴᴇʟ", url="https://t.me/Sanki_BOTs")
                ]
            ]
        )
   )


