import data
import table_rendering
import handle_text as t
        
def act():
    while True:
        action_choice = select_action()
        if action_choice == 'z':
            return
        action_choice = int(action_choice)
        action_name = data.action_list[action_choice]["Name"]
        (handle_vote if action_choice == 1 else record_action)(action_choice, action_name)

def record_action(action_choice: int, action_name: str, actor = None, target = None):
    if not actor:
        actor = select_character("acting", action_name)
        if  actor in ['z', 'p']:
            return
        actor = int(actor)
    if not target:
        target = get_target(actor)
        if target in ['z', 'p']:
            return
        target = int(target)
        
    action = data.action_list.get(action_choice, {}).get("Abbr")
    data.matrix[actor - 1][target - 1].append(action)
    target_name = data.characters.get(target, "\033[31mUnknown\033[0m")
    t.r_print(f"\033[92mRecorded:\033[0m {data.characters[actor]} {action_name} {target_name}")

def release_ties():
    if data.ties:
        for char_index in data.ties:
            char_name = data.characters[char_index]
            if char_name in data.words_to_color:
                del data.words_to_color[char_name]
        data.ties = []

def handle_vote(action_choice, action_name):
    while True:
        t.check_error()
        t.t_print("1. \033[91mStart the vote!\033[0m")
        t.t_print("2. \033[31mVote\033[0m") 
        t.t_print("3. \033[92mRelease current votes\033[0m")
        t.t_print("z. Go back")
        
        vote_menu_choice = t.t_input("Select an action by number: ")
        match vote_menu_choice:
            case '1':
                votes = {}
                while True:
                    for char_index, char_name in data.characters.items():
                        if char_name != " "  and data.words_to_color.get(char_name) not in [data.BLUE, data.RED]:
                            target = get_target(char_index)
                            if target == 'z':
                                return False
                            if target != 'p':
                                target = int(target)
                                votes[target] = votes.get(target, 0) + 1
                                record_action(action_choice, action_name, char_index, target)
                    max_votes = max(votes.values(), default=0)
                    most_voted = [char for char, votes in votes.items() if votes == max_votes]
                    if len(most_voted) == 1:
                        release_ties()
                        t.r_print(f"{data.characters[most_voted[0]]} is {data.BLUE}cold sleeped!{data.RESET}")
                        data.words_to_color[data.characters[most_voted[0]]] = data.BLUE
                    else:
                        release_ties()
                        data.ties = most_voted
                        t.r_print("\033[91mIt's a tie! Vote again.\033[0m")
                        for char in most_voted:
                            data.words_to_color[data.characters[char]] = data.YELLOW
                    table_rendering.print_table()
                    return
            case '2':
                record_action(action_choice, action_name)
            case '3':
                if not data.ties:
                    t.error_text = "\033[31mNo votes to release.\033[0m"
                else:
                    release_ties()
                    t.r_print("\033[92mCharacters voted tie are sucessfully released.\033[0m")
            case 'z':
                return
            case '':
                pass
            case _:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"

def get_target(actor):
    while True:
        target = select_character("target", f"Acting character: {data.BLUSH}{data.characters[actor]}{data.RESET}")
        if target in ['z', 'p']:
            return target
        if actor == int(target):
            t.t_print("\033[31mCannot act on self. Please try again.\033[0m")
        elif data.ties and int(target) not in data.ties:
            t.t_print("\033[31mInvalid choice. Please try again.\033[0m")
        else:
            return target
    
def display_characters():
    for number, character in data.characters.items():
        if character != " ":
            t.t_print(f"{number}. {character}")

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
            t.r_print(f"\033[91mDeleted:\033[0m {actor_name} {removed_action['Name']} {target_name}")

def select_action():
    while True:
        t.check_error()
        t.t_print("Select the action performed:")
        for action_num, action in data.action_list.items():
            t.t_print(f"{action_num}. {action['Name']}")
        t.t_print("z. Go back")

        action_choice = t.t_input("Select an action by number: ")
        if action_choice:
            if (action_choice.isdigit() and int(action_choice) in data.action_list) or action_choice == 'z':
                return action_choice
            else:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"

def select_character(role_type, action_name=None):
    while True:
        t.check_error()
        if action_name:
            t.t_print(action_name)
        if data.ties:
            most_voted_names = [data.characters[char_index] for char_index in data.ties]
            t.t_print(f"Select the {role_type} character from the following: {most_voted_names}")            
        else:
            t.t_print(f"Select the {role_type} character:")
        user_input = t.t_input("Enter the number for your choice (OR 'p' to pass OR 'z' to go back): ")
        if user_input:
            if user_input in ['z', 'p'] or validate_choice(user_input):
                return user_input
            else:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"

def assign_roles():
    while True:
        t.check_error()
        t.t_print("\033[92mAssign\033[0m/\033[91mremove\033[0m Roles: ")
        display_roles()
        role_choice = t.t_input("Select a role by number: ")
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
        if char_index not in ['z', 'p']:
            if not char_index:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"
            else:
                toggle_role(int(char_index), role_choice)

def display_roles():
    for role_num, role in data.roles.items():
        formatted_num = f" {role_num}" if role_num < 10 else str(role_num)
        t.t_print(f"{formatted_num}. {role["Name"]} ({role["Symbol"]})")
    t.t_print("z. Go back")

def toggle_role(char_index, role_choice):
    role_name = data.roles[role_choice]["Name"]
    role_symbol = data.roles[role_choice]["Symbol"]
    if role_name in ["Killed", "Cold Sleep"]:
        toggle_color(char_index, role_choice)
        return
    if char_index in data.current_roles[role_name]:
        data.current_roles[role_name].remove(char_index)
        t.r_print(f"\033[91mRemoved\033[0m {role_name} ({role_symbol}) from {data.characters[char_index]}.")
    else:
        data.current_roles[role_name].append(char_index)
        char_index = int(char_index)
        t.r_print(f"\033[94mAssigned\033[0m {role_name} ({role_symbol}) to {data.characters[char_index]}.")

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
            t.r_print(f"{data.characters[char_index]} is released from the state of being excepted.")
            return

    data.words_to_color[data.characters[char_index]] = color_code
    t.r_print(f"{data.characters[char_index]} is {state}.")

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
            t.r_print(f"\033[31mRemoved\033[0m {data.removed_characters[choice]} from the list.")

def restore_removed_characters():
    if not data.removed_characters:
        t.error_text = "\033[31mNo characters to restore.\033[0m"
        return
    for number, character in data.removed_characters.items():
        data.characters[number] = character
    t.r_print(f"\033[94mRestored all the characters to the list.\033[0m")
    data.removed_characters = {}