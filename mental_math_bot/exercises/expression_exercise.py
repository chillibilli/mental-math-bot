import random
import os
from os.path import abspath, dirname, join, splitext

from mental_math_bot.exercises.base_exercise import Exercise, DEFAULT_INTERIM_COUNT
from mental_math_bot.exercises.base_exercise import ExerciseFileNotFound, ExerciseTextError

current_dir = dirname(abspath(__file__))


def list_expression_exercises():
    dir_path = join(current_dir, 'files')
    res = []
    for file in os.listdir(dir_path):
        if file.endswith('.txt'):
            res.append(splitext(file)[0])
    return res


def load_exercise(name):
    title = name
    examples = []
    try:
        file_path = join(current_dir, 'files', f'{name}.txt')
        with open(file_path) as f:
            i = 0
            for line in f:
                text = line.strip()
                if i == 0:
                    title = text
                elif text != "":
                    eval(text)
                    examples.append(text)
                i += 1
    except FileNotFoundError:
        raise ExerciseFileNotFound(f'Exercise file "{name}.txt" not found')
    except SyntaxError:
        raise ExerciseTextError('Ошибка в примере из "{{name}.txt}": "{line}"')

    return title, examples


class ExpressionExercise(Exercise):
    def __init__(self, name, examples=None, interim_count=DEFAULT_INTERIM_COUNT):
        super().__init__()
        self.name = name
        self.interim_count = interim_count
        self.title, self.example_list = load_exercise(name)
        if examples is None:
            self.max_examples = len(self.example_list)
        else:
            self.max_examples = min(len(self.example_list), examples)

    def total_examples(self) -> int:
        return self.max_examples

    def examples(self):
        for _ in range(self.max_examples):
            while True:
                i = random.randint(0, len(self.example_list) - 1)
                if i not in self.asked:
                    break
            self.asked.add(i)

            text = self.example_list[i]
            c = eval(text)
            yield [text], [c]

    def task(self) -> str:
        text = self.arguments[0]
        return f'{text} = '
