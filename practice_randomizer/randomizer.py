from collections import namedtuple
from enum import Enum
from itertools import combinations
import math
import random
from typing import Literal, List

from practice_randomizer.utils import dotdict


NUM_ALLOWED_CHROMATIC_STARTING_NOTES = 31

REGISTER_MAP = {0: "low", 1: "middle", 2: "high"}

NOTE_CLASSES = ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")


class NoteToIntMap(dotdict):

    def __init__(self, instrument_key: Literal[NOTE_CLASSES] = "C", note_to_int_map: dict = None):
        if note_to_int_map is not None:
            for k, v in note_to_int_map.items():
                self[v] = k
        else:
            default_int_to_note_map = {k: v for k, v in zip(NOTE_CLASSES, range(12))}
            instrument_note_displacement = default_int_to_note_map[instrument_key]
            for k, v in default_int_to_note_map.items():
                self[k] = (v + instrument_note_displacement) % 12

class IntToNoteMap(dotdict):
   
    def __init__(self, instrument_key: Literal[NOTE_CLASSES] = "C", int_to_note_map: dict = None):
        if int_to_note_map is not None:
            for k, v in int_to_note_map.items():
                self[v] = k
        else:
            default_int_to_note_map = {k: v for k, v in zip(NOTE_CLASSES, range(12))}
            instrument_note_displacement = default_int_to_note_map[instrument_key]
            for k, v in default_int_to_note_map.items():
                self[(v + instrument_note_displacement) % 12] = k


# Randomize the note we start on, in key for keyed exercises, chromatically for chromatic exercise
# (no need to cover all per routine)
def randomize_starting_note(instrument_key: str, keyed_or_chromatic: str = "chromatic", key: list = "C", scale_notes: list = None) -> str:

    register = ""
    note_name = ""
    note_to_int_map = NoteToIntMap(instrument_key)
    int_to_note_map = IntToNoteMap(instrument_key)

    if keyed_or_chromatic == "keyed":
        key_int = note_to_int_map[key]

        key_scale_notes_ints_full_range = [
            scale_note_int + key_int + 12 * octave
            for scale_note_int in scale_notes for octave in range(-2, 3)
            if 0 <= scale_note_int + key_int + 12 * octave <= NUM_ALLOWED_CHROMATIC_STARTING_NOTES
        ]
        random_starting_note_int = random.choice(key_scale_notes_ints_full_range)
        register = REGISTER_MAP[random_starting_note_int // 12]
        note_name = int_to_note_map[random_starting_note_int % 12]

    else:
        random_starting_note_int = random.randint(0, NUM_ALLOWED_CHROMATIC_STARTING_NOTES)
        register = REGISTER_MAP[random_starting_note_int // 12]
        note_name = int_to_note_map[random_starting_note_int % 12]

    return f"{register} {note_name}"


# For keyed exercises, randomize which key we play
# (must cover all)
def randomize_key(keys: list = None) -> str:
    if keys is None:
        keys = NOTE_CLASSES
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
def randomize_inversion(number_of_notes: int) -> int:
    return random.randint(0, number_of_notes)

# In an up, down, up-down, down-up fashion, randomize all possible inversion patterns
# (must cover all)
def randomize_invert_pattern(invertible: bool = False) -> bool:
    return random.choice(["Up", "Down", "Up-Down", "Down-Up", "In-direction", "Reverse-direction"]) if invertible else None
