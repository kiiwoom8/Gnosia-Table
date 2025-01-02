import table_rendering
import data
import handle_text as t
import actions
import role
import backup
from copy import deepcopy

def onVote():
    return data.round > 5 or (data.ties and (data.round not in [1,2] or data.previous_ties == data.ties))

def handle_vote():
    if not data.ties or data.previous_ties != data.ties:
        vote()
    else:
        while True:
            t.check_error()
            table_rendering.print_table()
            t.t_print("1. \033[31mFreeze All\033[0m") 
            t.t_print("2. \033[34mFreeze Nobody\033[0m") 
            t.t_print("z. Go back")
            vote_menu_choice = t.t_input("Select an action by number: ")
            match vote_menu_choice:
                case '1':
                    freeze_all()
                    return
                case '2':
                    freeze_nobody()
                    return
                case 'z':
                    return
                case '':
                    pass
                case _:
                    t.error_text = "\033[31mInvalid choice. Try again.\033[0m"


def vote():
    vote_characters()
    if not data.voting_characters:
        max_votes = max(data.votes.values(), default=0)
        most_voted = sorted([char for char, votes in data.votes.items() if votes == max_votes])
        data.votes = {}
        if len(most_voted) == 1:
            role.toggle_role(most_voted[0], 10)
            release_ties()
            data.round = 1
        else:
            if data.ties:
                data.previous_ties = deepcopy(data.ties)
            data.ties = most_voted
            set_ties()
            data.round = 1

def vote_characters():
    if not data.voting_characters:
        data.voting_characters = list(data.characters.keys())
    for char_index in data.voting_characters.copy():
        '''
        # show reamining characters voting
        voting_character_names = [data.characters[char_index] for char_index in data.voting_characters 
                                  if data.characters[char_index] != " "]
        voting_character_names[0] = f"{data.BLUSH}{voting_character_names[0]}{data.RESET}"
        print(", ".join(voting_character_names))
        '''
        char_name = data.characters[char_index]
        if char_name != " "  and data.words_to_color.get(char_name) not in [data.RED, data.BLUE]:
            target = actions.get_target(char_index)
            if target == 'z':
                return
            target = int(target)
            actions.record_action(12, "Vote", char_index, target)
            data.votes[target] = data.votes.get(target, 0) + 1
            
        data.voting_characters.remove(char_index)


def freeze_all():
    if data.ties:
        backup.backup_state()
        for char in data.ties:
            role.toggle_role(char, 10)
        release_ties()
    else:
        t.error_text = "\033[31mNo votes to freeze.\033[0m"


def freeze_nobody():
    if data.ties:
        backup.backup_state()
        release_ties()
        t.r_print("\033[34mNobody is frozen.\033[0m")
    else:
        t.error_text = "\033[31mNo votes to release.\033[0m"


def set_ties():
    t.r_print("\033[91mIt's a tie! Vote again.\033[0m")
    for char_name in data.characters.values():
        if char_name in data.words_to_color and data.words_to_color[char_name] == data.YELLOW:
            del data.words_to_color[char_name]

    data.voting_characters = list(data.characters.keys())
    for char in reversed(data.ties):
        data.voting_characters.remove(char)
        data.voting_characters.insert(1, char)
        data.words_to_color[data.characters[char]] = data.YELLOW


def release_ties():
    if data.ties:
        for char_index in data.ties:
            char_name = data.characters[char_index]
            if char_name in data.words_to_color and data.words_to_color[char_name] == data.YELLOW:
                del data.words_to_color[char_name]
        data.ties = []
        data.round = 1
        data.voting_characters = {}