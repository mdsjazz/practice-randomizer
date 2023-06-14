import os
import sys

import hydra
from omegaconf import DictConfig

sys.path.append(os.getcwd())

from practice_randomizer.routines import Routine

def run() -> None:
    routine_choice_input = input("What routine would you like to practice?\n")
    # Get table/db, check names

    sample_exercises_without_replacement = input("Would you like to have unique exercises?\n")
    if sample_exercises_without_replacement in (1, True) or "y" in sample_exercises_without_replacement.lower():
        # Logic to set routine
        sample_exercises_without_replacement = True
    else:
        sample_exercises_without_replacement = False

    routine = Routine(choice = routine_choice_input, replacement = sample_exercises_without_replacement)
    routine.run()


if __name__ == "__main__":
    run()