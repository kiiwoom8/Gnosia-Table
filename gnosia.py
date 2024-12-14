import re

def display_character_names():
    return [
        "Me", "Setsu", "Gina", "SQ", "Raqio", "Shigemichi", "Stella", "Comet", "Chipie", "Jonas",
        "Kukrushka", "Otome", "Sha-Ming", "Remnan", "Yuriko"
    ]


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
    action_names = {1: "Vote", 2: "Doubt", 3: "Agree", 4: "Cover", 5: "Defend", 6: "Collab", 7: "ExAgree", 8: "ExDefend"}
    action_choice = select_action()

    if action_choice not in action_names:
        return

    action = action_names[action_choice]
    actor = select_character("acting")
    if actor is None:
        return
    target = select_character("target")
    if target is None:
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


def select_action():
    print("\nSelect the action performed:")
    print("1. \033[91mVote\033[0m")
    print("2. \033[91mDoubt\033[0m")
    print("3. \033[91mAgree\033[0m")
    print("4. \033[94mCover\033[0m")
    print("5. \033[94mDefend\033[0m")
    print("6. \033[94mCollab\033[0m")
    print("7. \033[91mExAgree\033[0m")
    print("8. \033[94mExDefend\033[0m")
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
    return get_user_choice(display_character_names())


def assign_roles(characters):
    role_symbols = {1: "🅰️", 2: "🕷️", 3: "🛠️", 4: "✙", 5: "☠️", 6: "🕊️", 7: "✳️"}
    role_names = {1: "Gnosia", 2: "AC Follower", 3: "Engineer", 4: "Doctor", 5: "Bug", 6: "Guardian Angel", 7: "Crew"}

    while True:
        print("\nAssign or Remove Roles:")
        print("1. Gnosia (🅰️)")
        print("2. AC Follower (🕷️)")
        print("3. Engineer (🛠️)")
        print("4. Doctor (✙)")
        print("5. Bug (☠️)")
        print("6. Guardian Angel (🕊️)")
        print("7. Crew (✳️)")
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
    print("\nCurrent Actions Table:\n")
    print(header)
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
    words_to_color = {
        "Vote": "\033[31m",
        "Doubt": "\033[31m",
        "Agree": "\033[31m",
        "Cover": "\033[34m",
        "Defend": "\033[34m",
        "Collab": "\033[34m",
        "ExAgree": "\033[31m",
        "ExDefend": "\033[34m"
    }
    reset_color = "\033[0m"

    def color_words(text, words_to_color):
        for word, color in words_to_color.items():
            text = re.sub(rf'\b({word})\b', rf'{color}\1{reset_color}', text, flags=re.IGNORECASE)
        return text

    return color_words(row_line, words_to_color)

def show_stats():
    print("\n1. \033[32mIntuition\033[0m\n")
    print("2. \033[35mPerformance\033[0m\n")
    # print("3. Logic")
    option = input("Enter your choice: ").strip()
    print()
    if option == '1':
        print("\n\033[32mIntuition\033[0m\n")
        print ("\033[31mStrongest\033[0m:")
        print ("Min: \033[33mComet (25.5)\033[0m, \033[97mRemnan (21)\033[0m, \033[90mYuriko (20.5)\033[0m, \033[92mChipie (17)\033[0m, \033[95mOtome (16.5)\033[0m, \033[31mKukurushka (16)\033[0m")
        print ("Max: \033[33mComet (49.5)\033[0m, \033[94mGina (45.5)\033[0m, \033[90mYuriko (42)\033[0m, \033[97mRemnan (41)\033[0m, \033[92mChipie (39)\033[0m, \033[31mKukurushka (35.5)\033[0m, \033[95mOtome (32)\033[0m, Setsu (28.5)\n")
        print ("\033[34mWeakest\033[0m:")
        print ("Min: \033[96mRaqio (0.5)\033[0m, Shigemichi (3.5), \033[94mGina\033[0m (4), \033[32mStella (5)\033[0m, \033[35mSha-Ming (5.5)\033[0m, Setsu (8), Jonas (9.5), SQ (11)")
        print ("Max: \033[96mRaqio (0.5)\033[0m, \033[35mSha-Ming (6.5)\033[0m, Shigemichi (14.5), \033[32mStella (18)\033[0m")
    elif option == '2':
        print("\n\033[35mPerformance\033[0m\n")
        print ("\033[31mStrongest\033[0m:")
        print ("Min: \033[90mYuriko (25)\033[0m, \033[35mSha-Ming (20.5)\033[0m, \033[31mKukurushka (20.5)\033[0m, \033[36mJonas (19.5)\033[0m, \033[91mSQ (14.5)\033[0m")
        print ("Max: \033[90mYuriko (49.5)\033[0m, \033[91mSQ (47.5)\033[0m, \033[31mKukurushka (45)\033[0m, \033[36mJonas (43.5)\033[0m, \033[35mSha-Ming (40.5)\033[0m\n")
        print ("\033[34mWeakest\033[0m:")
        print ("Min: Shigemichi (0.5), \033[94mGina (2)\033[0m, \033[33mComet (4.5)\033[0m, \033[32mStella (5)\033[0m")
        print ("Max: Shigemichi (6), \033[94mGina (13)\033[0m, \033[33mComet (16.5)\033[0m, \033[95mOtome (23)\033[0m, \033[92mChipie (26.5)\033[0m")
    else:
        print("\033[31mInvalid choice. Return to menu.\033[0m")

def main():
    characters = display_character_names()
    matrix = [[[] for _ in characters] for _ in characters]

    while True:
        display_matrix(matrix, characters)
        print("\nChoose an option:\n")
        print("1. Record an action\n")
        print("2. Delete the most recent action\n")
        print("3. Assign/Remove roles\n")
        print("4. Show character stats\n")
        print("9. Initialize\n")
        print("0. Exit\n")
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
            characters = display_character_names()
            matrix = [[[] for _ in characters] for _ in characters]
        elif option == '0':
            print("Exiting...")
            break
        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, or 9.\033[0m")


if __name__ == "__main__":
    main()
