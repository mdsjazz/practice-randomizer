from itertools import combinations
import math
import random
from typing import List


NUM_ALLOWED_CHROMATIC_STARTING_NOTES = 31

REGISTER_MAP = {0: "low", 1: "middle", 2: "high"}
INT_TO_NOTE_MAP = {0: "Bb", 1: "B", 2: "C", 3: "Db", 4: "D", 5: "Eb", 6: "E", 7: "F", 8: "F#", 9: "G", 10: "Ab", 11: "A"}
NOTE_TO_INT_MAP = {"Bb": 0, "B": 1, "C": 2, "Db": 3, "D": 4, "Eb": 5, "E": 6, "F": 7, "F#": 8, "G": 9, "Ab": 10, "A": 11}


def randomize_starting_note(keyed_or_chromatic: str = "chromatic", key: list = None, scale_notes: list = None) -> str:

    register = ""
    note_name = ""

    if keyed_or_chromatic == "key":
        key_int = NOTE_TO_INT_MAP[key]

        key_scale_notes_ints_full_range = [
            scale_note_int + key_int + 12 * octave
            for scale_note_int in scale_notes for octave in range(-2, 3)
            if 0 <= scale_note_int + key_int + 12 * octave <= NUM_ALLOWED_CHROMATIC_STARTING_NOTES
        ]
        random_starting_note_int = random.choice(key_scale_notes_ints_full_range)
        register = REGISTER_MAP[random_starting_note_int // 12]
        note_name = INT_TO_NOTE_MAP[random_starting_note_int % 12]

    else:
        random_starting_note_int = random.randint(0, NUM_ALLOWED_CHROMATIC_STARTING_NOTES + 1)
        register = REGISTER_MAP[random_starting_note_int // 12]
        note_name = INT_TO_NOTE_MAP[random_starting_note_int % 12]

    return f"{register} {note_name}"


def randomize_key(keys: list = None) -> str:
    if keys is None:
        keys = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
    return random.choice(keys)


def randomize_interval(max_interval: int = 0) -> int:
    return random.randint(1, max_interval + 1)


def randomize_displacement(number_of_notes: int = 0) -> int:
    return random.randint(0, number_of_notes)


def randomize_offset(notes_per_beat: int = 0) -> int:
    return random.randint(0, notes_per_beat)


def randomize_articulation(notes_per_beat: int = 0) -> int:

    number_of_possible_articulations = 2 ** notes_per_beat
    num_articulations_int = random.randint(0, number_of_possible_articulations)

    num_remaining_articulations = num_articulations_int

    num_articulated_notes = 0
    while num_remaining_articulations > 0:
        combos_numerator = math.factorial(notes_per_beat)
        combos_denominator = math.factorial(num_articulated_notes) * math.factorial(notes_per_beat - num_articulated_notes)
        num_remaining_articulations -= combos_numerator / combos_denominator

    articulations_tuple = tuple(combinations(range(1, notes_per_beat + 1), num_articulated_notes))

    return random.choice(articulations_tuple)


def randomize_inversion(inversions: List = None) -> int:
    return random.choice(inversions) if inversions is not None else None


def randomize_inverted(invertible: bool = False) -> bool:
    return random.choice(["Up", "Down", "Up-Down", "Down-Up"]) if invertible else None
