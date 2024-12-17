import data

def get_user_choice(characters):
    while True:
        display_characters(characters)
        user_input = input("Enter the number for your choice (or 'z' to go back): ")
        if user_input.lower() == 'z':
            print("Going back...")
            return None
        choice = validate_choice(user_input, characters)
        if choice is not None:
            return choice

def display_characters(characters):
    for number, character in characters.items():
        if character != " ":
            print(f"{number}. {character}")

def validate_choice(user_input, characters):
    try:
        choice = int(user_input)
        if choice in characters and " " not in characters[choice]:
            return choice
        elif " " in characters[choice]:
            print("\033[31mRemoved character cannot be selected.\033[0m")
        else:
            print(f"\033[31mPlease enter a number between 1 and {max(characters.keys())}.\033[0m")
    except ValueError:
        print("\033[31mInvalid input. Please enter a number or 'z' to go back.\033[0m")
    return None

def record_action(characters, matrix):
    action_names, action_names_abbr = data.get_action_list()
    action_choice = -1
    while True:
        if action_choice != 1:
            action_choice = select_action(action_names)

        if action_choice == -1:
            return matrix
        elif action_choice not in action_names:
            continue

        action = action_names_abbr[action_choice]
        actor = select_character(characters, "acting")
        if actor is None:
            action_choice = -1
            continue

        target = select_character(characters, "target")
        if target is None:
            action_choice = -1
            continue

        if actor == target:
            print("\033[31mCannot act on self. Please try again.\033[0m")
            continue

        actor_name = characters[actor]
        target_name = characters[target]
        matrix[actor - 1][target - 1].append(action)
        print(f"Recorded: {actor_name} {action} {target_name}")

def delete_recent_action(characters, matrix):
    print("\nDelete the most recent action from a character pair:")
    actor = select_character(characters, "actor")
    if actor is None:
        return matrix

    target = select_character(characters, "target")
    if target is None:
        return matrix

    actor_name = characters[actor - 1]
    target_name = characters[target - 1]
    actions = matrix[actor - 1][target - 1]

    if actions:
        removed_action = actions.pop()
        print(f"Deleted: {actor_name} {removed_action} {target_name}")
    else:
        print(f"No actions recorded between {actor_name} and {target_name}.")
    
    return matrix

def select_action(action_names):
    print("\nSelect the action performed:")
    for number, action_name in action_names.items():
        print(f"{number}. {action_name}")
    print("z. Go back")

    action_choice = input("Select an action by number: ").strip()
    if action_choice.lower() == 'z':
        return -1

    try:
        return int(action_choice)
    except ValueError:
        print("\033[31mInvalid input. Try again.\033[0m")
        return None

def select_character(characters, role_type):
    print(f"Select the {role_type} character:")
    return get_user_choice(characters)

def assign_roles(characters, original_characters_list, words_to_color):
    role_symbols, role_names = data.get_roles_list()
    while True:
        print("\nAssign or Remove Roles:")
        display_roles(role_names, role_symbols)
        role_choice = input("Select a role by number: ").strip()

        if role_choice.lower() == 'z':
            print("Returning to main menu...")
            return characters, original_characters_list, words_to_color

        role_choice = validate_role_choice(role_choice, role_symbols)
        if role_choice is None:
            continue

        char_index = select_character(characters, "assign/remove")
        if char_index is None:
            continue  

        characters, words_to_color = handle_role_assignment(
            characters, original_characters_list, words_to_color, role_choice, char_index, role_symbols, role_names
        )

def display_roles(role_names, role_symbols):
    for key in role_names:
        print(f"{key}. {role_names[key]} ({role_symbols[key]})")
    print("z. Go back")

def validate_role_choice(role_choice, role_symbols):
    try:
        role_choice = int(role_choice)
        if role_choice not in role_symbols:
            print("Invalid role choice. Try again.")
            return None
        return role_choice
    except ValueError:
        print("\033[31mInvalid input. Try again.\033[0m")
        return None

def handle_role_assignment(characters, original_characters_list, words_to_color, role_choice, char_index, role_symbols, role_names):
    if role_choice in [9, 10]:
        character = original_characters_list[char_index]
        if character in words_to_color:
            words_to_color.pop(character)
        else:
            color_code = "\033[31m" if role_choice == 9 else "\033[34m"
            words_to_color[character] = color_code
    else:
        symbol = role_symbols[role_choice]
        characters = toggle_role(characters, char_index, symbol, role_names[role_choice])
    
    return characters, words_to_color

def toggle_role(characters, char_index, symbol, role_name):
    if symbol in characters[char_index]:
        characters[char_index] = characters[char_index].replace(symbol, "")
        print(f"Removed {role_name} ({symbol}) from {characters[char_index]}.")
    else:
        characters[char_index] += symbol
        print(f"Assigned {role_name} ({symbol}) to {characters[char_index]}.")
    return characters

def remove_character_from_list(characters, original_characters_list, words_to_color):
    while True:
        choice = get_user_choice(characters)
        if choice == None:
            return characters, original_characters_list, words_to_color
        else:
            characters[choice] = " "