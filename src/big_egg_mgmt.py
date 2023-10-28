"""
+---------------------------------------+
|   CLI Restaurant Program,             |
|   for the chef and crew of Big Egg.   |
|   Created By Static Typing.           |
+---------------------------------------+
"""

import json
import os

# Yummy spaghetti code.
# Trying to (mostly) only use if-statements, loops, built-in functions and class methods.

_program_name = "Big Egg Menu Management System™"

# Items here are for testing purposes only. Will be removed after testing period.
menu : dict[str, dict[str, float|int]]  = {
    "appetizer": {"PEA": 1},
    "main": {"BEEF STEW": 100, "SOUP #5": 5},
    "side": {"FRIES": 5},
    "dessert": {"PIE": 12.5},
    "beverage and drink": {"COKE ZERO LARGE": 14},
    }


def item_is_present(item: str) -> bool:
    return item in retrieve_menu_items()


def retrieve_menu_items(values: bool = False) -> dict[str, int|float]|tuple[str]:
    if values:
        items = {item: value for course in menu for item, value in menu[course].items()}
    else:
        items = tuple(item for course in menu for item in menu[course])
    return items


s, c = 64, ' '
def lfmt(out) -> str:
    return str(out).ljust(int(s/2), c)


def rfmt(out) -> str:
    return str(out).rjust(int(s/2), c)


