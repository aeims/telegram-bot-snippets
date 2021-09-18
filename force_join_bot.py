# Telegram bot for gently forcing users to join a channel
# By aeims company
# This program is dedicated to the public domain under the CC0 license.

# About:
# Asks a user that started the bot 
# to join the specific channel or will not execute commands.
# Usefull for gathering real and huge members community
# from famous bots to channels. 

# Usage:
# Add your bot to your channel and make it admin with all privilages.
# Make sure to paste bot token and channel username or id to the code where needed.
# run the program and send /start or /help to bot.
# Bot will check the channel to see if you are a member of channel or not.

# User if member: will excute the start or help command sent to chat.
# If not member: stops all handlers for that user and 
# will send a message asking the user to join the channel.


from telegram import Update
from telegram.ext import (
    Updater, 
    CallbackContext, 
    CommandHandler, 
    TypeHandler, 
    DispatcherHandlerStop,
)

# Get your bot token from @botfather and paste it here.
BOT_TOKEN = "123456789:ABCDEFGHaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Make a new public channel and paste username of channel here.
CHANNEL_USERNAME = '@'


def chk_usr_in_chnl(update:Update, context:CallbackContext) -> None:
    if update.effective_user:
        chnl_member = context.bot.get_chat_member(CHANNEL_USERNAME, update.effective_user.id)
        if not chnl_member.status == 'member':
            update.effective_message.reply_text(
                f'Pls first join to this {CHANNEL_USERNAME} channel to be able to use my commands 🙌'
            )
            context.user_data[update.effective_user.id] = 'for_check_status'
            raise DispatcherHandlerStop()


def start(update:Update, context:CallbackContext) -> None:
    update.effective_message.reply_text(
        "You can use this command cause you are in my channel 🍕"
    )


def help(update:Update, context:CallbackContext) -> None:
    update.effective_message.reply_text(
        "Another command to test Bot's channel checking 👌"
    )


def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(TypeHandler(Update, chk_usr_in_chnl), group=-1)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()

if __name__ == '__main__':
    main()
