from textnode import TextNode
from filemanager import copy_static_to_public, generate_page

source_path = "content/index.md"
template_path = "template.html"
dest_path = "public/index.html"

def main():
	copy_static_to_public()
	generate_page(source_path, template_path, dest_path)

if __name__ == "__main__":
	main()