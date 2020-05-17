import re
from typing import List


def read_fact_set(filename):
    file = open(filename, "r")
    facts = set()
    for line in file:
        facts.add(clear_brackets(line))
    file.close()
    return facts


def parse_rule_line(line):
    conditions_string = re.search('\[(.*)\]', line).group(1)
    return [p.split(')')[0] for p in conditions_string.split('(') if ')' in p]


def read_rule_set(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("File Not Found.")
    rules = []

    try:
        while True:
            rule_name = file.readline().replace(":", "")
            if_line = file.readline()
            then_line = file.readline()
            line = file.readline()
            rules.append(Rule(rule_name,
                              parse_rule_line(if_line),
                              parse_rule_line(then_line)))
            if not line:
                break
    except AttributeError:
        print("Wrong File Format")

    file.close()
    return rules


def clear_brackets(line):
    line = line.replace("(", "")
    line = line.replace(")", "")
    line = line.replace("\n", "")
    return line


class Rule:
    def __init__(self, name, conditions: List[str], results: List[str]):
        self.name = name
        self.conditions = conditions
        self.results = results
        print("\n", name, "IF ", conditions, "\nTHEN ", results)


