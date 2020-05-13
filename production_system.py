def check_conditions(conditions, facts):
	for condition in conditions:
		none_matched = True
		for fact in facts:
			if fact == condition:
				none_matched = False
				break
		if none_matched:
			return False
	return True


