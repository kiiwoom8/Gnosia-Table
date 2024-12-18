import data

def take_note(notes):
    while True:
        print()
        draw_note_line()

        if notes:
            print("\n\033[32mYour Notes:\033[0m")
            for idx, content in enumerate(notes, start=1):
                print(f"({idx}) {content}")
        else:
            print("\n\033[91m(No note)\033[0m")

        draw_note_line()

        print("\n1. Take a note")
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

            print("\nWhich record do you want to delete:")
            for idx, content in enumerate(notes, start=1):
                print(f"{idx}. {content}")

            try:
                note_number = int(input("\nEnter the number of the note to delete: ").strip())
                if 1 <= note_number <= len(notes):
                    deleted_note = notes.pop(note_number - 1)
                    print(f"Note '{deleted_note}' deleted successfully.")
                else:
                    print("\033[31mInvalid number. Please try again.\033[0m")
            except ValueError:
                print("\033[31mInvalid input. Please enter a number.\033[0m")

        elif option == 'z':
            print("Returning to main menu...")
            return notes

        else:
            print("\033[31mInvalid choice. Please select 1, 2, 3, or 'z'.\033[0m")
        
def draw_note_line():
    for _ in range(100):
            print("\033[33m-\033[0m", end='')

def show_stats():
    while True:
        print("\n1. \033[32mIntuition\033[0m")
        print("2. \033[35mPerformance\033[0m")
        print("z. Go back")
        # print("3. Logic")
        option = input("Enter your choice: ").strip()

        if option.lower() == 'z':
            return
        
        data.print_stats(option)