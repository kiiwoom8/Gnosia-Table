import re
import os
import data
import functions

def print_table():
    clear()
    print_recent_history()
    data.numbered_characters = functions.set_numbered_list(data.characters)
    col_widths = calculate_column_widths()
    build_header(col_widths)
    build_row_line(col_widths)
    generate_characters(col_widths)
    print(data.table, end="")
    if data.discussion_doubt or data.discussion_defend:
        print(f"{data.GREEN}[On Discussion]{data.RESET}")
    if data.round > 5:
        print(f"{data.GREEN}[On Vote]{data.RESET}")
    if data.round < 6 or data.ties_round not in [0, 3]: 
        print(f"{data.YELLOW}Round {data.round if not data.ties else data.ties_round}{data.RESET}")


def clear():
    os.system("cls")


def print_recent_history():
    history = data.history[-3:] if len(data.history) > 3 else data.history
    if history:
        print("\n".join(history))
    

def get_char_with_symbols(characters):
    characters_with_symbols = {}
    for char_num, char_name in characters.items():
        for role in data.roles.values():
            if role["Name"] in ["Killed", "Cold Sleep"] or char_name == " ":
                pass
            elif char_num in data.current_roles[role["Name"]]:
                char_name += (role["Symbol"])
            characters_with_symbols[char_num] = char_name
    return characters_with_symbols


def calculate_column_widths():
    characters = get_char_with_symbols(data.characters)
    char_names = [characters[key] for key in sorted(characters)]
    return [
        max(len(char_names[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
        for i, column in enumerate(zip(*data.matrix))
    ]


def generate_characters(col_widths):
    removed_char_indices = [i for i, name in enumerate(data.characters.values()) if name == " "]
    for char_index, row in enumerate(data.matrix):
        char_names = [" " if name == " " else name for name in data.characters.values()]
        row_data = [
            " " if char_index in removed_char_indices or j in removed_char_indices or char_names[char_index] == char_names[j] 
            else ";".join(actions) if actions else "-"
            for j, actions in enumerate(row)
        ]
        row_line = format_row(char_index, row_data, col_widths)
        data.table += f"{apply_color(row_line)}\n\n"
        data.table = re.sub(r"[-─]", lambda match: f"\033[90m{match.group()}\033[0m", data.table)


def build_header(col_widths):
    characters = get_char_with_symbols(data.characters)
    numbered_char_with_symbols = get_char_with_symbols(data.numbered_characters)
    header_width = max(len(name) for name in numbered_char_with_symbols.values()) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(characters.values())
    )
    data.table = "\n"
    data.table += f"{apply_color(header)}\n"


def build_row_line(col_widths):
    numbered_char_with_symbols = get_char_with_symbols(data.numbered_characters)
    separator = "".join("─" * width for width in col_widths)
    header_width = max(len(name) for name in numbered_char_with_symbols.values()) + 2
    data.table += f"{'─' * header_width}{separator}\n"


def format_row(char_index, row_data, col_widths):
    numbered_char_with_symbols = get_char_with_symbols(data.numbered_characters)
    numbered_char_names_with_symbols = [numbered_char_with_symbols[key] for key in sorted(numbered_char_with_symbols)]
    header_width = max(len(name) for name in numbered_char_names_with_symbols) + 2
    row = numbered_char_names_with_symbols[char_index].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data)))
    return row


def apply_color(text):
    for word, color in data.words_to_color.items():
        text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{data.RESET}', text)
    return text