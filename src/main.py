import sys
from textnode import TextNode
from filemanager import copy_static_to_public, generate_pages_recursive

source_path = "content/index.md"
content_path = "content"
template_path = "template.html"
dest_path = "docs"
basepath = "/"

def main():
	if len(sys.argv) > 1:
		basepath = sys.argv[1]

	copy_static_to_public()
	generate_pages_recursive(content_path, template_path, dest_path, basepath)

if __name__ == "__main__":
	main()