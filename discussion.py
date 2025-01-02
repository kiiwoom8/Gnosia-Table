import data
import functions
import actions
import table_rendering
import handle_text as t
import vote
import backup

def handle_discussion():
    while True:
        type, action_range = print_discusstion_menu()        
        discussion_menu_choice = t.t_input("Select an action by number: ")
        if discussion_menu_choice:
            if discussion_menu_choice in ['z', 'p']:
                if type == 0:
                    init_unfinished_discussion()
                return
            if discussion_menu_choice == '0':
                init_discussion_settings()
                functions.increment_round()
                table_rendering.print_table()
            elif discussion_menu_choice.isdigit() and int(discussion_menu_choice) + type in action_range:
                discussion_menu_choice = int(discussion_menu_choice) + type
                actions.record_action(discussion_menu_choice, data.action_list[discussion_menu_choice]["Name"], data.actor, data.target)
                table_rendering.print_table()
            else:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"


def print_discusstion_menu():
    t.check_error()
    if data.round > 5 and data.ties_round in [0, 3]: # Voting round
        vote.handle_vote()
        return 0, []
    elif data.discussion_doubt:
        t.t_print(f"Target: {data.BLUE}{data.characters[data.target]}{data.RESET}")
        type, action_range = 2, range(3, 8)
    elif data.discussion_defend:
        t.t_print(f"Target: {data.BLUE}{data.characters[data.target]}{data.RESET}")
        type, action_range = 7, range(8, 12)
    else: # Beginning; Doubt or Cover
        type, action_range = 0, range(1, 3)

    for i in action_range:
        action = data.action_list[i]
        t.t_print(f"{i - type}. {action['Color']}{action['Name']}{data.RESET}")

    t.t_print("0. End discussion")
    if data.vote_history:
        t.t_print(f"r. {data.RED}Revert the most recent votes{data.RESET}")
    t.t_print("z. Go back")
    
    return type, action_range


def init_unfinished_discussion():
    data.first_actor, data.actor, data.participation = None, None, []


def init_discussion_settings():
    backup.backup_state()
    data.first_actor, data.actor, data.target = None, None, None
    data.discussion_doubt, data.discussion_defend = False, False
    data.participation = []


def set_discussion_options(action_choice):
    match action_choice:
        case 1:
            data.discussion_doubt = True
            data.first_actor = data.actor
        case 2:
            data.discussion_defend = True
        case 6:
            data.discussion_doubt = True
            data.discussion_defend = False
        case 7:
            data.discussion_doubt = False
            data.discussion_defend = True
        case 11:
            data.discussion_doubt = True
            data.discussion_defend = False
            
    data.actor = None