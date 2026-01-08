from textnode import TextNode
from filemanager import copy_static_to_public, generate_pages_recursive

source_path = "content/index.md"
content_path = "content"
template_path = "template.html"
dest_path = "public"

def main():
	copy_static_to_public()
	generate_pages_recursive(content_path, template_path, dest_path)

if __name__ == "__main__":
	main()