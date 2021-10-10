from asyncio.queues import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message
from callsmusic import callsmusic

from config import BOT_NAME as BN
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("𝐍𝐨 𝐀𝐧𝐲 𝐒𝐨𝐧𝐠 𝐢𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠...")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("▶️ 𝐏𝐚𝐮𝐬𝐞𝐝!!")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):a
        await message.reply_text("𝐍𝐨 𝐀𝐧𝐲 𝐒𝐨𝐧𝐠 𝐈𝐬 𝐏𝐚𝐮𝐬𝐞𝐝...")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("⏸ 𝐑𝐞𝐬𝐮𝐦𝐞𝐝!!")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("𝐍𝐨 𝐀𝐧𝐲 𝐒𝐨𝐧𝐠 𝐈𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠...")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("❌ 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠 𝐒𝐭𝐨𝐩𝐩𝐞𝐝!!")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐈𝐬 𝐒𝐭𝐫𝐞𝐚𝐦𝐢𝐧𝐠!!")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(
                chat_id, queues.get(chat_id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"⫸ 𝐒𝐤𝐢𝐩𝐩𝐞𝐝 : **{skip[0]}**\n⫸ 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 : **{qeue[0][0]}**")
