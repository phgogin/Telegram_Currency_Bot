import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from exchange_api import MOEXAPI
from utils import format_currency_message
from logger import logger

class CurrencyBot:
    def __init__(self):
        self.moex_api = MOEXAPI()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command"""
        welcome_message = (
            "Welcome to Currency Exchange Rate Bot!\n\n"
            "Available commands:\n"
            "/start - Start the bot\n"
            "/stop - Stop the bot\n"
            "/usdrate - Get USD rate\n"
            "/eurrate - Get EUR rate\n"
            "/cnyrate - Get CNY rate\n"
            "/allrates - Get all rates"
        )
        await update.message.reply_text(welcome_message)
        logger.info(f"New user started the bot: {update.effective_user.id}")

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /stop command"""
        await update.message.reply_text("Bot stopped. Use /start to begin again.")
        logger.info(f"User stopped the bot: {update.effective_user.id}")

    async def get_single_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE, currency: str) -> None:
        """Handle single currency rate requests"""
        rates = self.moex_api.get_exchange_rates()
        if rates and rates.get(currency):
            message = format_currency_message({currency: rates[currency]})
        else:
            message = f"Sorry, unable to fetch {currency} rate at the moment."
        await update.message.reply_text(message)
        logger.info(f"User {update.effective_user.id} requested {currency} rate")

    async def get_all_rates(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle all rates request"""
        rates = self.moex_api.get_exchange_rates()
        message = format_currency_message(rates)
        await update.message.reply_text(message)
        logger.info(f"User {update.effective_user.id} requested all rates")

    async def usd_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'USD')

    async def eur_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'EUR')

    async def cny_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'CNY')

async def main():
    """Main function to run the bot"""
    try:
        bot = CurrencyBot()
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CommandHandler("stop", bot.stop))
        application.add_handler(CommandHandler("usdrate", bot.usd_rate))
        application.add_handler(CommandHandler("eurrate", bot.eur_rate))
        application.add_handler(CommandHandler("cnyrate", bot.cny_rate))
        application.add_handler(CommandHandler("allrates", bot.get_all_rates))

        # Start the bot
        logger.info("Starting bot...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(main())