import data
import handle_text

t = handle_text.HandleText()

def take_note(notes):
    while True:
        t.delete_all()
        draw_note_line()

        if notes:
            t.printr("\033[32mYour Notes:\033[0m")
            for idx, content in enumerate(notes, start=1):
                t.printr(f"({idx}) {content}")
        else:
            t.printr("\033[91m(No note)\033[0m")

        draw_note_line()

        t.print("1. Take a note")
        t.print("2. Delete a note")
        t.print("z. Go back")

        option = t.input("Enter your choice: ").strip().lower()

        if option == '1':
            # Add a new note
            content = t.input("Enter the note content: ").strip()
            if not content:
                t.print("\033[31mNote content cannot be empty.\033[0m")
                continue
            notes.append(content)
            t.print("Note added successfully.")

        elif option == '2':
            # Delete an existing note by number
            if not notes:
                t.print("\033[31mNo notes to delete.\033[0m")
                continue

            t.print("Which record do you want to delete:")
            for idx, content in enumerate(notes, start=1):
                t.print(f"{idx}. {content}")

            try:
                note_number = int(t.input("Enter the number of the note to delete: ").strip())
                if 1 <= note_number <= len(notes):
                    deleted_note = notes.pop(note_number - 1)
                    t.print(f"Note '{deleted_note}' deleted successfully.")
                else:
                    t.print("\033[31mInvalid number. Please try again.\033[0m")
            except ValueError:
                t.print("\033[31mInvalid input. Please enter a number.\033[0m")

        elif option == 'z':
            return notes

        else:
            t.print("\033[31mInvalid choice. Please select 1, 2, 3, or 'z'.\033[0m")
        
def draw_note_line():
    for _ in range(100):
        print("\033[33m-\033[0m", end='')
    t.printr()

def show_stats():
    while True:
        t.print("1. \033[32mIntuition\033[0m")
        t.print("2. \033[35mPerformance\033[0m")
        t.print("z. Go back")
        # t.print("3. Logic")
        option = t.input("Enter your choice: ").strip()

        if option.lower() == 'z':
            return
        
        data.print_stats(option)