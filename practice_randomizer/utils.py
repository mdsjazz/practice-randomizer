def text_input_to_approx_true(input: str) -> bool:
    return input in (1, True) or "y" in input.lower()
