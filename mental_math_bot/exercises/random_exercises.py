# -*- coding: utf-8 -*-
import random

from mental_math_bot.exercises.base_exercise import Exercise, USUAL_EXAMPLES_COUNT
from mental_math_bot.wording import Wording


class MulTabExercise(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "mul_tab"
        self.title = "Таблица умножения"
        self.interim_count = 8

    def total_examples(self) -> int:
        return 8 * 8

    def examples(self):
        while True:
            if len(self.asked) == 8:
                break

            a = random.randint(2, 9)
            if a in self.asked:
                continue

            self.asked.add(a)

            b = 2
            while b < 10:
                yield [a, b], [a * b]
                b += 1

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} * {b} = '

    def final_greeting(self) -> str:
        return (f'{Wording.mt_elapsed(self.start_time, self.end_time)}\n'
                f'{Wording.wrong(self.wrong_answers, len(self.wrong_examples))}\n')


class RandomMulTabExercise(Exercise):
    def __init__(self):
        super().__init__()
        self.name = "random"
        self.title = "Вся таблица умножения вразбивку"
        self.asked = set()
        self.should_be_asked = set((i, j) for i in range(2, 10) for j in range(2, 10))

    def total_examples(self) -> int:
        return len(self.should_be_asked)

    def examples(self):
        while True:
            if len(self.should_be_asked - self.asked) == 0:
                break

            a = random.randint(2, 9)
            b = random.randint(2, 9)

            if (a, b) in self.asked:
                continue

            self.asked.add((a, b))

            yield [a, b], [a * b]

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} * {b} = '

    def final_greeting(self) -> str:
        return (f'{Wording.mt_elapsed(self.start_time, self.end_time)}\n'
                f'{Wording.wrong(self.wrong_answers, len(self.wrong_examples))}\n')


class MulExercise(Exercise):
    def __init__(self, examples=USUAL_EXAMPLES_COUNT):
        super().__init__()
        self.name = "mul"
        self.title = "Примеры из таблицы умножения"
        self.n_examples = examples

    def total_examples(self) -> int:
        return self.n_examples

    def examples(self):
        while True:
            if len(self.asked) >= self.total_examples():
                break

            a = random.randint(2, 9)
            b = random.randint(2, 9)

            if (a, b) in self.asked:
                continue

            self.asked.add((a, b))

            yield [a, b], [a * b]

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} * {b} = '


class DivExercise(Exercise):
    def __init__(self, examples=USUAL_EXAMPLES_COUNT):
        super().__init__()
        self.name = "div"
        self.title = "Примеры на деление из таблицы умножения"
        self.n_examples = examples

    def total_examples(self) -> int:
        return self.n_examples

    def examples(self):
        while True:
            if len(self.asked) >= self.total_examples():
                break

            a = random.randint(2, 9)
            b = random.randint(2, 9)
            c = a * b

            if (c, a) in self.asked:
                continue

            self.asked.add((c, a))

            yield [c, a], [b]

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} / {b} = '


class Plus1Exercise(Exercise):
    def __init__(self, examples=USUAL_EXAMPLES_COUNT):
        super().__init__()
        self.name = "plus1"
        self.title = "Устный счет на сложение"
        self.n_examples = examples

    def total_examples(self) -> int:
        return self.n_examples

    def examples(self):
        while True:
            if len(self.asked) >= self.total_examples():
                break

            a = random.randint(2, 12)
            b = random.randint(10, 100)
            if a < b:
                a, b = b, a
            c = a + b

            if (a, b) in self.asked:
                continue

            self.asked.add((a, b))

            yield [a, b], [c]

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} + {b} = '


class Plus2Exercise(Exercise):
    def __init__(self, examples=USUAL_EXAMPLES_COUNT):
        super().__init__()
        self.name = "plus2"
        self.title = "Устный счет на сложение двузначных чисел"
        self.n_examples = examples

    def total_examples(self) -> int:
        return self.n_examples

    def examples(self):
        while True:
            if len(self.asked) >= self.total_examples():
                break

            while True:
                a = random.randint(3, 50)
                if a != 10:
                    break
            b = random.randint(10, 100)
            if a < b:
                a, b = b, a
            c = a + b

            if (a, b) in self.asked:
                continue

            self.asked.add((a, b))

            yield [a, b], [c]

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} + {b} = '


class MinusExercise(Exercise):
    def __init__(self, examples=USUAL_EXAMPLES_COUNT):
        super().__init__()
        self.name = "minus"
        self.title = "Устный счет на вычитание"
        self.n_examples = examples

    def total_examples(self) -> int:
        return self.n_examples

    def examples(self):
        while True:
            if len(self.asked) >= self.total_examples():
                break

            a = random.randint(2, 12)
            b = random.randint(10, 100)
            if a < b:
                a, b = b, a
            c = a + b

            if (c, b) in self.asked:
                continue

            self.asked.add((c, b))

            yield [c, b], [a]

    def task(self) -> str:
        a, b = self.arguments
        return f'{a} - {b} = '



if __name__ == '__main__':

    def tst(cls):
        t = cls()

        print(cls.__name__)

        while True:
            t.next_example()
            if t.complete:
                break

            duration = t.end_time - t.start_time

            t.is_correct(str(t.result() + 1))
            t.is_correct(str(t.result()))

            if t.milestone():
                print(f'Отлично! {t.interim_report()}')

            print(t.arguments, t.results, t.task(),
                  t.complete, t.examples_solved, t.wrong_answers, len(t.wrong_examples), duration, t.start_time_str())

        print(t.final_greeting())

    tst(MulTabExercise)
    tst(RandomMulTabExercise)
    tst(MulExercise)
    tst(DivExercise)
    tst(Plus1Exercise)
    tst(Plus2Exercise)
    tst(MinusExercise)
