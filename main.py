import participants
import daily_job
import timer

from dotenv import load_dotenv
import os

from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

TARGET = {}
TARGET_FILENAME = "target.json"


def main() -> None:
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TOKEN"))
    bot = updater.bot
    job_queue = updater.job_queue

    chat_ids = daily_job.init_daily_job(job_queue)
    for chat_id in chat_ids:
        if chat_id < 0:
            timer.ADMIN_DICT.extend({chat_id: [admin.user.id for admin in bot.get_chat_administrators(chat_id)]})

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", timer.start))
    dispatcher.add_handler(CommandHandler("help", timer.start))
    dispatcher.add_handler(CommandHandler("set", timer.set_timer))
    dispatcher.add_handler(CommandHandler("unset", timer.unset))
    # dispatcher.add_handler(CommandHandler("message", set_message))
    # dispatcher.add_handler(CommandHandler("custom", add_custom_message))
    # dispatcher.add_handler(CommandHandler("view", view_custom_message))
    dispatcher.add_handler(CommandHandler("when", timer.get_next_timing))
    dispatcher.add_handler(CallbackQueryHandler(timer.button))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    participants.init(participants.PARTICIPANTS_FILENAME, participants.PARTICIPANTS_LIST)
    main()
