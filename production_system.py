from typing import List
from file_parser import Rule


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


def execute_result(result: str, variables: List[str]):
	filled_result = add_variables(result, variables)
	action, output_string = decode_result_action(filled_result)


def add_variables(generic_string: str, variables: List[str]):
	filled_string = "" + generic_string
	variable_markings = ["X", "Y", "Z"]
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
	output_string += "\n"
	return action, output_string[1:]
