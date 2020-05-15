from file_parser import read_fact_set, read_rule_set
from production_system import kombajn, action_add, action_delete


def init():
    facts = read_fact_set()
    rules = read_rule_set()
    stepping_enabled = True
    skip_num = 0
    while True:
        input_result = handle_input(stepping_enabled, skip_num, facts)
        if input_result == "exit":
            break
        if input_result == "continue":
            continue
        if input_result is not None and input_result.isdigit():
            skip_num = int(input_result)
        kombajn(rules, facts)


def handle_input(stepping_enabled, skip_num, facts: set):
    command = ""
    # print(skip_num)
    if skip_num > 0:
        # print("Skipping")
        skip_num -= 1
        return str(skip_num)
    if stepping_enabled:
        command = input('Next command '
                        '[ ENTER '
                        '| "next" '
                        '| "skip (N)" '
                        '| "exit" '
                        '| "facts" '
                        '| "add (FACT)" '
                        '| "delete (FACT/INDEX)" '
                        ']\n')
    if command == "":
        return "continue"
    if command == "next":
        return ""
    if command.split()[0] == "skip":
        if len(command.split()) >= 2:
            return str(int(command.split()[1]))
    if command.split()[0] == "add":
        action_add(command[4:], facts)
        return "continue"
    if command == "facts":
        index = 0
        if len(facts) == 0:
            print("No facts found.")
        for fact in facts:
            print(index, ".: ", fact)
            index += 1
        return "continue"
    if command.split()[0] == "delete":
        if len(command.split()) >= 2:
            if command.split()[1].isdigit():
                element = fact_from_index(int(command.split()[1]), facts)
                print("Deleting", element)
            else:
                element = command[7:]
            if input("Sure you want to delete (y/n)?\n") == "y":
                action_delete(element, facts)
        return "continue"
    if command == "exit":
        return "exit"
    return "continue"


def fact_from_index(index, facts: set):
    i = 0
    for fact in facts:
        if i == index:
            return fact
        i += 1


if __name__ == '__main__':
    init()



