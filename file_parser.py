import re


def read_fact_set():
    file = open("fact_set", "r")
    facts = []
    for line in file:
        facts.append(clear_brackets(line))
    return facts


def parse_rule_line(line):
    conditions_string = re.search('\((.*)\)', line).group(1)
    print(conditions_string)
    return [p.split(')')[0] for p in conditions_string.split('(') if ')' in p]


def read_rule_set():
    file = open("rule_set", "r")
    facts = []
    while True:
        rule_name = file.readline().replace(":", "")
        if_line = file.readline()
        then_line = file.readline()
        line = file.readline()
        rule_conditions = parse_rule_line(if_line)
        rule_results = parse_rule_line(then_line)
        print(rule_conditions, rule_results)
        if not line:
            break


def clear_brackets(line):
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("\n", "")
    return line



