import data

def get_user_choice(characters):
    while True:
        count = 0
        for character in characters:
            count += 1
            print(f"{count}. {character}")
        user_input = input("Enter the number for your choice (or 'z' to go back): ")
        if user_input.lower() == 'z':
            print("Going back...")
            return None
        try:
            choice = int(user_input)
            if 1 <= choice <= len(characters):
                return choice
            else:
                print(f"\033[31mPlease enter a number between 1 and {len(characters)}.\033[0m")
        except ValueError:
            print("\033[31mInvalid input. Please enter a number or 'z' to go back.\033[0m")

def record_action(characters, matrix):
    action_names, action_names_abbr = data.get_action_list()
    action_choice = select_action(action_names)

    if action_choice not in action_names:
        return matrix

    action = action_names_abbr[action_choice]
    actor = select_character(characters, "acting")
    if actor is None:
        return matrix
    target = select_character(characters, "target")
    if target is None:
        return matrix
    if actor == target:
        print("\033[31mCannot act on self. Please try again.\033[0m")
        return matrix
    actor_name = characters[actor - 1]
    target_name = characters[target - 1]

    matrix[actor - 1][target - 1].append(action)
    print(f"Recorded: {actor_name} {action} {target_name}")
    return matrix

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

    action_choice = input("Select a role by number: ").strip()
    if action_choice.lower() == 'z':
        print("Returning to main menu...")
        return None

    try:
        action_choice = int(action_choice)
        return action_choice
    except ValueError:
        print("\033[31mInvalid input. Try again.\033[0m")
        return None

def select_character(characters, role_type):
    print(f"Select the {role_type} character:")
    return get_user_choice(characters)

def assign_roles(characters, words_to_color):
    role_symbols, role_names = data.get_roles_list()
    while True:
        print("\nAssign or Remove Roles:")
        for key in role_names:
            print(f"{key}. {role_names[key]} ({role_symbols[key]})")
        print("z. Go back")

        role_choice = input("Select a role by number: ").strip()
        if role_choice.lower() == 'z':
            print("Returning to main menu...")
            return characters, words_to_color

        try:
            role_choice = int(role_choice)
            if role_choice not in role_symbols:
                print("Invalid role choice. Try again.")
                continue
        except ValueError:
            print("\033[31mInvalid input. Try again.\033[0m")
            continue

        char_index = select_character(characters, "assign/remove")
        if char_index is None:
            continue  
        char_index -= 1

        if role_choice in [9, 10]:
            original_characters_list = data.get_character_list()
            character = original_characters_list[char_index]
            if character in words_to_color:
                words_to_color.pop(character)
            else:
                if role_choice == 9:
                    words_to_color[character] = "\033[31m"
                elif role_choice == 10:
                    words_to_color[character] = "\033[34m"
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