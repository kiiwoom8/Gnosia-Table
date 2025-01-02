import data
import actions
import handle_text as t
import backup

def assign_roles():
    while True:
        t.check_error()
        t.t_print("\033[92mAssign\033[0m/\033[91mremove\033[0m Roles: ")
        display_roles()

        role_choice = t.t_input("Select a role by number: ")
        if role_choice:
            if role_choice == 'z':
                return
            if actions.validate_choice(role_choice, 'role'):
                role_choice = int(role_choice)
                char_index = actions.select_character("assigned/removed", 
                                                      f"{data.LGREEN}Assign{data.RESET}/{data.BLUSH}remove{data.RESET} a role ({data.roles[role_choice]["Symbol"]}): ")
                if char_index not in ['z', 'p']:
                    backup.backup_state()
                    toggle_role(int(char_index), role_choice)
            else:
                t.error_text = "\033[31mInvalid choice. Try again.\033[0m"


def display_roles():
    for role_num, role in data.roles.items():
        formatted_num = f" {role_num}" if role_num < 10 else str(role_num)
        t.t_print(f"{formatted_num}. {role["Name"]} ({role["Symbol"]})")
    t.t_print(" z. Go back")


def toggle_role(char_index, role_choice):
    role_name = data.roles[role_choice]["Name"]
    role_symbol = data.roles[role_choice]["Symbol"]
    if role_name in ["Killed", "Cold Sleep"]:
        actions.toggle_color(char_index, role_choice)
        return
    if char_index in data.current_roles[role_name]:
        data.current_roles[role_name].remove(char_index)
        t.r_print(f"\033[91mRemoved\033[0m {role_name} ({role_symbol}) from {data.characters[char_index]}.")
    else:
        data.current_roles[role_name].append(char_index)
        char_index = int(char_index)
        t.r_print(f"\033[94mAssigned\033[0m {role_name} ({role_symbol}) to {data.characters[char_index]}.")