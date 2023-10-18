"""
+---------------------------------------+
|   CLI Restaurant Program,             |
|   for the chef and crew of Big Egg.   |
|   Created By Static Typing.           |
+---------------------------------------+
"""


def main():
    menu = {"appetizer": {"pea": 1},
            "main": {},
            "side": {},
            "dessert": {},
            "beverages and drinks": {},
        }

    def is_item_present(item):
        return item in [item for course in menu for item in menu[course]]

    while True:
        mode = get_input_loop("Who are you? Are you the chef or a crew?",
                                ("chef", "crew", "exit restaurant"))

        #* START chef interface
        if mode == "chef":
            is_chef = True
            print("MSG: Welcome, Chef!\n")

            while is_chef:
                action = get_input_loop("What would you like to do?",
                                        (goto_course := "edit the menu",
                                         load := "import menu from file",
                                         "log out as chef"))

                if action == goto_course:
                    course = get_input_loop("Which course would you like to go to?",
                                            (menu))
                elif action == load:
                    try:
                        filename = input("PROMPT: Input file directory: ")
                        # TODO JSON file handling
                    except FileNotFoundError:
                        print(f"File {filename} is not found!")
                        continue
                    finally:
                        continue
                else:
                    mode = None
                    is_chef = False
                    print("MSG: Logging out as chef...\n")
                    break

                # course-localized modifications
                while True:
                    # prompt the chef on what to do in the current course
                    action = get_input_loop(f"Action for the {course.upper()} course.",
                                            (add := "add item",
                                            edit := "edit item",
                                            delete := "delete item",
                                            display := f"display {course} items",
                                            change_course := "change course",
                                            "log out as chef"))

                    if action == add:
                        item = input("PROMPT: Please specify the name of the item: ").title()
                        if is_item_present(item):
                            print(f"MSG: {item} is already in the menu.")
                        else:
                            price = get_num_loop(f"Please specify the price for {item}: $")
                            menu[course][item] = price
                            print(f"MSG: Added {course} '{item}' for ${price}.\n")

                    elif action == edit:
                        if len(menu[course]) == 0:
                            print(f"MSG: No {course} item to edit yet!\n")
                            continue

                        item_to_edit = get_input_loop("Which item would you like to edit?", menu[course])
                        property_to_edit = get_input_loop("What would you like to change?", ("name", "price"))

                        if property_to_edit == "name":
                            new_name = input(f"PROMPT: Please enter the new name for {item_to_edit}: ")
                            if is_item_present(new_name):
                                print(f"{new_name} is already in {course}!\n")
                            else:
                                old_p = menu[course].pop(item_to_edit)
                                menu[course][new_name] = old_p
                                print(f"MSG: You have edited the name of {item_to_edit} to {new_name}.\n")
                        else:
                            new_price = menu[course][item_to_edit] = get_num_loop(f"Please enter the new price for {item_to_edit}: $")
                            print(f"MSG: You have edited the price of {item_to_edit} to ${new_price}.\n")

                    elif action == delete:
                        if len(menu[course]) == 0:
                            print(f"MSG: No {course} item to delete yet!\n")
                            continue

                        to_delete = get_input_loop("Select which item you want to remove:", menu[course])
                        confirm = get_input_loop(f"Are you sure you want to delete {to_delete}? (There is no undoing this.)", ("yes", "no"))

                        if confirm == "yes":
                            del menu[course][to_delete]
                            print(f"MSG: You have removed {to_delete} from {course}.")
                        else:
                            print("MSG: Cancelling deletion...\n")

                    elif action == display:
                        print(f"MSG: Displaying {course} items...")
                        if not menu[course]:
                            print(f"MSG: No {course}s yet.\n")
                            continue
                        for item, price in menu[course].items():
                            print(f"- '{item.title()}' for ${price}")
                        print("")

                    elif action == change_course:
                        break

                    else:
                        mode = None
                        is_chef = False
                        print("MSG: Logging out as chef...\n")
                        break
        #* END chef interface

        #* START crew interface
        elif mode == "crew":
            print("MSG: Welcome, crew!\n")

            empty_menu = False
            if sum((len(menu[course]) for course in menu)) == 0:
                print("MSG: Sorry! The menu isn't prepared yet.\n")
                empty_menu = True
            else:
                print("MSG: Displaying menu...")
                for course in menu:
                    print(f"{course.upper()}:")
                    for item, price in menu[course].items():
                        print(f"> {item} - ${price}")
                    print("")

            while True:
                action = get_input_loop("What would you like to do?",
                                        (order := "take order" if not empty_menu else "",
                                         "log out as crew"))
                costumer_num = 0
                if action == order:
                    is_ordering = True
                    orders, total = {},  0

                    costumer_type = get_input_loop("What type of costumer is ordering?",
                                                   ("regular", "senior citizen/PWD"))
                    while is_ordering:
                        course = get_input_loop("What course would the costumer like to go to?",
                                                menu.keys())

                        if len(menu[course]) == 0:
                            print(f"Sorry, no {course} dishes yet.")
                            continue

                        while True:
                            choice = get_input_loop(f"What {course} would the costumer like to order?",
                                                    (*(f"{item} - ${price}" for item, price in menu[course].items()),
                                                     choose_course := "choose another course") )

                            if choice == choose_course:
                                break

                            amount = get_num_loop(f"Amount of {order}: ", numtype="int", nl=False)
                            if amount <= 0:
                                print("Invalid amount!")
                                continue

                            order, price = choice.split(" - $")
                            if order in orders:
                                print(f"MSG: Added {amount} to {order}")
                                orders[order][0] += amount
                            else:
                                print(f"MSG: Costumer orderd {order} x {amount}.\n")
                                orders[order] = [price, amount]

                            # end prompt
                            if get_input_loop("Does the costumer want to order another item?", ("yes", "no")) == "yes":
                                continue
                            else:
                                #* confirmation prompt loop
                                while True:
                                    for order in orders:
                                        print("Ordered:")
                                        print(f"> {order} -- ${orders[order][0]} x  {orders[order][1]}")
                                    confirm = get_input_loop("Confirm?",
                                                            (edit := "No, edit amount",
                                                            remove := "No, remove order",
                                                            "yes"))
                                    if confirm == edit:
                                        to_edit_amount = get_input_loop("Which would you like to edit the amount of?", orders)
                                        amount = get_num_loop(f"New amount of {order}: ", numtype="int")
                                        orders[to_edit_amount][1] = amount
                                        print(f"MSG: Changed {to_edit_amount}'s amount to {amount}.\n")
                                    elif confirm == remove:
                                        to_remove = get_input_loop("Which order would you like to remove?", orders)
                                        del orders[to_remove]
                                    else:
                                        is_ordering = False
                                        break
                                break

                    #* START receipt
                    total += float(price) * amount
                    s, c = 32, '.'
                    print("=" * s * 2)
                    print("ITEMS ORDERED:")
                    for order in orders:
                            print(order.ljust(s, c) + f"${orders[order][0]} x {orders[order][1]}".rjust(s, c))

                    print("")
                    print('TOTAL:'.ljust(s, c) + f"${total}".rjust(s, c))

                    if costumer_type in ["senior citizen", "PWD"]:
                        print("DISCOUNT:".ljust(s, c) + "APPLICABLE 20%".rjust(s, c))
                        total = total + (total * 0.2)

                    while True:
                        payment = get_num_loop("PAYMENT: ")
                        if payment < total:
                            print("MSG: Insufficient payment.")
                            continue
                        else:
                            break

                    print('BILL:'.ljust(s, c) + f"${total}".rjust(s, c))
                    print("CHANGE:".ljust(s, c) + f"${payment - total}".rjust(s, c))
                    print("THANKS FOR COMING IN BIG EGG.")
                    print("=" * s * 2 + "\n")
                    #* END receipt

                    costumer_num += 1

                else:
                    mode = None
                    break
        #* END crew interface

        else:
            print("MSG: See you again soon!")


def get_input_loop(prompt, returnVals, nl=True) -> str:
    if not returnVals:
        raise ValueError("Empty choice. Nothing to print.")
    print("PROMPT:", prompt)

    while True:
        for i, choice in enumerate(returnVals):
            if choice:
                print(f"{i+1}: {choice.upper()}")
        try:
            index = int(input("Enter integer: "))
            if 0 <= index > len(returnVals):
                raise ValueError
            break
        except ValueError:
            print("Invalid input!\n")
            continue

    if nl:
        print("")

    return list(returnVals)[index-1]


def get_num_loop(prompt: str, numtype="float", nl=True):
    while True:
        try:
            inp = input("PROMPT: " + prompt)
            num = float(inp) if numtype == "float" else int(inp)
            if nl:
                print("")
            return num
        except ValueError:
            print("Invalid input. Must be numerical.")
            continue



if __name__ == "__main__":
    main()
