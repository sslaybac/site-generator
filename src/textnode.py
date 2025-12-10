from enum import Enum
from leafnode import LeafNode
import re

class TextType(Enum):
	PLAIN = "plain"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if self.text != other.text:
			return False
		elif self.text_type != other.text_type:
			return False
		elif self.url != other.url:
			return False
		else:
			return True

	def __repr__(self):
		return f"TextNode('{self.text}', {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.PLAIN:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise Exception("Invalid TextNode type.")

"""
Accepts a list of premade TextNode objects, and breaks
the 'plaintext' nodes into subnodes, based on the first
appearance of the delimiter

This is a recursive function. Each apparent PLAIN node will
be assessed based on the same delimiter, until no further
sections can be broken out. A calling function will be responsible
for re-executing this function for each type of delimiter
"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type == TextType.PLAIN:
			substrings = node.text.split(delimiter, maxsplit=2)
			if len(substrings) == 1: # No delimiters, no splits
				new_nodes.append(TextNode(node.text, TextType.PLAIN))
			elif len(substrings) == 2:
				raise Exception(f"invalid syntax: {text_type} nodes require 2 '{delimiter}' delimiters")
			else: # Found two matching delimeters
				first_node = TextNode(substrings[0], TextType.PLAIN)
				new_nodes.extend(split_nodes_delimiter([first_node], delimiter, text_type))

				# We will ignore nesting at this stage
				new_nodes.append(TextNode(substrings[1], text_type))

				third_node = TextNode(substrings[2], TextType.PLAIN)
				new_nodes.extend(split_nodes_delimiter([third_node], delimiter, text_type))
		else: # ignore nesting
			new_nodes.append(node)
	return new_nodes

"""
function for converting a line of markdown text to a list of type-specific TextNodes.
Currently, the sequence is:
1. Bold: '**'
2. Italic: '_'
3. Code: '`'
"""
def convert_line_to_textnodes(text):
	starting_point = [TextNode(text, TextType.PLAIN)]
	bold_stage = split_nodes_delimiter(starting_point, "**", TextType.BOLD)
	italic_stage = split_nodes_delimiter(bold_stage, "_", TextType.ITALIC)
	code_stage = split_nodes_delimiter(italic_stage, "`", TextType.CODE)
	image_stage = split_nodes_image(code_stage)
	link_stage = split_nodes_link(image_stage)
	return link_stage

"""
function for identifying images in markdown.
Uses regular expressions to extract link urls and return tuples
parameter:
text: a line of markdown text
"""
def extract_markdown_images(text):
	image_expr = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(image_expr, text)
	
"""
function for identifying images in markdown.
Uses regular expressions to extract link urls and return tuples
parameter:
text: a line of markdown text
"""
def extract_markdown_links(text):
	link_expr = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
	return re.findall(link_expr, text)

"""
function to (possibly) split a plaintext node into a list of
plaintext nodes and image nodes.
"""
def split_nodes_image(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.PLAIN:
			new_nodes.append(node)
			continue
		images = extract_markdown_images(node.text)
		remainder = node.text
		for image in images:
			delim = f"![{image[0]}]({image[1]})"
			substrings = remainder.split(delim, maxsplit=1)
			new_nodes.append(TextNode(substrings[0], TextType.PLAIN))
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			remainder = substrings[1]
		if remainder:
			new_nodes.append(TextNode(remainder, TextType.PLAIN))
	return new_nodes


def split_nodes_link(old_nodes):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.PLAIN:
			new_nodes.append(node)
			continue
		links = extract_markdown_links(node.text)
		remainder = node.text
		for link in links:
			delim = f"[{link[0]}]({link[1]})"
			substrings = remainder.split(delim, maxsplit=1)
			new_nodes.append(TextNode(substrings[0], TextType.PLAIN))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			remainder = substrings[1]
		if remainder:
			new_nodes.append(TextNode(remainder, TextType.PLAIN))
	return new_nodes
