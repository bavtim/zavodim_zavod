import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from config import settings

dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(
        text=f"Привет пользователь, {markdown.hbold(message.from_user.full_name)}! Я бот для мониторинга состояния БД на PostgreSQL",
        parse_mode=ParseMode.HTML,
    )

@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an {echo} bot."),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                    "any",
                ),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        # parse_mode=None,
        # parse_mode=ParseMode.MARKDOWN_V2,
    )


@dp.message(Command("code"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        "",
        markdown.markdown_decoration.pre_language(
            # markdown.markdown_decoration.pre(
            markdown.text(
                "print('Hello world!')",
                "\n",
                "def foo():\n    return 'bar'",
                sep="\n",
            ),
            language="python",
        ),
        "And here's some JS:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text(
                "console.log('Hello world!')",
                "\n",
                "function foo() {\n  return 'bar'\n}",
                sep="\n",
            ),
            language="javascript",
        ),
        sep="\n",
    )
    await message.answer(text=text)


@dp.message()
async def echo_message(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Start processing...",
    # )
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Detected message...",
    #     reply_to_message_id=message.message_id,
    # )

    await message.answer(
        text="Wait a second...",
        parse_mode=None,
    )
    if message.text:
        await message.answer(
            text=message.text,
            entities=message.entities,
            parse_mode=None,
        )
        return
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new 🙂")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=settings.bot_token,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())