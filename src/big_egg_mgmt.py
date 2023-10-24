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

# Items here are for testing purposes only. Will be removed after testing period.
menu : dict[str: dict[str: int]]  = {
    "appetizer": {"PEA": 1},
    "main": {"BEEF STEW": 100, "SOUP #5": 5},
    "side": {"FRIES": 5},
    "dessert": {"PIE": 12.5},
    "beverage and drink": {"COKE ZERO LARGE": 14},
    }


def item_is_present(item) -> bool:
    return item in retrieve_menu_items()


def retrieve_menu_items(values: bool = False):
    if values:
        iterable = ((item, value) for course in menu for (item, value) in menu[course].items())
    else:
        iterable = (item for course in menu for item in menu[course])
    return iterable


def menu_is_empty() -> bool:
    return not tuple(retrieve_menu_items())


s, c = 32, ' '
def lfmt(out) -> str:
    return str(out).ljust(s, c)


def rfmt(out) -> str:
    return str(out).rjust(s, c)


def main():
    global menu
    customer_n = 0

    while True:
        mode = get_input_loop("Who are you? Are you the chef or crew?", ("chef", "crew", "exit restaurant"))

        #* START chef interface
        if mode == "chef":
            is_chef = True
            print("MSG: Welcome, Chef!\n")

            while is_chef:
                action = get_input_loop("What would you like to do?",
                                        (edit := "edit the menu",
                                         load := "import menu from JSON",
                                         save := "save  menu as JSON",
                                         see := "see current menu",
                                         "log out as chef"))

                if action == edit:
                    in_course = True

                    while in_course:
                        course = get_input_loop("Which course would you like to go to?", (*menu, "go back"))
                        if course == "go back":
                            break

                        # course-localized modifications
                        while True:
                            # prompt the chef on what to do in the current course
                            choices = (*menu[course], "cancel")
                            empty_menu = menu_is_empty()
                            course_action = get_input_loop(f"Action for the {course.upper()} course.",
                                                        (add := "add item",
                                                         edit := "edit item",
                                                         delete := "delete item",
                                                         display := f"display {course} items",
                                                         change_course := "change course (back)",
                                                         "log out as chef"))

                            if course_action == add:
                                item = input("PROMPT: Please specify the name of the item (enter 1 to cancel): ")
                                if not item:
                                    print("MSG: Invalid name for an item. Must have a character.\n")
                                    continue
                                elif item == "1":
                                    print("MSG: Cancel adding...\n")
                                    continue
                                elif item_is_present(item):
                                    print(f"\nMSG: {item} is already in the menu.\n")
                                else:
                                    if course == "beverages and drinks":
                                        size = get_input_loop("Specify the serve size: ", ("small", "medium", "large")).upper()
                                        item += " " + size
                                    price = get_num_loop(f"Please specify the price for {item}: $")
                                    menu[course][item] = price
                                    print(f"MSG: Added {course} item {item} for ${price}.\n")

                            elif course_action == edit:
                                if empty_menu:
                                    print(f"MSG: No {course} item to edit yet!\n")
                                    continue

                                item_to_edit = get_input_loop("Which item would you like to edit? (enter 1 to cancel):", choices)
                                if item_to_edit == "cancel":
                                    print("MSG: Cancelling edit...\n")
                                    continue
                                property_to_edit = get_input_loop("What would you like to change?", ("name", "price"))

                                if property_to_edit == "name":
                                    new_name = input(f"PROMPT: Please enter the new name for {item_to_edit}: ")
                                    if item_is_present(new_name):
                                        print(f"{new_name} is already in {course}!\n")
                                    else:
                                        old_p = menu[course].pop(item_to_edit)
                                        menu[course][new_name] = old_p
                                        print(f"MSG: You have edited the name of {item_to_edit} to {new_name}.\n")
                                else:
                                    new_price = menu[course][item_to_edit] = get_num_loop(f"Please enter the new price for {item_to_edit}: $")
                                    print(f"MSG: You have edited the price of {item_to_edit} to ${new_price}.\n")

                            elif course_action == delete:
                                if empty_menu:
                                    print(f"MSG: No {course} item to delete yet!\n")
                                    continue

                                to_delete = get_input_loop("Select which item you want to remove (enter 1 to cancel):", choices)
                                if to_delete == "cancel":
                                    print("MSG: Cancelling delete...\n")
                                confirm = get_input_loop(f"Are you sure you want to delete {to_delete}? (There is no undoing this.)", ("yes", "no"))

                                if confirm == "yes":
                                    del menu[course][to_delete]
                                    print(f"MSG: You have removed {to_delete} from {course}.\n")
                                else:
                                    print("MSG: Cancelling deletion...\n")

                            elif course_action == display:
                                print(f"MSG: Displaying {course} items...")
                                if empty_menu:
                                    print(f"MSG: No {course} yet.\n")
                                    continue
                                for item, price in menu[course].items():
                                    print(f"> '{item.title()}': ${price}")
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
                                print("Invalid JSON. Must have the same 5 courses.")
                                continue
                            menu = loaded_menu
                            print(f"Successfully imported {filename} as menu.\n")

                    except FileNotFoundError:
                        print(f"No such file/path '{filename}'.")

                elif action == save:
                    while True:
                        output = input("PROMPT: Name of save file (end in .json) (enter 1 to cancel): ")
                        if output == "1":
                            print("MSG: Cancelling save...\n")
                            continue
                        if not output.lower().endswith(".json"):
                            print("MSG: Must end the file with .json.\n")
                            continue
                        else:
                            break

                    xw, msg = "x", f"MSG: Created file {output}.\n"
                    if os.path.exists(output):
                        confirm_overwrite = get_input_loop(f"File {output} exists. Overwrite?", ("yes", "no"))
                        if confirm_overwrite == "no":
                            print("MSG: Cancelling saving menu as JSON...\n")
                            continue
                        xw, msg = "w", f"Overwritten {output} with current menu.\n"

                    with open(output, xw) as f:
                        json.dump(menu, f)
                    print(msg)

                elif action == see:
                    items = retrieve_menu_items(values=True)
                    if not items:
                        print("MSG: Menu is currently empty.\n")
                    else:
                        print("Displaying current menu:")
                        for item, price in items:
                            print(f"> {item}: ${price}")
                        print("")

                else:
                    mode = None
                    is_chef = False
                    print("MSG: Logging out as chef...\n")
                    break
        #* END chef interface

        #* START crew interface
        elif mode == "crew":
            print("MSG: Welcome, crew!\n")
            items = retrieve_menu_items()

            if not items:
                print("MSG: Sorry! The menu isn't prepared yet.\n")
                continue

            print("MSG: Displaying menu...")
            for course in menu:
                print(f"{course.upper()}:")
                for item, price in menu[course].items():
                    print(f"> {item} - ${price}")
                print("")

            while True:
                action = get_input_loop("What would you like to do?", (take := "take order", "log out as crew"))

                if action == take:
                    print(f"MSG: Taking order of customer #{customer_n + 1}.\n")
                    orders, total = {},  0

                    customer_type = get_input_loop("What is the type of customer?", ("regular", "senior citizen/PWD"))

                    is_ordering = True
                    in_confirmation = False

                    while is_ordering:
                        course = get_input_loop("What course would the customer like to go to?", menu)

                        if len(menu[course]) == 0:
                            print(f"Sorry, no {course} dishes yet.")
                            continue

                        in_course = True
                        while in_course:
                            choice = get_input_loop(f"What {course} would the customer like to order?",
                                                    (*(f"{item} - ${price}" for item, price in menu[course].items()),
                                                    choose_course := "choose another course") )

                            if choice == choose_course:
                                break

                            order, price = choice.split(" - $")
                            amount = get_num_loop(f"Amount of {order}: ", numtype="int", nl=False)
                            price = float(price)

                            if amount <= 0:
                                print("Invalid amount!")
                                continue
                            elif order in orders:
                                print(f"MSG: Added {amount} to {order}.\n")
                                orders[order][1] += amount
                            else:
                                print(lfmt(f"MSG: Customer ordered\t\t{order} x {amount}.\n"))
                                orders[order] = [price, amount]

                            total += price * amount

                            # end order prompt
                            if not in_confirmation:
                                order_again = get_input_loop("Does the customer want to order another item?", ("yes", "no"))
                                if order_again == "yes":
                                    in_course = False
                                    continue

                            #* confirmation prompt loop
                            is_confirmed = False
                            while not is_confirmed:
                                print("Ordered:")
                                for item in orders:
                                    print(f"> {item}: ${orders[item][0]} x {orders[item][1]}")
                                print(f"Total: ${total}\n")

                                confirm = get_input_loop("Confirm order?",
                                                         ("yes, confirm",
                                                          edit := "No, edit amount",
                                                          add := "No, add item",
                                                          remove := "No, remove order",
                                                          cancel_order := "cancel order"))

                                choices = (*orders, cancel := "cancel")

                                if confirm == edit:
                                    item_to_edit = get_input_loop("Which would you like to edit the amount of?", choices)
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
                                            print(f"MSG: Changed {item_to_edit}'s amount from {old_amount} to {new_amount}.\n")
                                            break

                                elif confirm == remove:
                                    to_remove = get_input_loop("Which order would you like to remove?", choices)
                                    if to_remove == cancel:
                                        print("MSG: Cancelling order deletion...\n")
                                        continue

                                    if len(orders) == 1:
                                        print("Consider CANCELLING the order.\n")
                                        continue

                                    del_price, del_am = orders.pop(to_remove)
                                    total -= del_price * del_am
                                    print(f"MSG: Removed {to_remove} x {del_am} from orders.")

                                elif confirm == add:
                                    in_confirmation = True
                                    in_course = False
                                    break

                                elif confirm == cancel_order:
                                    confirm_cancel = get_input_loop("Are you sure want to cancel the whole order?", ("yes", "no"))
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
                                if customer_type == "senior citizen/PWD":
                                    applicable = "20%"
                                    bill = total - total * 0.2
                                else:
                                    applicable = "NONE"

                                paid = False
                                while not paid:
                                    print(lfmt("Subtotal:") + rfmt(f"${total}"))
                                    print(lfmt("Discounted price:") + rfmt(f"${bill}"))
                                    payment = get_num_loop("CUSTOMER PAYMENT: $")
                                    if payment < total:
                                        print("MSG: Insufficient payment.")
                                        continue
                                    break

                                #* START receipt
                                print("=" * s * 2)
                                print("BIG EGG RESTAURANT GROUP".center(s*2))
                                print("JAMBO JAMBO STREET, LOS ANGELES, MARIKINA".center(s*2), end="\n\n")
                                print("ITEMS ORDERED:")
                                for item in orders:
                                        price = (p := orders[item][0]) * (a := orders[item][1])
                                        print(lfmt("> " + item) + rfmt(f"${p} QTY {a} ${price}"))
                                print("~" * s * 2, end="\n\n")

                                print(lfmt("SUBTOTAL:") + rfmt(f"${total}"), end="\n\n")
                                print(lfmt("APPLICABLE DISCOUNT:") + rfmt(applicable))
                                print(lfmt("AMOUNT DUE:") + rfmt(f"${bill}"), end="\n\n")
                                print(lfmt("CASH PAYMENT:") + rfmt(f"${payment}"))
                                print(lfmt("CHANGE:") + rfmt(f"${payment - bill}"), end="\n\n")
                                print("THANKS FOR VISITING BIG EGG! COME AGAIN SOON!".center(s*2, c))
                                print("=" * s * 2 + "\n")
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


