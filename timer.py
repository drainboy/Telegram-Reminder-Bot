import logging
import participants
import daily_job
import util

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

MESSAGE = ["Where's my hair update?!?"]
ADMIN_DICT = {}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Adds user to the participation list"""
    chat_id = update.message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    participants.add_to_list(chat_id, first_name, last_name, participants.PARTICIPANTS_LIST)
    update.message.reply_text('Welcome to the gang')
    participants.update_file(participants.PARTICIPANTS_FILENAME, participants.PARTICIPANTS_LIST)


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    keyboard = [[InlineKeyboardButton("pass the baton", callback_data="pass_the_baton")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    for chat_id in participants.PARTICIPANTS_LIST[0]:
        context.bot.send_message(chat_id, text="hey! it's your turn to remind {target name} to {action}",
                                 reply_markup=reply_markup)


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    try:
        chat_id = update.message.chat_id
        h, m, s = [int(number) for number in context.args[0].split(":")]
        keyboard = [[InlineKeyboardButton("yes", callback_data=f"{h}:{m}:{s}:{chat_id}"),
                     InlineKeyboardButton("no", callback_data='no')]]

        if h < 0 or m < 0 or s < 0:
            update.message.reply_text("Sorry we can not go back to future!")
            return

        old_job = context.job_queue.get_jobs_by_name(f"{chat_id}_{h:02d}{m:02d}{s:02d}")
        if old_job:
            old_hour, old_minute, old_second, old_chat_id = list(old_job[0].context.values())
            old_timing = f"{old_hour:02d}:{old_minute:02d}:{old_second:02d}"
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"There's an existing timer for {old_timing}\nWould you like to replace it?",
                                      reply_markup=reply_markup)
        else:
            daily_job.create_daily_job(context.job_queue, h, m, s, chat_id)
            text = f"Daily Timer successfully set for {h:02d}:{m:02d}:{s:02d}!"
            update.message.reply_text(text)

        if update.message.chat.type == "group":
            util.update_admin_list(chat_id, context.bot, ADMIN_DICT)

    except (IndexError, ValueError) as error:
        print(error)
        update.message.reply_text('Usage: /set HH:MM:SS')


def button(update: Update, context: CallbackContext) -> None:
    """Button CallBackHandler"""
    query = update.callback_query
    print(query)
    chat_id = query.message.chat_id
    query.answer()

    if ":" in query.data:
        h, m, s, chat_id = [int(x) for x in query.data.split(":")]

        daily_job.remove_job_if_exists(str(chat_id) + "daily", context)
        daily_job.create_daily_job(context.job_queue, h, m, s, chat_id)
        query.edit_message_text(f"Timer set to {h:02d}:{m:02d}:{s:02d}")

    elif query.data == "no":
        old_job = context.job_queue.get_jobs_by_name(str(chat_id) + "daily")
        old_hour, old_minute, old_second, chat_id = list(old_job[0].context.values())
        old_timing = f"{old_hour:02d}:{old_minute:02d}:{old_second:02d}"
        query.edit_message_text(f"Timer will continue at {old_timing}")

    elif query.data == "pass_the_baton":
        participants.pass_baton(chat_id, participants.PARTICIPANTS_LIST, participants.PASSED_BATON_LIST)
        context.bot.send_message(chat_id=chat_id, text=f"{participants.PARTICIPANTS_LIST=}\n{participants.PASSED_BATON_LIST=}")


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = daily_job.remove_job_if_exists(str(chat_id) + "daily", context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def get_next_timing(update: Update, context: CallbackContext):
    """Sends a message with next timing to chat if job exists"""
    chat_id = update.message.chat_id
    job_q = context.job_queue.get_jobs_by_name(str(chat_id) + "daily")
    if job_q:
        job = job_q[0]
        next_timing = job.next_t
        text = f"I alert you at {next_timing.hour}:{next_timing.minute}:{next_timing.second}"
        context.bot.send_message(chat_id=chat_id, text=text)
    else:
        context.bot.send_message(chat_id=chat_id, text="Couldn't find any timer")
