# Telegram bot for gently forcing users to join a channel - version 2
# By aeims company
# This program is dedicated to the public domain under the CC0 license.

# IMPORTANT WARNING: DO NOT CHANGE HANDLERS ORDER OR THE BOT WILL NOT WORK PROPERLY!
# IMPORTANT: MAKE SURE BOT IS ADMIN IN THE CHANNEL WITH ALL PRIVILAGES.

# About:
# Asks a user that started the bot 
# to join the specific channel or will not execute commands.
# Usefull for gathering real and huge members community
# from famous bots to channels. 

# Usage:
# Add your bot to your channel and make it admin with all privilages.
# Make sure to paste bot token and channel username to the code where needed.
# run the program and send /start or /help to bot.
# Bot will check the channel to see if you are a member of channel or not.

# User if member: will excute the start or help command sent to chat.
# If not member: stops all handlers for that user and 
# will send a message asking the user to join the channel.

# Diffrence with version 1:
# User if joined: will send a message to user who joined via bot to inform the accessibility to commands of bot.
# If left: will send a message to inform the unaccessibility to use of commands 
# cuase of lefting channel.


from telegram import Update
from telegram.ext import (
    Updater, 
    CallbackContext, 
    CommandHandler, 
    ChatMemberHandler,
    TypeHandler, 
    DispatcherHandlerStop,
)

# Get your bot token from @botfather and paste it here.
BOT_TOKEN = "123456789:ABCDEFGHaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Make a new public channel and paste username of channel here.
CHANNEL_USERNAME = '@'


def check_status(update:Update, context:CallbackContext):
    member = update.chat_member.new_chat_member
    usr_id = member.user.id
    if usr_id in context.user_data:
        if member.status == 'member':
            text = "Thanks for joining 🖤 now you can use the commands."
        elif member.status == 'left':
            text = "You have left the channel 😓 you can't use my commands anymore.\n"
            f"unless... you join again {CHANNEL_USERNAME}"
        try:
            context.bot.send_message(
                usr_id,
                text,
            )
        except:
            pass


def chk_usr_in_chnl(update:Update, context:CallbackContext) -> None:
    if update.effective_user:
        usr_id = update.effective_user.id
        chnl_member = context.bot.get_chat_member(CHANNEL_USERNAME, usr_id)
        if not chnl_member or chnl_member.status == 'left':
            update.effective_message.reply_text(
                f'Pls first join to this {CHANNEL_USERNAME} channel to be able to use my commands 🙌'
            )
            context.user_data[usr_id] = 'for_check_status'
            raise DispatcherHandlerStop()
            

def start(update:Update, context:CallbackContext) -> None:
    update.effective_message.reply_text(
        'You can use this command cause you are in my channel 🍕'
    )


def help(update:Update, context:CallbackContext) -> None:
    update.effective_message.reply_text(
        'Another command to test Bot\'s channel checking 👌'
    )


def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(ChatMemberHandler(check_status, ChatMemberHandler.CHAT_MEMBER), group=-1)
    dispatcher.add_handler(TypeHandler(Update, chk_usr_in_chnl), group=-1)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()

if __name__ == '__main__':
    main()