def main():
    global menu
    customer_n = 0
    cancel_key = "`"
    cancel_msg = f"(enter {cancel_key} to cancel)"
    yesno = ("yes", "no")

    while True:
        mode = get_choice_loop("Who are you? Are you the chef or crew?", ("chef", "crew", "exit restaurant"))

        #* START chef interface
        if mode == "chef":
            is_chef = True
            print("MSG: Welcome, Chef!\n")


            while is_chef:
                items = retrieve_menu_items(values=True)
                action = get_choice_loop("What would you like to do?",
                                        (edit := "edit the menu",
                                         load := "import menu from JSON",
                                         save := "save menu as JSON",
                                         see := "see current menu",
                                         clear := "clear menu",
                                         "log out as chef"))

                if action == edit:
                    in_course = True

                    while in_course:
                        course = get_choice_loop("Which course would you like to go to?", (*menu, "go back"))
                        if course == "go back":
                            break
                        course_items = menu[course]

                        # course-localized modifications
                        while True:
                            # prompt the chef on what to do in the current course
                            items = retrieve_menu_items(values=True)

                            choices = (*course_items, "cancel")
                            course_action = get_choice_loop(f"Action for the {course.upper()} course.",
                                                        (add := "add item",
                                                         edit := "edit item",
                                                         delete := "delete item",
                                                         display := f"display {course} items",
                                                         change_course := "change course (back)",
                                                         "log out as chef"))

                            if course_action == add:
                                item = input(f"PROMPT: Please specify the name of the item {cancel_msg}: ")
                                if not item:
                                    print("MSG: Invalid name for an item. Must have a character.\n")
                                elif item == cancel_key:
                                    print("MSG: Cancel adding...\n")
                                elif item in items:
                                    print(f"\nMSG: {item} is already in the menu.\n")
                                else:
                                    if course == "beverage and drink":
                                        size = get_choice_loop("Specify the serve size: ", ("small", "medium", "large", "none")).upper()
                                        item = item + " " + size if size == "none" else item
                                    price = get_num_loop(f"Please specify the price for {item}: $")
                                    menu[course][item] = price
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
                                    if item_is_present(new_name):
                                        print(f"{new_name} is already in {course}!\n")
                                    else:
                                        old_p = menu[course].pop(item_to_edit)
                                        menu[course][new_name] = old_p
                                        print(f"MSG: You have changed the name of {item_to_edit} to {new_name}.\n")
                                else:
                                    new_price = menu[course][item_to_edit] = get_num_loop(f"Please enter the new price for {item_to_edit}: $")
                                    print(f"MSG: You have changed the price of {item_to_edit} to ${new_price:,g}.\n")

                            elif course_action == delete:
                                if not course_items:
                                    print(f"MSG: No {course} item to delete yet!\n")
                                    continue

                                to_delete = get_choice_loop("Select which item you want to remove:", choices)
                                if to_delete == "cancel":
                                    print("MSG: Cancelling deletion...\n")
                                    continue
                                else:
                                    confirm = get_choice_loop(f"Are you sure you want to delete {to_delete}? (There is no undoing this.)", yesno)
                                    if confirm == "yes":
                                        del menu[course][to_delete]
                                        print(f"MSG: You have removed {to_delete} from {course}.\n")
                                    else:
                                        print("MSG: Cancelling deletion...\n")

                            elif course_action == display:
                                print(f"MSG: Displaying {course} items...")
                                if not course_items:
                                    print(f"MSG: No {course} yet.\n")
                                    continue
                                for item, price in course_items.items():
                                    print(f"> '{item.title()}': ${price:,g}")
                                print("")

                            elif course_action == change_course:
                                break

                            else:
                                mode = None
                                is_chef = in_course = False
                                print("MSG: Logging out as chef...\n")
                                break

                elif action == load:
                    try:
                        filename = input("PROMPT: File path (enter 1 to cancel):\n")
                        if filename == "1":
                            print("MSG: Cancelling import...\n")
                            continue

                        with open(filename) as f:
                            loaded_menu = json.load(f)
                            if loaded_menu.keys() != menu.keys():
                                print("MSG: Invalid JSON. Must have the same 5 courses.\n")
                                continue
                            menu = loaded_menu
                            print(f"MSG: Successfully imported {filename} as menu.\n")

                    except FileNotFoundError:
                        print(f"MSG: No such file/path '{filename}'.\n")
                        continue

                elif action == save:
                    if not items:
                        print("MSG: Menu is empty.\n")
                        continue
                    while True:
                        output = input("PROMPT: Name of save file (end in .json) (enter 1 to cancel):\n")
                        if output == "1":
                            print("MSG: Cancelling save...\n")
                            break
                        elif not output.lower().endswith(".json"):
                            print("MSG: Must end the file with .json.\n")
                            continue
                        else:
                            break

                    xw, msg = "x", f"MSG: Created file {output}.\n"
                    if os.path.exists(output):
                        confirm_overwrite = get_choice_loop(f"File {output} exists. Overwrite?", yesno)
                        if confirm_overwrite == "no":
                            print("MSG: Cancelling saving menu as JSON...\n")
                            continue
                        xw, msg = "w", f"Overwritten {output} with current menu.\n"

                    with open(output, xw) as f:
                        json.dump(menu, f)
                    print(msg)

                elif action == see:
                    if not items:
                        print("MSG: Menu is currently empty.\n")
                    else:
                        print("Displaying current menu:")
                        for course in menu:
                            if not menu[course]:
                                print(f"No {course.upper()} yet...\n")
                                continue
                            print(f"{course.upper()} items:")
                            for item, price in menu[course].items():
                                print(f"> {item}: ${price:,g}")
                            print("")

                elif action == clear:
                    print("WARN: YOU ARE ABOUT TO DELETE THE WHOLE MENU!")
                    confirm = get_choice_loop("ARE YOU SURE YOU WANT TO DO THIS?", yesno)
                    if confirm == "yes":
                        final_confirm = get_choice_loop("DELETE THE WHOLE MENU?", yesno)
                        if final_confirm == "yes":
                            print("MSG: CLEARING MENU...\n")
                            for course in menu:
                                menu[course] = {}
                            print("MSG: The menu is now empty.\n")
                            continue
                        else:
                            pass
                    print("MSG: Cancelling emptying menu...\n")

                else:
                    mode = None
                    is_chef = False
                    print("MSG: Logging out as chef...\n")
                    break
        #* END chef interface

        #* START crew interface
        elif mode == "crew":
            print("MSG: Welcome, crew!\n")
            items = retrieve_menu_items(values=True)

            if not items:
                print("MSG: Sorry! The menu isn't prepared yet.\n")
                continue

            print("MSG: Displaying menu...")
            for course in menu:
                print(f"{course.upper()}:")
                for item, price in menu[course].items():
                    print(f"> {item} - ${price:,g}")
                print("")

            while True:
                action = get_choice_loop("What would you like to do?", (take := "take order", "log out as crew"))

                if action == take:
                    print(f"MSG: Taking order of customer #{customer_n + 1}.\n")
                    orders, total = {},  0

                    customer_type = get_choice_loop("What is the type of customer?", ("regular", "senior citizen/PWD"))

                    is_ordering = True
                    in_confirmation = False

                    while is_ordering:
                        course = get_choice_loop("What course would the customer like to go to?", (*menu, "cancel order"))

                        if course == "cancel order":
                            final_confirm = get_choice_loop("Cancel the whole order?", yesno)
                            if final_confirm == "yes":
                                print(f"MSG: Customer #{customer_n+1} cancelled their order.\n")
                                break
                            else:
                                continue

                        course_items = menu[course]

                        if len(course_items) == 0:
                            print(f"Sorry, no {course} dishes yet.")
                            continue

                        in_course = True
                        while in_course:
                            choice = get_choice_loop(f"What {course} would the customer like to order?",
                                                    (*(f"{item} - ${price}" for item, price in course_items.items()),
                                                    choose_course := "choose another course") )

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
                                print(lfmt(f"MSG: Customer ordered -> {order} (${price}) x {amount:,g}.\n"))
                                orders[order] = [price, amount]

                            total += price * amount

                            # end order prompt
                            if not in_confirmation:
                                order_again = get_choice_loop("Does the customer want to order another item?", yesno)
                                if order_again == "yes":
                                    in_course = False
                                    continue

                            #* confirmation prompt loop
                            is_confirmed = False
                            while not is_confirmed:
                                print("Ordered:")
                                for item in orders:
                                    print(f"> {item}: ${orders[item][0]:,g} x {orders[item][1]:,g}")
                                print(f"Total: ${total:,g}\n")

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
                                            print(f"MSG: Changed {item_to_edit}'s amount from {old_amount:,g} to {new_amount:,g}.\n")
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
                                    confirm_cancel = get_choice_loop("Are you sure want to cancel the whole order?", yesno)
                                    if confirm_cancel == "yes":
                                        print(f"Customer #{customer_n + 1} cancelled their order.\n")
                                        is_ordering = in_course = in_confirmation = False
                                        break
                                    else:
                                        continue

                                else:
                                    is_confirmed = True
                                    in_confirmation = in_course = False
                                    break

                            if is_ordering and not in_confirmation:
                                bill = total
                                #* payment
                                if discountable := customer_type == "senior citizen/PWD":
                                    applicable = "20%"
                                    bill = total - total * 0.2
                                else:
                                    applicable = "0%"

                                paid = False
                                while not paid:
                                    print(lfmt("Subtotal:") + f"${total:,g}")
                                    if discountable:
                                        print(lfmt("Discounted price:") + f"${bill:,g}", end="\n\n")
                                    payment = get_num_loop(lfmt("CUSTOMER PAYMENT:"), prefix="", suffix="$", clear=False)
                                    if payment < bill:
                                        print("MSG: Insufficient payment.\n")
                                        continue
                                    break

                                #* START receipt
                                print("=" * s)
                                print("BIG EGG RESTAURANT GROUP".center(s))
                                print("JAMBO-JAMBO STREET, LOS ANGELES, MARIKINA".center(s), end="\n\n")
                                print("ITEMS ORDERED:")
                                for item in orders:
                                        price = (p := orders[item][0]) * (a := orders[item][1])
                                        print(lfmt(f"> {item} - ${p:,g}") + rfmt(f"QTY x {a:,} ${price:,}"))
                                print("~" * s)

                                print(lfmt("SUBTOTAL:") + rfmt(f"${total:,}"))
                                print(lfmt("APPLICABLE DISCOUNT:") + rfmt(applicable), end="\n\n")
                                print(lfmt("AMOUNT DUE:") + rfmt(f"${bill:,}"))
                                print(lfmt("CASH PAYMENT:") + rfmt(f"${payment:,}"))

                                print("~" * s)
                                print(lfmt("CHANGE:") + rfmt(f"${payment - bill:,}"), end="\n\n")
                                print("THANKS FOR VISITING BIG EGG! COME AGAIN SOON!".center(s, c))
                                print("=" * s + "\n")
                                #* END receipt

                                customer_n += 1
                                is_ordering = False
                                break

                else:
                    mode = None
                    break
        #* END crew interface

        else:
            return


