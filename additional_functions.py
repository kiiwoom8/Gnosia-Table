import data
import handle_text as t

def delete_all():
    t.delete_text()

def take_note():
    while True:
        delete_all()
        draw_note_line()
        if data.notes:
            t.t_print("\033[32mYour Notes:\033[0m")
            for idx, content in enumerate(data.notes, start=1):
                t.t_print(f"({idx}) {content}")
        else:
            t.t_print("\033[91m(No note)\033[0m")
        draw_note_line()
        t.t_print("1. Take a note")
        t.t_print("2. Delete a note")
        t.t_print("z. Go back")

        option = t.t_input("Enter your choice: ").strip().lower()
        if option == '1':
            content = t.t_input("Enter the note content: ").strip()
            if not content:
                t.t_print("\033[31mNote content cannot be empty.\033[0m")
                continue
            data.notes.append(content)
            t.t_print("Note added successfully.")
        elif option == '2':
            if not data.notes:
                t.t_print("\033[31mNo notes to delete.\033[0m")
                continue

            try:
                note_number = int(t.t_input("Enter the number of the note to delete: ").strip())
                if 1 <= note_number <= len(data.notes):
                    deleted_note = data.notes.pop(note_number - 1)
                    t.t_print(f"Note '{deleted_note}' deleted successfully.")
                else:
                    t.t_print("\033[31mInvalid number. Please try again.\033[0m")
            except ValueError:
                t.t_print("\033[31mInvalid input. Please enter a number.\033[0m")
        elif option == 'z':
            delete_all()
            return
        else:
            t.t_print("\033[31mInvalid choice. Please select 1, 2, 3, or 'z'.\033[0m")
        
def draw_note_line():
    text= ""
    for _ in range(100):
        text +="\033[33m-\033[0m"
    t.t_print(f"{text}")

def show_stats():
    option = "0"
    while True:
        t.check_error()
        option = t.t_input("Enter your choice (or 'z' to go back): ")
        if option == 'z':
            return
        elif not option:
            pass
        else: 
            print_stats(option)

def print_stats(option):
    if option == "1":
        t.error_text = "\033[31mYou cannot check the stats of the player.\033[0m"
    try: 
        character_name = data.characters[int(option)]
        if character_name in data.character_stats:
            stats = data.character_stats[character_name]
            t.t_print(f"Name: {character_name}")
            for key, value in stats.items():
                t.t_print(f"{key}: {value}")
    except (ValueError, KeyError):
        t.error_text = "\033[31mInvalid choice. Please select a valid character.\033[0m"

def see_full_history():
    history = data.history
    text = "\n".join(history) if history else "\033[91m(There's no history recorded.)\033[0m"
    print(text)
    input("Press any key to exit: ").strip().lower()