from .base_exercise import Exercise
from .random_exercises import MulTabExercise, RandomMulTabExercise, MulExercise, DivExercise
from .random_exercises import Plus1Exercise, Plus2Exercise, MinusExercise
# from .expression_exercise import ExpressionExercise, list_expression_exercises

EXERCISE_MAP = {
    "mul_tab": (MulTabExercise, []),
    "random": (RandomMulTabExercise, []),
    "mul": (MulExercise, []),
    "div": (DivExercise, []),
    "plus1": (Plus1Exercise, []),
    "plus2": (Plus2Exercise, []),
    "minus": (MinusExercise, []),
}

#EXERCISE_MAP.update({filename: (ExpressionExercise, [filename]) for filename in list_expression_exercises()})

def create(exercise_name):
    exercise_class, args = EXERCISE_MAP.get(exercise_name)
    if exercise_class is None:
        return None
    else:
        return exercise_class(*args)
