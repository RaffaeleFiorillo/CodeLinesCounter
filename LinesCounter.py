import os

root = os.path.abspath(os.getcwd())
UNDESIRED = []
user_chosen_extensions = []


def apply_configurations():
	global root
	global UNDESIRED
	global user_chosen_extensions
	try:
		with open("LinesCounter-config.txt", 'r') as f:
			lines = f.readlines()
			for line in lines:
				try:
					exec(line.strip(), globals())
				except Exception as e:
					print(f"Error executing line: {line.strip()}")
					print(f"Error message: {e}")
	except SyntaxError:
		print(f"Error: {SyntaxError}")

	UNDESIRED = [root + d for d in UNDESIRED]
	print(root)
	print(UNDESIRED)
	print(user_chosen_extensions)


def count_lines(file_name):
	with open(file_name, 'r') as f:
		lines = f.readlines()
		non_blank_lines = len([line for line in lines if line.strip()])
		total_lines = len(lines)
		return total_lines, non_blank_lines


def file_has_correct_extension(f):
	global user_chosen_extensions
	for extension in user_chosen_extensions:
		if f.endswith(extension):
			return True
	return False


def count_lines_recursive(directory_used):
	global UNDESIRED
	res = {}
	r_non_blank_count = 0
	r_total_count = 0
	for root, dirs, files in os.walk(directory_used):
		if root in UNDESIRED:
			continue
		root_path = os.path.relpath(root, directory_used)
		root_count = [0, 0]
		for file in files:
			filepath = os.path.join(root, file)
			if file_has_correct_extension(file):
				count = count_lines(filepath)
				root_count[0] += count[0]
				root_count[1] += count[1]
				file_path = os.path.join(root_path, file)
				res[file_path] = count
		if root_count != [0, 0]:
			res[root_path] = tuple(root_count)
		r_non_blank_count += root_count[1]
		r_total_count += root_count[0]
	return res, r_non_blank_count, r_total_count


if __name__ == '__main__':
	apply_configurations()
	directory = os.getcwd()
	results, root_non_blank_count, root_total_count = count_lines_recursive(directory)
	with open('code_line_counts.txt', 'w') as file:
		file.write(f'Total lines of code (including blanks) in {directory}: {root_total_count}\n')
		file.write(f'Total non-blank lines of code in {directory}: {root_non_blank_count}\n\n')
		for filename, count in results.items():
			if os.path.isfile(os.path.join(directory, filename)):
				file.write(f'{filename}: {count[1]}/{count[0]} lines\n')
			else:
				file.write(f'{filename}/: {count[1]}/{count[0]} lines\n')
