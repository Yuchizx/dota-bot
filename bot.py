"""
Dota 2 Draft Bot — Telegram Bot
"""

import logging
import os
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

# ─── НАСТРОЙКИ (читаются из переменных окружения Railway) ────────────────────
BOT_TOKEN  = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://example.com")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


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
            "Нажми кнопку ниже 👇"
        ),
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def draft(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⚔️  Открыть Драфтер", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await update.message.reply_text(
        "⚔️ <b>Драфтер Dota 2</b>\n\nВыбирай героев, бань, получай AI-анализ!",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def heroes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("🛡  Герои", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await update.message.reply_text(
        "🛡 <b>Герои Dota 2</b>\n\nБилды, тайминги, порядок скиллов по патчу 7.41c",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("👤  Профиль", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await update.message.reply_text(
        "👤 <b>Профиль игрока</b>\n\nВставь ссылку Steam/Dotabuff — получи винрейт и топ героев.\n\n"
        "⚠️ Профиль Steam должен быть <b>публичным</b>",
        parse_mode="HTML",
        reply_markup=keyboard,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📖 <b>Команды бота</b>\n\n"
        "/start — главное меню\n"
        "/draft — открыть драфтер\n"
        "/heroes — список героев с билдами\n"
        "/profile — твой профиль и статистика\n"
        "/help — эта справка",
        parse_mode="HTML",
    )


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == "help":
        await query.message.reply_text(
            "📖 <b>Команды:</b>\n/start /draft /heroes /profile /help",
            parse_mode="HTML",
        )
    elif query.data == "about":
        await query.message.reply_text(
            "📊 <b>О боте</b>\n\n"
            "🤖 Dota 2 Draft Analyzer\n"
            "🧠 AI: Claude (Anthropic)\n"
            "📊 Статистика: OpenDota API\n"
            "🎮 Патч: 7.41c",
            parse_mode="HTML",
        )


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.web_app_data.data
    await update.message.reply_text(f"✅ Данные из приложения:\n<code>{data}</code>", parse_mode="HTML")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⚔️  Открыть Драфтер", web_app=WebAppInfo(url=WEBAPP_URL))
    ]])
    await update.message.reply_text("Используй /help или открой приложение:", reply_markup=keyboard)


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([
        BotCommand("start",   "🏠 Главное меню"),
        BotCommand("draft",   "⚔️ Открыть драфтер"),
        BotCommand("heroes",  "🛡 Список героев"),
        BotCommand("profile", "👤 Мой профиль"),
        BotCommand("help",    "📖 Помощь"),
    ])
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="⚔️ Драфтер",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )
    logger.info("Bot started!")


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
