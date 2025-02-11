import asyncio
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"20.x version of this example, visit https://docs.python-telegram-bot.org/en/v20.0/examples.html"
    )

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from exchange_api import MOEXAPI
from utils import format_currency_message
from logger import logger

class CurrencyBot:
    def __init__(self):
        self.moex_api = MOEXAPI()
        logger.info("CurrencyBot initialized")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /start command"""
        try:
            welcome_message = (
                "Welcome to Currency Exchange Rate Bot!\n\n"
                "Available commands:\n"
                "/start - Start the bot\n"
                "/stop - Stop the bot\n"
                "/usdrate - Get USD rate\n"
                "/eurrate - Get EUR rate\n"
                "/cnyrate - Get CNY rate\n"
                "/jpyrate - Get JPY rate\n"
                "/bynrate - Get BYN rate\n"
                "/gbprate - Get GBP rate\n"
                "/allrates - Get all rates\n"
                "/convert - Convert currencies (e.g., /convert 100 USD to RUB)"
            )
            await update.message.reply_text(welcome_message)
            logger.info(f"New user started the bot: {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in start command: {str(e)}")
            await update.message.reply_text("An error occurred. Please try again.")

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle the /stop command"""
        try:
            await update.message.reply_text("Bot stopped. Use /start to begin again.")
            logger.info(f"User stopped the bot: {update.effective_user.id}")
        except Exception as e:
            logger.error(f"Error in stop command: {str(e)}")
            await update.message.reply_text("An error occurred. Please try again.")

    async def get_single_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE, currency: str) -> None:
        """Handle single currency rate requests"""
        try:
            logger.info(f"Fetching {currency} rate...")
            rates = self.moex_api.get_exchange_rates()
            logger.debug(f"Received rates: {rates}")

            if rates and rates.get(currency):
                message = format_currency_message({currency: rates[currency]})
            else:
                message = f"Sorry, unable to fetch {currency} rate at the moment."

            await update.message.reply_text(message)
            logger.info(f"User {update.effective_user.id} requested {currency} rate")
        except Exception as e:
            logger.error(f"Error fetching {currency} rate: {str(e)}")
            await update.message.reply_text("An error occurred. Please try again.")

    async def get_all_rates(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle all rates request"""
        try:
            logger.info("Fetching all rates...")
            rates = self.moex_api.get_exchange_rates()
            logger.debug(f"Received rates: {rates}")

            message = format_currency_message(rates)
            await update.message.reply_text(message)
            logger.info(f"User {update.effective_user.id} requested all rates")
        except Exception as e:
            logger.error(f"Error fetching all rates: {str(e)}")
            await update.message.reply_text("An error occurred. Please try again.")

    async def usd_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'USD')

    async def eur_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'EUR')

    async def cny_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'CNY')

    async def jpy_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'JPY')

    async def byn_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'BYN')

    async def gbp_rate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.get_single_rate(update, context, 'GBP')

    async def convert(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Convert between currencies using format: /convert 100 USD to RUB"""
        try:
            args = context.args
            if len(args) != 4 or args[2].lower() != 'to':
                await update.message.reply_text("Usage: /convert 100 USD to RUB")
                return

            amount = float(args[0])
            from_currency = args[1].upper()
            to_currency = args[3].upper()

            if to_currency != 'RUB' and from_currency != 'RUB':
                await update.message.reply_text("One currency must be RUB")
                return

            rates = self.moex_api.get_exchange_rates()
            
            if from_currency == 'RUB':
                if to_currency not in rates:
                    await update.message.reply_text(f"Cannot convert to {to_currency}")
                    return
                result = amount / rates[to_currency]
                await update.message.reply_text(f"{amount:.2f} RUB = {result:.2f} {to_currency}")
            else:
                if from_currency not in rates:
                    await update.message.reply_text(f"Cannot convert from {from_currency}")
                    return
                result = amount * rates[from_currency]
                await update.message.reply_text(f"{amount:.2f} {from_currency} = {result:.2f} RUB")

        except (ValueError, KeyError) as e:
            logger.error(f"Conversion error: {str(e)}")
            await update.message.reply_text("Invalid currency or amount")

def main() -> None:
    """Main function to run the bot"""
    try:
        logger.info("Initializing bot...")
        logger.debug(f"Bot token present: {bool(TELEGRAM_BOT_TOKEN)}")

        # Create the Application and pass it your bot's token
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Create bot instance
        bot = CurrencyBot()

        # Add command handlers
        logger.info("Setting up command handlers...")
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CommandHandler("stop", bot.stop))
        application.add_handler(CommandHandler("usdrate", bot.usd_rate))
        application.add_handler(CommandHandler("eurrate", bot.eur_rate))
        application.add_handler(CommandHandler("cnyrate", bot.cny_rate))
        application.add_handler(CommandHandler("jpyrate", bot.jpy_rate))
        application.add_handler(CommandHandler("bynrate", bot.byn_rate))
        application.add_handler(CommandHandler("gbprate", bot.gbp_rate))
        application.add_handler(CommandHandler("allrates", bot.get_all_rates))
        application.add_handler(CommandHandler("convert", bot.convert))

        # Start the bot
        logger.info("Starting bot polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
        raise

if __name__ == '__main__':
    main()