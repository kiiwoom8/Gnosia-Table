import os
import data
import actions as a
import handle_text
import table_rendering as tr
import additional_functions as af

class Main:
    def __init__(self):
        self.initialize_all()

    def initialize_all(self):
        os.system("cls")
        self.characters = data.get_character_list()
        self.original_characters_list = data.get_character_list()
        self.matrix = [[[] for _ in self.characters] for _ in self.characters]
        self.words_to_color = data.get_words_to_color()
        self.notes = []

def main():
    m = Main()
    t = handle_text.HandleText()
    while True:
        tr.display_matrix(m.characters, m.matrix, m.words_to_color)
        t.print("Choose an option:")
        t.print ("1. Record an action")
        t.print ("2. Delete the most recent action")
        t.print ("3. Assign/Remove roles")
        t.print ("4. Notepad")
        t.print ("5. Show character stats")
        t.print ("8. Remove character from the list")
        t.print ("9. Initialize table")
        t.print ("0. Exit")
        option = t.input("Enter your choice: ").strip()

        if option == '1':
            m.matrix = a.record_action(m.characters, m.matrix)
        elif option == '2':
            m.matrix = a.delete_recent_action(m.characters, m.matrix)
        elif option == '3':
            m.characters, m.original_characters_list, m.words_to_color = a.assign_roles(m.characters, m.original_characters_list, m.words_to_color)
        elif option == '4':
            m.notes = af.take_note(m.notes)
        elif option == '5':
            af.show_stats()
        elif option == '8':
            m.characters, m.original_characters_list, m.words_to_color = a.remove_character_from_list(m.characters, m.original_characters_list, m.words_to_color)
        elif option =='9':
            m.initialize_all()
        elif option == '0':
            print("Exiting...")
            break
        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, 9, or 0.\033[0m")

if __name__ == "__main__":
    main()
