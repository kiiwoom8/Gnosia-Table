import re
import os
import data

def clear():
    os.system("cls")
    
def print_table():
    clear()
    print(data.stored_texts)

    col_widths = calculate_column_widths()
    header = build_header(col_widths)

    data.table = ""
    data.table += f"{header}\n"
    data.table += f"{"-" * len(header)}\n"

    generate_characters(col_widths)
    print(data.table, end="")


def generate_characters(col_widths):
    rc_index = [i for i, name in enumerate(data.characters.values()) if name == " "]

    for i, row in enumerate(data.matrix):
        char_names = [data.characters[key] for key in sorted(data.characters)]
        char_names[i] = " " if char_names[i] != " " else char_names[i]

        if i in rc_index:
            row_data = [" " for _ in row]
        else:
            row_data = [
                " " if char_names[i] == char_names[j] or j in rc_index else ";".join(actions) if actions else "-"
                for j, actions in enumerate(row)
            ]

        for j in range(len(row_data)):
            if char_names[j] != " ":
                char_names[j] = " "

        row_line = format_row(i, row_data, col_widths)
        data.table += f"{apply_color(row_line)}\n\n"

def calculate_column_widths():
    char_names = [data.characters[key] for key in sorted(data.characters)]
    return [
        max(len(char_names[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
        for i, column in enumerate(zip(*data.matrix))
    ]

def build_header(col_widths):
    header_width = max(len(name) for name in data.characters.values()) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(data.characters.values())
    )
    return apply_color(header)

def format_row(i, row_data, col_widths):
    char_names = [data.characters[key] for key in sorted(data.characters)]
    header_width = max(len(name) for name in char_names) + 2
    return char_names[i].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
    )

def apply_color(text):
    reset_color = "\033[0m"
    for word, color in data.words_to_color.items():
        text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{reset_color}', text)
    return text