def get_choice_loop(prompt: str, choices, prefix : str = "PROMPT: ", suffix: str = "", nl: bool = True, clear: bool = True) -> str:
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
        print("MSG: No choices provided.\n")
        return
    while True:
        print(f"{prefix}{prompt}{suffix}")
        for i, choice in enumerate(choices):
            if choice:
                print(f"[{i+1}] {choice.upper()}")
        try:
            inp = input("\nEnter choice: ")
            index = int(verify_comma_num(inp))
            if index < 0:
                raise IndexError
            chosen = tuple(choices)[index-1]
            break
        except ValueError:
            if clear:
                clear_text()
            if not inp:
                print("MSG: Must input an option.\n")
            elif inp.isalpha():
                print("MSG: Input must be the number of your choice.\n")
            else:
                print(f"MSG: Choice '{inp}' is invalid.\n")
            continue
        except IndexError:
            if clear:
                clear_text()
            print(f"MSG: Choice {index} is out of bounds.\n")
            continue
    if nl:
        print("")
    if clear:
        clear_text()
    return chosen


def get_num_loop(prompt: str, prefix: str = "PROMPT: ", suffix: str = "", numtype: str = "float", nl: bool = True, clear: bool = True, negative: bool = False) -> float|int:
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
            inp = input(f"{prefix}{prompt}{suffix}")
            vinp = verify_comma_num(inp)
            num = float(vinp) if numtype == "float" else int(vinp)
            if not negative and num < 0:
                raise ValueError
            break
        except ValueError:
            if clear:
                clear_text()
            print(f"MSG: Invalid input {inp}.\n")
            continue
    if nl:
        print("")
    if clear:
        clear_text()
    return num

def verify_comma_num(num: str) -> str:
    if "," in num:
        sections = num.split(",")
        l = len(sections[0])
        if "." in sections[-1]:
            sections[-1] = sections[-1].split(".")[0]
        if (0 >= l or l > 3) or any((len(s) != 3 for s in sections[1:])):
            raise ValueError
        return num.replace(",", "")
    else:
        return num

def clear_text():
    os.system('cls')
    print(f" {_program_name} ".center(s, "-"), end="\n\n")


if __name__ == "__main__":
    print(f" {_program_name} ".center(s, "-"), end="\n\n")
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
    print(" See you again soon! ".center(s, "-"))
