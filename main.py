import data
import handle_text
import table_rendering

t = handle_text.HandleText()

def print_options():
    t.print ("Choose an option:")

    for key, value in data.get_selections().items():
        t.print(f"{key}. {value["title"]}")

def get_option():
    try:
        option = int(t.input("Enter your choice: ").strip())
    except ValueError:
        option = -1

    return option

def execute_function(option):
    if option in data.get_selections().keys():
        data.get_selections()[option]["function"]()

def main():
    data.reset()
    while True:
        table_rendering.print_table()
        print_options()
        option = get_option()
        execute_function(option)

if __name__ == "__main__":
    main()
