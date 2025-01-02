import data
import backup
import handle_text as t
import table_rendering

def reset():
    if data.characters:
        backup.backup_state()
    data.reset()


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


def set_numbered_list(list:dict):
    numbered_list = {
        num: element if element == " " else f"{' ' if num < 10 else ''}{num}. {element}"
        for num, element in list.items()
    }
    return numbered_list


def exit_program():
    choice = t.t_input("Are you sure you want to exit? (y/n): ")
    if choice == 'y':
        table_rendering.clear()
        exit(0)