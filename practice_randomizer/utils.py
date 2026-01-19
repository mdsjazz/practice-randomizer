from typing import Any

def text_input_to_approximate_truth(input: str) -> bool:
    return input in (1, True) or "y" in input.lower()

class dotdict(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'") from e

    def __setattr__(self, key: str, value: Any):
        self[key] = value

    def __delattr__(self, key: str) -> None:
        try:
            del self[key]
        except KeyError as e:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'") from e

    @classmethod
    def fromdict(cls, dictionary: dict):
        dot_dict = cls() 
        for k, v in dictionary.items():
            dot_dict[k] = v

        return dot_dict
