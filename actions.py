import data
import functions
import table_rendering
import handle_text as t
import discussion
import backup

def record_action(action_name: str, actor = None, target = None):
    action = data.action_list[action_name]
    if action_name == "Retaliate/Don't be fooled":
        actor = data.target
        target = data.first_attacker

    if not actor:
        if target:
            t.t_print(f"Target: {data.BLUE}{data.characters[target]}{data.RESET}" )
        actor = select_character("acting", action['Name'])
        if  actor == 'z':
            return
        
        actor = int(actor)
        if actor == target:
            t.error_text = "\033[31mCannot act on self. Please try again.\033[0m"
            return
        if actor in data.participation:
            t.error_text = "\033[31mCannot act twice in a round. Please try again.\033[0m"
            return

    if not target:
        target = get_target(actor)
        if target == 'z':
            return
        target = int(target)

    backup.backup_state()
    data.actor = actor
    data.target = target
    action = action["Abbr"]
    data.matrix[actor - 1][target - 1].append(action)
    target_name = data.characters.get(target, "\033[31mUnknown\033[0m")
    t.r_print(f"\033[92mRecorded:\033[0m {data.characters[actor]} {action_name} {target_name}")
    discussion.set_discussion_options(action_name)
    if action_name != "Vote":
        data.participation.append(actor)


def get_target(actor):
    while True:
        target = select_character("target", f"Acting character: {data.BLUSH}{data.characters[actor]}{data.RESET}")
        if target == 'z':
            return target
        if actor == int(target):
            t.t_print("\033[31mCannot act on self. Please try again.\033[0m")
        elif data.ties and int(target) not in data.ties:
            t.t_print("\033[31mInvalid choice. Please try again.\033[0m")
        else:
            return target


def delete_recent_action(actor = None, target = None):
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