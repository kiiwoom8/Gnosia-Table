import data
import handle_text

t = handle_text.HandleText()

def get_user_choice(characters):
    while True:
        display_characters(characters)
        user_input = t.input("Enter the number for your choice (or 'z' to go back): ")
        if user_input.lower() == 'z':
            return None
        choice = validate_choice(user_input, characters)
        if choice is not None:
            return choice

def display_characters(characters):
    for number, character in characters.items():
        if character != " ":
            t.print(f"{number}. {character}")

def validate_choice(user_input, characters):
    try:
        choice = int(user_input)
        if choice in characters.keys():
            if " " not in characters[choice]:
                return choice
            elif " " in characters[choice]:
                t.print("\033[31mRemoved character cannot be selected.\033[0m")
        else:
            t.print(f"\033[31mPlease enter a number between 1 and {max(characters.keys())}: \033[0m ")
    except ValueError:
        t.print("\033[31mInvalid input. Please enter a number or 'z' to go back.\033[0m")
    return None

def record_action(characters, matrix):
    action_names, action_names_abbr = data.get_action_list()
    action_choice = -1
    while True:
        if action_choice != 1:
            action_choice = select_action(action_names)
        
        if action_choice == -1:
            return
        elif action_choice not in action_names:
            continue

        action = action_names_abbr[action_choice]
        option = action_names[action_choice]

        actor = select_character(characters, "acting", option)

        if actor is None:
            action_choice = -1
            continue
        
        actor_name = characters[actor]
        if not actor_name:
            actor_name = "\033[91mNone\033[0m"
        target = select_character(characters, "target", f"Acting character: {actor_name}")
        if target is None:
            action_choice = -1
            continue

        if actor == target:
            t.print("\033[31mCannot act on self. Please try again.\033[0m")
            continue

        target_name = characters[target]
        matrix[actor - 1][target - 1].append(action)
        print(f"Recorded: {actor_name} {option} {target_name}")

def delete_recent_action(characters, matrix):
    while True:
        actor = select_character(characters, "actor")
        if actor is None:
            return

        target = select_character(characters, "target")
        if target is None:
            return

        actor_name = characters[actor]
        target_name = characters[target]
        actions = matrix[actor - 1][target - 1]
        action_names, action_names_abbr = data.get_action_list()
        if actions:
            removed_action = actions.pop()
            key = next((k for k, v in action_names_abbr.items() if v == removed_action), None)
            if key:
                removed_action = action_names.get(key)
            print(f"Deleted: {actor_name} {removed_action} {target_name}")
        else:
            t.print(f"No actions recorded between {actor_name} and {target_name}.")

def select_action(action_names):
    while True:
        t.print("Select the action performed:")
        for number, action_name in action_names.items():
            t.print(f"{number}. {action_name}")
        t.print("z. Go back")

        action_choice = t.input("Select an action by number: ").strip()

        if action_choice.lower() == 'z':
            return -1
        try:
            return int(action_choice)
        except ValueError:
            t.print("\033[31mInvalid input. Try again.\033[0m")

def select_character(characters, role_type, option = None):
    if option:
        t.print(f"{option}")
    t.print(f"Select the {role_type} character:")
    return get_user_choice(characters)

def assign_roles(characters, original_characters_list, words_to_color):
    role_symbols, role_names = data.get_roles_list()
    while True:
        t.print("\033[92mAssign or Remove Roles:\033[0m")
        display_roles(role_names, role_symbols)
        role_choice = t.input("Select a role by number: ").strip()

        if role_choice.lower() == 'z':
            return

        role_choice = validate_role_choice(role_choice, role_symbols)
        if role_choice is None:
            continue
        
        char_index = select_character(characters, "assign/remove", "\033[92mAssign/remove a role: \033[0m")
        if char_index is None:
            continue  

        characters, words_to_color = handle_role_assignment(
            characters, original_characters_list, words_to_color, role_choice, char_index, role_symbols, role_names
        )

def display_roles(role_names, role_symbols):
    for key in role_names:
        t.print(f"{key}. {role_names[key]} ({role_symbols[key]})")
    t.print("z. Go back")

def validate_role_choice(role_choice, role_symbols):
    try:
        role_choice = int(role_choice)
        if role_choice not in role_symbols:
            t.print("Invalid role choice. Try again.")
            return None
        return role_choice
    except ValueError:
        t.print("\033[31mInvalid input. Try again.\033[0m")
        return None

def handle_role_assignment(characters, original_characters_list, words_to_color, role_choice, char_index, role_symbols, role_names):
    if role_choice in [9, 10]:
        toggle_color(original_characters_list, char_index, words_to_color, role_choice)
    else:
        symbol = role_symbols[role_choice]
        characters = toggle_role(characters, original_characters_list, char_index, symbol, role_names[role_choice])
    
    return characters, words_to_color

def toggle_role(characters, original_characters_list, char_index, symbol, role_name):
    if symbol in characters[char_index]:
        characters[char_index] = characters[char_index].replace(symbol, "")
        print(f"Removed {role_name} ({symbol}) from {characters[char_index]}.")
    else:
        characters[char_index] += symbol
        print(f"Assigned {role_name} ({symbol}) to {original_characters_list[char_index]}.")
    return characters

def toggle_color(original_characters_list, char_index, words_to_color, role_choice):
    character = original_characters_list[char_index]
    if character in words_to_color:
        words_to_color.pop(character)
        print(f"{character} is released from the state of being excepted.")
    else:
        if role_choice == 9:
            color_code = "\033[31m"
            state = "\033[31mkilled\033[0m"
        else:
            color_code = "\033[34m"
            state = "\033[34mcold sleeped\033[0m"
            
        words_to_color[character] = color_code
        print(f"{character} is {state}.")
    return words_to_color

def remove_character_from_list(characters, original_characters_list, removed_characters, words_to_color):
    while True:
        option = "\033[31mRemove character\033[0m"
        choice = select_character(characters, "target", option)
        if choice == None:
            return
        else:
            removed_characters[choice] = characters[choice]
            characters[choice] = " "

def restore_removed_characters(characters, removed_characters):
    for number, character in removed_characters.items():
                characters[number] = character
    removed_characters = {}