import re
import data

class Main:
    def __init__(self):
        self.initialize_table()
        self.action_names, self.action_names_abbr = data.get_action_list()
        self.role_symbols, self.role_names = data.get_roles_list()
        
    def get_user_choice(self):
        while True:
            count = 0
            for character in self.characters:
                count += 1
                print(f"{count}. {character}")
            user_input = input("Enter the number for your choice (or 'z' to go back): ")
            if user_input.lower() == 'z':
                print("Going back...")
                return None
            try:
                choice = int(user_input)
                if 1 <= choice <= len(self.characters):
                    return choice
                else:
                    print(f"\033[31mPlease enter a number between 1 and {len(self.characters)}.\033[0m")
            except ValueError:
                print("\033[31mInvalid input. Please enter a number or 'z' to go back.\033[0m")

    def record_action(self):
        action_choice = self.select_action()

        if action_choice not in self.action_names:
            return

        action = self.action_names_abbr[action_choice]
        actor = self.select_character("acting")
        if actor is None:
            return
        target = self.select_character("target")
        if target is None:
            return
        if actor == target:
            print("\033[31mCannot act on self. Please try again.\033[0m")
            return
        actor_name = self.characters[actor - 1]
        target_name = self.characters[target - 1]

        self.matrix[actor - 1][target - 1].append(action)
        print(f"Recorded: {actor_name} {action} {target_name}")

    def delete_recent_action(self):
        print("\nDelete the most recent action from a character pair:")
        actor = self.select_character("actor")
        if actor is None:
            return
        target = self.select_character("target")
        if target is None:
            return

        actor_name = self.characters[actor - 1]
        target_name = self.characters[target - 1]
        actions = self.matrix[actor - 1][target - 1]

        if actions:
            removed_action = actions.pop()
            print(f"Deleted: {actor_name} {removed_action} {target_name}")
        else:
            print(f"No actions recorded between {actor_name} and {target_name}.")

    def select_action(self):
        print("\nSelect the action performed:")
        for number, action_name in self.action_names.items():
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

    def select_character(self, role_type):
        print(f"Select the {role_type} character:")
        return self.get_user_choice()

    def assign_roles(self):
        while True:
            print("\nAssign or Remove Roles:")
            for key in self.role_names:
                print(f"{key}. {self.role_names[key]} ({self.role_symbols[key]})")
            print("z. Go back")

            role_choice = input("Select a role by number: ").strip()
            if role_choice.lower() == 'z':
                print("Returning to main menu...")
                break
    
            try:
                role_choice = int(role_choice)
                if role_choice not in self.role_symbols:
                    print("Invalid role choice. Try again.")
                    continue
            except ValueError:
                print("\033[31mInvalid input. Try again.\033[0m")
                continue

            char_index = self.select_character("assign/remove")
            if char_index is None:
                continue  
            char_index -= 1

            if role_choice in [9, 10]:
                character = self.characters_original[char_index]
                if character in self.words_to_color:
                    self.words_to_color.pop(character)
                else:
                    if role_choice == 9:
                        self.words_to_color[character] = "\033[31m"
                    elif role_choice == 10:
                        self.words_to_color[character] = "\033[34m"
            else:    
                symbol = self.role_symbols[role_choice]
                self.toggle_role(char_index, symbol, self.role_names[role_choice])

    def toggle_role(self, char_index, symbol, role_name):
        if symbol in self.characters[char_index]:
            self.characters[char_index] = self.characters[char_index].replace(symbol, "")
            print(f"Removed {role_name} ({symbol}) from {self.characters[char_index]}.")
        else:
            self.characters[char_index] += symbol
            print(f"Assigned {role_name} ({symbol}) to {self.characters[char_index]}.")

    def display_matrix(self):
        col_widths = self.calculate_column_widths()
        header = self.build_header(col_widths)
        header = self.apply_color(header)
        print(f"\n{header}")
        print("-" * len(header))

        for i, row in enumerate(self.matrix):
            row_data = [";".join(actions) if actions else "-" for actions in row]
            row_line = self.format_row(i, row_data, col_widths)
            colored_text = self.apply_color(row_line)
            print(f"{colored_text}\n")

    def calculate_column_widths(self):
        col_widths = [max(len(self.characters[i]), max((len(";".join(actions)) for actions in column), default=0)) + 2
                    for i, column in enumerate(zip(*self.matrix))]
        return col_widths

    def build_header(self, col_widths):
        header_width = max(len(name) for name in self.characters) + 2
        header = "".ljust(header_width) + "".join(
            char.ljust(col_widths[i]) for i, char in enumerate(self.characters)
        )
        header = self.apply_color(header)
        return header

    def format_row(self, i, row_data, col_widths):
        header_width = max(len(name) for name in self.characters) + 2
        row_line = self.characters[i].ljust(header_width) + "".join(
            row_data[j].ljust(col_widths[j]) for j in range(len(row_data))
        )
        return row_line

    def apply_color(self, text):
        reset_color = "\033[0m"
        for word, color in self.words_to_color.items():
            text = re.sub(rf'(?<!\w)({re.escape(word)})(?!\w)', rf'{color}\1{reset_color}', text)
        return text

    def show_stats(self):
        print("1. \033[32mIntuition\033[0m")
        print("2. \033[35mPerformance\033[0m")
        # print("3. Logic")
        option = input("Enter your choice: ").strip()
        print()
        data.print_stats(option)

    def initialize_table(self):
        self.characters = data.get_character_list()
        self.characters_original = data.get_character_list()
        self.matrix = [[[] for _ in self.characters] for _ in self.characters]
        self.words_to_color = data.get_words_to_color()

def main():
    m = Main()
    while True:
        m.display_matrix()
        print("Choose an option:")
        print ("1. Record an action")
        print ("2. Delete the most recent action")
        print ("3. Assign/Remove roles")
        print ("4. Show character stats")
        print ("9. Initialize table")
        print ("0. Exit")
        option = input("Enter your choice: ").strip()

        if option == '1':
            m.record_action()
        elif option == '2':
            m.delete_recent_action()
        elif option == '3':
            m.assign_roles()
        elif option == '4':
            m.show_stats()
        elif option =='9':
            m.initialize_table()
        elif option == '0':
            print("Exiting...")
            break
        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, 9, or 0.\033[0m")

if __name__ == "__main__":
    main()
