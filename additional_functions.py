import data

def take_note(notes):
    while True:
        if notes:
            print("\n\033[32mYour Notes:\033[0m")
            for idx, content in enumerate(notes, start=1):
                print(f"{idx}. {content}")

        print("\nNotepad:")
        print("1. Take a note")
        print("2. Delete a note")
        print("z. Go back")

        option = input("Enter your choice: ").strip().lower()

        if option == '1':
            # Add a new note
            content = input("Enter the note content: ").strip()
            if not content:
                print("\033[31mNote content cannot be empty.\033[0m")
                continue
            notes.append(content)
            print("Note added successfully.")

        elif option == '2':
            # Delete an existing note by number
            if not notes:
                print("\033[31mNo notes to delete.\033[0m")
                continue

            print("\nYour Notes:")
            for idx, content in enumerate(notes, start=1):
                print(f"{idx}. {content}")

            try:
                note_number = int(input("\nEnter the number of the note to delete: ").strip())
                if 1 <= note_number <= len(notes):
                    deleted_note = notes.pop(note_number - 1)
                    print(f"\033[32mNote '{deleted_note}' deleted successfully.\033[0m")
                else:
                    print("\033[31mInvalid number. Please try again.\033[0m")
            except ValueError:
                print("\033[31mInvalid input. Please enter a number.\033[0m")

        elif option == 'z':
            print("Returning to main menu...")
            return notes

        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, or 'z'.\033[0m")
        
def show_stats():
    print("1. \033[32mIntuition\033[0m")
    print("2. \033[35mPerformance\033[0m")
    # print("3. Logic")
    option = input("Enter your choice: ").strip()
    print()
    data.print_stats(option)