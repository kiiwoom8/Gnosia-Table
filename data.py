import functions
import actions
import discussion
import role
import additional_functions
import backup
import file

RED, BLUSH, GREEN, LBLUE, BLUE, YELLOW, LYELLOW, LGREEN, GRAY, RESET = "\033[31m", "\033[91m", "\033[92m","\033[94m", "\033[34m", "\033[33m", "\033[93m", "\033[92m", "\033[90m", "\033[0m"

characters_list = {
    1: "Me", 2: "Setsu", 3: "Gina", 4: "SQ", 5: "Raqio", 6: "Stella", 
    7: "Shigemichi", 8: "Chipie", 9: "Comet", 10: "Jonas", 11: "Kukurushka", 
    12: "Otome", 13: "ShaMing", 14: "Remnan", 15: "Yuriko"
}

character_stats = additional_functions.color_code_stats({name: dict(zip(
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
    ("ShaMing", ["14.5-29", "5.5-6.5", "6.5-6.5", "16.5-34.5", "20.5-40.5", "25-49.5"]),
    ("Remnan", ["2-2", "21-41", "15-28", "10-29", "13-33", "22.5-43.5"]),
    ("Yuriko", ["25.5-49.5", "20.5-42", "22-44", "17.5-37.5", "25-49.5", "12-25"])
]})

roles = {name: symbol for (name, symbol) in [
        ("Gnosia", "🅰️"),
        ("AC Follower", "🕷️"),
        ("Engineer", "🛠️"),
        ("Doctor", "⚕️"),
        ("Bug", "☠️"),
        ("Guardian Angel", "🕊️"),
        ("Crew", "✳️"),
        ("Enemy", "⚠️"),
        ("Suspicious", "👁️"),
        ("Killed", "🔪"),
        ("Cold Sleep", "🧊"),
    ]}

action_list = {
    name: {"Name": f"{color}{name}{RESET}", "Abbr": abbr, "Color": color, "Type": type}
    for name, (name, abbr, color, type) in enumerate([
        ("Doubt", "Dou", RED, "Default"),
        ("Cover", "Cov", BLUE, "Default"),
        ("Collab", "Col", BLUE, "Default"),
        ("Refuse", "Ref", BLUSH, None),
        ("Agree Doubt", "Ag", BLUSH, "Doubt"),
        ("Exaggerate Agree", "ExA", RED, "Doubt"),
        ("Seek Agreement Doubt", "SeA", RED, "Doubt"),
        ("Retaliate", "Ret", RED, "Doubt"),
        ("Defend", "Def", BLUE, "Doubt"),
        ("Block Argument Doubt", "BlA", RED, "Doubt"),
        ("Help", "Hlp", BLUE, "Doubt"),
        ("Agree Defend", "AgD", LBLUE, "Defend"),
        ("Exaggerate Defend", "ExD", BLUE, "Defend"),
        ("Seek Agreement Defend", "SeD", BLUE, "Defend"),
        ("Argue", "Arg", RED, "Defend"),
        ("Block Argument Defend", "BlD", BLUE, "Defend"),
        ("Vote", "Vo", RED, None),
    ])
}

options = {
    k if "Exit" not in title else 0: {"title": title, "function": func}
    for k, (title, func) in enumerate([
        ("Record an action", discussion.handle_discussion),
        ("Delete last actions", actions.delete_last_action),
        ("Assign/Remove roles", role.assign_roles),
        # (f"{LYELLOW}Notepad{RESET}", additional_functions.take_note),
        ("Show character stats", additional_functions.show_stats),
        ("Display the full history", additional_functions.see_full_history),
        ("Remove character from the list", actions.remove_character_from_list),
        ("Import/export table", file.choose_option),
        ("Initialize table", functions.reset),
        (f"{GRAY}Exit{RESET}", functions.exit_program)
    ], start=1)
}

def reset():
    global characters, removed_characters, votes, voting_characters, current_roles
    global matrix, words_to_color, participation, collab, ties, previous_ties, notes, history
    global table
    global first_attacker, first_defender, target
    global discussion_doubt, discussion_defend
    global round

    characters = characters_list.copy()
    matrix = [[[] for _ in characters] for _ in characters]
    words_to_color = {action["Abbr"]: action["Color"] for action in action_list.values()}
    current_roles = {role: [] for role in roles.keys()}
    removed_characters, votes, voting_characters = {}, {}, {}
    participation, collab, ties, previous_ties, notes, history = [], [], [], [], [], []
    first_attacker, first_defender, target = None, None, None
    discussion_doubt, discussion_defend = False, False
    table = ""
    round= 1

def convert_digits(i):
    if i > 9:
        i = chr(87 + i)
    else:
        i = str(i)
    return i