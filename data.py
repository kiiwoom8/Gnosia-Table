import actions
import additional_functions

DEFAULT, Z, INVALID, PASS, VOTE =-1, -1, -2, -3, 1,

characters, numbered_characters, removed_characters, action_names, action_names_abbr, role_symbols, role_names = {}, {}, {}, {}, {}, {}, {}
matrix, words_to_color, notes, history = [], [], [], []
table = ""
character_data = [
    (2, "Setsu", "10-35", "8-28.5", "12-38.5", "11-36.5", "9.5-31", "3.5-17.5"),
    (3, "Gina", "3.5-17.5", "4-45.5", "10-31.5", "7.5-24", "2-13", "9-31.5"),
    (4, "SQ", "5.5-22", "11-21.5", "2.5-12", "15.5-46", "14.5-47.5", "3-38.5"),
    (5, "Raqio", "3-16.5", "0.5-0.5", "20.5-49.5", "2-7.5", "11-35.5", "4.5-20.5"),
    (6, "Stella", "7.5-27", "5-18", "13-42", "1.5-27.5", "5-30.5", "7.5-29"),
    (7, "Shigemichi", "17-45.5", "3.5-14.5", "2-9.5", "0.5-17.5", "0.5-6", "16-45"),
    (8, "Chipie", "10-25", "17-39", "7.5-18.5", "13.5-31", "10.5-26.5", "15-33.5"),
    (9, "Comet", "5.5-17", "25.5-49.5", "0.5-0.5", "11-32.5", "4.5-16.5", "7.5-22"),
    (10, "Jonas", "16.5-38.5", "9.5-25", "12-34", "7-21.5", "19.5-43.5", "15.5-37"),
    (11, "Kukurushka", "4.5-14", "16-35.5", "0.5-3.5", "22.5-49.5", "20.5-45", "17.5-40.5"),
    (12, "Otome", "7.5-16", "16.5-32", "24-46.5", "20.5-42", "11-23", "13.5-26.5"),
    (13, "Sha-Ming", "14.5-29", "5.5-6.5", "6.5-6.5", "16.5-34.5", "20.5-40.5", "25-49.5"),
    (14, "Remnan", "2-2", "21-41", "15-28", "10-29", "13-33", "22.5-43.5"),
    (15, "Yuriko", "25.5-49.5", "20.5-42", "22-44", "17.5-37.5", "25-49.5", "12-25"),
]
character_stats = {
    char_id: {
        "Name": name,
        "Charisma": charisma,
        "Intuition": intuition,
        "Logic": logic,
        "Charm": charm,
        "Performance": performance,
        "Stealth": stealth,
    }
    for char_id, name, charisma, intuition, logic, charm, performance, stealth in character_data
}



def reset():
    global characters, removed_characters, matrix, action_names, action_names_abbr, role_symbols, role_names, words_to_color, notes, history
    characters = get_character_list()
    words_to_color = get_words_to_color()
    matrix = [[[] for _ in characters] for _ in characters]
    notes, history = [], []
    removed_characters = {}
    if not role_names or not role_symbols or not action_names or not action_names_abbr:
        role_symbols, role_names = get_roles_list()
        action_names, action_names_abbr = get_action_list()

def get_character_list():
    return {
        1: "Me", 2: "Setsu", 3: "Gina", 4: "SQ", 5: "Raqio", 6: "Stella", 7: "Shigemichi", 8: "Chipie", 9: "Comet", 10: "Jonas",
        11: "Kukurushka", 12: "Otome", 13: "Sha-Ming", 14: "Remnan", 15: "Yuriko"
    }

def set_numbered_character_list():
    global characters, numbered_characters
    numbered_characters = {}
    for num, char in characters.items():
        if char == " ":
            numbered_characters[num] = char
        else:
            if num < 10:
                numbered_characters[num] = f" {num}. {char}"
            else:
                numbered_characters[num] = f"{num}. {char}"
    return numbered_characters

def get_action_list():
    action_names = {1: "\033[91mVote\033[0m", 2: "\033[91mDoubt\033[0m", 3: "\033[91mAgree\033[0m", 4: "\033[94mCover\033[0m", 5: "\033[94mDefend\033[0m", 
                    6: "\033[91mExaggerate Agree\033[0m", 7: "\033[94mExaggerate Defend\033[0m", 8: "\033[91mArgue\033[0m", 
                    9: "\033[91mSeek Agreement\033[0m", 0: "\033[94mSeek Agreement\033[0m"}
    action_names_abbr = {1: "Vo", 2: "Dou", 3: "Ag", 4: "Cov", 5: "Def", 6: "ExA", 7: "ExD", 8: "Arg", 9: "SeA", 0: "SeD"}
    return action_names, action_names_abbr

def get_roles_list():
    role_symbols = {1: "🅰️", 2: "🕷️", 3: "🛠️", 4: "⚕️", 5: "☠️", 6: "🕊️", 7: "✳️", 8: "⚠️", 9: "🔪", 10: "🧊", 11: "👁️"}
    role_names = {1: "Gnosia", 2: "AC Follower", 3: "Engineer", 4: "Doctor", 5: "Bug", 6: "Guardian Angel", 7: "Crew", 8: "Enemy", 9: "Kiiled", 10: "Cold Sleep", 11: "Suspicous"}
    return role_symbols, role_names

def get_words_to_color():
    return {
        "Vo": "\033[31m", "Dou": "\033[31m", "Ag": "\033[91m",
        "Cov": "\033[34m", "Def": "\033[94m", "ExA": "\033[31m", 
        "ExD": "\033[34m", "Arg": "\033[31m", "SeA": "\033[31m", 
        "SeD": "\033[34m",
    }

def print_stats(option, t):
    if option != "" and int(option) in list(character_stats.keys()):
        stats = character_stats.get(int(option), None)
        for key, value in stats.items():
            t.print(f"{key}: {value}")
    else:
        t.print("\033[31mInvalid choice. Please select a valid character.\033[0m")

def get_selections():
    return {
    1: {"title": "Record an action", 
        "function": lambda: actions.act()}, 
    2: {"title": "Delete the most recent action", 
        "function": lambda: actions.delete_recent_action()}, 
    3: {"title": "Assign/Remove roles", 
        "function": lambda: actions.assign_roles()},
    4: {"title": "Notepad", 
        "function": lambda: additional_functions.take_note()}, 
    5: {"title": "Show character stats", 
        "function": lambda: additional_functions.show_stats()}, 
    6: {"title": "See the full history", 
        "function": lambda: additional_functions.see_full_history()}, 
    7: {"title": "Remove character from the list", 
        "function": lambda: actions.remove_character_from_list()}, 
    8: {"title": "Restore removed characters", 
        "function": lambda: actions.restore_removed_characters()}, 
    9: {"title": "Initialize table", 
        "function": lambda: reset()}, 
    0: {"title": "Exit", 
        "function": lambda: actions.exit_program()}
    }