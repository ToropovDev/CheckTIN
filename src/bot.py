import aiogram

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.config import BOT_TOKEN
from src.ofd import handle_ofd
from src.utils import is_valid_tin

dp = aiogram.Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {message.from_user.full_name}\\!"
        f"\n\n"
        f"Это тестовая версия бота\\! Просто пришли мне сообщение"
        f"с ИНН и я пришлю тебе данные полученные с ofd\\.nalog\\.ru",
    )


async def main() -> None:
    bot = aiogram.Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN_V2,
        ),
    )

    await dp.start_polling(bot)


@dp.message()
async def ofd_handler(message: Message) -> None:
    if is_valid_tin(message.text):
        subject = await handle_ofd(int(message.text))

        if isinstance(subject, str):
            await message.answer(subject)
            return

        answer_text = (
            f"Данные по ИНН {subject.inn}\n\n"
            f"<b>ФИО:</b> {subject.name_ex}\n"
            f"<b>ОГРН:</b> {subject.ogrn}\n"
            f"<b>Код региона</b>: {subject.regioncode}\n\n"
            f"<b>Дата регистрации</b>: {subject.dtregistry.split()[0]}\n"
            f"<b>Тип</b>: {'ИП' if subject.nptype == 'IP' else 'Не ИП (требует изучения)'}\n\n"
            f"<b>Статус</b>: {'АКТИВНЫЙ' if subject.is_active else 'НЕАКТИВНЫЙ'}\n"
        )

        await message.answer(answer_text, parse_mode=ParseMode.HTML)

    else:
        await message.answer("Некорректный ИНН")
