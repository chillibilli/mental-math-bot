# -*- coding: utf-8 -*-

import asyncio
import sqlite3
from datetime import datetime, timedelta

from mental_math_bot.exercises import Exercise, EXERCISE_MAP
from mental_math_bot.wording import Wording, timelapse, grammar_case
from mental_math_bot.logger import logger

DATABASE_NAME = "test_results.db"

N_TOP = 3
DEFAULT_N_DAYS = 7

locker = asyncio.Lock()


def add_nickname(user_id, nickname):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT user_id, nickname FROM users
            WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchall()

        if len(result) == 0:
            cursor.execute('''
                INSERT INTO users (
                    user_id, nickname
                ) VALUES (?, ?)
            ''', (user_id, nickname))
        else:
            cursor.execute('''
                UPDATE users
                SET user_id = ?, nickname = ?
            ''', (user_id, nickname))
        conn.commit()

    except Exception as e:
        logger.error(str(e))
        raise
    finally:
        conn.close()


def setup():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                user_id TEXT,
                username TEXT,
                test_type TEXT,
                test_title TEXT,
                start_time TEXT,
                duration REAL,
                completed INTEGER,
                test_examples INTEGER,
                examples_passed INTEGER,
                examples_with_errors INTEGER,
                wrong_answers INTEGER
            )
        ''')
        conn.commit()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT,
                nickname TEXT
            )
        ''')
        conn.commit()

        add_nickname("7506138638", "Олег/Даша")

    except Exception as e:
        logger.error(str(e))
        raise
    finally:
        conn.close()


async def save_test_results(user_id, username, exercise: Exercise):
    duration = exercise.end_time - exercise.start_time

    async with locker:
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO results (
                    user_id, username, test_type, test_title, start_time, duration, completed, 
                    test_examples, examples_passed, examples_with_errors, wrong_answers
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, exercise.name, exercise.title,
                  exercise.start_time_str(), duration, int(int(exercise.complete)),
                  exercise.total_examples(), exercise.examples_solved,
                  len(exercise.wrong_examples), exercise.wrong_answers))
        except Exception as e:
            logger.error(str(e))
        finally:
            conn.commit()
            conn.close()


async def get_same_tests(user_id, n_days, test_type, current_test_start=None):

    lines = []

    async with locker:
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT coalesce(username, nickname, r.user_id) as username, test_title, start_time, duration, examples_passed, wrong_answers 
                FROM results r LEFT JOIN users u ON r.user_id = u.user_id
                WHERE r.user_id=? AND test_type=? AND completed = 1
                ORDER BY 
                    substr(start_time, 7, 4),  -- Year
                    substr(start_time, 4, 2),  -- Month
                    substr(start_time, 1, 2),  -- Day
                    substr(start_time, 12, 8);  -- Time (HH:MM:SS)
                ''', (user_id, test_type))

            results = cursor.fetchall()
            n = len(results)
            if n > 0:
                test_title = results[0][1]
                lines = [f'Задание "{test_title}" выполнено {n} {Wording.raz(n)}:']

                for r in results:
                    username, test_title, start_time, duration, examples_passed, wrong_answers = r
                    when = start_time[:16]
                    how_long = timelapse(duration)
                    line = f"- {when} - за {how_long} {Wording.num_err(wrong_answers)}"
                    if current_test_start is not None and current_test_start == start_time:
                        line += " <-- сейчас"
                    lines.append(line)

        except Exception as e:
            logger.error(str(e))
            raise

        finally:
            conn.close()

    response = "\n".join(lines)
    return response


async def get_personal_list(user_id):
    reports = [s for s in [await get_same_tests(user_id, test_type, 7) for test_type in EXERCISE_MAP.keys()] if s != ""]
    if len(reports) == 0:
        response = "Чтобы получить результаты, нужно выполнить до конца хотя бы одно задание"
    else:
        response = "\n\n".join(reports)
    return response


async def get_admin_report(n_days):

    lines = []

    async with locker:
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()

            today = datetime.today()
            dates = ", ".join([f'"{(today - timedelta(days=n_days - i - 1)).strftime("%d.%m.%Y")}"' for i in range(n_days)])

            cursor.execute(f'''
                SELECT test_type
                FROM results 
                WHERE SUBSTR(start_time, 1, 10) in ({dates})
                GROUP BY test_type
                ORDER BY test_type
            ''')

            exercise_index = {r[0]: i for i, r in enumerate(cursor.fetchall())}

            for i in range(n_days):
                day = today - timedelta(days=n_days - i - 1)
                day_str = day.strftime("%d.%m.%Y")

                cursor.execute('''
                    SELECT coalesce(username, nickname, r.user_id) as username, test_type, test_title, completed, count(*)
                    FROM results r LEFT JOIN users u ON r.user_id = u.user_id
                    WHERE SUBSTR(start_time, 1, 10) = ?
                    GROUP BY username, test_title, completed
                    ORDER BY username, test_title, completed
                ''', (day_str, ))

                results = cursor.fetchall()

                data = {}
                for username, test_type, test_title, completed, count in results:
                    if username not in data:
                        data[username] = [[0, 0] for _ in range(len(exercise_index))]
                    data[username][exercise_index[test_type]][completed] = count

                if len(data) > 0:
                    lines.append(f'{day_str}:')
                    for username, counts in data.items():
                        test_counts = ' | '.join([f'{str(a[0])}-{str(a[1])}' for a in counts])
                        lines.append(f'{test_counts} {username}')

                    lines.append('')

            test_names = ' | '.join([k for k in exercise_index.keys()])
            lines.append(f'({test_names} : незавершенные-завершенные)')

        except Exception as e:
            logger.error(str(e))
            raise

        finally:
            conn.close()

    response = "\n".join(lines)
    return response


async def get_full_list(n_days):

    lines = []

    async with locker:
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()

            today = datetime.today()

            for i in range(n_days):
                day = today - timedelta(days=n_days - i - 1)
                day_str = day.strftime("%d.%m.%Y")

                cursor.execute('''
                    SELECT coalesce(username, nickname, r.user_id) as username, test_type, test_title, start_time, duration, completed, test_examples,
                           examples_passed, examples_with_errors, wrong_answers
                    FROM results r LEFT JOIN users u ON r.user_id = u.user_id
                    WHERE SUBSTR(start_time, 1, 10) = ?
                    ORDER BY start_time
                ''', (day_str, ))

                results = cursor.fetchall()

                for r in results:
                    (username, test_type, test_title, start_time, duration, completed, test_examples,
                     examples_passed, examples_with_errors, wrong_answers) = r
                    lines.append(f'{("-", "+")[completed]} {username} '
                                 f'{start_time[:16]} {examples_passed}/{test_examples} '
                                 f'({timelapse(duration)}) {test_title} ')

                if len(lines) > 0:
                    lines.append('')

        except Exception as e:
            logger.error(str(e))
            raise

        finally:
            conn.close()

    if len(lines) == 0:
        response = f'За {n_days} {grammar_case(n_days, "день", "дня", "дней")} '\
                   '(включая сегодняшний) никто никаких заданий не сделал'
    else:
        response = "\n".join(lines)

    return response
