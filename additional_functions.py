import data
import handle_text as t

def take_note():
    while True:
        t.check_error()
        display_notes()
        option = t.t_input("Enter your choice: ")
        if option:
            match option:
                case '1':
                    create_note()
                case '2':
                    if data.notes:
                        delete_note()
                    else:
                        t.error_text = "\033[31mNo notes to delete.\033[0m"
                case 'z':
                    return
                case _:
                    t.error_text = "\033[31mInvalid choice. Please select 1, 2, or 'z'.\033[0m"


def create_note():
    content = t.tn_input("Enter the note content or press Enter to return: ")
    if content and content not in ['z', 'Z']:
        data.notes.append(content)
        t.t_print(f"{data.GREEN}Note added successfully.{data.RESET}")


def delete_note():
    while True:
        t.check_error()
        note_number = t.t_input("Enter the number of the note to delete: ").strip()
        if note_number:
            if note_number == 'z':
                break
            note_number = int(note_number)
            if 0 < note_number <= len(data.notes):
                deleted_note = data.notes.pop(note_number - 1)
                t.t_print(f"{data.GREEN}The note '{deleted_note}' has been deleted successfully.{data.RESET}")
                break
            else:
                t.error_text = "\033[31mInvalid input. Please enter a number.\033[0m"


def display_notes():
    draw_note_line()
    if data.notes:
        t.t_print("\033[32mYour Notes:\033[0m")
        for idx, content in enumerate(data.notes, start=1):
            t.t_print(f"({idx}) {content}")
    else:
        t.t_print("\033[91m(No note)\033[0m")
    draw_note_line()
    t.t_print("1. Take a note")
    t.t_print("2. Delete a note")
    t.t_print("z. Go back")  


def draw_note_line():
    text= ""
    for _ in range(100):
        text +="\033[33m─\033[0m"
    t.t_print(f"{text}")


def show_stats():
    option = None
    while True:
        if option:
            print_stats(option)
        t.check_error()
        option = t.t_input("Enter your choice (or 'z' to go back): ")
        if option == 'z':
                return


def color_code_stats(character_stats):
    def color_code(value):
        if value >= 40: return f"\033[31m{value}\033[0m"
        if value >= 30: return f"\033[32m{value}\033[0m"
        if value >= 20: return f"\033[33m{value}\033[0m"
        return str(value)

    def color_code_range(range_str):
        lower, upper = map(float, range_str.split("-"))
        return f"{color_code(lower)} \033[90m-\033[0m {color_code(upper)}"

    for stats_dict in character_stats.values():
        for stat_name, stat_value in stats_dict.items():
            stats_dict[stat_name] = color_code_range(stat_value)

    return character_stats


def print_stats(option):
    if option == "1":
        t.error_text = "\033[31mYou cannot check the stats of the player.\033[0m"
    try: 
        character_name = data.characters[int(option)]
        if character_name in data.character_stats:
            stats = data.character_stats[character_name]
            t.t_print(f"Name: {character_name}")
            for key, value in stats.items():
                t.t_print(f"{key}: {value}")
    except (ValueError, KeyError):
        t.error_text = "\033[31mInvalid choice. Please select a valid character.\033[0m"


def see_full_history():
    history = data.history
    text = "\n".join(history) if history else "\033[91m(There's no history recorded.)\033[0m"
    print(text)
    t.t_input("Press any key to exit: ").strip().lower()