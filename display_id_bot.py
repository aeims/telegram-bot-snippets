# Telegram bot for displaying id of user or chat
# By aeims company
# This program is dedicated to the public domain under the CC0 license.

# Use /id in private chat to get your id in telegram
# for chats sometimes users need to call command with bot's
# username cause of privacy settings.
# In chats get id like this -> /id@usernamebot
# Works just fine with replied or forwarded messages as well.
# You can pass arguments along with the command /id <12345>
# as 12345 is id of someone unknown, bot will give name and username instantly.
# or if there is no message from target user call the command and mention him/her
# /id <mention> to display id name and username.
# geting id with username is not possible with bot api 
# hence this works for text_mentions only.


from telegram import Update
from telegram.utils.helpers import mention_html as mention
from telegram.ext import (
    Updater, 
    CallbackContext, 
    CommandHandler, 
)

# Create bot and get your token from telegram @botfather 
BOT_TOKEN = ""


def id_disply(update: Update, context: CallbackContext):
    message = update.effective_message
    args = context.args
    if args and args[0].isdecimal() and len(args[0]) > 7:
        user = context.bot.get_chat_member(message.chat_id, int(args[0])).user
    elif entity := message.parse_entities('text_mention'):
        user = tuple(entity.keys())[0].user
    elif message.reply_to_message:
        if fwd_usr := message.reply_to_message.forward_from:
            user = fwd_usr
        else:
            user = message.reply_to_message.from_user
    else:
        user = message.chat
    try:
        message.reply_html(
            f'{mention(user.id, user.full_name if user.full_name != None else user.title)}'
            f'\nID: <code>{user.id}</code>'
            f'\n{("@"+user.username) if user.username != None else ""}'
        )
    except:
        message.reply_text("User not found.")


def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('id', id_disply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
