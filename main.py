import os
import data
import actions
import handle_text
import table_rendering
import additional_functions as af

class Main:
    def __init__(self):
        self.initialize_all()

    def initialize_all(self):
        data.characters = data.get_character_list()
        data.removed_characters = {}
        data.matrix = [[[] for _ in data.characters] for _ in data.characters]
        data.words_to_color = data.get_words_to_color()
        data.notes = []
        data.stored_texts = ""

def main():
    m = Main()
    t = handle_text.HandleText()
    while True:
        table_rendering.print_table()
        t.print ("Choose an option:")
        t.print ("1. Record an action")
        t.print ("2. Delete the most recent action")
        t.print ("3. Assign/Remove roles")
        t.print ("4. Notepad")
        t.print ("5. Show character stats")
        t.print ("7. Remove character from the list")
        t.print ("8. Restore removed characters")
        t.print ("9. Initialize table")
        t.print ("0. Exit")
        option = t.input("Enter your choice: ").strip()

        if option == '1':
            actions.record_action()
        elif option == '2':
            actions.delete_recent_action()
        elif option == '3':
            actions.assign_roles()
        elif option == '4':
            af.take_note()
        elif option == '5':
            af.show_stats()
        elif option == '7':
            actions.remove_character_from_list()
        elif option == '8':
            actions.restore_removed_characters()
        elif option =='9':
            m.initialize_all()
        elif option == '0':
            print("Exiting...")
            break
        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, 9, or 0.\033[0m")

if __name__ == "__main__":
    main()
