import re
import os
import data

def print_table():
    clear()
    print_recent_history()
    data.set_numbered_character_list()
    col_widths = calculate_column_widths()
    build_header(col_widths)
    build_row_line(col_widths)
    generate_characters(col_widths)
    print(data.table, end="")

def clear():
    os.system("cls")

def print_recent_history():
    history = data.history[-3:] if len(data.history) > 3 else data.history
    print("\n".join(history) + "\n")
    
def calculate_column_widths():
    char_names = [data.characters[key] for key in sorted(data.characters)]
    return [
        max(len(char_names[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
        for i, column in enumerate(zip(*data.matrix))
    ]

def generate_characters(col_widths):
    rc_index = [i for i, name in enumerate(data.numbered_characters.values()) if name == " "]
    for i, row in enumerate(data.matrix):
        char_names = [" " if name == " " 
                      else name for name in data.numbered_characters.values()]
        row_data = [
            " " if i in rc_index or j in rc_index or char_names[i] == char_names[j] 
            else ";".join(actions) if actions else "-"
            for j, actions in enumerate(row)
        ]
        row_line = format_row(i, row_data, col_widths)
        data.table += f"{apply_color(row_line)}\n\n"

def build_header(col_widths):
    header_width = max(len(name) for name in data.numbered_characters.values()) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(data.characters.values())
    )
    data.table = ""
    data.table += f"{apply_color(header)}\n"

def build_row_line(col_widths):
    separator = "".join("─" * width for width in col_widths)
    header_width = max(len(name) for name in data.numbered_characters.values()) + 2
    data.table += f"{'─' * header_width}{separator}\n"

def format_row(i, row_data, col_widths):
    char_names = [data.numbered_characters[key] for key in sorted(data.numbered_characters)]
    header_width = max(len(name) for name in char_names) + 2
    return char_names[i].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
    )

def apply_color(text):
    reset_color = "\033[0m"
    for word, color in data.words_to_color.items():
        text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{reset_color}', text)
    return text