import data
import table_rendering
import handle_text

t = handle_text.HandleText()
        
def act():
    action_choice = data.DEFAULT
    while True:
        common = True
        action_choice = select_action()
        if action_choice == data.Z:
            return
        elif action_choice not in data.action_names:
            continue
        option = data.action_names[action_choice]

        if action_choice == data.VOTE:
            action_choice, common = vote(option)
        if common == True:
            actor, record, action_choice = get_actor(option, action_choice)
            target, record, action_choice = get_target(actor, action_choice, record)
            if record == True:
                record_action(action_choice, actor, target, option)

def vote(option):
    action_choice = data.VOTE
    common = False
    t.print("1. \033[91mStart the vote!\033[0m")
    t.print("2. Vote")
    t.print("z. Go back")
    vote_choice = t.input("Select an action by number: ").strip()
    if vote_choice == '1':
        for num, char in data.characters.items():
            if char != " " and char[:2] != "Me" and char not in data.words_to_color:
                target = 0
                while target != data.INVALID:
                    target, record, action_choice = get_target(num, action_choice)
                    if action_choice == data.Z:
                        return data.DEFAULT, False
                    elif record == True:
                        record_action(action_choice, num, target, option)
                        break
    elif vote_choice == '2':
        common = True
    elif vote_choice.lower() == 'z':
        action_choice = data.DEFAULT
    return action_choice, common

def get_actor(option, action_choice):
    actor = select_character("acting", option)
    if actor is data.Z:
        action_choice = data.DEFAULT
        record = False
    else:
        record = True
    return actor, record, action_choice

def get_target(actor, action_choice, record = True):
    if record == False:
        return data.INVALID, record, data.INVALID
    target = select_character("target", f"Acting character: \033[91m{data.characters[actor]}\033[0m")
    if target is data.Z:
        action_choice = data.DEFAULT
        record = False
    elif actor == target:
        t.print("\033[31mCannot act on self. Please try again.\033[0m")
        record = False
    else: 
        record = True
    return target, record, action_choice
    
def record_action(action_choice, actor, target, option):
    action = data.action_names_abbr[action_choice]
    data.matrix[actor - 1][target - 1].append(action)
    target_name = data.characters[target]
    t.printr(f"\033[92mRecorded:\033[0m {data.characters[actor]} {option} {target_name}")

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

        if actions:
            removed_action = actions.pop()
            key = next((k for k, v in data.action_names_abbr.items() if v == removed_action), None)
            if key:
                removed_action = data.action_names.get(key)
            t.printr(f"\033[91mDeleted:\033[0m {actor_name} {removed_action} {target_name}")
        else:
            t.print(f"No actions recorded between {actor_name} and {target_name}.")

def select_action():
    while True:
        t.print("Select the action performed:")
        for number, action_name in data.action_names.items():
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
    while True:
        if option:
            t.print(f"{option}")
        t.print(f"Select the {role_type} character.")
        # display_characters()
        user_input = t.input("Enter the number for your choice (or 'z' to go back): ")
        if user_input.lower() == 'z':
            return data.Z
        choice = validate_choice(user_input)
        if choice is not data.INVALID:
            return choice

def assign_roles():
    while True:
        t.print("\033[92mAssign or Remove Roles:\033[0m")
        display_roles()
        role_choice = t.input("Select a role by number: ").strip()

        if role_choice.lower() == 'z':
            return

        role_choice = validate_role_choice(role_choice)
        if role_choice is data.INVALID:
            continue
        
        char_index = select_character("assign/remove", f"\033[92mAssign\033[0m/\033[91mremove\033[0m a role ({data.role_symbols[role_choice]}): ")
        if char_index is data.Z:
            continue  

        handle_role_assignment(role_choice, char_index)

def display_roles():
    for key in data.role_names:
        t.print(f"{key}. {data.role_names[key]} ({data.role_symbols[key]})")
    t.print("z. Go back")

def validate_role_choice(role_choice):
    try:
        role_choice = int(role_choice)
        if role_choice not in data.role_symbols:
            t.print("\033[31mInvalid role choice. Try again.\033[0m")
            return data.INVALID
        return role_choice
    except ValueError:
        t.print("\033[31mInvalid input. Try again.\033[0m")
        return data.INVALID

def handle_role_assignment(role_choice, char_index):
    if role_choice in [9, 10]:
        toggle_color(char_index, role_choice)
    else:
        symbol = data.role_symbols[role_choice]
        toggle_role(char_index, symbol, data.role_names[role_choice])

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
        if choice == data.Z:
            return
        elif len(data.characters.keys()) - list(data.characters.values()).count(" ") <= 2:
            t.printr("\033[31mThere should be at least 2 characters in the list.\033[0m")
        elif data.characters[choice][:2] == "Me":
            t.printr("\033[31mCannot remove the character of player.\033[0m")
        else:
            data.removed_characters[choice] = data.characters[choice]
            data.characters[choice] = " "
            t.printr(f"\033[31mRemoved\033[0m {data.removed_characters[choice]} from the list.")

def restore_removed_characters():
    for number, character in data.removed_characters.items():
        data.characters[number] = character
        t.printr(f"\033[94mRestored\033[0m {character} to the list.")
    data.removed_characters = {}

def exit_program():
    print("Exiting...")
    exit(0)