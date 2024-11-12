# -*- coding: utf-8 -*-

import random
import time
from abc import ABC, abstractmethod

from mental_math_bot.wording import Wording


EPSILON = 0.00001

USUAL_EXAMPLES_COUNT = 15
DEFAULT_INTERIM_COUNT = 5


class ExerciseFileNotFound(RuntimeError):
    pass

class ExerciseTextError(RuntimeError):
    pass


class Exercise(ABC):
    def __init__(self):
        self.name = ""
        self.title = ""
        self.example_generator = self.examples()
        self.complete = False
        self.interim_count = DEFAULT_INTERIM_COUNT
        self.arguments = []
        self.results = []
        self.start_time = time.time()
        self.end_time = self.start_time
        self.asked = set()
        self.examples_solved = 0
        self.wrong_answers = 0
        self.wrong_examples = set()

    @abstractmethod
    def total_examples(self) -> int:
        ...

    @abstractmethod
    def examples(self):
        ...

    @abstractmethod
    def task(self) -> str:
        ...

    def next_example(self) -> None:
        self.end_time = time.time()
        try:
            self.arguments, self.results = next(self.example_generator)
        except StopIteration:
            self._finish()

    def _log_answer(self, correct: bool) -> None:
        if correct:
            self.examples_solved += 1
            if self.examples_solved >= self.total_examples():
                self._finish()
        else:
            self.wrong_answers += 1
            self.wrong_examples.add(tuple(self.arguments))

    def cancel(self):
        self.end_time = time.time()

    def _finish(self):
        self.complete = True

    def result(self) -> float | int | None:
        return self.results[0] if len(self.results) > 0 else None

    def is_correct(self, answer: str) -> bool:
        try:
            answer = float(answer)
            correct = abs(answer - self.result()) < EPSILON
        except ValueError:
            correct = False
        self._log_answer(correct)
        return correct

    def start_time_str(self):
        return time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(self.start_time))

    def milestone(self):
        return (self.examples_solved % self.interim_count == 0
                and 0 < self.examples_solved < self.total_examples())

    def interim_report(self) -> str:
        return Wording.partial(self.examples_solved, self.total_examples(), self.start_time, self.end_time)

    def final_greeting(self) -> str:
        return (f'{Wording.total(self.examples_solved)} {Wording.elapsed(self.start_time, self.end_time)}\n'
                f'{Wording.wrong(self.wrong_answers, len(self.wrong_examples))}\n')

