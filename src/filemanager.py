import shutil
import os

from text_converter import extract_title, markdown_to_html_node

SRC_DIR = "./static"
DST_DIR = "./public"

def copy_static_to_public():
	clear_public()
	copy_dir("")

def clear_public():
	try:
		shutil.rmtree(DST_DIR)
	except FileNotFoundError:
		# We don't care if it doesn't exist
		pass
	os.mkdir(DST_DIR)


def copy_dir(dirpath):
	src_dir = os.path.join(SRC_DIR, dirpath)
	dst_dir = os.path.join(DST_DIR, dirpath)
	files = os.listdir(src_dir)
	for f in files:
		new_path = os.path.join(dirpath, f)
		print(f"new_path = {new_path}")
		if os.path.isdir(os.path.join(SRC_DIR, new_path)):
			os.mkdir(os.path.join(DST_DIR, new_path))
			copy_dir(new_path)
		else:
			src = os.path.join(src_dir, f)
			print(f"source: {src}")
			dst = os.path.join(dst_dir, f)
			print(f"destination: {dst}")
			shutil.copy(src, dst)

"""
generate_page()
inputs
	from_path: The markdown file that will be used as the source for page content
	template_path: A boilerplate html frame used to present the translated content
	dest_path: the path to the complete generated html file. If any directories in this path don't exist, they will be created
	basepath: the url to the root of the final web page
outputs
	No return
	An html file will be generated at the location specified by dest_path.
	Any necessary directories will also be created.
"""
def generate_page(from_path, template_path, dest_path, basepath):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	markdown = ""
	template = ""
	with open(from_path, "r") as file1:
		markdown = file1.read()

	with open(template_path, "r") as file2:
		template = file2.read()
	
	md_node = markdown_to_html_node(markdown)
	html = md_node.to_html()

	title = extract_title(markdown)

	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", html)
	template = template.replace('href="/', f'href="{basepath}/')
	template = template.replace('src="/', f'src="{basepath}/')

	# Create the directory for dest_path, if it doesn't exist.
	dest_dir = os.path.dirname(dest_path)
	print(f"destination directory: {dest_dir}")
	os.makedirs(dest_dir, exist_ok=True)

	with open(dest_path, "w") as file3:
		file3.write(template)

"""
generate_pages_recursive()
inputs
	content_dir_path: which directory should be searched for markdown
	template_path: an html file to be used as a template for the new content
	dest_dir_path: the directory to be used to store the newly generted html
	basepath: the url to the root of the final web page
outputs:
	no direct return
	new html files and directories will be created in dest_dir_path, with a structure parallelling
		that of the markdown files in content_dir_path
1. get a list of all contents of the content_dir
2. for each entry in the list:
	1. if it is a directory:
		1. join the directory name to content_dir_path and dest_dir_path to generate new paths
		2. recursively call this function using the new paths
	2. Otherwise:
		1. If it is not a markdown file, ignore it.
		2. If it is a markdown file:
			1. create full paths for the source and destination
			2. call generate page using the new paths
"""
def generate_pages_recursive(content_dir_path, template_path, dest_dir_path, basepath):
	entries = os.listdir(content_dir_path)
	for entry in entries:
		entry_path = os.path.join(content_dir_path, entry)
		dest_path = os.path.join(dest_dir_path, entry)
		if os.path.isdir(entry_path):
			generate_pages_recursive(entry_path, template_path, dest_path, basepath)
		else:
			base, ext = os.path.splitext(entry)
			if ext == '.md':
				dest_path = os.path.join(dest_dir_path, base + '.html')
				generate_page(entry_path, template_path, dest_path, basepath)