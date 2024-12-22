import actions
import additional_functions

DEFAULT, Z, INVALID, VOTE =-1, -1, -2, 1

characters, numbered_characters, removed_characters, action_names, action_names_abbr, role_symbols, role_names = {}, {}, {}, {}, {}, {}, {}
matrix, words_to_color, notes, history = [], [], [], []
table = ""

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
    if option == '1':
        t.print("\033[32mIntuition\033[0m")
        t.print ("Strongest:")
        t.print ("Min: \033[33mComet (25.5)\033[0m, \033[97mRemnan (21)\033[0m, \033[90mYuriko (20.5)\033[0m, \033[92mChipie (17)\033[0m, \033[95mOtome (16.5)\033[0m, \033[31mKukurushka (16)\033[0m")
        t.print ("Max: \033[33mComet (49.5)\033[0m, \033[94mGina (45.5)\033[0m, \033[90mYuriko (42)\033[0m, \033[97mRemnan (41)\033[0m, \033[92mChipie (39)\033[0m, \033[31mKukurushka (35.5)\033[0m, \033[95mOtome (32)\033[0m, Setsu (28.5)")
        t.print ("Weakest:")
        t.print ("Min: \033[96mRaqio (0.5)\033[0m, Shigemichi (3.5), \033[94mGina\033[0m (4), \033[32mStella (5)\033[0m, \033[35mSha-Ming (5.5)\033[0m, Setsu (8), Jonas (9.5), SQ (11)")
        t.print ("Max: \033[96mRaqio (0.5)\033[0m, \033[35mSha-Ming (6.5)\033[0m, Shigemichi (14.5), \033[32mStella (18)\033[0m")
    elif option == '2':
        t.print("\033[35mPerformance\033[0m")
        t.print ("Strongest:")
        t.print ("Min: \033[90mYuriko (25)\033[0m, \033[35mSha-Ming (20.5)\033[0m, \033[31mKukurushka (20.5)\033[0m, \033[36mJonas (19.5)\033[0m, \033[91mSQ (14.5)\033[0m")
        t.print ("Max: \033[90mYuriko (49.5)\033[0m, \033[91mSQ (47.5)\033[0m, \033[31mKukurushka (45)\033[0m, \033[36mJonas (43.5)\033[0m, \033[35mSha-Ming (40.5)\033[0m")
        t.print ("Weakest:")
        t.print ("Min: Shigemichi (0.5), \033[94mGina (2)\033[0m, \033[33mComet (4.5)\033[0m, \033[32mStella (5)\033[0m")
        t.print ("Max: Shigemichi (6), \033[94mGina (13)\033[0m, \033[33mComet (16.5)\033[0m, \033[95mOtome (23)\033[0m, \033[92mChipie (26.5)\033[0m")
    else:
        t.print("\033[91mInvalid input\033[0m")   

    t.print()

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
        "function": lambda: additional_functions.see_full_hostory()}, 
    7: {"title": "Remove character from the list", 
        "function": lambda: actions.remove_character_from_list()}, 
    8: {"title": "Restore removed characters", 
        "function": lambda: actions.restore_removed_characters()}, 
    9: {"title": "Initialize table", 
        "function": lambda: reset()}, 
    0: {"title": "Exit", 
        "function": lambda: actions.exit_program()}
    }