def get_input_loop(prompt, returnVals, nl=True, clear=True):
    if not returnVals:
        print("MSG: No choices provided.\n")
    while True:
        print("PROMPT:", prompt)
        for i, choice in enumerate(returnVals):
            if choice:
                print(f"[{i+1}] {choice.upper()}")
        try:
            index = int(input("Enter integer: "))
            if 0 <= index > len(returnVals):
                raise ValueError
            break
        except ValueError:
            if clear:
                os.system('cls')
            print("MSG: Invalid input!\n")
            continue
    if nl:
        print("")
    if clear:
        os.system('cls')
    return list(returnVals)[index-1]


def get_num_loop(prompt: str, numtype="float", nl=True, clear=True, negative=False) -> float|int:
    while True:
        try:
            inp = input("PROMPT: " + prompt)
            num = float(inp) if numtype == "float" else int(inp)
            if not negative and num < 0:
                if clear:
                    os.system('cls')
                print("MSG: Invalid input. Must be positive.\n")
                continue
            break
        except ValueError:
            if clear:
                os.system('cls')
            print("MSG: Invalid input. Must be numerical.\n")
            continue
    if nl:
        print("")
    if clear:
        os.system('cls')
    return num


if __name__ == "__main__":
    print(" Big Egg MMS (Menu Management System) ".center(s*2, "-"), end="\n\n")
    main()
    print(" See you again soon! ".center(s*2, "-"), end="\n\n")
