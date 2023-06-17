import json
import os
import numpy as np
import random
from typing import List

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

from practice_randomizer.randomizer import (
    NOTE_TO_INT_MAP,
    randomize_starting_note,
    randomize_interval,
    randomize_displacement,
    randomize_offset,
    randomize_articulation,
    randomize_inversion,
    randomize_inverted,
)

ROUTINES_PATH = "/Users/mikey/Personal/Programming and Development/Miscellaneous Projects/practice-randomizer/routines"


class Exercise:

    def __init__(
        self,
        name: str = "",
        category: str = "",
        keyed_or_chromatic: str = "chromatic",
        number_of_notes: int = 0,
        notes_per_beat: int = 0,
        max_interval: int = 1,
        inversions: List = None,
        invertible: bool = False,
        **kwargs
    ):

        self.name = name
        self.category = category
        self.keyed_or_chromatic = keyed_or_chromatic
        self.number_of_notes = number_of_notes
        self.notes_per_beat = notes_per_beat
        self.max_interval = max_interval
        self.inversions = inversions
        self.invertible = invertible

        (
            self.starting_note,
            self.interval,
            self.displacement,
            self.offset,
            self.articulation,
            self.inversions,
            self.inverted,
        ) = self.return_randomized_exercise(
            keyed_or_chromatic=self.keyed_or_chromatic,
            number_of_notes=self.number_of_notes,
            notes_per_beat=self.notes_per_beat,
            max_interval=self.max_interval,
            inversions=self.inversions,
            invertible=self.invertible,
        )

    def __str__(self):
        exercise_str =  f"""
        {self.category}:
            {self.name},
            start on {self.starting_note},
            displace by {self.displacement},
            offset by {self.offset},
            articulate as {self.articulation}"""
        if self.inversions:
            exercise_str += f", {self.inversions} inversion"
        if self.inverted:
            exercise_str += f", {self.inverted}"
        return exercise_str

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def return_randomized_exercise(
        keyed_or_chromatic: bool,
        number_of_notes: int,
        notes_per_beat: int,
        max_interval: int,
        inversions: List,
        invertible: bool,
    ):
        starting_note = randomize_starting_note(keyed_or_chromatic=keyed_or_chromatic)
        interval = randomize_interval(max_interval=max_interval)
        displacement = randomize_displacement(number_of_notes=number_of_notes)
        offset = randomize_offset(notes_per_beat=notes_per_beat)
        articulation = randomize_articulation(notes_per_beat=notes_per_beat)
        inversion = randomize_inversion(inversions=inversions)
        inverted = randomize_inverted(invertible=invertible)

        return (starting_note, interval, displacement, offset, articulation, inversion, inverted)

    def list_all_mandatory_combinations(self):

        all_keys = list(NOTE_TO_INT_MAP.keys()) if self.keyed_or_chromatic == "keyed" else ["NA"]
        all_intervals = list(range(1, self.max_interval + 1))
        all_inversions = self.inversions
        all_invertibles = ["up", "down", "up-down", "down-up"] if self.invertible else ["NA"]

        mandatory_params = (all_keys, all_intervals, all_inversions, all_invertibles)

        return np.array(np.meshgrid(*mandatory_params)).reshape(-1, len(mandatory_params))



class Routine:

    def __init__(self, choice: str, replacement: bool = False):

        routine_config_name = f"{choice}.yaml"
        routine_state_rel_path = f"./routine_states/{choice}/state.json"

        if not os.path.exists(routine_state_rel_path):
            with open(routine_state_rel_path, "w", encoding="UTF-8") as routine_state_fp:
                json.dump({}, routine_state_fp)

        initialize(version_base="1.2", config_path="configs")
        exercises_hydra = compose(config_name=routine_config_name)
        self.routine_config = OmegaConf.to_container(exercises_hydra, resolve=True)

        self.exercises_templates = {
            exercise_name: exercise_config for exercise_group_config in self.routine_config["exercises"].values() for exercise_name, exercise_config in exercise_group_config.items()
        }

        with open(routine_state_rel_path, "r", encoding="UTF-8") as routine_state_fp:
            self.state = json.load(routine_state_fp)

        self.unpracticed_exercises_templates = ["hi"]

    def choose_exercise(self):
        return random.choice(list(self.exercises_templates.keys()))

    def update(self, exercise_id: int, rating: float = None):
        self.state[exercise_id]["practiced"] = True
        if rating is not None:
            self.state[exercise_id]["rating"] = rating
        del self.unpracticed_exercises[exercise_id]

    def save_state(self):
        pass

    def run(self):
        try:
            while self.unpracticed_exercises:
                exercise_id = self.choose_exercise()
                exercise = Exercise(**self.exercises_templates[exercise_id])

                print(exercise)
                rating = input("Please press any key for the next exercise. Input a rating if you wish.")
                if rating.isnumeric():
                    rating = float(rating)
                else:
                    rating = None
                self.update(exercise_id, rating)

        except:
            pass

        self.save_state()

    