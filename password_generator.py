import string
import secrets


AMBIGUOUS_CHARACTERS = "0Ol1"


def generate_password(
    length,
    use_uppercase,
    use_lowercase,
    use_numbers,
    use_symbols,
    exclude_ambiguous=False
):
    """Generate a cryptographically secure password."""

    if not isinstance(length, int) or isinstance(length, bool):
        raise ValueError("Length must be a whole number.")

    if not 8 <= length <= 128:
        raise ValueError("Length must be between 8 and 128.")

    character_sets = []

    if use_uppercase:
        character_sets.append(string.ascii_uppercase)

    if use_lowercase:
        character_sets.append(string.ascii_lowercase)

    if use_numbers:
        character_sets.append(string.digits)

    if use_symbols:
        character_sets.append(string.punctuation)

    if len(character_sets) < 2:
        raise ValueError("Select at least two character types.")

    if exclude_ambiguous:
        character_sets = [
            "".join(c for c in chars if c not in AMBIGUOUS_CHARACTERS)
            for chars in character_sets
        ]

    if any(not chars for chars in character_sets):
        raise ValueError("A selected type has no available characters.")

    all_characters = "".join(character_sets)

    # Guarantee one character from every selected category.
    password = [
        secrets.choice(chars)
        for chars in character_sets
    ]

    # Fill the remaining positions.
    password.extend(
        secrets.choice(all_characters)
        for _ in range(length - len(password))
    )

    # Securely shuffle the characters.
    secrets.SystemRandom().shuffle(password)

    return "".join(password)
