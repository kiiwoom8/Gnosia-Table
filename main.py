import data
import handle_text as t
import table_rendering
import backup

def print_options():
    t.t_print ("Choose an option:")
    for key, value in data.options.items():
        if 'Exit' in value["title"]:
            t.t_print(f"{data.YELLOW}q{data.RESET}. Undo")
            t.t_print(f"{data.YELLOW}w{data.RESET}. Redo")
        t.t_print(f"{key}. {value["title"]}")


def get_option():
    option = t.t_input(f"Enter your choice: ")
    if option and not (option.isdigit() and (option := int(option)) in data.options.keys() or option in ['q', 'w', 'z']):
        t.error_text = "\033[31mInvalid choice. Please select a valid option.\033[0m"

    return option


def execute_function(option):
    if option in data.options.keys():
        data.options[option]["function"]()
    elif option in ['q', 'w']:
        match option:
            case 'q': 
                backup.undo()
            case 'w': 
                backup.redo()


def main():
    data.reset() # should reset from data.py, not from functions.py
    while True:
        table_rendering.print_table()
        t.check_error()
        print_options()
        option = get_option()
        execute_function(option)


if __name__ == "__main__":
    main()
