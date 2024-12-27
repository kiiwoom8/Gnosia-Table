import re
import os
import data

def print_table():
    clear()
    print_recent_history()
    data.numbered_characters = data.set_numbered_list(data.characters)
    col_widths = calculate_column_widths()
    build_header(col_widths)
    build_row_line(col_widths)
    generate_characters(col_widths)
    print(data.table, end="")

def clear():
    os.system("cls")

def print_recent_history():
    history = data.history[-3:] if len(data.history) > 3 else data.history
    if history:
        print("\n".join(history))
    
def get_characters_with_symbols(characters):
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
    characters = get_characters_with_symbols(data.characters)
    char_names = [characters[key] for key in sorted(characters)]
    return [
        max(len(char_names[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
        for i, column in enumerate(zip(*data.matrix))
    ]

def generate_characters(col_widths):
    rc_index = [i for i, name in enumerate(data.characters.values()) if name == " "]
    for i, row in enumerate(data.matrix):
        char_names = [" " if name == " " else name for name in data.characters.values()]
        row_data = [
            " " if i in rc_index or j in rc_index or char_names[i] == char_names[j] 
            else ";".join(actions) if actions else "-"
            for j, actions in enumerate(row)
        ]
        row_line = format_row(i, row_data, col_widths)
        data.table += f"{apply_color(row_line)}\n\n"
        # data.table = data.table.replace("-", "\033[90m-\033[0m")
        data.table = re.sub(r"[-─]", lambda match: f"\033[90m{match.group()}\033[0m", data.table)

def build_header(col_widths):
    characters = get_characters_with_symbols(data.characters)
    numbered_characters = get_characters_with_symbols(data.numbered_characters)
    header_width = max(len(name) for name in numbered_characters.values()) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(characters.values())
    )
    data.table = "\n"
    data.table += f"{apply_color(header)}\n"

def build_row_line(col_widths):
    numbered_characters = get_characters_with_symbols(data.numbered_characters)
    separator = "".join("─" * width for width in col_widths)
    header_width = max(len(name) for name in numbered_characters.values()) + 2
    data.table += f"{'─' * header_width}{separator}\n"

def format_row(i, row_data, col_widths):
    numbered_characters = get_characters_with_symbols(data.numbered_characters)
    char_names = [numbered_characters[key] for key in sorted(numbered_characters)]
    header_width = max(len(name) for name in char_names) + 2
    return char_names[i].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
    )

def apply_color(text):
    for word, color in data.words_to_color.items():
        text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{data.RESET}', text)
    return text