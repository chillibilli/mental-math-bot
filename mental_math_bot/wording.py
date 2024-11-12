# -*- coding: utf-8 -*-

import math


def timelapse(sec):
    sec = round(sec)
    m = int(sec / 60)
    sec = sec - m * 60
    if m == 0:
        return f'{sec} сек.'
    else:
        return f'{m} мин. {sec} сек.'


def grammar_case(n, single, double, multiple):
    # вывод слова в одной из трех грамматических форм числа в зависимости от количества n
    dec = int(n/10)
    n = n - dec * 10
    i = math.ceil(n / 3 + 0.5) if n != 0 and dec != 1 else 0
    return {0: multiple, 1: single, 2: double}.get(i, multiple)


class Wording:
    @staticmethod
    def resheno(n):
        return grammar_case(n, "Решен", "Решено", "Решено")

    @staticmethod
    def primerov(n):
        return grammar_case(n, "пример", "примера", "примеров")

    @staticmethod
    def bylo(n):
        return grammar_case(n, "Был", "Было", "Было")

    @staticmethod
    def oshibochnyh_otvetov(n):
        return grammar_case(n, "ошибочный ответ", "ошибочных ответа", "ошибочных ответов")

    @staticmethod
    def primerah(n):
        return grammar_case(n, "примере", "примерах", "примерах")

    @staticmethod
    def raz(n):
        return grammar_case(n, "раз", "раза", "раз")

    @classmethod
    def oshibkami(cls, n):
        return grammar_case(n, "ошибкой", "ошибками", "ошибками")

    @staticmethod
    def total(n):
        return f'Ура, задание выполнено! {Wording.resheno(n)} {n} {Wording.primerov(n)}'

    @staticmethod
    def elapsed(s, e):
        return f'за {timelapse(e - s)}'

    @staticmethod
    def mt_elapsed(s, e):
        return f'Ура! Повторили всю таблицу умножения за {timelapse(e - s)}'

    @staticmethod
    def partial(n, t, s, e):
        return (f'{Wording.resheno(n)} {n} {Wording.primerov(n)} из {t}') # {Wording.elapsed(s, e)}, осталось решить {t - n}')

    @staticmethod
    def wrong(wa, we):
        if wa > 0:
            return f'{Wording.bylo(wa)} {wa} {Wording.oshibochnyh_otvetov(wa)} в {we} {Wording.primerah(we)}'
        else:
            return 'Без ошибок'

    @staticmethod
    def num_err(n):
        if n > 0:
            return f'c {n} {Wording.oshibkami(n)}'
        else:
            return 'без ошибок'
