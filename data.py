import actions
import additional_functions

RED, BLUSH, LBLUE, BLUE, RESET = "\033[31m", "\033[91m", "\033[94m", "\033[34m", "\033[0m"

numbered_characters, removed_characters, current_roles = {}, {}, {}
matrix, words_to_color, notes, history = [], [], [], []
table = ""

characters = {
    1: "Me", 2: "Setsu", 3: "Gina", 4: "SQ", 5: "Raqio", 6: "Stella", 
    7: "Shigemichi", 8: "Chipie", 9: "Comet", 10: "Jonas", 11: "Kukurushka", 
    12: "Otome", 13: "Sha-Ming", 14: "Remnan", 15: "Yuriko"
}

character_stats = {name: dict(zip(
    ["Charisma", "Intuition", "Logic", "Charm", "Performance", "Stealth"], stats)) for name, stats in [
    ("Setsu", ["10-35", "8-28.5", "12-38.5", "11-36.5", "9.5-31", "3.5-17.5"]),
    ("Gina", ["3.5-17.5", "4-45.5", "10-31.5", "7.5-24", "2-13", "9-31.5"]),
    ("SQ", ["5.5-22", "11-21.5", "2.5-12", "15.5-46", "14.5-47.5", "3-38.5"]),
    ("Raqio", ["3-16.5", "0.5-0.5", "20.5-49.5", "2-7.5", "11-35.5", "4.5-20.5"]),
    ("Stella", ["7.5-27", "5-18", "13-42", "1.5-27.5", "5-30.5", "7.5-29"]),
    ("Shigemichi", ["17-45.5", "3.5-14.5", "2-9.5", "0.5-17.5", "0.5-6", "16-45"]),
    ("Chipie", ["10-25", "17-39", "7.5-18.5", "13.5-31", "10.5-26.5", "15-33.5"]),
    ("Comet", ["5.5-17", "25.5-49.5", "0.5-0.5", "11-32.5", "4.5-16.5", "7.5-22"]),
    ("Jonas", ["16.5-38.5", "9.5-25", "12-34", "7-21.5", "19.5-43.5", "15.5-37"]),
    ("Kukurushka", ["4.5-14", "16-35.5", "0.5-3.5", "22.5-49.5", "20.5-45", "17.5-40.5"]),
    ("Otome", ["7.5-16", "16.5-32", "24-46.5", "20.5-42", "11-23", "13.5-26.5"]),
    ("Sha-Ming", ["14.5-29", "5.5-6.5", "6.5-6.5", "16.5-34.5", "20.5-40.5", "25-49.5"]),
    ("Remnan", ["2-2", "21-41", "15-28", "10-29", "13-33", "22.5-43.5"]),
    ("Yuriko", ["25.5-49.5", "20.5-42", "22-44", "17.5-37.5", "25-49.5", "12-25"])
]}

roles = {i + 1: {"Name": name, "Symbol": symbol} for i, (name, symbol) in enumerate([
        ("Gnosia", "🅰️"),
        ("AC Follower", "🕷️"),
        ("Engineer", "🛠️"),
        ("Doctor", "⚕️"),
        ("Bug", "☠️"),
        ("Guardian Angel", "🕊️"),
        ("Crew", "✳️"),
        ("Enemy", "⚠️"),
        ("Killed", "🔪"),
        ("Cold Sleep", "🧊"),
        ("Suspicious", "👁️"),
    ])}

action_list = {
    i + 1: {"Name": f"{color}{name}{RESET}", "Abbr": abbr, "Color": color}
    for i, (name, abbr, color) in enumerate([
        ("Vote", "Vo", RED),
        ("Doubt", "Dou", RED),
        ("Agree", "Ag", BLUSH),
        ("Cover", "Cov", BLUE),
        ("Defend", "Def", LBLUE),
        ("Exaggerate Agree", "ExA", RED),
        ("Exaggerate Defend", "ExD", BLUE),
        ("Argue", "Arg", RED),
        ("Seek Agreement", "SeA", RED),
        ("Seek Agreement", "SeD", BLUE),
    ])
}

options = {
    1: {"title": "Record an action", 
        "function": lambda: actions.act()}, 
    2: {"title": "Delete the most recent action", 
        "function": lambda: actions.delete_recent_action()}, 
    3: {"title": "Assign/Remove roles", 
        "function": lambda: actions.assign_roles()},
    4: {"title": "\033[33mNotepad\033[0m", 
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
    0: {"title": "\033[90mExit\033[0m", 
        "function": lambda: exit(0)}
    }

def reset():
    global matrix, current_roles, roles, words_to_color, notes, history, removed_characters
    matrix = [[[] for _ in characters] for _ in characters]
    words_to_color = get_words_to_color()
    current_roles = get_empty_roles_list()
    notes, history = [], []
    removed_characters = {}

def set_numbered_character_list():
    global characters, numbered_characters
    numbered_characters = {
        num: char if char == " " else f"{' ' if num < 10 else ''}{num}. {char}"
        for num, char in characters.items()
    }
    return numbered_characters

def get_empty_roles_list():
    return {role["Name"]: [] for role in roles.values()}

def get_words_to_color():
    return {action["Abbr"]: action["Color"] for action in action_list.values()}