import data
import table_rendering
import backup

class Z(Exception):
    pass

text_lines = 0
error_text = ""

def t_print(text = ""):
    global text_lines
    print(text)
    text_lines += 1


def r_print(text = ""):
    data.history.append(text)
    table_rendering.print_table()
    

def t_input(text:str):
    result = input(text).strip().lower()
    global text_lines
    text_lines += 1
    delete_text()
    return result


def delete_text():
    global text_lines
    for _ in range(text_lines):
        print("\033[F\033[K", end= "")
    text_lines = 0


def check_error():
    global error_text
    if error_text:
        t_print(f"\033[91m{error_text}\033[0m")
    error_text = ""