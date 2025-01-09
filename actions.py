import data
import functions
import table_rendering
import handle_text as t
import discussion
import backup

def record_action(action_name: str, actor = None, target = None, backup_status = True):
    action = data.action_list[action_name]
    actor, target = set_actor_and_target(action, action_name, actor, target)
    if not (actor and target):
        return

    if action_name == "Collab" and any({actor, target} & char_set for char_set in data.collab):
        t.error_text = (f"{data.RED}Collaboration already exists with {data.characters[actor]} "
                        f"or {data.characters[target]}. Please try again.{data.RESET}")
        return
    
    if backup_status:
        backup.backup_state()
    record(action, actor, target)
    post_action(action_name, actor, target)


def set_actor_and_target(action, action_name, actor, target):
    match action_name:
        case "Retaliate":
            actor = target
            target = data.first_attacker
        case "Help":
            actor = target
            target = None

    if target:
        t.t_print(f"Target: {data.BLUE}{data.characters[target]}{data.RESET}" )

    # handle actor
    if not actor:
        actor = select_character("acting", action['Name']) 
        if actor == 'z':
            return None, None
        
        actor = int(actor)
        if actor == target:
            t.error_text = "\033[31mCannot act on self. Please try again.\033[0m"
            return None, None
        if actor in data.participation:
            t.error_text = "\033[31mCannot act twice in a round. Please try again.\033[0m"
            return None, None

    # handle target
    if not target:
        target = get_target(actor)
        if target == 'z':
            return None, None
            
        target = int(target)
        
    return actor, target
    
    
def record(action, actor, target):
    action_abbr = action["Abbr"]
    cell = data.matrix[actor - 1][target - 1]
    if cell:
        if cell[-1] == action_abbr:
            cell[-1] =  f"{action_abbr}x2"
        elif cell[-1][:len(action_abbr)] == action_abbr and cell[-1][-2] == 'x':
            cell[-1] = f"{action_abbr}x{str(int(cell[-1][-1]) + 1)}"
        else:
            cell.append(action_abbr)
    else:
        cell.append(action_abbr)
    target_name = data.characters.get(target, "\033[31mUnknown\033[0m")
    record_history(action, actor, target_name)


def handle_collab(actor, target):
    action = data.action_list['Collab']
    while True:
        t.check_error()
        choice = t.t_input(f"Accept the collaboration with {data.characters[actor]}? (y/n): ")
        if choice:
            match choice:
                case 'y':
                    data.collab.append({actor, target})
                    data.matrix[target - 1][actor - 1].append(action['Abbr'])
                    record_history(action, target, data.characters[actor])
                    break
                case 'n':
                    data.matrix[target - 1][actor - 1].append("Ref")
                    record_history(data.action_list["Refuse"], target, data.characters[actor])
                    break
                case _:
                    t.error_text = "\033[31mInvalid choice. Try again.\033[0m"


def handle_help(actor, target):
    while True:
        t.check_error()
        choice = t.t_input(f"Accept the Help with {data.characters[actor]}? (y/n): ")
        if choice:
            match choice:
                case 'y':
                    record_action("Defend", target, actor, backup_status = False) # don't backup to conbine Help and it's reply
                    break
                case 'n':
                    record_action("Reject", target, actor, backup_status = False)
                    break
                case _:
                    t.error_text = "\033[31mInvalid choice. Try again.\033[0m"    


def post_action(action_name, actor, target):
    match action_name:
        case "Vote":
            pass
        case "Collab":
            handle_collab(actor, target)
            discussion.end_round()  # don't backup
        case "Help":
            handle_help(actor, target)
        case _:
            discussion.set_discussion_options(action_name, actor)
            data.target = target
            data.participation.append(actor)


def get_target(actor):
    while True:
        target = select_character("target", f"Acting character: {data.BLUSH}{data.characters[actor]}{data.RESET}")
        if target == 'z':
            return target
        if actor == int(target):
            t.error_text = "\033[31mCannot act on self. Please try again.\033[0m"
        elif data.ties and int(target) not in data.ties:
            t.error_text = "\033[31mInvalid choice. Please try again.\033[0m"
        else:
            return target


def record_history(action, actor, target_name):
    t.r_print(f"\033[92mRecorded:\033[0m {data.characters[actor]} {action['Name']} {target_name}")


def delete_last_action(actor = None, target = None):
    while True:
        if not actor or not target:
            actor = select_character("actor")
            if actor == 'z':
                return
            actor = int(actor)
            target = select_character("target", f"Acting character: \033[91m{data.characters[actor]}\033[0m")
            if target == 'z':
                return
            target = int(target)
            remove_action_from_table(actor, target)
            actor = None
        else:
            remove_action_from_table(actor, target)
            return


def remove_action_from_table(actor, target):
    backup.backup_state()
    actor_name = data.characters[actor]
    target_name = data.characters[target]
    actions = data.matrix[actor - 1][target - 1]
    if actions:
        removed_action = actions.pop()
        key = next((action_num for action_num, action in data.action_list.items() if action["Abbr"] == removed_action), None)
        if key:
            removed_action = data.action_list[key]
        t.r_print(f"\033[91mDeleted:\033[0m {actor_name} {removed_action['Name']} {target_name}")
        table_rendering.print_table()
    else:
        t.error_text = "\033[31mNo actions to delete.\033[0m"


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
        user_input = t.t_input("Enter the number for your choice (or 'z' to go back): ")
        if user_input:
            if user_input == 'z' or functions.validate_choice(user_input):
                return user_input
            else:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"
        else:
            table_rendering.print_table()


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
            backup.backup_state()
            data.removed_characters[choice] = data.characters[choice]
            data.characters[choice] = " "
            t.r_print(f"\033[31mRemoved\033[0m {data.removed_characters[choice]} from the list.")