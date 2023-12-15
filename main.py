import asyncio
import logging
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from tokenbot import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

data = pd.read_excel("https://drive.google.com/uc?export=download&id=1Bo5Oili5dAvWDSzAZXjzgjS71IrmLWun")
groups = data["Группа"]
groups_unique = groups.unique()

def convert_symbols_to_string(symbols):
    return ', '.join(map(str, symbols))

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text=f"Здравствуйте, {message.from_user.first_name}. Укажите группу, которую нужно найти.")

@dp.message(Command("list"))
async def handle_help(message: types.Message):
    text = (f"Вот список групп, по которым можно получить информацию: {convert_symbols_to_string(groups_unique)}")
    await message.answer(text=text)

@dp.message()
async def choice(message: types.Message):
    if message.text in groups.values:
        all_marks = data["Оценка"]
        group_marks = data[groups == message.text].shape[0]
        students_count = data[groups == message.text]["Личный номер студента"]
        unique_student_count = students_count.unique()
        unique_control_level = data["Уровень контроля"].unique()
        unique_years = sorted(data["Год"].unique())
        output_string = (f"В исходном датасете содержалось {all_marks.size} оценок, из них {group_marks} оценок относятся к группе {message.text}\n"
        f"В датасете находятся оценки {unique_student_count.size} студентов со следующими личными номерами {message.text}: {convert_symbols_to_string(unique_student_count)}\n"
        f"Используемые формы контроля: {convert_symbols_to_string(unique_control_level)}\n"
        f"Данные представлены по следующим учебным годам: {convert_symbols_to_string(sorted(unique_years))}")
        await message.reply(output_string)
    else:
        await message.reply("В файле такой группы нет")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())