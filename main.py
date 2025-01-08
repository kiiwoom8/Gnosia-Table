import data
import handle_text as t
import table_rendering
import backup

def print_options():
    t.t_print ("Choose an option:")
    for key, value in data.options.items():
        t.t_print(f"{key}. {value["title"]}")


def get_option():
    option = t.t_input("Enter your choice ('q' for Undo, 'w' for Redo): ")
    if option.isdigit() and -1 < int(option) < len(data.options):
        option = int(option)
        if option in data.options.keys():
            return option
        t.error_text = "\033[31mInvalid choice. Please select a valid option.\033[0m"
    elif option in ['q', 'w']:
        return option
    return -1


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
