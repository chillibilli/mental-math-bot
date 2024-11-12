# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import ContextTypes

from mental_math_bot import database
from mental_math_bot.database import DEFAULT_N_DAYS
from mental_math_bot.lifecycle import CURRENT_TEST_CONTEXT_ITEM, start_test, misplaced_command
from mental_math_bot.exercises import Exercise


async def mul_tab_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise and not exercise.complete:
        await misplaced_command(update)
    else:
        await start_test("mul_tab", update, context)


async def random_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise and not exercise.complete:
        await misplaced_command(update)
    else:
        await start_test("random", update, context)


async def div_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise and not exercise.complete:
        await misplaced_command(update)
    else:
        await start_test("div", update, context)


async def plus1_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise and not exercise.complete:
        await misplaced_command(update)
    else:
        await start_test("plus1", update, context)


async def plus2_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise and not exercise.complete:
        await misplaced_command(update)
    else:
        await start_test("plus2", update, context)


async def minus_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
    if exercise and not exercise.complete:
        await misplaced_command(update)
    else:
        await start_test("minus", update, context)


async def personal_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if update.message:
        args = update.message.text.split(' ')
        if len(args) > 1:
            user_id = args[1]

    response = await database.get_personal_list(user_id)
    await update.message.reply_text(response)


async def admin_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    n_days = DEFAULT_N_DAYS
    if update.message:
        args = update.message.text.split(' ')
        if len(args) > 1 and args[1].isdigit():
            n_days = int(args[1])

    response = await database.get_admin_report(n_days)
    await update.message.reply_text(response)


async def full_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    n_days = DEFAULT_N_DAYS
    if update.message:
        args = update.message.text.split(' ')
        if len(args) > 1 and args[1].isdigit():
            n_days = int(args[1])

    response = await database.get_full_list(n_days)
    await update.message.reply_text(response)


def expression_exercise(filename):
    async def _wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        exercise: Exercise = context.chat_data.get(CURRENT_TEST_CONTEXT_ITEM, None)
        if exercise and not exercise.complete:
            await misplaced_command(update)
        else:
            await start_test(filename, update, context)

    return _wrapped

