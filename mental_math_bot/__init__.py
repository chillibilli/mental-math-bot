# -*- coding: utf-8 -*-
import os

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from mental_math_bot import database
from mental_math_bot.commands import mul_tab_exercise, random_exercise, div_exercise, plus1_exercise, \
    plus2_exercise, minus_exercise, personal_list, admin_report, full_list, expression_exercise
#from mental_math_bot.exercises import list_expression_exercises
from mental_math_bot.lifecycle import end_test, accept_text, greeting
from mental_math_bot.version import VERSION

# - TODO отчеты ограничить только владельцем
# - TODO Сделать красивые кнопки

# TODO Сделать красивую структуру приложения
# TODO сделать инсталяшку
# TODO Разместить на хостинге
# TODO сделать второго бота для тестирования обновлений
# TODO Выложить на гитхаб

BOT_TOKEN = os.getenv("MENTAL_MATH_BOT_TOKEN")


def start_bot():
    print(f"Mental Math Bot version {VERSION}")

    database.setup()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", greeting))
    app.add_handler(CommandHandler("stop", end_test))
    app.add_handler(CommandHandler("mul_tab", mul_tab_exercise))
    app.add_handler(CommandHandler("random", random_exercise))
    app.add_handler(CommandHandler("div", div_exercise))
    app.add_handler(CommandHandler("plus1", plus1_exercise))
    app.add_handler(CommandHandler("plus2", plus2_exercise))
    app.add_handler(CommandHandler("minus", minus_exercise))
    app.add_handler(CommandHandler("list", personal_list))
    app.add_handler(CommandHandler("report", admin_report))
    app.add_handler(CommandHandler("list_all", full_list))

#    for filename in list_expression_exercises():
#        app.add_handler(
#            CommandHandler(filename, lambda update, context:
#                           expression_exercise(filename)(update, context)))

    app.add_handler(MessageHandler(filters.TEXT, accept_text))

    app.run_polling()


if __name__ == '__main__':
    start_bot()
