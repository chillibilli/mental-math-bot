# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import ContextTypes

from mental_math_bot import database
from mental_math_bot.exercises import random_exercises, create, Exercise

CURRENT_TEST_CONTEXT_ITEM = 'current_test'


async def greeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Нажми кнопку "Меню" и выбери команду')


async def misplaced_command(update: Update):
    await update.message.reply_text('Остановить задание можно командой /stop')


async def misplaced_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Что-что? Непонятно.')
    await greeting(update, context)


async def start_test(test_name, update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise = create(test_name)
    if exercise:
        await update.message.reply_text(exercise.title)
        context.chat_data[CURRENT_TEST_CONTEXT_ITEM] = exercise
        exercise.next_example()
        await update.message.reply_text(exercise.task())


async def accept_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise:
        # test is on its way
        answer = update.message.text
        if exercise.is_correct(answer):
            if exercise.complete:
                await end_test(update, context)
                user_id = update.message.from_user.id
                await update.message.reply_text(
                    await database.get_same_tests(user_id, exercise.name, 7,
                                                  current_test_start=exercise.start_time_str()))
            else:
                if exercise.milestone():
                    await update.message.reply_text(f'Отлично! {exercise.interim_report()}')
                exercise.next_example()
                await update.message.reply_text(exercise.task())
        else:
            await update.message.reply_text("Неправильно")
            await update.message.reply_text(exercise.task())
    else:
        await misplaced_text(update, context)


async def end_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise:
        if exercise.complete:
            await update.message.reply_text(exercise.final_greeting())
        else:
            await update.message.reply_text(exercise.interim_report())

        user_id = update.message.from_user.id
        username = update.message.from_user.username
        await database.save_test_results(user_id, username, exercise)

        exercise.complete = True
        context.chat_data[CURRENT_TEST_CONTEXT_ITEM] = None


