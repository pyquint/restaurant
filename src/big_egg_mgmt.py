"""
+---------------------------------------+
|   CLI Restaurant Program,             |
|   for the chef and crew of Big Egg.   |
|   Created By Static Typing.           |
+---------------------------------------+
"""

# Mmmm... Yummy spaghetti code.

import json
import os
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

_PROGRAM_NAME = " Big Egg Menu Management System™ "
WIDTH: int = 64
CURR = '$'
CANCEL_KEY = '`'
CANCEL_MSG = f"({CANCEL_KEY} to cancel)"
DISCOUNT: float | int = 0.2

MENU: dict[str, dict[str, float | int]] = {
    "appetizer": {"Pea": 1},
    "main": {"Steak": 100},
    "side": {},
    "dessert": {},
    "beverage": {},
}


def main():
    while True:
        mode = get_choice_loop("Who are you? Are you the chef or crew?",
                               ("chef", "crew", "exit program"))
        if mode == "chef":
            run_chef_interface()
        elif mode == "crew":
            run_crew_interface()
        else:
            return


def get_flat_menu_dict() -> dict[str, int | float]:
    """Returns the menu's items and the corresponding price in a flat dictionary."""
    return {item: value for course in MENU for item, value in MENU[course].items()}


def clear_cli() -> None:
    """Clears the command line."""
    os.system('cls')
    print(f" {_PROGRAM_NAME} ".center(WIDTH, '-'))


def align(txt: str, alignment: str, padding: int = WIDTH, char: str = ' ') -> str:
    """
    Formats the input string either into left-, center-, or right-aligned. Or fills the line.

    :param txt: input string
    :param alignment: 'l' for left-aligned, 'c' for centered, 'r' for right-aligned, or 'f' for fill
    :param padding: length of the string when formatted
    :param char: character of the padding

    :return: aligned text
    """
    if alignment == 'c':
        aligned_text = txt.center(padding)
    elif alignment == 'l':
        aligned_text = txt.ljust(padding, char)
    elif alignment == 'r':
        aligned_text = txt.rjust(padding, char)
    else:
        raise ValueError

    return aligned_text


