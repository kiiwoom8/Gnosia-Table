import data
import handle_text as t
import table_rendering
import copy

undo_stack = []
redo_stack = []

def backup_state(stack = True):
    state = {
        'characters': copy.deepcopy(data.characters),
        'numbered_characters': copy.deepcopy(data.numbered_characters),
        'removed_characters': copy.deepcopy(data.removed_characters),
        'votes': copy.deepcopy(data.votes),
        'vote_history': copy.deepcopy(data.vote_history),
        'voting_characters': copy.deepcopy(data.voting_characters),
        'current_roles': copy.deepcopy(data.current_roles),
        'matrix': copy.deepcopy(data.matrix),
        'words_to_color': copy.deepcopy(data.words_to_color),
        'ties': copy.deepcopy(data.ties),
        'previous_ties': copy.deepcopy(data.previous_ties),
        'ties_history': copy.deepcopy(data.ties_history),
        'table': data.table,
        'first_actor': data.first_actor,
        'actor': data.actor,
        'target': data.target,
        'discussion_doubt': data.discussion_doubt,
        'discussion_defend': data.discussion_defend,
        'round': data.round,
        'ties_round': data.ties_round
    }
    if undo_stack and undo_stack[-1] == state:
        return

    if stack:
        undo_stack.append(state)
        redo_stack.clear()
    return state

def restore_state(state):
    data.characters = state['characters']
    data.numbered_characters = state['numbered_characters']
    data.removed_characters = state['removed_characters']
    data.votes = state['votes']
    data.vote_history = state['vote_history']
    data.voting_characters = state['voting_characters']
    data.current_roles = state['current_roles']
    data.matrix = state['matrix']
    data.words_to_color = state['words_to_color']
    data.ties = state['ties']
    data.previous_ties = state['previous_ties']
    data.ties_history = state['ties_history']
    data.table = state['table']
    data.first_actor = state['first_actor']
    data.actor = state['actor']
    data.target = state['target']
    data.discussion_doubt = state['discussion_doubt']
    data.discussion_defend = state['discussion_defend']
    data.round = state['round']
    data.ties_round = state['ties_round']

def undo():
    if undo_stack:
        state = undo_stack.pop()
        current = backup_state(False)
        redo_stack.append(current)
        restore_state(state)
        table_rendering.print_table()
    else:
        t.error_text = "\033[31mNo more actions to undo.\033[0m"

def redo():
    if redo_stack:
        state = redo_stack.pop()
        current = backup_state(False)
        undo_stack.append(current)
        restore_state(state)
        table_rendering.print_table()
    else:
        t.error_text = "\033[31mNo more actions to redo.\033[0m"

def choose_option():
    while True:
        t.check_error()
        t.t_print("Choose an option:")
        t.t_print("1. Undo")
        t.t_print("2. Redo")
        t.t_print("z. Go back")
        option = t.t_input("Enter your choice: ")
        if option:
            match option:
                case '1':
                    undo()
                case '2':
                    redo()
                case 'z':
                    return
                case _:
                    t.error_text = "\033[31mInvalid choice. Please select a valid option.\033[0m"