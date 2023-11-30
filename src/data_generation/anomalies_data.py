import random
import faker
# random.seed(0)

fake = faker.Faker('de_DE')


dic_char = {
 'a': 'i', 'b': 'f', 'c': '2', 'd': '0', 'e': 'a', 'f': 'v', 'g': 'y', 'h': 'r',
 'i': 'o', 'j': 'x', 'k': 'g', 'l': 'u', 'm': '5', 'n': 'q', 'o': 'e', 'p': 'h',
 'q': 'a', 'r': '6', 's': 'b', 't': 'n', 'u': 'l', 'v': 'm', 'w': '1', 'x': 't',
 'y': '9', 'z': '7', '0': '4', '1': 'c', '2': 'p', '3': 's', '4': '8', '5': '3',
 '6': 'z', '7': 'w', '8': 'd', '9': 'k'
}

def create_typo_in_item(item):
    """
    Introduces a random typo into a given string.

    This function randomly selects one of four typo types (swap, drop, repeat, replace)
    and applies it at a random position within the string. The types of typos are:
    - 'swap': Swaps two adjacent characters.
    - 'drop': Removes a character.
    - 'repeat': Repeats a character.
    - 'replace': Replaces a character with another character, based on a predefined mapping.

    Parameters:
    item (str): The string in which to create a typo.

    Returns:
    str: The modified string with a typo.

    Note: The 'replace' typo type relies on a global dictionary 'dic_char' that maps characters
    to their replacements. This dictionary needs to be defined in the scope where the function is used.
    """

    # Choose a random position for the typo
    pos = random.randint(0, len(item) - 1)
    typo_type = random.choice(['swap', 'drop', 'repeat', 'replace'])

    if typo_type == 'swap':
        # Ensuring there's a character to swap with
        swap_with = pos + 1 if pos < len(item) - 1 else pos - 1
        item = item[:pos] + item[swap_with] + item[pos] + item[swap_with+1:]
    elif typo_type == 'drop':
        item = item[:pos] + item[pos+1:]
    elif typo_type == 'repeat':
        item = item[:pos] + item[pos] + item[pos:]
    elif typo_type == 'replace':
        item = item[:pos] + dic_char.get(item[pos], item[pos]) + item[pos + 1:]

    return item


def create_typo_in_full_name(full_name):
    """
    Randomly modifies a full name by performing an action like swapping names,
    abbreviating, introducing a typo, omitting a part, or making no change.

    The function randomly chooses one of the following actions:
    - 'swap': Swaps the first and last names.
    - 'abbreviate': Abbreviates the first, last, or both names to their initials.
    - 'typo': Introduces a typo in one of the name parts.
    - 'omit': Removes a part of the name.
    - 'nochange': Leaves the name unchanged.

    Parameters:
    full_name (str): The full name to be modified.

    Returns:
    str: The modified full name.
    """
    words = full_name.split()

    # Randomly choose an action: swap, abbreviate, or typo
    action = random.choice(['swap', 'abbreviate', 'typo', 'omit', 'nochange'])

    if action == 'omit':
        # Omit a random part of the address
        del words[random.randint(0, len(words) - 1)]
    elif action == 'swap':
        # Swap first and last names
        words[0], words[-1] = words[-1], words[0]
    elif action == 'abbreviate':
        # Choose a part to abbreviate
        abbreviation_style = random.choice(['first', 'last', 'both'])
        if abbreviation_style == 'first':
            words[0] = words[0][0] + '.'
        elif abbreviation_style == 'last':
            words[-1] = words[-1][0] + '.'
        elif abbreviation_style == 'both':
            words = [word[0] + '.' for word in words]
    elif action == 'typo':
        # Choose a random word to introduce a typo
        word_pos = random.randint(0, len(words) - 1)
        words[word_pos] = create_typo_in_item(words[word_pos])
    else:
      words = words

    return ' '.join(words)


def create_typo_in_email(email):
    """
    Introduces a typo into either the local part or the domain of an email address.

    The function randomly decides to alter either the local part (before the '@') or the domain (after the '@') of the email address. It then applies a typo modification to the chosen part.

    Parameters:
    email (str): The email address to be modified.

    Returns:
    str: The email address with a typo introduced in either its local part or domain.
    """

    local_part, domain = email.split('@')

    # Directly incorporate the random choice into the if-else condition
    if random.choice(['local', 'domain']) == 'local':
        local_part = create_typo_in_item(local_part)  # Apply typo to local part
    else:
        domain = create_typo_in_item(domain)  # Apply typo to domain

    return f"{local_part}@{domain}"

def create_typo_in_address(address):
    """
    Randomly modifies an address by either omitting a part, introducing a typo, or making no change.

    The function chooses one of the following actions at random:
    - 'omit': Removes a randomly selected part of the address.
    - 'typo': Introduces a typo into a randomly selected part of the address.
    - 'nochange': Leaves the address unchanged.

    Parameters:
    address (str): The address string to be modified.

    Returns:
    str: The modified address with either a part omitted, a typo introduced, or unchanged.
    """
    words = address.split()

    # Randomly choose an action: omit or typo
    action = random.choice(['omit', 'typo', 'nochange'])

    if action == 'omit':
        # Omit a random part of the address
        del words[random.randint(0, len(words) - 1)]
    elif action == 'typo':
        # Randomly choose a part of the address for the typo
        typo_index = random.randint(0, len(words) - 1)
        # Apply typo to the chosen part
        words[typo_index] = create_typo_in_item(words[typo_index])
    else:
      words = words

    return ' '.join(words)


    if __name__ == '__main__':
        print(create_typo_in_full_name('Anita Okoh'))
        print(create_typo_in_email('ty.sed@yahoo.com'))
        print(create_typo_in_address('Gerorgia 1a 12345 Berlin'))
