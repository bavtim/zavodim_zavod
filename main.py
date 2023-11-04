import asyncio
import logging


from aiogram import F
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
import DBcontrol

from config import settings
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    kb = [[types.KeyboardButton(text="Работа с БД")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        text=f"Привет пользователь, {markdown.hbold(message.from_user.full_name)}! Я бот для мониторинга состояния БД на PostgreSQL",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )


@dp.message(Command("reset_kb"))
async def handle_help(message: types.Message):
    kb = [[types.KeyboardButton(text="Работа с БД")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        text=f"Выполнен сброс клавиатуры",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("Я бот мониторинга PostgreSQL"),
        markdown.text(
            markdown.underline("Для начала работы необходимо:"),
            markdown.text("1\) Нажать кнопку",markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("Работа с БД"),
                ),
            ),),
            "2\) Потом заполнить все PostgreSQL, которые нужно мониторить",
            "3\) В случае происшествия будет приходить уведомления с возможным быстрым решением",
            sep="\n"
        ),
        sep="\n",
    )
    await message.answer(
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
@dp.message(F.text == "Получить список БД")
async def echo_message(message: types.Message):

    rawData=DBcontrol.getDBdataUsers(message.chat.id)
    print(rawData)
    str_temp=[]
    for i in range(len(rawData)):
        row=rawData[i]
        s = f"БД № {i}\n"
        s += f"pSQL_dbname: {row['pSQL_dbname']}\n"
        s += f"pSQL_dbuser: {row['pSQL_dbuser']}\n"
        s += f"pSQL_dbpassword: {row['pSQL_dbpassword']}\n"
        s += f"pSQL_dbhost: {row['pSQL_dbhost']}\n"
        str_temp.append(s)


    text = markdown.text(
        markdown.markdown_decoration.quote(f"Количество указанных БД: {len(rawData)}"),
        markdown.text(
            "Список БД пуст" if len(rawData)==0 else "Перечень БД:",
            *str_temp,
            sep="\n"
        ),
            sep="\n"
        )

    await message.answer(
        text=text,
    )
@dp.message(F.text[:len( "Добавить БД")] == "Добавить БД")
async def echo_message(message: types.Message):
    strip_s=message.text[len( "Добавить БД"):].split()
    if len(strip_s)==4:
        try:
            s = f"Аргументы\n"
            s += f"pSQL_dbname: {strip_s[0]}\n"
            s += f"pSQL_dbuser: {strip_s[1]}\n"
            s += f"pSQL_dbpassword: {strip_s[2]}\n"
            s += f"pSQL_dbhost: {strip_s[3]}\n"
            await message.answer(
                text=s,
            )
            DBcontrol.add_user_info(message.chat.id,strip_s[0],strip_s[1],strip_s[2],strip_s[3])
            await message.answer(
                text="Успешно добавлена база данных, ожидайте информацию о подключении",
            )
        except:
            await message.answer(
                text="Произошла ошибка при добавлении",
            )
    else:
        await message.answer(
             text="Введите сообщение в формате:\n\"Добавить БД pSQL_dbname pSQL_dbuser pSQL_dbpassword pSQL_dbhost\",\nНапример, \"Добавить БД testDB TGbot 12345 0.0.0.0:8888\"",
        )


    print( strip_s)
    # rawData=DBcontrol.getDBdataUsers(message.chat.id)
    # str_temp=[]
    # for i in range(len(rawData)):
    #     row=rawData[i]
    #     s = f"{i}\)"
    #     s += f"pSQL_dbname:{row['pSQL_dbname']}\n"
    #     s += f"pSQL_dbuser:{row['pSQL_dbuser']}\n"
    #     s += f"pSQL_dbpassword:{row['pSQL_dbpassword']}\n"
    #     s += f"pSQL_dbhost:{row['pSQL_dbhost']}\n"
    #     str_temp.append(s)
    # text = markdown.text(
    #     markdown.markdown_decoration.quote(f"Количество указанных БД: {len(rawData)}"),
    #     markdown.text(
    #         markdown.underline( "Список БД пуст" if len(rawData)==0 else "Перечень БД:"),
    #         *str_temp,
    #     ),
    #         sep="\n"
    #     )
    #
    # await message.answer(
    #     text=text,
    #     parse_mode=ParseMode.MARKDOWN_V2,
    # )
@dp.message(F.text == "Работа с БД")
async def echo_message(message: types.Message):
    kb = [[types.KeyboardButton(text="Получить список БД")],[types.KeyboardButton(text="Добавить БД")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        text=f"Работа с БД",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@dp.message()
async def echo_message(message: types.Message):
    await message.reply(text="Что-то неизвестное, попробуйте обратиться к администратору - https://t.me/repeared_apple")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.bot_token,)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
