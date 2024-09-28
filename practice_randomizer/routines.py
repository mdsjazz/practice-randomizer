import itertools
import json
import os
from pydantic import BaseModel, RootValidator
import random
from typing import List

from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf

from practice_randomizer.randomizer import (
    NOTE_TO_INT_MAP,
    randomize_starting_note,
    randomize_key,
    randomize_interval,
    randomize_displacement,
    randomize_offset,
    randomize_articulation,
    randomize_inversion,
    randomize_invert_pattern,
)
from practice_randomizer.utils import text_input_to_approx_true

ROUTINE_STATE_PATH = "/Users/mikey/Personal/Programming and Development/Miscellaneous Projects/practice-randomizer/routine_states"

@dataclass
class Exercise(BaseModel):
    name: str = ""
    category: str = ""
    keyed_or_chromatic: Optional[str] = None
    key: str = None
    scale_notes: Optional[List] = None
    starting_note: Optional[str] = None

@dataclass
class KeyedExercise(Exercise):
    keyed_or_chromatic: str = "keyed"
    key: str = ""
    scale_notes: List[str] = 
    


class Exercise:

    def __init__(
        self,
        name: str = "",
        category: str = "",
        keyed_or_chromatic: str = None,
        key: str = None,
        scale_notes: List = None,
        starting_note: str = None,
        number_of_notes: int = None,
        notes_per_beat: int = None,
        displacement: int = None,
        offset: int = None,
        interval: int = None,
        inversion: int = None,
        invert_pattern: str = None,
        articulation: List = None,
    ):

        self.name = name
        self.category = category
        self.keyed_or_chromatic = keyed_or_chromatic
        self.key = key
        self.starting_note = starting_note if starting_note else randomize_starting_note(keyed_or_chromatic=keyed_or_chromatic, key=key, scale_notes=scale_notes)

        self.notes_per_beat = notes_per_beat
        self.displacement = displacement if displacement else randomize_displacement(number_of_notes=number_of_notes)
        self.offset = offset if offset else randomize_offset(notes_per_beat=notes_per_beat)

        self.interval = interval
        self.inversion = inversion
        self.invert_pattern = invert_pattern

        self.articulation = articulation if articulation else randomize_articulation(notes_per_beat=notes_per_beat)


    def __str__(self):
        exercise_str =  f"""
        {self.category}:
            {self.name},
        """
        if self.key:
            exercise_str += f"""
            key: {self.key},"""

        exercise_str += f"""
            start on {self.starting_note},
            displace by {self.displacement},
            offset by {self.offset},
            {self.notes_per_beat} notes per beat,
            articulate as {self.articulation},
            in intervals of {self.interval}"""

        if self.inversion:
            exercise_str += f""",
            inversion {self.inversion}"""
        if self.invert_pattern:
            exercise_str += f""",
            {self.invert_pattern}"""
        exercise_str += "\n"
        return exercise_str

    def __repr__(self):
        return self.__str__()

    def get_mandatory_exercise_params_form(self):
        return {
            "name": self.name,
            "category": self.category,
            "key": self.key,
            "notes_per_beat": self.notes_per_beat,
            "interval": self.interval,
            "inversion": self.inversion,
            "invert_pattern": self.invert_pattern,
        }

    def get_ustrid(self):
        exercise_str = str(list(self.get_mandatory_exercise_params_form().values()))
        return exercise_str



