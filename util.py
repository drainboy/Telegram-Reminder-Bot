import datetime
import pytz
from functools import wraps


def return_time_object(hour, min, sec, tzinfo=pytz.timezone("Asia/Singapore")):
    """Returns a datetime.time object with given hour, minute, second and tzinfo"""
    return datetime.time(hour=hour, minute=min, second=sec, tzinfo=tzinfo)


def restricted(func, admin_list):
    """Restrict usage of func to allowed users only and replies if necessary"""

    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in admin_list:
            print("WARNING: Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text('User disallowed.')
            return  # quit function
        return func(bot, update, *args, **kwargs)

    return wrapped


def update_admin_list(chat_id, bot, admin_dict):
    """Updates give admin_dict with updated list of admins"""
    updated_admin_list = [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
    admin_dict[chat_id] = updated_admin_list
