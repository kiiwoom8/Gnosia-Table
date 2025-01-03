import data
import functions
import actions
import table_rendering
import handle_text as t
import vote
import backup

def handle_discussion():
    while True:
        if vote.onVote():
            vote.handle_vote()
            return

        action_name_list = print_discusstion_menu()        
        discussion_menu_choice = t.t_input("Select an action by number: ")
        if discussion_menu_choice:
            if discussion_menu_choice == 'z':
                return
            if discussion_menu_choice == '0':
                init_discussion_settings()
                data.round += 1
                table_rendering.print_table()
            elif discussion_menu_choice.isdigit() and 0 < int(discussion_menu_choice) < len(action_name_list) + 1:
                discussion_menu_choice = int(discussion_menu_choice) - 1
                actions.record_action(action_name_list[discussion_menu_choice], data.actor, data.target)
                table_rendering.print_table()
            else:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"


def print_discusstion_menu():
    t.check_error()
    if data.discussion_doubt:
        t.t_print(f"Target: {data.BLUE}{data.characters[data.target]}{data.RESET}")
        type = "Doubt"
    elif data.discussion_defend:
        t.t_print(f"Target: {data.BLUE}{data.characters[data.target]}{data.RESET}")
        type = "Defend"
    else: # Doubt or Cover
        type = "Default"

    action_name_list = [action_name for action_name, action in data.action_list.items() if action["Type"] == type]

    if data.first_attacker or data.first_defender: # Remove options that are not allowed
        if data.first_attacker and data.first_defender:
            excluded_actions = ["Argue", "Block Argument Defend", "Defend", "Retaliate/Don't be fooled", "Block Argument Doubt"]
        elif data.first_attacker:
            excluded_actions = ["Argue", "Block Argument Defend"]
        elif data.first_defender:
            excluded_actions = ["Defend", "Retaliate/Don't be fooled", "Block Argument Doubt", "Help"]
        
        action_name_list = [action for action in action_name_list if action not in excluded_actions]

    for i, action_name in enumerate(action_name_list):
        t.t_print(f"{i + 1}. {data.action_list[action_name]['Name']}")

    t.t_print("0. End discussion")
    t.t_print("z. Go back")
    
    return action_name_list


def init_discussion_settings():
    backup.backup_state()
    data.first_attacker, data.first_defender, data.actor, data.target = None, None, None, None
    data.discussion_doubt, data.discussion_defend = False, False
    data.participation = []


def set_discussion_options(action_name):
    match action_name:
        case "Doubt":
            data.discussion_doubt = True
            data.first_attacker = data.actor
        case "Cover":
            data.discussion_defend = True
            data.first_defender = data.actor
        case "Retaliate/Don't be fooled":
            data.discussion_doubt = True
            data.discussion_defend = False
            data.first_attacker, data.first_defender = data.actor, data.actor
        case "Block Argument Doubt" | "Block Argument Defend":
            data.first_attacker, data.first_defender = data.actor, data.actor
        case "Defend" | "Help":
            data.discussion_doubt = False
            data.discussion_defend = True
        case "Argue":
            data.discussion_doubt = True
            data.discussion_defend = False

    data.actor = None