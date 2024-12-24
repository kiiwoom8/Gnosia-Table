import data
import table_rendering
import handle_text

t = handle_text.HandleText()
        
def act():
    while True:
        action_choice = select_action()
        if action_choice == 'z':
            return
        action_choice = int(action_choice)
        action_name = data.action_list[action_choice]["Name"]
        (handle_vote if action_choice == data.VOTE else record_action)(action_choice, action_name)

def record_action(action_choice: int, action_name: str, actor_target: list = []):
    if actor_target:
        actor, target = actor_target
    else:
        actor = select_character("acting", action_name)
        if  actor in ['z', 'p']:
            return
        actor = int(actor)
        target = get_target(actor)
        if target in ['z', 'p']:
            return
        target = int(target)
        
    action = data.action_list.get(action_choice, {}).get("Abbr")
    if not action:
        t.print("\033[91mError: Invalid action choice.\033[0m")
        return

    data.matrix[actor - 1][target - 1].append(action)
    target_name = data.characters.get(target, "Unknown Target")
    t.printr(f"\033[92mRecorded:\033[0m {data.characters[actor]} {action_name} {target_name}")

def handle_vote(action_choice, action_name):
    while True:
        t.print("1. \033[91mStart the vote!\033[0m")
        t.print("2. Vote")
        t.print("z. Go back")
        
        vote_menu_choice = t.input("Select an action by number: ")
        if vote_menu_choice == '1':
            for char_index, char_name in data.characters.items():
                if char_name != " " and not char_name.startswith("Me") and char_name not in data.words_to_color:
                    target = get_target(char_index)
                    if target == 'z':
                        return False
                    elif target == 'p':
                        continue
                    else:
                        record_action(action_choice, action_name, [char_index, int(target)])
        elif vote_menu_choice == '2':
            record_action(action_choice, action_name)
        elif not vote_menu_choice:
            pass
        elif vote_menu_choice == 'z':
            return

def get_target(actor):
    while True:
        target = select_character("target", f"Acting character: \033[91m{data.characters[actor]}\033[0m")
        if actor == target:
            t.print("\033[31mCannot act on self. Please try again.\033[0m")
        else:
            return target
    
def display_characters():
    for number, character in data.characters.items():
        if character != " ":
            t.print(f"{number}. {character}")

def validate_choice(user_input:str, choice_type='character'):
    if user_input.isdigit():
        choice = int(user_input)
        valid_data = data.characters if choice_type == 'character' else data.roles
        if choice in valid_data and (choice_type != 'character' or " " not in valid_data[choice]) or not user_input:
            return choice
        else:
            return False
    else:
        return False

def delete_recent_action():
    while True:
        table_rendering.print_table()
        actor = select_character("actor")
        if actor in ['z', 'p']:
            return
        else:
            actor = int(actor)

        actor_name = data.characters[actor]
        target = select_character("target", f"Acting character: \033[91m{data.characters[actor]}\033[0m")
        if target == 'z':
            return
        else:
            target = int(target)

        target_name = data.characters[target]
        actions = data.matrix[actor - 1][target - 1]

        if actions:
            removed_action = actions.pop()
            key = next((action_num for action_num, action in data.action_list.items() if action["Abbr"] == removed_action), None)
            if key:
                removed_action = data.action_list[key]
            t.printr(f"\033[91mDeleted:\033[0m {actor_name} {removed_action['Name']} {target_name}")

def select_action():
    while True:
        t.check_error()
        t.print("Select the action performed:")
        for action_num, action in data.action_list.items():
            t.print(f"{action_num}. {action['Name']}")
        t.print("z. Go back")

        action_choice = t.input("Select an action by number: ")

        if (action_choice.isdigit() and int(action_choice) in data.action_list) or action_choice == 'z':
            return action_choice
        elif not action_choice:
            pass
        else:
            t.error_text = "\033[31mInvalid choice. Try again.\033[0m"

def select_character(role_type, action_name=None):
    while True:
        t.check_error()
        if action_name:
            t.print(action_name)
        t.print(f"Select the {role_type} character:")
        user_input = t.input("Enter the number for your choice (OR 'p' to pass OR 'z' to go back): ")
        if user_input in ['z', 'p']:
            return user_input
        elif (validate_choice(user_input)):
            return user_input
        elif not user_input:
            pass
        else:
            t.error_text = "\033[31mInvalid choice. Try again.\033[0m"

def assign_roles():
    while True:
        t.check_error()
        t.print("\033[92mAssign\033[0m/\033[91mremove\033[0m Roles: ")
        display_roles()
        role_choice = t.input("Select a role by number: ")
        if role_choice == 'z':
            return
        elif not role_choice:
            continue
            
        if validate_choice(role_choice, 'role') == False:
            t.error_text = "\033[31mInvalid choice. Try again.\033[0m"
            continue
        else:
            role_choice = int(role_choice)
        char_index = select_character("assigned/removed", f"\033[92mAssign\033[0m/\033[91mremove\033[0m a role ({data.roles[role_choice]["Symbol"]}): ")
        if char_index in ['z', False]:
            return
        else:
            char_index = int(char_index)
            
        toggle_role(char_index, role_choice)

def display_roles():
    for role_num, role in data.roles.items():
        t.print(f"{role_num}. {role["Name"]} ({role["Symbol"]})")
    t.print("z. Go back")

def toggle_role(char_index, role_choice):
    role_name = data.roles[role_choice]["Name"]
    role_symbol = data.roles[role_choice]["Symbol"]
    if role_name in ["Killed", "Cold Sleep"]:
        toggle_color(char_index, role_choice)
        return
    if char_index in data.current_roles[role_name]:
        data.current_roles[role_name].remove(char_index)
        t.printr(f"\033[91mRemoved\033[0m {role_name} ({role_symbol}) from {data.characters[char_index]}.")
    else:
        data.current_roles[role_name].append(char_index)
        char_index = int(char_index)
        t.printr(f"\033[94mAssigned\033[0m {role_name} ({role_symbol}) to {data.characters[char_index]}.")

def toggle_color(char_index, role_choice):
    if role_choice == 9:
        color_code = "\033[31m"
        state = "\033[31mkilled\033[0m"
    elif role_choice == 10:
        color_code = "\033[34m"
        state = "\033[34mcold sleeped\033[0m"

    if data.characters[char_index] in data.words_to_color and data.words_to_color[data.characters[char_index]] == color_code:
        removed_color = data.words_to_color.pop(data.characters[char_index])
        if color_code == removed_color:
            t.printr(f"{data.characters[char_index]} is released from the state of being excepted.")
            return

    data.words_to_color[data.characters[char_index]] = color_code
    t.printr(f"{data.characters[char_index]} is {state}.")

def remove_character_from_list():
    while True:
        table_rendering.print_table()
        t.check_error()
        option = "\033[91mRemove character\033[0m"
        choice = select_character("target", option)
        if choice == 'z':
            return
        choice = int(choice)
        if len(data.characters.keys()) - list(data.characters.values()).count(" ") <= 2:
            t.error_text = "\033[31m[Failed] There should be at least 2 characters in the list.\033[0m"
        elif data.characters[choice][:2] == "Me":
            t.error_text = "\033[31mCannot remove the character of player.\033[0m"
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