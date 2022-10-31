import yaml
from yaml.loader import SafeLoader
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from stock import get_stock_data


# start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(f'Hi {user.mention_html()}!\n'
                                    f'Get current stock values using symbol\n'
                                    f'Click /help to know more.\n')


# help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('/start - Start the conversation with bot.\n'
                                    '/help  - Describe various commands in bot.\n'
                                    'Use stock symbol to get the latest data of stocks. (AMZN, AAPL)\n'
                                    'Some Indian stock requires ".NS" at end. (TCS.NS)', )


# message handler
async def get_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stock_data = get_stock_data(update.message.text)
    if stock_data == 'timeout':
        await update.message.reply_text('Server Timeout!\n'
                                        'Please try again')
    elif stock_data == 'not-found':
        await update.message.reply_text('Stock Not Found!\n'
                                        'Please check the symbol of the stock')
    else:
        await update.message.reply_text(f'{stock_data[0]}\n'
                                        f'{stock_data[1]}\n'
                                        f'{stock_data[2]}')


if __name__ == '__main__':
    print('Bot is running.')

    # read telegram-bot token from yaml file
    with open('token.yaml', 'r') as file:
        TOKEN = yaml.load(file, Loader=SafeLoader)['token']

    # create application to interact with bot
    application = Application.builder().token(TOKEN).build()

    # add handlers to bot
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_stock))

    # start bot (press CTRL+C to stop)
    application.run_polling()

    print('END')
