def text_input_to_approximate_truth(input: str) -> bool:
    return input in (1, True) or "y" in input.lower()
