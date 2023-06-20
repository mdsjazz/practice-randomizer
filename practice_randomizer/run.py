import os
import sys

import hydra
from omegaconf import DictConfig

sys.path.append(os.getcwd())

from practice_randomizer.routines import Routine
from practice_randomizer.utils import text_input_to_approx_true

def run() -> None:
    routine_choice_input = input("What routine would you like to practice?\n")
    # Get table/db, check names

    sample_exercises_without_replacement = input("Would you like to have unique exercises?\n")
    reset = input("Would you like to reset the routine?\n")

    sample_exercises_without_replacement = text_input_to_approx_true(sample_exercises_without_replacement)
    reset = text_input_to_approx_true(reset)

    routine = Routine(choice = routine_choice_input, replacement = sample_exercises_without_replacement, reset = reset)
    routine.run()


if __name__ == "__main__":
    run()