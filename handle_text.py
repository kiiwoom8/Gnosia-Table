import data
import table_rendering
import msvcrt

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
    t_print(text)
    result = msvcrt.getch()
    try:
        result = result.decode('utf-8').strip().lower()  # Decode to string and process
        match result:
            case 'a': result = '10'
            case 'b': result = '11'
            case 'c': result = '12'
            case 'd': result = '13'
            case 'e': result = '14'
            case 'f': result = '15'
    except UnicodeDecodeError:
        result = '-1'

    global text_lines
    delete_text()

    return result


def tn_input(text:str): # without lowering
    result = input(text)
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