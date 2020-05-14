from file_parser import read_fact_set, read_rule_set
from production_system import kombajn


def init():
    facts = read_fact_set()
    rules = read_rule_set()
    kombajn(rules, facts)


if __name__ == '__main__':
    init()



