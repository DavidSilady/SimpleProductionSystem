from typing import List
from file_parser import Rule
from itertools import permutations


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
	perm = permutations(names, len(variable_markings_from_file()))
	for variables in perm:
		check_rules(rules, facts, variables)


def check_rules(rules: List[Rule], facts: set, variables):
	for rule in rules:
		if all_conditions_match(rule, facts, variables):
			for result in rule.results:
				execute_result(result, variables, facts)


def all_conditions_match(rule: Rule, facts, variables):
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


def execute_result(result: str, variables, facts: set):
	filled_result = add_variables(result, variables)
	action, output_string = decode_result_action(filled_result)
	if action == "pridaj":
		action_add(output_string, facts)
		return
	if action == "sprava":
		action_message(output_string)
		return
	if action == "vymaz":
		action_delete(action + output_string)
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


def add_variables(generic_string: str, variables):
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
