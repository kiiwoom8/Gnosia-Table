import data
import handle_text as t
import table_rendering

def print_options():
    t.t_print ("Choose an option:")
    for key, value in data.options.items():
        t.t_print(f"{key}. {value["title"]}")

def get_option():
    try:
        option = int(t.t_input("Enter your choice: ").strip())
    except ValueError:
        option = -1
    return option

def execute_function(option):
    if option in data.options.keys():
        data.options[option]["function"]()

def main():
    data.reset()
    while True:
        table_rendering.print_table()
        t.check_error()
        print_options()
        option = get_option()
        execute_function(option)

if __name__ == "__main__":
    main()
