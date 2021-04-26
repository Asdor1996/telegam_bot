from aiogram import Bot, Dispatcher, executor, types
import config
import aiogram.utils.markdown as fmt
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.filters import Text
import random
import asyncio
import datetime

bot = Bot(token=config.token)
dp = Dispatcher(bot)

photo = "https://www.fotoprizer.ru/img_inf/st_159.jpg"


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply("Привет друг")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Вот что я пока умею:\n /start \n /help")


@dp.message_handler(commands="but")
async def command_but(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Это первая кнопка", "А это вторая"]
    keyboard.add(*buttons)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить номер", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    await message.answer("Тут например вопрос", reply_markup=keyboard)


@dp.message_handler(commands="dice")
async def command_dice(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Бросить кубик " + emojize(":game_die: "),
                                            callback_data="rand"))
    await message.answer("Вы можете бросить кубик:", reply_markup=keyboard)


@dp.callback_query_handler(text="rand")
async def send_random_value(call: types.CallbackQuery):
    k = str(random.randint(1, 10))
    await call.answer(text="Бросаем...!", show_alert=True)
    await asyncio.sleep(3)
    await call.message.answer("Вам выпало число " + k)


def get_keyboard():
    buttons = [types.InlineKeyboardButton(text="обновить", callback_data="dt_refr"),
               types.InlineKeyboardButton(text="закрыть", callback_data="dt_fin")]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


async def update_datetime(message: types.Message):
    time = datetime.datetime.now()
    await message.edit_text("Дата и время: " + str(time), reply_markup=get_keyboard())


@dp.message_handler(commands="date")
async def command_datetime(message: types.Message):
    time = datetime.datetime.now()
    await message.answer("Дата и время: " + str(time), reply_markup=get_keyboard())


@dp.callback_query_handler(Text(startswith="dt_"))
async def callback_datetime(call: types.CallbackQuery):
    if call.data == "dt_refr":
        await update_datetime(call.message)
    elif call.data == "dt_fin":
        await call.message.edit_text("если еще надумайте глянуть дату пишите /date")
    await call.answer()


@dp.message_handler(commands="inline")
async def command_inline(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Ютубчик", url="https://www.youtube.com/"),
        types.InlineKeyboardButton(text="Телеграмчик", url="tg://resolve?domain=telegram")
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer("Это кнопки ссылочки", reply_markup=keyboard)


@dp.message_handler(Text(equals="Это первая кнопка"))
async def first_but(message: types.Message):
    await message.reply("Ты нажал 1 кнопку!")


@dp.message_handler(lambda message: message.text == "А это вторая")
async def second_but(message: types.Message):
    await message.reply("Теперь нажал втрорую", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['text'])
async def text_message(msg: types.Message):
    if msg.text and not msg.text.startswith("/"):
        if msg.text.lower() == "привет":
            await bot.send_message(msg.from_user.id, "Привет!")
        elif msg.text.lower() == "как дела?":
            await bot.send_message(msg.from_user.id, "Хорошо! А у тебя как?")
        elif msg.text.lower() == "как тебя зовут?" or msg.text.lower() == "как тебя зовут":
            await bot.send_message(msg.from_user.id, "quazun")
        elif msg.text.lower() == "фото":
            await bot.send_photo(msg.from_user.id, photo)
        elif msg.text.lower() == "текст":
            await msg.answer("обычный, *жирный* , _курсив_ , `ошибка`", parse_mode="Markdown")
        elif msg.text.lower() == "эмодзи":
            await msg.reply(emojize(":fire:") + emojize(":ghost:"))
        elif msg.text.lower() == "кто твой папочка" or msg.text.lower() == "кто твой папочка?":
            button = types.InlineKeyboardButton(text="Папочка всех ботов", url="tg://resolve?domain=quazun")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(button)
            await msg.answer("Мой батька:", reply_markup=keyboard)
        elif msg.text.lower() == "стикер":
            await bot.send_sticker(msg.from_user.id,
                                   "CAACAgQAAxkBAAIBL2BXOUXucU8oG9GXxB28tyd5TospAAKFAwACyt9oBeyJQn52NhMoHgQ")
        elif msg.text.lower() == "текст2":
            await msg.answer(fmt.text(fmt.text(fmt.hunderline("подчеркнутый")),
                                      fmt.text(fmt.hstrikethrough("зачеркнутый")),
                                      sep="\n"), parse_mode="HTML")
        else:
            await bot.send_message(msg.from_user.id, msg.from_user.first_name + ", я тебя непонял")
    else:
        await bot.send_message(msg.from_user.id,
                               "`У меня нет такой команды`", parse_mode="Markdown")


@dp.message_handler(content_types=['sticker'])
async def sticker_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.sticker.file_id)
    await bot.send_message(msg.from_user.id, msg.sticker.emoji)


@dp.message_handler(content_types=['voice'])
async def voice_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Я не умею пока слушать голосовые, но по айди отправить могу:")
    voiceID = str(msg.voice.file_id)
    await bot.send_voice(msg.from_user.id, voiceID)


@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def animation_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Это гифка!")
    await msg.reply_animation(msg.animation.file_id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
