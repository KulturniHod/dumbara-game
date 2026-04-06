import asyncio
import random
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.storage.memory import MemoryStorage

# ========== ТОКЕН ИЗ ПЕРЕМЕННОЙ ОКРУЖЕНИЯ ==========
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("❌ Ошибка: переменная TELEGRAM_BOT_TOKEN не найдена!")
    print("На сервере добавь Environment Variable: TELEGRAM_BOT_TOKEN = твой_токен")
    exit(1)

# ========== ИНИЦИАЛИЗАЦИЯ БОТА ==========
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Ссылка на твой Mini App (замени на свою, если нужно)
MINI_APP_URL = "https://KulturniHod.github.io/dumbara-game/"

# ========== КЛАВИАТУРЫ ==========
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Открыть игру", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton(text="🎲 Бросить кубик", callback_data="roll_dice")],
        [InlineKeyboardButton(text="🗺️ Карта", callback_data="map_show")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory_show")],
        [InlineKeyboardButton(text="🔄 Перезапустить игру", callback_data="reset_game")]
    ])

# ========== КОМАНДЫ ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🏠 *Старинный дом*\n\n"
        "Ты находишься перед большим деревянным сундуком.\n"
        "На крышке выгравирована *думбыра* — древний инструмент сказителей.\n\n"
        "🎮 *Нажми «Открыть игру»*, чтобы запустить визуальную новеллу,\n"
        "настроить струны и открыть проход в подвал!\n\n"
        "📖 *Команды:*\n"
        "• /start — начать игру\n"
        "• /roll — бросить кубик\n"
        "• /map — показать карту\n"
        "• /inventory — инвентарь\n"
        "• /reset — перезапустить",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("roll"))
async def cmd_roll(message: types.Message):
    dice = random.randint(1, 6)
    await message.answer(f"🎲 Ты бросил кубик! Выпало: *{dice}*", parse_mode="Markdown")

@dp.message(Command("map"))
async def cmd_map(message: types.Message):
    await message.answer(
        "🗺️ *Карта*\n\n"
        "📍 *Текущая позиция:* Комната с сундуком\n\n"
        "🏠 *Старый дом*\n"
        "├── 🚪 Вход\n"
        "├── 📦 *Комната с сундуком* ← вы здесь\n"
        "└── 🚧 Запертый подвал (нужно открыть думбырой)",
        parse_mode="Markdown"
    )

@dp.message(Command("inventory"))
async def cmd_inventory(message: types.Message):
    await message.answer(
        "🎒 *Инвентарь*\n\n"
        "📖 *Дневник сэсэна*\n"
        "   — Страница 12: о трёх струнах\n"
        "   — Страница 17: о настройке тона\n"
        "   — Страница 24: о хамаках\n\n"
        "🎸 *Думбыра*\n"
        "   — Старинный инструмент\n"
        "   — Три струны (батыр, конь, ветер)",
        parse_mode="Markdown"
    )

@dp.message(Command("reset"))
async def cmd_reset(message: types.Message):
    await message.answer(
        "🔄 *Игра перезапущена!*\n\n"
        "Напиши /start, чтобы начать заново.\n"
        "Или нажми «Открыть игру», чтобы продолжить.",
        parse_mode="Markdown"
    )

# ========== ОБРАБОТЧИКИ КНОПОК ==========
@dp.callback_query(lambda c: c.data == "roll_dice")
async def roll_dice_callback(callback: types.CallbackQuery):
    dice = random.randint(1, 6)
    await callback.message.answer(f"🎲 Тебе выпало: *{dice}*", parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "map_show")
async def map_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "🗺️ *Карта*\n\n📍 Комната с сундуком\n🚪 Запертый подвал",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "inventory_show")
async def inventory_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "🎒 *Инвентарь*\n\n📖 Дневник сэсэна\n🎸 Думбыра",
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(lambda c: c.data == "reset_game")
async def reset_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        "🔄 *Игра перезапущена!*\n\nНапиши /start или нажми «Открыть игру».",
        parse_mode="Markdown"
    )
    await callback.answer()

# ========== ЗАПУСК ==========
async def main():
    print("✅ Бот запущен и работает 24/7!")
    print(f"🌐 Mini App доступен по ссылке: {MINI_APP_URL}")
    print("🤖 Ожидание сообщений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())