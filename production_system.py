from typing import List
from file_parser import Rule


def extract_names(facts: set):
	names = set()
	for fact in facts:
		split_fact = fact.split()
		for word in split_fact:
			if word.istitle():
				names.add(word)
	return names


def kombajn(rules: List[Rule], facts: set):
	names = extract_names(facts)
	for name1 in names:
		for name2 in names:
			for name3 in names:
				variables = [name1, name2, name3]
				check_rules(rules, facts, variables)


def check_rules(rules: List[Rule], facts: set, variables: List[str]):
	for rule in rules:
		if all_conditions_match(rule, facts, variables):
			for result in rule.results:
				execute_result(result, variables, facts)


def all_conditions_match(rule: Rule, facts, variables: List[str]):
	for condition in rule.conditions:
		none_matched = True

		filled_condition = add_variables(condition, variables)
		if is_special_condition(filled_condition):
			continue

		for fact in facts:
			if fact == filled_condition:
				none_matched = False
				break
		if none_matched:
			return False
	return True


def is_special_condition(condition: str):
	split_condition = condition.split()
	if split_condition[0] == "<>":  # is not equal
		if not split_condition[1] == split_condition[2]:
			return True
	return False


def execute_result(result: str, variables: List[str], facts: set):
	filled_result = add_variables(result, variables)
	action, output_string = decode_result_action(filled_result)
	if action == "pridaj":
		action_add(output_string, facts)
		return
	if action == "sprava":
		action_message(output_string)
		return
	if action == "vymaz":
		action_delete(output_string)
		return


def action_add(string, facts: set):
	if string in facts:
		return
	facts.add(string)
	file = open("output", "a")
	file.write("(" + string + ")\n")
	file.close()


def action_message(string):
	print(string)


def action_delete(string):
	print(string)
	pass


def variable_markings_from_file():
	file = open("variable_markings", "r")
	return file.read().split()


def add_variables(generic_string: str, variables: List[str]):
	filled_string = "" + generic_string
	variable_markings = variable_markings_from_file()
	i = 0
	for variable in variables:
		filled_string = filled_string.replace("?" + variable_markings[i], variable)
		i += 1
	return filled_string


def decode_result_action(result: str):
	split_result = result.split()
	action = split_result[0]
	output_string = ""
	for split in split_result[1:]:
		output_string += " " + split
	return action, output_string[1:]