class ExerciseTemplate:

    def __init__(
        self,
        name: str = "",
        category: str = "",
        keyed_or_chromatic: str = "chromatic",
        scale_notes: List = None,
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
        self.scale_notes = scale_notes
        self.number_of_notes = number_of_notes
        self.notes_per_beat = notes_per_beat
        self.max_interval = max_interval
        self.inversions = inversions
        self.invertible = invertible

    def return_randomized_exercise(
        self,
        keyed_or_chromatic: bool = None,
        number_of_notes: int = None,
        notes_per_beat: int = None,
        max_interval: int = None,
        inversions: List = None,
        invertible: bool = None,
    ):

        if keyed_or_chromatic is None:
            keyed_or_chromatic = self.keyed_or_chromatic
        if number_of_notes is None:
            number_of_notes = self.number_of_notes
        if notes_per_beat is None:
            notes_per_beat = self.notes_per_beat
        if max_interval is None:
            max_interval = self.max_interval
        if inversions is None:
            inversions = self.inversions
        if invertible is None:
            invertible = self.invertible

        key = randomize_key() if keyed_or_chromatic else None
        starting_note = randomize_starting_note(keyed_or_chromatic=keyed_or_chromatic)
        interval = randomize_interval(max_interval=max_interval)
        displacement = randomize_displacement(number_of_notes=number_of_notes)
        offset = randomize_offset(notes_per_beat=notes_per_beat)
        articulation = randomize_articulation(notes_per_beat=notes_per_beat)
        inversion = randomize_inversion(inversions=inversions)
        invert_pattern = randomize_invert_pattern(invertible=invertible)

        return Exercise(
            name=self.name,
            category=self.category,
            keyed_or_chromatic=self.keyed_or_chromatic,
            key=key,
            scale_notes=self.scale_notes,
            starting_note=starting_note,
            notes_per_beat=self.notes_per_beat,
            displacement=displacement,
            offset=offset,
            interval=interval,
            inversion=inversion,
            invert_pattern=invert_pattern,
            articulation=articulation
        )

    def list_all_mandatory_combinations(self):
        all_keys = list(NOTE_TO_INT_MAP.keys()) if self.keyed_or_chromatic == "keyed" else [None]
        all_intervals = list(range(1, self.max_interval + 1))
        all_inversions = self.inversions if self.inversions else [None]
        all_invert_patterns = ["up", "down", "up-down", "down-up", "in-direction", "opposite"] if self.invertible else [None]

        mandatory_params = (all_keys, all_intervals, all_inversions, all_invert_patterns)

        return [{
            "key": combo[0],
            "interval": combo[1],
            "inversion": combo[2],
            "invert_pattern": combo[3]
        } for combo in itertools.product(*mandatory_params)]


class Routine:

    def __init__(self, choice: str, replacement: bool = False, reset: bool = False):

        routine_config_name = f"{choice}.yaml"
        self.routine_state_dir_rel_path = f"{ROUTINE_STATE_PATH}/{choice}"
        self.routine_state_rel_path = f"{self.routine_state_dir_rel_path}/state.json"

        self.replacement = replacement

        if not os.path.exists(self.routine_state_rel_path) or reset:
            self.restart_state()

        initialize(version_base="1.2", config_path="configs")
        exercises_hydra = compose(config_name=routine_config_name)
        self.routine_config = OmegaConf.to_container(exercises_hydra, resolve=True)

        self.exercises_templates = {
            exercise_name: exercise_config
            for exercise_group_config in self.routine_config["exercises"].values()
            for exercise_name, exercise_config in exercise_group_config.items()
        }

        with open(self.routine_state_rel_path, "r", encoding="UTF-8") as routine_state_fp:
            self.practiced_exercises = json.load(routine_state_fp)

        self.all_mandatory_exercises = self.list_all_mandatory_exercises()

        self.unpracticed_exercises = {}
        for incomplete_exercise in self.all_mandatory_exercises:
            exercise = Exercise(**incomplete_exercise)
            exercise_u_str_id = exercise.get_ustrid()
            if not self.check_if_exercise_in_state(exercise):
                self.unpracticed_exercises[exercise_u_str_id] = incomplete_exercise


    def list_all_mandatory_exercises(self):
        all_mandatory_exercises = []
        for exercise_id in self.exercises_templates:
            exercise_template = ExerciseTemplate(**self.exercises_templates[exercise_id])
            all_param_combos = exercise_template.list_all_mandatory_combinations()

            all_mandatory_exercises += [{
                "name": exercise_template.name,
                "category": exercise_template.category,
                "keyed_or_chromatic": exercise_template.keyed_or_chromatic,
                "number_of_notes": exercise_template.number_of_notes,
                "notes_per_beat": exercise_template.notes_per_beat,
                "scale_notes": exercise_template.scale_notes,
                "key": param_combo["key"],
                "interval": param_combo["interval"],
                "inversion": param_combo["inversion"],
                "invert_pattern": param_combo["invert_pattern"],
            } for param_combo in all_param_combos]

        return all_mandatory_exercises

    def choose_exercise(self):
        if self.replacement:
            return random.choice(list(self.unpracticed_exercises.values()))
        else:
            return random.choice(list(self.exercises_templates.keys()))

    def sample_display_exercise(self):
        exercise_template = self.choose_exercise()
        exercise = Exercise(**exercise_template)
        print(exercise)
        rating = input("Please press any key for the next exercise. Input a rating if you wish.\n")

        return exercise, rating


    def check_if_exercise_in_state(self, exercise: Exercise) -> bool:
        return exercise.get_ustrid() in self.practiced_exercises


    def update(self, exercise: Exercise, rating: float = None, bpm: float = None):
        practiced_exercise_dict = exercise.__dict__

        practiced_exercise_dict["practiced"] = True
        practiced_exercise_dict["rating"] = rating
        practiced_exercise_dict["bpm"] = bpm

        self.practiced_exercises[exercise.get_ustrid()] = practiced_exercise_dict

        del self.unpracticed_exercises[exercise.get_ustrid()]

    def save_state(self, save_object: dict = None):
        if not save_object:
            save_object = {}

        if not os.path.exists(self.routine_state_dir_rel_path):
            os.makedirs(self.routine_state_dir_rel_path)

        with open(self.routine_state_rel_path, "w", encoding="UTF-8") as routine_state_fp:
            json.dump(save_object, routine_state_fp, indent=4)

    def restart_state(self):
        self.save_state()

    def run(self):
        if self.replacement:
            try:
                while self.unpracticed_exercises:
                    exercise, rating = self.sample_display_exercise()
                    if rating.isnumeric():
                        rating = float(rating)
                    else:
                        rating = None
                    self.update(exercise, rating)

                    if not self.unpracticed_exercises:
                        restart = input("Routine finished! Would you like to restart?")
                        restart = text_input_to_approx_true(restart)
                        if restart:
                            self.restart_state()

                print("State saved! All exercises practiced.")
                self.save_state(self.practiced_exercises)

            except KeyboardInterrupt:
                print("\n")
                print("Routine finished for now! State updated.")
                self.save_state(self.practiced_exercises)
        else:
            try:
                while True:
                    _ = self.sample_display_exercise()
            except KeyboardInterrupt:
                print("\n")
                print("Routine finished for now!")
