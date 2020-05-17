import re
from typing import List
from file_parser import Rule, read_fact_set
from itertools import permutations, product


def extract_variables(facts: set):
	variables = []
	num_variables = 0
	for fact in facts:
		split_fact = fact.split()
		for word in split_fact:
			if word.istitle():
				num_variables += 1
				variables.append(word)
			if word.isdigit():
				num_variables += 1
				variables.append(word)
	# print(variables)
	return variables, num_variables


def kombajn(rules: List[Rule], facts: set, fact_file):
	variables, num_variables = extract_variables(facts)
	# print("Num variables: ", num_variables)
	perms = set(permutations(variables, min(len(variable_markings_from_file()), num_variables)))
	# print(perms)
	for variables_perm in perms:
		if check_rules(rules, facts, variables_perm, fact_file):
			return


def check_rules(rules: List[Rule], facts: set, variables, fact_file):
	for rule in rules:
		if all_conditions_match(rule, facts, variables):
			# print(rule.conditions, "\n", rule.results)
			is_new_result = False
			for result in rule.results:
				is_new_result = execute_result(result, variables, facts, fact_file) or is_new_result
			return is_new_result
	return False


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


# returns Boolean whether the result was successful & new
def execute_result(result: str, variables, facts: set, fact_file):
	filled_result = add_variables(result, variables)
	action, output_string = decode_result_action(filled_result)
	# print("System: Executing action", action, "\n", output_string)
	if action == "ADD":
		if output_string.split()[0] == "EVAL":
			output_string = do_math(output_string[4:])
		return action_add(output_string, facts, fact_file)
	if action == "MSG":
		return action_message(output_string)
	if action == "DEL":
		return action_delete(output_string, facts, fact_file)


def do_math(string):
	# print("Math string: ", string)
	expressions = get_math_expressions(string)
	# print(expressions)
	output = ""
	for expression in expressions:
		# print("eval( ", expression, " )")
		try:
			result = str(eval(expression))
			result = result.replace("{", "")
			result = result.replace("}", "")
			output += " " + result
		except NameError:
			output += " " + expression
	return output[1:]


def get_math_expressions(string):
	return list(filter(None, re.split(r"\s+(?=[^{}]*(?:{|$))", string)))


# returns Boolean whether the action was successful & new
def action_add(string, facts: set, fact_file):
	# print("ADD ", string)
	if string in facts:
		return False
	facts.add(string)
	file = open(fact_file, "a")
	file.write("(" + string + ")\n")
	file.close()
	return True


# returns Boolean whether the action was successful & new
def action_message(string):
	print(string)
	return True


# returns Boolean whether the action was successful & new
def action_delete(string, facts: set, fact_file):
	# print("REMOVE ", string)
	# print(facts)
	if string not in facts:
		print("No such fact exists.")
		return False
	facts.remove(string)
	# print(facts)
	file = open(fact_file, "w")
	for fact in facts:
		file.write("(" + fact + ")\n")
	file.close()
	return True


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
