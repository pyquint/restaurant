"""
+---------------------------------------+
|   CLI Restaurant Program,             |
|   for the chef and crew of Big Egg.   |
|   Created By Static Typing.           |
+---------------------------------------+
"""

import json
import os
import tkinter as tk
from tkinter import filedialog

# Yummy spaghetti code.

_PROGRAM_NAME = "Big Egg Menu Management System™"
filedialog_root = tk.Tk()
filedialog_root.withdraw()
filedialog_root.attributes("-topmost", True)

MENU: dict[str, dict[str, float | int]] = {
    "appetizer": {},
    "main": {},
    "side": {},
    "dessert": {},
    "drink": {},
}

CUSTOMER_N = 0
CANCEL_KEY = "`"
CANCEL_MSG = f"(enter {CANCEL_KEY} to cancel)"
YES_OR_NO = ("yes", "no")


def get_menu_items(values: bool = False) -> tuple[str] | dict[str, int | float]:
    if values:
        items = {item: value for course in MENU for item, value in MENU[course].items()}
    else:
        items = tuple(item for course in MENU for item in MENU[course])
    return items


def clear_text():
    os.system('cls')
    print(f" {_PROGRAM_NAME} ".center(64, '-'))
    print('')


def fmt(string: str, align: str = 'c', padding: int = 64, char: str = ' ') -> str:
    if align == 'c':
        formatted = string.center(padding)
    elif align == 'l':
        formatted = string.ljust(padding // 2, char)
    elif align == 'r':
        formatted = string.rjust(padding // 2, char)
    elif align == 'f':
        formatted = string * padding
    else:
        raise ValueError
    return formatted


def col_fmt(string1: str, string2: str) -> str:
    return fmt(string1, 'l') + fmt(string2, 'r')


def confirm_action(action: str, repeat=1) -> bool:
    to_confirm = get_choice_loop(f"ARE YOU SURE YOU WANT TO {action.upper()}?", YES_OR_NO)
    if to_confirm == "yes":
        for i in range(repeat-1):
            if get_choice_loop(f"{action.upper()}?", YES_OR_NO) == "yes":
                return True
            else:
                return False
        return True
    else:
        return False


def get_choice_loop(prompt: str, choices,
                    prefix: str = "PROMPT: ", suffix: str = "",
                    nl: bool = True, clear: bool = True) -> str:
    """
    params:
    - prompt - message
    - choices - iterable of choices
    - prefix - prefix before the prompt (default "PROMPT: ")
    - nl - newline after successful input (default True)
    - clear - clear text after successful input (default True)

    return:
    - an element of choices
    """
    if not choices:
        raise ValueError

    while True:
        print(f"{prefix}{prompt}{suffix}")

        for i, option in enumerate(choices):
            if option:
                print(f"[{i + 1}] {option.upper()}")
        try:
            user_input = input("Enter choice: ")
            if user_input.startswith('0'):
                raise ValueError
            index = int(verify_num_with_sep(user_input))
            if index < 0:
                raise IndexError
            choice = tuple(choices)[index - 1]
            break
        except ValueError:
            print(f"\nMSG: Input is invalid.\n")
        except IndexError:
            print(f"\nMSG: Input is out of bounds.\n")

    if nl:
        print()
    if clear:
        clear_text()

    return choice


def get_num_loop(prompt: str, prefix: str = "PROMPT: ", suffix: str = "", numtype: str = "float", nl: bool = True,
                 clear: bool = True, negative: bool = False) -> float | int:
    """
    params:
    - prompt - message
    - prefix - prefix before the prompt (default "PROMPT: ")
    - numtype - type of return value ("float" or "int", default "float")
    - nl - newline after successful input (default True)
    - clear - clear text after successful input (default True)
    - negative - if allowing negative (default False)

    returns:
    - float or int value (default float)"""
    if numtype not in ("float", "int"):
        print("Parameter 'numtype' must be 'int' or 'float'.")

    while True:
        try:
            user_input = input(f"{prefix}{prompt}{suffix}")
            verified_num = verify_num_with_sep(user_input)
            number = int(verified_num) if numtype == "int" else float(verified_num)
            if not negative and number < 0:
                raise ValueError
            break
        except ValueError:
            print(f"MSG: Invalid input.\n")

    if nl:
        print()
    if clear:
        clear_text()
    return number


def verify_num_with_sep(num: str) -> str:
    if "," in num:
        sections = num.split(",")
        length = len(sections[0])
        if "." in sections[-1]:
            sections[-1] = sections[-1].split(".")[0]
        if (0 >= length or length > 3) or any((len(s) != 3 for s in sections[1:])):
            raise ValueError
        return num.replace(",", "")
    else:
        return num


def run_chef_interface():
    global MENU

    print("MSG: Welcome, Chef!\n")

    while True:
        items = get_menu_items(values=True)
        action = get_choice_loop("What would you like to do?",
                                 (edit := "edit the menu",
                                  load := "import menu from JSON",
                                  save := "save menu as JSON",
                                  see := "see current menu",
                                  clear := "clear menu",
                                  "log out as chef"))

        if action == edit:
            while True:
                course = get_choice_loop("Which course would you like to go to?", (*MENU, "go back"))
                if course == "go back":
                    break
                course_items = MENU[course]

                # COURSE-SPECIFIC EDITING
                while True:
                    # WHAT TO DO IN THE CURRENT COURSE
                    items = get_menu_items(values=True)

                    choices = (*course_items, "cancel")
                    course_action = get_choice_loop(f"Action for the {course.upper()} course.",
                                                    (add := "add item",
                                                     edit := "edit item",
                                                     remove := "remove item",
                                                     display := f"display {course} items",
                                                     change_course := "change course (back)",
                                                     "log out as chef"))

                    if course_action == add:
                        item = input(f"PROMPT: Please specify the name of the item {CANCEL_MSG}: ")
                        if not item:
                            print("MSG: Invalid name for an item. Must have a character.\n")
                        elif item == CANCEL_KEY:
                            print("MSG: Cancel adding...\n")
                        elif item in items:
                            print(f"\nMSG: {item} is already in the menu.\n")
                        else:
                            if course == "beverage and drink":
                                size = get_choice_loop("Specify the serve size: ",
                                                       ("small", "medium", "large", "none")).upper()
                                item = item + " " + size if size == "none" else item
                            price = get_num_loop(f"Please specify the price for {item}: $")
                            MENU[course][item] = price
                            print(f"MSG: Added {course} item {item} priced ${price:,g}.\n")

                    elif course_action == edit:
                        if not course_items:
                            print(f"MSG: No {course} item to edit yet!\n")
                            continue

                        item_to_edit = get_choice_loop("Which item would you like to edit?:", choices)

                        if item_to_edit == "cancel":
                            print("MSG: Cancelling edit...\n")
                            continue

                        property_to_edit = get_choice_loop("What would you like to change?", ("name", "price"))

                        if property_to_edit == "name":
                            new_name = input(f"PROMPT: Please enter the new name for {item_to_edit}: ")
                            if new_name in MENU[course]:
                                print(f"{new_name} is already in {course}!\n")
                            else:
                                old_p = MENU[course].pop(item_to_edit)
                                MENU[course][new_name] = old_p
                                print(f"MSG: You have changed the name of {item_to_edit} to {new_name}.\n")
                        else:
                            new_price = MENU[course][item_to_edit] = get_num_loop(
                                f"Please enter the new price for {item_to_edit}: $")
                            print(f"MSG: You have changed the price of {item_to_edit} to ${new_price:,g}.\n")

                    elif course_action == remove:
                        if not course_items:
                            print(f"MSG: No {course} items to remove yet!\n")
                            continue

                        item_to_remove = get_choice_loop("Select which item you want to remove:", choices)
                        if item_to_remove == "cancel":
                            print("MSG: Cancelling deletion...\n")
                            continue
                        else:
                            if confirm_action(f"REMOVE {item_to_remove}?"):
                                del MENU[course][item_to_remove]
                                print(f"MSG: You have removed {item_to_remove} from {course}.\n")
                            else:
                                print("MSG: Cancelling deletion...\n")

                    elif course_action == display:
                        if not course_items:
                            print(f"MSG: No {course} yet.\n")
                            continue

                        print(f"MSG: Displaying {course} items...")
                        for item, price in course_items.items():
                            print(f"> '{item.title()}': ${price:,g}")
                        print()

                    elif course_action == change_course:
                        break

                    else:
                        print("MSG: Logging out as chef...\n")
                        return

        elif action == load:
            filename = filedialog.askopenfilename(parent=filedialog_root,
                                                  title="Import menu from JSON file",
                                                  filetypes=[("JSON files", "*.json")])
            try:
                with open(filename) as f:
                    loaded_menu = json.load(f)
            except FileNotFoundError as e:
                print(f"MSG: Error {e}")
                continue

            if loaded_menu.keys() != MENU.keys():
                print("MSG: File must have the same five courses.\n")
                continue
            MENU = loaded_menu
            print(f"MSG: Successfully imported {filename} as menu.\n")

        elif action == save:
            if not items:
                print("MSG: Menu is empty.\n")
                continue
            file = filedialog.asksaveasfilename(parent=filedialog_root,
                                                title="Save menu as JSON file",
                                                defaultextension=".json",
                                                filetypes=[("JSON file", ".json")])
            try:
                with open(file, 'w') as f:
                    json.dump(MENU, f)
            except FileNotFoundError:
                print("MSG: Cancelling saving menu as JSON...\n")
            else:
                print(f"MSG: Created file {file}.\n")

        elif action == see:
            if not items:
                print("MSG: Menu is currently empty.\n")
            else:
                print("Displaying current menu:")
                for course in MENU:
                    if not MENU[course]:
                        print(f"No {course.upper()} yet...\n")
                        continue
                    print(f"{course.upper()} items:")
                    for item, price in MENU[course].items():
                        print(f"> {item}: ${price:,g}")
                    print()

        elif action == clear:
            print("WARNING: YOU ARE ABOUT TO DELETE THE WHOLE MENU!")
            if confirm_action("DELETE THE MENU", 2):
                print("MSG: CLEARING MENU...\n")
                for course in MENU:
                    MENU[course] = {}
                print("MSG: The menu is now empty.\n")
                continue
            else:
                print("MSG: Cancelling emptying menu...\n")

        else:
            print("MSG: Logging out as chef...\n")
            return


def run_crew_interface():
    global MENU
    global CUSTOMER_N

    items = get_menu_items(values=True)

    if not items:
        print("MSG: Sorry! The menu isn't prepared yet.\n")
        return

    print("MSG: Welcome, crew!\n")

    print("MSG: Displaying menu...")
    for course in MENU:
        print(f"{course.upper()}:")
        for item, price in MENU[course].items():
            print(f"> {item} - ${price:,g}")
        print()

    while True:
        action = get_choice_loop("What would you like to do?", (take := "take order", "log out as crew"))

        if action == take:
            print(f"MSG: Taking order of customer #{CUSTOMER_N + 1}.\n")
            orders: dict[str, list[float | int]] = {}
            total = 0

            in_ordering = True
            to_confirm = in_confirmation = to_pay = False

            customer_type = get_choice_loop(f"What type of customer is customer #{CUSTOMER_N + 1}?",
                                            ("regular", "senior citizen/PWD"))

            while in_ordering:
                course = get_choice_loop(f"What course would customer #{CUSTOMER_N + 1} like to go to?",
                                         (*MENU, "cancel adding" if in_confirmation else "cancel order"))

                if course == "cancel order":
                    if confirm_action("Cancel the customer's order", 2):
                        print(f"MSG: Customer #{CUSTOMER_N + 1} cancelled their order.\n")
                        break
                elif course == "cancel adding":
                    in_course = False
                else:
                    course_items = MENU[course]
                    if len(course_items) == 0:
                        print(f"Sorry, no {course} dishes yet.")
                        continue
                    in_course = True

                while in_course:
                    choice = get_choice_loop(f"What {course} would customer #{CUSTOMER_N + 1} like to order?",
                                             (*(f"{item} - ${price}" for item, price in course_items.items()),
                                              choose_course := "choose another course"))

                    if choice == choose_course:
                        break

                    order = choice.split(" - $")[0]
                    price = items[order]
                    amount = get_num_loop(f"Amount of {order}: ", numtype="int", nl=False)
                    price = float(price)

                    if amount <= 0:
                        print("Invalid amount!")
                        continue
                    elif order in orders:
                        print(f"MSG: Added {amount:,g} to {order}.\n")
                        orders[order][1] += amount
                    else:
                        print(fmt(f"MSG: Customer ordered -> {order} (${price}) x {amount:,g}.\n", "l"))
                        orders[order] = [price, amount]

                    total += price * amount

                    # end order prompt
                    if not in_confirmation:
                        order_again = get_choice_loop(
                            f"Does customer #{CUSTOMER_N + 1} want to order another item?", YES_OR_NO)
                        if order_again == "no":
                            to_confirm = True
                    in_course = False

                # * confirmation prompt loop
                while to_confirm:
                    bill = total
                    if customer_type == "senior citizen/PWD":
                        discount = 0.2
                        bill = total - total * discount
                    else:
                        discount = 0
                    print("Ordered items:")
                    for item in orders:
                        print(f"> {item}: ${orders[item][0]:,g} x {orders[item][1]:,g}")
                    print(f"\nSubtotal: ${total:,g}")
                    if discount:
                        print(f"Discounted price: ${bill:,g}\n")
                    else:
                        print()

                    confirm = get_choice_loop("Confirm order?",
                                              ("yes, confirm",
                                               edit := "No, edit amount",
                                               add := "No, add item",
                                               remove := "No, remove item",
                                               cancel_order := "cancel order"))

                    choices = (*orders, cancel := "cancel")

                    if confirm == edit:
                        item_to_edit = get_choice_loop("Which would you like to edit the amount of?", choices)
                        if item_to_edit == cancel:
                            print("MSG: Cancelling order edit...\n")
                            continue
                        while True:
                            new_amount = get_num_loop(f"New amount of {item_to_edit}: ", numtype="int")
                            if new_amount < 0:
                                print("MSG: Invalid amount.\n")
                            elif new_amount == 0:
                                print("MSG: Consider REMOVING the order.\n")
                                break
                            else:
                                old_amount = orders[item_to_edit][1]
                                total += orders[item_to_edit][0] * (new_amount - old_amount)
                                orders[item_to_edit][1] = new_amount
                                print(
                                    f"MSG: Changed {item_to_edit}'s amount from {old_amount:,g} to {new_amount:,g}.\n")
                                break

                    elif confirm == remove:
                        to_remove = get_choice_loop("Which order would you like to remove?", choices)
                        if to_remove == cancel:
                            print("MSG: Cancelling order deletion...\n")
                            continue
                        elif len(orders) == 1:
                            print("Consider CANCELLING the order.\n")
                            continue
                        else:
                            del_price, del_am = orders.pop(to_remove)
                            total -= del_price * del_am
                            print(f"MSG: Removed {to_remove} x {del_am} from orders.")

                    elif confirm == add:
                        in_confirmation = True
                        in_course = False
                        break

                    elif confirm == cancel_order:
                        confirm_cancel = get_choice_loop("Are you sure you want to cancel the whole order?", YES_OR_NO)
                        if confirm_cancel == "yes":
                            final_confirm = get_choice_loop(
                                "You are about to cancel the customer's order. Are you sure?", YES_OR_NO)
                            if final_confirm == "yes":
                                print(f"Customer #{CUSTOMER_N + 1} cancelled their order.\n")
                                in_ordering = in_course = in_confirmation = False
                                to_confirm = False
                                break

                    else:
                        in_confirmation = to_confirm = False
                        to_pay = True
                        break

                if to_pay:
                    # PAYMENT
                    while True:
                        print(fmt("Subtotal:", "l") + f"${total:,g}")
                        if discount:
                            print(fmt("Discounted price:", 'l') + f"${bill:,g}", end="\n\n")
                        payment = get_num_loop(fmt("CUSTOMER PAYMENT:", 'l'), prefix="", suffix="$", clear=False)
                        if payment < bill:
                            print("MSG: Insufficient payment.\n")
                            continue
                        break

                    # * RECEIPT FORMAT
                    print(fmt("=", 'f'))
                    print(fmt("BIG EGG RESTAURANT GROUP", 'c'))
                    print(fmt("JAMBO-JAMBO STREET, LOS ANGELES, MARIKINA", 'c'))
                    print("\n\n")

                    print(f"CUSTOMER #{CUSTOMER_N + 1} ORDERED:")
                    for item in orders:
                        price = (p := orders[item][0]) * (a := orders[item][1])
                        print(col_fmt(f"> {item} - ${p:,g}", f"QTY x {a:,} ${price:,}"))

                    print(fmt("~" 'f'))

                    print(col_fmt("SUBTOTAL:", f"${total:,}"))
                    print(col_fmt("APPLICABLE DISCOUNT:", f"{discount:.2%}"))
                    print("\n\n")

                    print(col_fmt("AMOUNT DUE:", f"${bill:,}"))
                    print(col_fmt("CASH PAYMENT:", f"${payment:,}"))

                    print(fmt("~", 'f'))

                    print(col_fmt("CHANGE:", f"${payment - bill:,}"))
                    print("\n\n")

                    print(fmt("THANKS FOR VISITING BIG EGG! COME AGAIN SOON!", 'c'))
                    print(fmt("=", 'f'))
                    print("\n")
                    # * END receipt
                    break

            CUSTOMER_N += 1


def main():
    while True:
        mode = get_choice_loop("Who are you? Are you the chef or crew?",
                               ("chef", "crew", "exit restaurant"))

        if mode == "chef":
            run_chef_interface()
        elif mode == "crew":
            run_crew_interface()
        else:
            return


if __name__ == "__main__":
    clear_text()
    print("Welcome!\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\n")

    print(" See you again soon! ".center(64, '-'))
