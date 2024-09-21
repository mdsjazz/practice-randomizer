import os
import sys

import hydra
from omegaconf import DictConfig

sys.path.append(os.getcwd())
sys.path.append("/Users/mikey/Personal/Programming and Development/Miscellaneous Projects/practice-randomizer")

from practice_randomizer.routines import Routine
from practice_randomizer.utils import text_input_to_approx_true

def run() -> None:
    print()
    routine_choice_input = input("What routine would you like to practice?\n")
    if not routine_choice_input:
        routine_choice_input = "basic"
    # Get table/db, check names

    sample_exercises_without_replacement = input("Would you like to have unique exercises?\n")
    if not sample_exercises_without_replacement:
        sample_exercises_without_replacement = "yes"
    reset = input("Would you like to reset the routine?\n")
    if not reset:
        reset = "no"

    sample_exercises_without_replacement = text_input_to_approx_true(sample_exercises_without_replacement)
    reset = text_input_to_approx_true(reset)

    routine = Routine(choice = routine_choice_input, replacement = sample_exercises_without_replacement, reset = reset)
    routine.run()


if __name__ == "__main__":
    run()