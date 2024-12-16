import re

def display_matrix(characters, matrix, words_to_color):
        col_widths = calculate_column_widths(characters, matrix)
        header = build_header(characters, col_widths, words_to_color)
        header = apply_color(words_to_color, header)
        print(f"\n{header}")
        print("-" * len(header))

        for i, row in enumerate(matrix):
            row_data = [";".join(actions) if actions else "-" for actions in row]
            row_line = format_row(characters, i, row_data, col_widths)
            colored_text = apply_color(words_to_color, row_line)
            print(f"{colored_text}\n")

def calculate_column_widths(characters, matrix):
    col_widths = [max(len(characters[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
                for i, column in enumerate(zip(*matrix))]
    return col_widths

def build_header(characters, col_widths, words_to_color):
    header_width = max(len(name) for name in characters) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(characters)
    )
    header = apply_color(words_to_color, header)
    return header

def format_row(characters, i, row_data, col_widths):
    header_width = max(len(name) for name in characters) + 2
    row_line = characters[i].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
    )
    return row_line

def apply_color(words_to_color, text):
    reset_color = "\033[0m"
    for word, color in words_to_color.items():
        text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{reset_color}', text)
    return text