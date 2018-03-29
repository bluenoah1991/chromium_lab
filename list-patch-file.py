import os, sys, re

def patches_from_directory(dir=None):
	directory_children = os.listdir(sys.path[0] if dir is None else dir)
	patch_files = []
	for path in directory_children:
		if os.path.isfile(path) and path.endswith('.patch'):
			patch_files.append(path)
		elif os.path.isdir(path):
			patch_files.extend(patches_from_directory(path))
	return patch_files
	
def paths_from_patch_file(patch_file):
	paths = []
	with open(patch_file) as f:
		lines = f.readlines()
		for line in lines:
			if line.startswith('diff '):
				paths.append(line)
	return paths

def paths_from_cwd():
	paths = []
	patch_files = patches_from_directory()
	for patch_file in patch_files:
		paths.extend(paths_from_patch_file(patch_file))
	return list(set(paths))
	
def main():
	for index, path in enumerate(paths_from_cwd()):
		path = re.search('(?:--git a)(\S+)', path).group(1)
		print '%s: %s' % (index, path) 
	
if __name__ == '__main__':
	main()