def col_fmt(string1: str, string2: str) -> str:
    """
    Formats string input 1 and string input 2 into one 2-column string.

    :param string1: left text
    :param string2: right text
    :return: string with two bodies of text at opposite ends
    """
    return align(string1, 'l', WIDTH // 2) + align(string2, 'r', WIDTH // 2)


def confirm_action(action: str, repeat: int = 1) -> bool:
    """
    Asks for confirmation of an action in a yes/no question.

    :param action: the act being confirmed
    :param repeat: number of times to ask confirmation
    :return: boolean True if confirm is yes else False
    """
    action = action.upper()
    initial_reply = get_choice_loop(f"ARE YOU SURE YOU WANT TO {action}?", ("yes", "no"))

    if initial_reply == "yes":
        reply = True
        for i in range(repeat - 1):
            if get_choice_loop(f"{action}?", ("yes", "no")) == "no":
                reply = False
    else:
        reply = False

    return reply


def print_items(course=None):
    to_display = course or "menu"
    print(f"MSG: Displaying {to_display} items...")

    for menu_course in MENU:
        if course and menu_course != course:
            continue
        if MENU[menu_course]:
            print(f"{menu_course.upper()} items:")
            for item, price in MENU[menu_course].items():
                print(f"> {item}: {CURR}{price:,g}")
            print("")
        else:
            print(f"No {menu_course.upper()} items yet...\n")


def remove_course_item(course):
    item_to_remove = get_choice_loop("Select which item you want to remove:",
                                     (*MENU[course], "cancel"))
    if item_to_remove == "cancel":
        raise ValueError("MSG: Cancelling deletion...\n")

    if confirm_action(f"REMOVE '{item_to_remove}'"):
        del MENU[course][item_to_remove]
        print(f"MSG: You have removed '{item_to_remove}' from the {course} course.\n")
    else:
        raise ValueError("MSG: Cancelling deletion...\n")


def edit_course_item(course: str):
    item_to_edit = get_choice_loop("Which item would you like to edit?:", (*MENU[course], "cancel"))

    if item_to_edit == "cancel":
        raise ValueError("MSG: Cancelling edit...\n")

    property_to_edit = get_choice_loop("What would you like to change?", ("name", "price"))

    if property_to_edit == "name":
        new_name = input(f"PROMPT: Please enter the new name for {item_to_edit} {CANCEL_MSG}: ")

        if new_name in MENU[course]:
            raise ValueError(f"'{new_name}' is already in the menu!\n")
        elif new_name == CANCEL_KEY:
            raise ValueError("MSG: Cancelling edit name...\n")

        old_p = MENU[course].pop(item_to_edit)
        MENU[course][new_name] = old_p
        print(f"MSG: You have renamed '{item_to_edit}' into '{new_name}'.\n")

    else:
        new_price = get_num_loop(f"Please enter the new price for {item_to_edit}: {CURR}")
        if new_price == 0 and not confirm_action(f"Offer {item_to_edit} free of charge"):
            raise ValueError("MSG: Cancelling edit price...\n")

        MENU[course][item_to_edit] = new_price
        print(f"MSG: You have changed the price of '{item_to_edit}' to {CURR}{new_price:,g}.\n")


def add_course_item(course):
    item = input(f"PROMPT: Please specify the name of the new item {CANCEL_MSG}: ")

    if item == CANCEL_KEY:
        raise ValueError("MSG: Cancel adding...\n")
    elif not item or item.isspace():
        raise ValueError("MSG: Item name must have at least one non-whitespace character.\n")
    elif item in get_flat_menu_dict():
        raise ValueError(f"MSG: '{item}' is already in the menu.\n")

    if course == "beverage":
        size = get_choice_loop("Specify the serve size: ",
                               ("small", "medium", "large", "none"), clear=False)
        item = f"'{item}' {size.upper()}" if size != "none" else item
        if item in get_flat_menu_dict():
            raise ValueError(f"MSG: '{item}' is already in the menu.\n")

    price = get_num_loop(f"Please specify the price for '{item}': {CURR}")

    if price == 0 and not confirm_action(f"Offer '{item}' free of charge"):
        raise ValueError("MSG: Cancelling edit price...\n")

    MENU[course][item] = price
    print(f"MSG: Added {course} item '{item}' priced {CURR}{price:,g}.\n")


def load_json(filename):
    with open(filename) as f:
        content = f.read()
        loaded_menu = json.loads(content)

    for imported_course, course in zip(loaded_menu, MENU):
        if imported_course != course:
            raise json.decoder.JSONDecodeError(f"'{imported_course}' is invalid. Did you mean '{course}'?",
                                               content, content.index(imported_course))
        for item, price in loaded_menu[imported_course].items():
            if not isinstance(price, (float, int)):
                raise json.decoder.JSONDecodeError(f"Data is incorrect at item '{item}'",
                                                   content, content.index(item))

    if not [item for imported_course in loaded_menu for item in loaded_menu[imported_course]]:
        raise FileNotFoundError("The JSON file you are about to import is empty.\n")
    elif get_flat_menu_dict() and not confirm_action("Overwrite the current menu"):
        raise FileNotFoundError

    return loaded_menu


def take_order(customer_num, is_in_confirmation: bool = False) -> dict[str, int] | int:
    """
    :param customer_num:
    :param is_in_confirmation: bool that just modifies "cancel order" to "cancel adding"
    :return: returns item and amount if successful, returns 1 if empty or change course or stop add, returns 0 if cancel
    """
    course = get_choice_loop(f"What course would customer #{customer_num} like to go to?",
                             (*MENU, "cancel adding" if is_in_confirmation else "cancel order"))

    if course == "cancel order":
        if confirm_action(f"Cancel customer {customer_num}'s order", 2):
            print(f"MSG: Customer #{customer_num} cancelled their order.\n")
            return 0
    elif course == "cancel adding":
        return 1

    course_items = MENU[course]

    if len(course_items) == 0:
        print(f"Sorry, no {course} items yet.\n")
        return 1

    sep = f" - {CURR}"
    choice: str = get_choice_loop(f"What {course} item would customer #{customer_num} like to order?",
                                  (*(f"{item}{sep}{course_items[item]}" for item in course_items),
                                   go_back := "choose another course"))

    if choice == go_back:
        return 1

    item_ordered, _ = choice.split(sep)
    amount_ordered = get_num_loop(f"Amount of {item_ordered}: ", numtype="int")

    if amount_ordered <= 0:
        print("MSG: Invalid amount!")

    return {item_ordered: amount_ordered}


def get_payment(orders: dict[str, int], discountable: bool = False) -> int | float:
    """
    Receives
    :param orders:
    :param discountable:
    :return:
    """
    bill = sum([orders[item] * get_flat_menu_dict()[item] for item in orders])

    if discountable:
        bill = bill - bill * DISCOUNT

    while True:
        print(align("DUE:", "l") + f"{CURR}{bill:,g}")
        payment = get_num_loop(align("PAYMENT", 'l'),
                               prefix="", suffix=f"{CURR}")
        if payment < bill:
            print("MSG: Insufficient payment.\n")
        else:
            break
    return payment


def print_receipt(orders: dict[str, int], customer_num: int, payment: int | float, discountable: float = False) -> None:
    """
    It uh, print receipts.

    :param orders: dictionary consisting of item name and amount ordered
    :param customer_num: the current customer number being catered
    :param payment: customer's payment
    :param discountable: boolean
    :return: None
    """
    menu_items = get_flat_menu_dict()
    bill = sum([menu_items[item] * orders[item] for item in orders])

    if discountable:
        bill = bill - bill * DISCOUNT

    print('=' * WIDTH)
    print(align("BIG EGG RESTAURANT GROUP", 'c'))
    print(align("Watson  0106, Jambo-Jambo Street", 'c'))
    print(align("Los Angeles, Marikina, Philippines", 'c'))
    print(align('=' * (WIDTH * 3 // 4), 'c'))

    print(align("ORDER RECEIPT", 'c'))
    print(col_fmt(f"CUSTOMER #{customer_num}",
                  time.strftime("%Y-%m-%d %I:%M:%S %p")))

    print('~' * WIDTH)
    for item in orders:
        price = (p := menu_items[item]) * (a := orders[item])
        print(col_fmt(f"{item} - {CURR}{p:,g}",
                      f"QTY x {a:,g}{" " * 4}{CURR}{price:,g}"))
    print("~" * WIDTH)

    print(col_fmt("SUB TOTAL", f"{CURR}{bill:,g}"))
    print(col_fmt("PAYMENT", f"{CURR}{payment:,g}"))
    print(col_fmt("CHANGE", f"{CURR}{payment - bill:,g}"))

    print("~" * WIDTH)
    print(align("Thank You For Visiting Big Egg!", 'c'))
    print(align("Please Come Again!", 'c'))
    print("=" * WIDTH + "\n")


def get_choice_loop(prompt: str, choices, prefix: str = "PROMPT: ", suffix: str = "", clear: bool = True):
    """
    Repeatedly asks the user to enter a number representing the chosen option from an iterable of choices.

    :param prompt: message
    :param choices: iterable of choices
    :param prefix: prefix before the prompt (default "PROMPT: ")
    :param suffix: suffix after the prompt (default "")
    :param clear: clear text after input (default True)
    :return: an element of choices
    """
    try:
        choices = tuple(choice for choice in choices if choice)
    except TypeError:
        raise TypeError("`choices` must be an iterable.")
    except ValueError:
        raise ValueError("`choices` must have at least one element.")

    while True:
        print(prefix, prompt, suffix, sep="")

        for i, option in enumerate(choices, 1):
            if type(option) is str:
                option = option.upper()
            print(f"[{i}] {option}")

        try:
            print("")
            user_input = input("Enter choice: ")
            if clear: clear_cli()
            if user_input.startswith('0'):
                raise ValueError("Leading zeros should be omitted.")
            index = int(user_input)
            if index < 0:
                raise IndexError
            choice = choices[index - 1]
        except ValueError:
            print(f"MSG: Invalid input. Enter a positive integer number.\n")
        except IndexError:
            print(f"MSG: Input is out of bounds. Enter the valid number of your choice.\n")
        except AttributeError:
            print("MSG: Invalid `choice` argument passed.")
        else:
            break

    return choice


def get_num_loop(prompt: str, prefix: str = "PROMPT: ", suffix: str = "", numtype: str = "float", nl: bool = True,
                 clear: bool = True, negative: bool = False) -> float | int:
    """
    Repeatedly asks the user for a number until it is valid input.

    :param prompt: message
    :param prefix: prefix before the prompt (default "PROMPT: ")
    :param suffix: suffix after the prompt (default "")
    :param numtype: type of return value ("float" or "int", default "float")
    :param nl: newline after successful input (default True)
    :param clear: clear text after input (default True)
    :param negative: if allowing negative (default False)
    :return: float or int value of the input (default float)
    """
    if numtype not in ("float", "int"):
        print("Parameter 'numtype' must be 'int' or 'float'.")

    while True:
        try:
            user_input = input(f"{prefix}{prompt}{suffix}")

            # cleans input with commas
            if "," in user_input:
                sections = user_input.split(",")
                length = len(sections[0])
                if "." in sections[-1]:
                    sections[-1] = sections[-1].split(".")[0]
                if (0 >= length or length > 3) or any((len(s) != 3 for s in sections[1:])):
                    raise ValueError("Invalid number format.")
                user_input = user_input.replace(",", "")

            number = int(user_input) if numtype == "int" else float(user_input)
            if not negative and number < 0:
                raise ValueError("Positive numbers only.")
        except ValueError as e:
            if clear:
                clear_cli()
            print(f"MSG: Invalid input. {e}")
            print(f"MSG: Enter a valid {"integer" if numtype == "int" else "number"}\n")
        else:
            break

    if nl:
        print()
    if clear:
        clear_cli()

    return number


def run_chef_interface():
    print("MSG: Welcome, Chef!\n")

    while True:
        items = get_flat_menu_dict()
        action = get_choice_loop("What would you like to do?",
                                 (modify := "manage the menu",
                                  load := "import menu from JSON",
                                  save := "save menu as JSON",
                                  see := "see current menu",
                                  create_template := "create template menu file",
                                  clear := "clear menu", "log out as chef"))

        if action in (save, see, clear) and not items:
            print("MSG: The menu is currently empty.\n")
            continue

        if action == modify:
            modify_menu()
        elif action == load:
            load_menu_from_json()
        elif action == save:
            save_menu_to_json()
        elif action == see:
            print_items()
        elif action == clear:
            clear_menu()
        elif action == create_template:
            save_menu_to_json(template=True)  # TODO
        else:
            print("MSG: Logging out as chef...\n")
            return 0


def modify_menu():
    while True:
        course = get_choice_loop("Which course would you like to go to?", (*MENU, "go back"))

        if course == "go back":
            break

        while True:
            course_items = MENU[course]

            if course_items:
                edit, remove, display = "edit item", "remove item", f"display {course} items"
            else:
                edit, remove, display = [""] * 3
                print(f"NOTICE: The {course} course is currently empty. Only adding is allowed.\n")

            course_action = get_choice_loop(f"Action for the {course.upper()} course.",
                                            (add := "add item", edit, remove, display,
                                             change_course := "change course", "log out as chef"))
            try:
                if course_action == add:
                    add_course_item(course)
                elif course_action == edit:
                    edit_course_item(course)
                elif course_action == remove:
                    remove_course_item(course)
                elif course_action == display:
                    print_items(course)
                elif course_action == change_course:
                    break
                else:
                    print("MSG: Logging out as chef...\n")
                    return 0
            except ValueError as e:
                print(e)


def load_menu_from_json():
    global MENU

    filename = filedialog.askopenfilename(parent=root, title="Import menu from JSON file",
                                          filetypes=[("JSON file", "*.json")])
    try:
        loaded_menu = load_json(filename)
    except json.decoder.JSONDecodeError as e:
        print(f"MSG: Something is wrong with the JSON data.\n{e}.\n")
    except FileNotFoundError:
        print("MSG: Cancelling importing menu from JSON...\n")
    else:
        MENU = loaded_menu
        print(f"MSG: Successfully imported {filename} as menu.\n")


def save_menu_to_json(template: bool = False):
    if template:
        menu = {course: {} for course in MENU}
    else:
        menu = MENU

    file = filedialog.asksaveasfilename(parent=root, title="Save menu as JSON file",
                                        defaultextension=".json", filetypes=[("JSON file", ".json")])
    try:
        with open(file, 'w') as f:
            json.dump(menu, f)
    except FileNotFoundError as e:
        print(f"{e}\nMSG: Cancelling file save...\n")
    else:
        print(f"MSG: Created file {file}.\n")


def clear_menu():
    global MENU

    print("WARNING: YOU ARE ABOUT TO CLEAR THE WHOLE MENU!")
    if confirm_action("CLEAR THE MENU", 2):
        print("MSG: CLEARING MENU...\n")
        for course in MENU:
            MENU[course].clear()
        print("MSG: The menu is now empty.\n")
    else:
        print("MSG: Cancelling clearing menu...\n")


def run_crew_interface():
    customer_num = 0
    menu_items = get_flat_menu_dict()

    if not menu_items:
        print("MSG: Sorry! The menu isn't prepared yet.\n")
        return 0

    print_items()
    print("MSG: Welcome, crew!\n")

    while True:
        customer_num += 1
        action = get_choice_loop("What would you like to do?", ("take order", log_out := "log out as crew"))

        if action == log_out:
            print("MSG: Logging out as crew...\n")
            return 0

        # `orders` consists of item name and the amount ordered
        orders: dict[str, int] = {}
        customer_bill = 0
        is_cancelled = False

        print(f"MSG: Taking order of customer #{customer_num}.\n")

        customer_type = get_choice_loop(f"What type of customer is customer #{customer_num}?",
                                        ("regular", "senior citizen/PWD"))
        customer_is_discountable = False if customer_type == "regular" else True

        # TO BE USED AFTER MAIN ORDER SEQUENCE, WHEN EDITING THE ORDER
        def modify_order_amount(item_order, order_action="edit", change_to=None):
            """
            :param item_order: the ordered item to be modified
            :param order_action: accepts either "remove" or "edit" (default)
            :param change_to: if order_action is "edit", the updated amount, otherwise None
            """
            nonlocal customer_bill

            if order_action == "edit":
                if not change_to:
                    raise ValueError(f"Calling `modify_order_amount()` in 'edit' mode must have a `new_amount` passed.")
                old_amount = orders[item_order]
                customer_bill += menu_items[item_order] * (change_to - old_amount)
                orders[item_order] = change_to
                print(f"MSG: Changed {item_order}'s amount from {old_amount:,g} to {change_to:,g}.\n")
            elif order_action == "remove":
                del_am = orders.pop(to_remove)
                customer_bill -= menu_items[to_remove] * del_am
                print(f"MSG: Removed {to_remove} x {del_am} from orders.\n")
            else:
                raise ValueError("`modify_order_amount()` only accepts 'edit' or 'remove' as `order_action`.\n")

        # TAKING ORDER
        while True:
            order = take_order(customer_num)

            if order == 1:
                continue
            elif order == 0:
                is_cancelled = True
                break

            item, amount = *order.keys(), *order.values()
            price = menu_items[item]

            if item in orders:
                print(f"MSG: Added {amount:,g} '{item}' to order.\n")
                orders[item] += amount
            else:
                print(align(f"MSG: Customer ordered -> {item} ({CURR}{price}) x {amount:,g}.\n", "l"))
                orders.update(order)

            customer_bill += amount * price
            order_again = get_choice_loop(
                f"Does customer #{customer_num} want to order another item?", ("yes", "no"))

            if order_again == "no":
                break

        if is_cancelled:
            continue

        # CONFIRMING THE ORDER
        while True:
            confirm = get_choice_loop("Confirm order?",
                                      ("Yes, confirm",
                                       edit := "No, edit amount",
                                       add := "No, add item",
                                       remove := "No, remove item",
                                       show_order := "Show ordered items",
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
                        continue
                    elif new_amount == 0:
                        print("TIP: Consider REMOVING the order.\n")
                    else:
                        modify_order_amount(item_to_edit, "edit", new_amount)
                    break
            elif confirm == remove:
                to_remove = get_choice_loop("Which order would you like to remove?", choices)
                if to_remove == cancel:
                    print("MSG: Cancelling order deletion...\n")
                elif len(orders) == 1:
                    print("TIP: Consider CANCELLING the order.\n")
                else:
                    modify_order_amount(to_remove, "remove")
            elif confirm == add:
                order = take_order(customer_num, is_in_confirmation=True)
                if order == 1:
                    continue
                item, amount = *order.keys(), *order.values()
                customer_bill += menu_items[item] * amount
                print(f"MSG: Added item '{item}' in orders.\n")
                orders.update(order)
            elif confirm == cancel_order:
                if confirm_action("Cancel the whole order", 2):
                    print(f"Customer #{customer_num} cancelled their order.\n")
                    is_cancelled = True
                    break
            elif confirm == show_order:
                print("Ordered items:")
                for item in orders:
                    print(f"> {item}: {CURR}{orders[item]:,g} x {menu_items[item]:,g}")
                print(f"\nTotal: {CURR}{customer_bill:,g}")
                if customer_is_discountable:
                    print(f"Discounted: {CURR}{customer_bill - customer_bill * DISCOUNT:,g}\n")
                else:
                    print("DISCOUNT NOT APPLICABLE.\n")
            else:
                break

        if is_cancelled:
            continue

        customer_payment = get_payment(orders, customer_is_discountable)
        print_receipt(orders, customer_num, customer_payment, customer_is_discountable)


if __name__ == "__main__":
    clear_cli()
    print("Welcome!\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram forcefully terminated... Goodbye!\n")
    else:
        print(" See you again soon! ".center(WIDTH, '-'))
