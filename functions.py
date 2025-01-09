import data
import backup
import handle_text as t
import table_rendering

def reset():
    if data.characters:
        backup.backup_state()
    data.reset()


def validate_choice(user_input:str):
    if user_input.isdigit() and (user_input := int(user_input)) in data.characters:
        char_name = data.characters[user_input]
        if " " not in char_name and char_name not in data.words_to_color:
            return user_input
    else:
        return False
    

def toggle_color(char_index, role_name):
    match role_name:
        case "Killed":
            color_code = "\033[31m"
            state = "\033[31mkilled\033[0m"
        case "Cold Sleep":
            color_code = "\033[34m"
            state = "\033[34mcold sleeped\033[0m"

    if data.characters[char_index] in data.words_to_color and data.words_to_color[data.characters[char_index]] == color_code:
        removed_color = data.words_to_color.pop(data.characters[char_index])
        if color_code == removed_color:
            t.r_print((f"{data.characters[char_index]} is released from the state of being excepted. "
                       f"{data.BLUSH}Previous collaboration is not restored{data.RESET}, so please consider that."))
    else:
        data.words_to_color[data.characters[char_index]] = color_code
        t.r_print(f"{data.characters[char_index]} is {state}.")
        exclude_char_from_collab(char_index)


def exclude_char_from_collab(char_index):
    data.collab = [char_set for char_set in data.collab if char_index not in char_set]

    
def set_num_char_list(list:dict):
    numbered_list = {
        num: element if element == " " else f"{data.convert_digits(num)}. {element}"
        for num, element in list.items()
    }
    return numbered_list


def exit_program():
    choice = t.t_input("Are you sure you want to exit? (y/n): ")
    if choice == 'y':
        table_rendering.clear()
        exit(0)