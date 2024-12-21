import data
import table_rendering
import handle_text

t = handle_text.HandleText()

def record_action():
    action_names, action_names_abbr = data.get_action_list()
    action_choice = data.DEFAULT
    first = True
    while True:
        if action_choice == data.VOTE:
            first = False
        else:
            action_choice = select_action(action_names)
            if action_choice == data.Z:
                return
            elif action_choice not in action_names:
                continue

        option = action_names[action_choice]
        actor = select_character("acting", option)

        if actor is data.Z:
            if not first:
                return
            else:
                action_choice = data.DEFAULT
                continue
        
        actor_name = data.characters[actor]
        target = select_character("target", f"Acting character: {actor_name}")

        if target is data.Z:
            action_choice = data.DEFAULT
            continue

        if actor == target:
            t.print("\033[31mCannot act on self. Please try again.\033[0m")
            continue

        action = action_names_abbr[action_choice]
        data.matrix[actor - 1][target - 1].append(action)
        target_name = data.characters[target]
        t.printr(f"\033[92mRecorded:\033[0m {actor_name} {option} {target_name}")

def get_user_choice():
    while True:
        display_characters()
        user_input = t.input("Enter the number for your choice (or 'z' to go back): ")
        if user_input.lower() == 'z':
            return data.Z
        choice = validate_choice(user_input)
        if choice is not data.INVALID:
            return choice

def display_characters():
    for number, character in data.characters.items():
        if character != " ":
            t.print(f"{number}. {character}")

def validate_choice(user_input):
    try:
        choice = int(user_input)
        if choice in data.characters.keys():
            if " " not in data.characters[choice]:
                return choice
            elif " " in data.characters[choice]:
                t.print("\033[31mRemoved character cannot be selected.\033[0m")
        else:
            t.print(f"\033[31mPlease enter a number between 1 and {max(data.characters.keys())}: \033[0m ")
    except ValueError:
        t.print("\033[31mInvalid input. Please enter a number or 'z' to go back.\033[0m")
    return data.INVALID

def delete_recent_action():
    while True:
        table_rendering.print_table()
        actor = select_character("actor")
        if actor is data.Z:
            return

        actor_name = data.characters[actor]
        target = select_character("target", f"Acting character: {actor_name}")
        if target is data.Z:
            return

        target_name = data.characters[target]
        actions = data.matrix[actor - 1][target - 1]
        action_names, action_names_abbr = data.get_action_list()

        if actions:
            removed_action = actions.pop()
            key = next((k for k, v in action_names_abbr.items() if v == removed_action), None)
            if key:
                removed_action = action_names.get(key)
            t.printr(f"\033[91mDeleted:\033[0m {actor_name} {removed_action} {target_name}")
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
            return data.Z
        try:
            return int(action_choice)
        except ValueError:
            t.print("\033[31mInvalid input. Try again.\033[0m")

def select_character(role_type, option = None):
    if option:
        t.print(f"{option}")
    t.print(f"Select the {role_type} character:")
    return get_user_choice()

def assign_roles():
    role_symbols, role_names = data.get_roles_list()
    while True:
        t.print("\033[92mAssign or Remove Roles:\033[0m")
        display_roles(role_names, role_symbols)
        role_choice = t.input("Select a role by number: ").strip()

        if role_choice.lower() == 'z':
            return

        role_choice = validate_role_choice(role_choice, role_symbols)
        if role_choice is data.INVALID:
            continue
        
        char_index = select_character("assign/remove", "\033[92mAssign/remove a role: \033[0m")
        if char_index is data.Z:
            continue  

        handle_role_assignment(
            role_choice, char_index, role_symbols, role_names
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

def handle_role_assignment(role_choice, char_index, role_symbols, role_names):
    if role_choice in [9, 10]:
        toggle_color(char_index, role_choice)
    else:
        symbol = role_symbols[role_choice]
        toggle_role(char_index, symbol, role_names[role_choice])

def toggle_role(char_index, symbol, role_name):
    if symbol in data.characters[char_index]:
        data.characters[char_index] = data.characters[char_index].replace(symbol, "")
        t.printr(f"\033[91mRemoved\033[0m {role_name} ({symbol}) from {data.characters[char_index]}.")
    else:
        data.characters[char_index] += symbol
        t.printr(f"\033[94mAssigned\033[0m {role_name} ({symbol}) to {data.get_character_list()[char_index]}.")

def toggle_color(char_index, role_choice):
    character = data.get_character_list()[char_index]

    if role_choice == 9:
        color_code = "\033[31m"
        state = "\033[31mkilled\033[0m"
    else:
        color_code = "\033[34m"
        state = "\033[34mcold sleeped\033[0m"

    if character in data.words_to_color:
        removed_color = data.words_to_color.pop(character)
        if color_code == removed_color:
            t.printr(f"{character} is released from the state of being excepted.")
            return

    data.words_to_color[character] = color_code
    t.printr(f"{character} is {state}.")

def remove_character_from_list():
    while True:
        table_rendering.print_table()
        option = "\033[31mRemove character\033[0m"
        choice = select_character("target", option)
        if choice == None:
            return
        else:
            data.removed_characters[choice] = data.characters[choice]
            data.characters[choice] = " "

def restore_removed_characters():
    for number, character in data.removed_characters.items():
                data.characters[number] = character
    data.removed_characters = {}

def exit_program():
    print("Exiting...")
    exit(0)