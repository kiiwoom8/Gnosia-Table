import re
import data

def get_user_choice(characters):
    while True:
        count = 0
        for character in characters:
            count += 1
            print(f"{count}. {character}")
        user_input = input("Enter the number for your choice (or 'z' to go back): ")
        if user_input.lower() == 'z':
            print("Going back...")
            return None
        try:
            choice = int(user_input)
            if 1 <= choice <= len(characters):
                return choice
            else:
                print(f"Please enter a number between 1 and {len(characters)}.")
        except ValueError:
            print("\033[31mInvalid input. Please enter a number or 'z' to go back.\033[0m")

def record_action(matrix, characters):
    action_names, action_names_abbr = data.get_action_list()
    action_choice = select_action(action_names)

    if action_choice not in action_names:
        return

    action = action_names_abbr[action_choice]
    actor = select_character("acting")
    if actor is None:
        return
    target = select_character("target")
    if target is None:
        return
    if actor == target:
        print("\033[31mCannot act on self. Please try again.\033[0m")
        return
    actor_name = characters[actor - 1]
    target_name = characters[target - 1]

    matrix[actor - 1][target - 1].append(action)
    print(f"Recorded: {actor_name} {action} {target_name}")

def delete_recent_action(matrix, characters):
    print("\nDelete the most recent action from a character pair:")
    actor = select_character("actor")
    if actor is None:
        return
    target = select_character("target")
    if target is None:
        return

    actor_name = characters[actor - 1]
    target_name = characters[target - 1]
    actions = matrix[actor - 1][target - 1]

    if actions:
        removed_action = actions.pop()
        print(f"Deleted: {actor_name} {removed_action} {target_name}")
    else:
        print(f"No actions recorded between {actor_name} and {target_name}.")

def select_action(action_names):
    print("\nSelect the action performed:")
    for number, action_name in action_names.items():
        print(f"{number}. {action_name}")
    print("z. Go back")

    action_choice = input("Select a role by number: ").strip()
    if action_choice.lower() == 'z':
        print("Returning to main menu...")
        return None

    try:
        action_choice = int(action_choice)
        return action_choice
    except ValueError:
        print("\033[31mInvalid input. Try again.\033[0m")
        return None

def select_character(role_type):
    print(f"Select the {role_type} character:")
    return get_user_choice(data.get_character_list())

def assign_roles(characters):
    role_symbols, role_names = data.get_get_roles_list()

    while True:
        print("\nAssign or Remove Roles:")
        for key in role_names:
            print(f"{key}. {role_names[key]} ({role_symbols[key]})")
        print("z. Go back")

        role_choice = input("Select a role by number: ").strip()
        if role_choice.lower() == 'z':
            print("Returning to main menu...")
            break

        try:
            role_choice = int(role_choice)
            if role_choice not in role_symbols:
                print("Invalid role choice. Try again.")
                continue
        except ValueError:
            print("\033[31mInvalid input. Try again.\033[0m")
            continue

        char_index = select_character("assign/remove")
        if char_index is None:
            continue  
        char_index -= 1

        symbol = role_symbols[role_choice]
        toggle_role(characters, char_index, symbol, role_names[role_choice])

def toggle_role(characters, char_index, symbol, role_name):
    if symbol in characters[char_index]:
        characters[char_index] = characters[char_index].replace(symbol, "")
        print(f"Removed {role_name} ({symbol}) from {characters[char_index]}.")
    else:
        characters[char_index] += symbol
        print(f"Assigned {role_name} ({symbol}) to {characters[char_index]}.")

def display_matrix(matrix, characters):
    col_widths = calculate_column_widths(matrix, characters)
    header = build_header(characters, col_widths)
    print(f"\n{header}")
    print("-" * len(header))

    for i, row in enumerate(matrix):
        row_data = [";".join(actions) if actions else "-" for actions in row]
        row_line = format_row(characters, i, row_data, col_widths)
        colored_text = apply_color(row_line)
        print(f"{colored_text}\n")

def calculate_column_widths(matrix, characters):
    col_widths = [max(len(characters[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
                  for i, column in enumerate(zip(*matrix))]
    return col_widths

def build_header(characters, col_widths):
    header_width = max(len(name) for name in characters) + 2
    header = "".ljust(header_width) + "".join(
        char.ljust(col_widths[i]) for i, char in enumerate(characters)
    )
    return header

def format_row(characters, i, row_data, col_widths):
    header_width = max(len(name) for name in characters) + 2
    row_line = characters[i].ljust(header_width) + "".join(
        row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
    )
    return row_line

def apply_color(row_line):
    words_to_color = data.get_words_to_color()
    reset_color = "\033[0m"
    for word, color in words_to_color.items():
        row_line = re.sub(rf'\b({word})\b', rf'{color}\1{reset_color}', row_line, flags=re.IGNORECASE)
    return row_line

def show_stats():
    print("1. \033[32mIntuition\033[0m")
    print("2. \033[35mPerformance\033[0m")
    # print("3. Logic")
    option = input("Enter your choice: ").strip()
    print()
    data.print_stats(option)

def initialize_table():
    characters = data.get_character_list()
    matrix = [[[] for _ in characters] for _ in characters]
    return characters, matrix

def main():
    characters, matrix = initialize_table()
    while True:
        display_matrix(matrix, characters)
        print("Choose an option:")
        print("1. Record an action")
        print("2. Delete the most recent action")
        print("3. Assign/Remove roles")
        print("4. Show character stats")
        print("9. Initialize")
        print("0. Exit")
        option = input("Enter your choice: ").strip()

        if option == '1':
            record_action(matrix, characters)
        elif option == '2':
            delete_recent_action(matrix, characters)
        elif option == '3':
            assign_roles(characters)
        elif option == '4':
            show_stats()
        elif option =='9':
            characters, matrix = initialize_table()
        elif option == '0':
            print("Exiting...")
            break
        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, 9, or 0.\033[0m")

if __name__ == "__main__":
    main()
