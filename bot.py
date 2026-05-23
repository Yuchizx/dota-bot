"""
Dota 2 Draft Bot — Telegram Bot
Запускает Mini App + отвечает на команды
"""

import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    MenuButtonWebApp,
    BotCommand,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ─── НАСТРОЙКИ ───────────────────────────────────────────────────────────────
BOT_TOKEN  = "ВАШ_ТОКЕН_ОТ_BOTFATHER"   # Замени на свой токен
WEBAPP_URL = "https://ВАШ_САЙТ.vercel.app"  # URL задеплоенного React-приложения

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─── /start ──────────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "⚔️  Открыть Драфтер",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )],
        [
            InlineKeyboardButton("📖 Помощь", callback_data="help"),
            InlineKeyboardButton("📊 О боте", callback_data="about"),
        ],
    ])
    await update.message.reply_photo(
        photo="https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/home/dota2-social.jpg",
        caption=(
            f"👋 Привет, <b>{user.first_name}</b>!\n\n"
            "⚔️ <b>Dota 2 Draft Analyzer</b>\n\n"
            "Я помогу тебе:\n"
            "• Составить драфт 5v5\n"
            "• Проанализировать его с помощью AI\n"
            "• Найти контрпики и синергии\n"
            "• Посмотреть билды и тайминги предметов\n"
            "• Отслеживать свой профиль и винрейт\n\n"
            "Нажми кнопку ниже, чтобы открыть приложение 👇"
        ),
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ─── /draft ──────────────────────────────────────────────────────────────────
async def draft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "⚔️  Открыть Драфтер",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])
    await update.message.reply_text(
        "⚔️ <b>Драфтер Dota 2</b>\n\nВыбирай героев, бань, получай AI-анализ и рекомендации!",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ─── /heroes ─────────────────────────────────────────────────────────────────
async def heroes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "🛡  Открыть список героев",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}#hero")
        )
    ]])
    await update.message.reply_text(
        "🛡 <b>Герои Dota 2</b>\n\n"
        "• Полный список с иконками и винрейтами\n"
        "• Билды предметов по патчу 7.41c\n"
        "• Тайминги: когда покупать ключевые предметы\n"
        "• Порядок прокачки скиллов\n"
        "• Добавляй в избранное ⭐",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ─── /profile ────────────────────────────────────────────────────────────────
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "👤  Открыть профиль",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}#profile")
        )
    ]])
    await update.message.reply_text(
        "👤 <b>Профиль игрока</b>\n\n"
        "Вставь ссылку на свой Steam или Dotabuff профиль и получи:\n"
        "• Свой MMR и винрейт\n"
        "• Топ героев с процентом побед\n"
        "• Быстрый доступ к билдам своих любимых героев\n\n"
        "⚠️ Профиль Steam должен быть <b>публичным</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


# ─── /help ───────────────────────────────────────────────────────────────────
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📖 <b>Команды бота</b>\n\n"
        "/start — главное меню\n"
        "/draft — открыть драфтер\n"
        "/heroes — список героев с билдами\n"
        "/profile — твой профиль и статистика\n"
        "/help — эта справка\n\n"
        "💡 <b>Как пользоваться драфтером:</b>\n"
        "1. Нажми на слот Сил Света или Тьмы\n"
        "2. Выбери героя из списка\n"
        "3. Забань нужных героев\n"
        "4. Нажми «Анализировать драфт»\n"
        "5. Получи AI-рекомендации по пикам и предметам",
        parse_mode="HTML",
    )


# ─── CALLBACK BUTTONS ────────────────────────────────────────────────────────
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.message.reply_text(
            "📖 <b>Команды бота</b>\n\n"
            "/start — главное меню\n"
            "/draft — открыть драфтер\n"
            "/heroes — список героев\n"
            "/profile — профиль\n"
            "/help — справка",
            parse_mode="HTML",
        )
    elif query.data == "about":
        await query.message.reply_text(
            "📊 <b>О боте</b>\n\n"
            "🤖 Dota 2 Draft Analyzer\n"
            "📦 Версия: 1.0\n"
            "🧠 AI-анализ: Claude (Anthropic)\n"
            "📊 Статистика: OpenDota API\n"
            "🎮 Патч: 7.41c\n\n"
            "Создан для помощи в драфте и изучении героев Dota 2.",
            parse_mode="HTML",
        )


# ─── WEBAPP DATA (получаем данные из Mini App если нужно) ────────────────────
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.web_app_data.data
    logger.info(f"WebApp data received: {data}")
    # Здесь можно обрабатывать данные отправленные из Mini App
    await update.message.reply_text(
        f"✅ Данные получены из приложения:\n<code>{data}</code>",
        parse_mode="HTML",
    )


# ─── НЕИЗВЕСТНЫЕ КОМАНДЫ ─────────────────────────────────────────────────────
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⚔️  Открыть Драфтер", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await update.message.reply_text(
        "Не понимаю эту команду. Используй /help или открой приложение:",
        reply_markup=keyboard,
    )


# ─── MAIN ────────────────────────────────────────────────────────────────────
async def post_init(application: Application) -> None:
    """Устанавливает команды и кнопку меню при старте бота"""
    await application.bot.set_my_commands([
        BotCommand("start",   "🏠 Главное меню"),
        BotCommand("draft",   "⚔️ Открыть драфтер"),
        BotCommand("heroes",  "🛡 Список героев"),
        BotCommand("profile", "👤 Мой профиль"),
        BotCommand("help",    "📖 Помощь"),
    ])
    # Кнопка меню (кнопка рядом с полем ввода) открывает Mini App
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="⚔️ Драфтер",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )
    logger.info("Bot started and configured!")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("draft",   draft))
    app.add_handler(CommandHandler("heroes",  heroes))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("help",    help_cmd))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Starting bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
