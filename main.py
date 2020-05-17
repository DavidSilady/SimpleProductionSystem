from file_parser import read_fact_set, read_rule_set
from production_system import kombajn, action_add, action_delete

"""
Commands:

"next"                      - lets the system execute 1 step
"skip N"                    - lets the system execute N steps
"exit"                      - exits the program
"facts"                     - prints all the currently known facts
"add FACT"                  - adds a fact to the file
"delete FACT/INDEX"         - deletes a fact based on its string or its index
"file fact/rule FILENAME"   - change the file for rules or facts

"""


def init():
    fact_file = "factorial"
    rule_file = "factorial_rule"
    facts = read_fact_set(fact_file)
    rules = read_rule_set(rule_file)
    is_skipping = False
    skip_num = 0
    while True:
        input_result = handle_input(skip_num, facts, fact_file)
        if input_result == "exit":
            break

        if input_result == "continue":
            continue

        if not input_result == "" and input_result.split()[0] == "file" and len(input_result.split()) > 2:
            if input_result.split()[1] == "fact":
                fact_file = input_result[10:]
                facts = read_fact_set(fact_file)
            if input_result.split()[1] == "rule":
                rule_file = input_result[10:]
                rules = read_rule_set(rule_file)
            continue

        if input_result is not None and input_result.isdigit():
            skip_num = int(input_result)
            if skip_num <= 0:
                is_skipping = False
                continue
            is_skipping = True

        kombajn(rules, facts, fact_file, is_skipping)


def handle_input(skip_num, facts: set, fact_file):
    command = ""
    # print(skip_num)
    if skip_num > 0:
        # print("Skipping")
        skip_num -= 1
        return str(skip_num)

    command = input('Next command '
                    '[ ENTER '
                    '| "next" '  
                    '| "skip N" '
                    '| "exit" '
                    '| "facts" '
                    '| "add FACT" '
                    '| "delete FACT/INDEX" '
                    '| "file fact/rule FILENAME"'
                    ']\n')

    if command == "":
        return "continue"
    if command == "next":
        return ""
    if command.split()[0] == "skip":
        if len(command.split()) >= 2:
            return str(int(command.split()[1]))
    if command.split()[0] == "add":
        action_add(command[4:], facts, fact_file)
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
                action_delete(element, facts, fact_file)
        return "continue"
    if command.split()[0] == "file":
        return command
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



