import re
import data
import actions
import table_rendering as tr
import additional_functions as af

class Main:
    def __init__(self):
        self.initialize_all()

    def initialize_all(self):
        self.characters = data.get_character_list()
        self.matrix = [[[] for _ in self.characters] for _ in self.characters]
        self.words_to_color = data.get_words_to_color()
        self.notes = []

def main():
    m = Main()
    while True:
        tr.display_matrix(m.characters, m.matrix, m.words_to_color)
        print("Choose an option:")
        print ("1. Record an action")
        print ("2. Delete the most recent action")
        print ("3. Assign/Remove roles")
        print ("4. Notepad")
        print ("5. Show character stats")
        print ("9. Initialize table")
        print ("0. Exit")
        option = input("Enter your choice: ").strip()

        if option == '1':
            m.matrix = actions.record_action(m.characters, m.matrix)
        elif option == '2':
            m.matrix = actions.delete_recent_action(m.characters, m.matrix)
        elif option == '3':
            m.characters, m.words_to_color = actions.assign_roles(m.characters, m.words_to_color)
        elif option == '4':
            m.notes = af.take_note(m.notes)
        elif option == '5':
            af.show_stats()
        elif option =='9':
            m.initialize_all()
        elif option == '0':
            print("Exiting...")
            break
        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, 9, or 0.\033[0m")

if __name__ == "__main__":
    main()
