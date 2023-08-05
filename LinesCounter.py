import os


root = "C:\\Users\\Dark Knight\\Desktop\\Projects\\Games\\Fast_and_Curious"
UNDESIRED = [root+"\src\deprecated",
			 root+"\src\\testing_env",
			 root+"\src\\tools"]


def count_lines(filename):
	with open(filename, 'r') as file:
		lines = file.readlines()
		non_blank_lines = len([line for line in lines if line.strip()])
		total_lines = len(lines)
		return total_lines, non_blank_lines


def count_lines_recursive(directory):
	results = {}
	root_non_blank_count = 0
	root_total_count = 0
	for root, dirs, files in os.walk(directory):
		if root in UNDESIRED:
			continue
		root_path = os.path.relpath(root, directory)
		root_count = [0, 0]
		for file in files:
			filepath = os.path.join(root, file)
			if file.endswith('.py'): # and filepath not in UNDESIRED:
				count = count_lines(filepath)
				root_count[0] += count[0]
				root_count[1] += count[1]
				file_path = os.path.join(root_path, file)
				results[file_path] = count
		if root_count != [0, 0]:
			results[root_path] = tuple(root_count)
		root_non_blank_count += root_count[1]
		root_total_count += root_count[0]
	return results, root_non_blank_count, root_total_count


if __name__ == '__main__':
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
