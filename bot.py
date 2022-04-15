from aiogram import executor
from aiogram import types
from dispatcher import dp
from aiogram.dispatcher import FSMContext


from Bothelp import BotDB,Dialog
BotDB = BotDB('Your DB')

@dp.message_handler(commands = "start",)
async def start(message: types.Message):
    await message.reply("""Добро пожаловать!Вот, что я умею:
    
/check_url - Проверяю вредоносность ссылки
/add_url - Добавляю ссылку в базу данных

Начнем?""")


@dp.message_handler(commands='check_url')
async def start(message: types.Message):
    await message.reply("Отправьте сслыку")
    await Dialog.S1.set()


@dp.message_handler(state=Dialog.S1)
async def check_url(message: types.Message,state:FSMContext):
    f=True
    if (BotDB.is_url(message.text)):
        if (not BotDB.url(message.text)):
            if (BotDB.classification(message.text)):
                await message.answer('Скорее всего это не фишинговая ссылка, но будте бдительны!')
                BotDB.add_url(message.text, 1)
            else:
                await message.answer('Возможно это фишинговая ссылка. Будьте бдительны')
                BotDB.add_url(message.text, 0)
        else:
            if (not BotDB.label(message.text)):
                await message.answer('Это  фишинговая ссылка')
            else:
                await message.answer('Это  не фишинговая ссылка')
    else:
        await message.answer('Это не ссылка.Попробуйте еще раз')
        f=False
    if f:
        await state.finish()



@dp.message_handler(commands='add_url',)
async def start(message: types.Message):
    await message.reply("""Отправьте сслыку и ярлык(0-плохая ссылка,1-хорошая ссылка) через пробел:
"ссылка" "ярлык" """)
    await Dialog.S2.set()


@dp.message_handler(state=Dialog.S2)
async def add_url(message: types.Message, state:FSMContext):
    f=True
    result = message.text.split()
    if (BotDB.is_url(result[0])):
        if (not BotDB.url(result[0])):
            BotDB.add_url(result[0], result[1])
            await message.answer("Ссылка успешно добавлена")
        else:
            await message.answer("Такая ссылка уже есть")
    else:
        await message.answer('Это не ссылка.Попробуйте еще раз')
        f=False
    if f:
        await state.finish()

@dp.message_handler()
async def start(message: types.Message):
    await message.answer("Выберете команду!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)