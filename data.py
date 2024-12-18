def get_character_list():
    character_list = {
        1: "Me", 2: "Setsu", 3: "Gina", 4: "SQ", 5: "Raqio", 6: "Stella", 7: "Shigemichi", 8: "Chipie", 9: "Comet", 10: "Jonas",
        11: "Kukurushka", 12: "Otome", 13: "Sha-Ming", 14: "Remnan", 15: "Yuriko"
    }
    return character_list

def get_options():
    options = {1: "Record an action", 2: "Delete the most recent action", 3: "Assign/Remove roles", 4: "Notepad", 5: "Show character stats",
               8: "Remove character from the list", 9: "Initialize table", 0: "Exit"}
    return options


def get_action_list():
    action_names = {1: "\033[91mVote\033[0m", 2: "\033[91mDoubt\033[0m", 3: "\033[91mAgree\033[0m", 4: "\033[94mCover\033[0m", 5: "\033[94mDefend\033[0m", 
                    6: "\033[91mExaggerate Agree\033[0m", 7: "\033[94mExaggerate Defend\033[0m", 8: "\033[91mArgue\033[0m", 
                    9: "\033[91mSeek Agreement\033[0m", 0: "\033[94mSeek Agreement\033[0m"}
    action_names_abbr = {1: "Vo", 2: "Dou", 3: "Ag", 4: "Cov", 5: "Def", 6: "ExA", 7: "ExD", 8: "Arg", 9: "SeA", 0: "SeD"}
    return action_names, action_names_abbr

def get_words_to_color():
    words_to_color = {
        "Vo": "\033[31m", "Dou": "\033[31m", "Ag": "\033[91m",
        "Cov": "\033[34m", "Def": "\033[94m", "ExA": "\033[31m", 
        "ExD": "\033[34m", "Arg": "\033[31m", "SeA": "\033[31m", 
        "SeD": "\033[34m",
    }
    return words_to_color

def get_roles_list():
    role_symbols = {1: "🅰️", 2: "🕷️", 3: "🛠️", 4: "⚕️", 5: "☠️", 6: "🕊️", 7: "✳️", 8: "⚠️", 9: "🔪", 10: "🧊"}
    role_names = {1: "Gnosia", 2: "AC Follower", 3: "Engineer", 4: "Doctor", 5: "Bug", 6: "Guardian Angel", 7: "Crew", 8: "Enemy", 9: "Kiiled", 10: "Cold Sleep"}
    return role_symbols, role_names


def print_stats(option):
    print()
    if option == '1':
        print("\033[32mIntuition\033[0m")
        print ("\033[31mStrongest\033[0m:")
        print ("Min: \033[33mComet (25.5)\033[0m, \033[97mRemnan (21)\033[0m, \033[90mYuriko (20.5)\033[0m, \033[92mChipie (17)\033[0m, \033[95mOtome (16.5)\033[0m, \033[31mKukurushka (16)\033[0m")
        print ("Max: \033[33mComet (49.5)\033[0m, \033[94mGina (45.5)\033[0m, \033[90mYuriko (42)\033[0m, \033[97mRemnan (41)\033[0m, \033[92mChipie (39)\033[0m, \033[31mKukurushka (35.5)\033[0m, \033[95mOtome (32)\033[0m, Setsu (28.5)")
        print ("\033[34mWeakest\033[0m:")
        print ("Min: \033[96mRaqio (0.5)\033[0m, Shigemichi (3.5), \033[94mGina\033[0m (4), \033[32mStella (5)\033[0m, \033[35mSha-Ming (5.5)\033[0m, Setsu (8), Jonas (9.5), SQ (11)")
        print ("Max: \033[96mRaqio (0.5)\033[0m, \033[35mSha-Ming (6.5)\033[0m, Shigemichi (14.5), \033[32mStella (18)\033[0m")
    elif option == '2':
        print("\033[35mPerformance\033[0m")
        print ("\033[31mStrongest\033[0m:")
        print ("Min: \033[90mYuriko (25)\033[0m, \033[35mSha-Ming (20.5)\033[0m, \033[31mKukurushka (20.5)\033[0m, \033[36mJonas (19.5)\033[0m, \033[91mSQ (14.5)\033[0m")
        print ("Max: \033[90mYuriko (49.5)\033[0m, \033[91mSQ (47.5)\033[0m, \033[31mKukurushka (45)\033[0m, \033[36mJonas (43.5)\033[0m, \033[35mSha-Ming (40.5)\033[0m")
        print ("\033[34mWeakest\033[0m:")
        print ("Min: Shigemichi (0.5), \033[94mGina (2)\033[0m, \033[33mComet (4.5)\033[0m, \033[32mStella (5)\033[0m")
        print ("Max: Shigemichi (6), \033[94mGina (13)\033[0m, \033[33mComet (16.5)\033[0m, \033[95mOtome (23)\033[0m, \033[92mChipie (26.5)\033[0m")
    else:
        print("\033[31mInvalid choice. Return to menu.\033[0m")