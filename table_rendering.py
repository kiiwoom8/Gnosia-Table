import re

def display_matrix(characters, matrix, words_to_color):
    col_widths = calculate_column_widths(characters, matrix)
    header = build_header(characters, col_widths, words_to_color)
    print(f"\n{header}")
    print("-" * len(header))

    rc_index = [i for i, name in enumerate(characters.values()) if name == " "]

    for i, row in enumerate(matrix):
        char_names = [characters[key] for key in sorted(characters)]
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

        row_line = format_row(characters, i, row_data, col_widths)
        print(apply_color(words_to_color, row_line))
        print()

def calculate_column_widths(characters, matrix):
    char_names = [characters[key] for key in sorted(characters)]
    return [
        max(len(char_names[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
        for i, column in enumerate(zip(*matrix))
    ]

def build_header(characters, col_widths, words_to_color):
    header_width = max(len(name) for name in characters.values()) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(characters.values())
    )
    return apply_color(words_to_color, header)

def format_row(characters, i, row_data, col_widths):
    char_names = [characters[key] for key in sorted(characters)]
    header_width = max(len(name) for name in char_names) + 2
    return char_names[i].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
    )

def apply_color(words_to_color, text):
    reset_color = "\033[0m"
    for word, color in words_to_color.items():
        text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{reset_color}', text)
    return text
