from itertools import combinations
import math
import random
from typing import List


NUM_ALLOWED_CHROMATIC_STARTING_NOTES = 31

REGISTER_MAP = {0: "low", 1: "middle", 2: "high"}
INT_TO_NOTE_MAP = {0: "Bb", 1: "B", 2: "C", 3: "Db", 4: "D", 5: "Eb", 6: "E", 7: "F", 8: "F#", 9: "G", 10: "Ab", 11: "A"}
NOTE_TO_INT_MAP = {"Bb": 0, "B": 1, "C": 2, "Db": 3, "D": 4, "Eb": 5, "E": 6, "F": 7, "F#": 8, "G": 9, "Ab": 10, "A": 11}

# Randomize the note we start on, in key for keyed exercises, chromatically for chromatic exercise
# (no need to cover all per routine)
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
        random_starting_note_int = random.randint(0, NUM_ALLOWED_CHROMATIC_STARTING_NOTES)
        register = REGISTER_MAP[random_starting_note_int // 12]
        note_name = INT_TO_NOTE_MAP[random_starting_note_int % 12]

    return f"{register} {note_name}"


# For keyed exercises, randomize which key we play
# (must cover all)
def randomize_key(keys: list = None) -> str:
    if keys is None:
        keys = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]
    return random.choice(keys)

# For exercises where we can play a cell/pattern and then rise/fall by a certain interval, randomize these
# (must cover all)
def randomize_interval(max_interval: int = 0) -> int:
    return random.randint(1, max_interval)

# Randomize which nth note we place on the downbeat in an N-note pattern
# (no need to cover all per routine)
def randomize_displacement(number_of_notes: int = 0) -> int:
    return random.randint(0, number_of_notes - 1)

# Randomize which subdivision we start on in M notes per beat
# (no need to cover all per routine)
def randomize_offset(notes_per_beat: int = 0) -> int:
    return random.randint(0, notes_per_beat - 1)

# Randomize articulation patterns
# (Do not need to cover all per routine)
def randomize_articulation(notes_per_beat: int = 0) -> int:

    number_of_possible_articulations = 2 ** notes_per_beat
    num_articulations_int = random.randint(0, number_of_possible_articulations)

    binary_articulations_int = bin(num_articulations_int)[2:]
    binary_articulations_int = "0" * (notes_per_beat - len(binary_articulations_int)) + binary_articulations_int
    articulated_notes = [i + 1 for i in range(notes_per_beat) if binary_articulations_int[i] == "1"]

    return tuple(articulated_notes)

# In patterns with allowed inversions (e.g. arpeggios), randomize the chosen inversions
def randomize_inversion(inversions: List = None) -> int:
    return random.choice(inversions) if inversions is not None else None

# In an up, down, up-down, down-up fashion, randomize all possible inversion patterns
# (must cover all)
def randomize_inverted(invertible: bool = False) -> bool:
    return random.choice(["Up", "Down", "Up-Down", "Down-Up"]) if invertible else None
