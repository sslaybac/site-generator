import re
from enum import Enum

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import convert_line_to_textnodes, text_node_to_html_node

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

"""
Returns the raw text of the heading at the top of a markdown page. This text will be used as the <title> of the html translation
parameters:
- markdown: a string, intended to be the full contents of a markdown file
return:
- title: the text of the h1 header at the top of the file. The leading '# ' will be stripped away.
	If the file does not begin with an h1 header block, This method will raise an exception
"""
def extract_title(markdown):
	blocks = markdown_to_blocks(markdown)
	title_block = blocks[0]
	title_node = block_to_heading(title_block)
	if title_node.tag != "h1":
		raise ValueError("The first block of markdown must be a h1 header (begins with '# ')")
	return title_node.to_raw_text()
	
	


def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []
	for block in blocks:
		b_type = identify_block_type(block)
		match b_type:
			case BlockType.PARAGRAPH:
				children.append(block_to_paragraph(block))
			case BlockType.HEADING:
				children.append(block_to_heading(block))
			case BlockType.CODE:
				children.append(block_to_code(block))
			case BlockType.QUOTE:
				children.append(block_to_quote(block))
			case BlockType.UNORDERED_LIST:
				children.append(block_to_list(block, False))
			case BlockType.ORDERED_LIST:
				children.append(block_to_list(block, True))
			case _:
				raise Exception("Unrecognized Block Type.")
	return ParentNode("div", children)

def markdown_to_blocks(markdown):
	initial_split = markdown.split("\n\n")
	stripped = [clean_block(block) for block in initial_split]
	blocks = [block for block in stripped if block != ""]
	return blocks

def clean_block(block):
	lines = block.split("\n")
	stripped = [line.strip() for line in lines]
	filtered = [line for line in stripped if line != ""]
	if len(filtered) == 0:
		return ""
	newBlock = "\n".join(filtered)
	return newBlock

re_heading = r"#{1,6} .+"
re_ordered = r"\d+\. "
def identify_block_type(block):
	if re.match(re_heading, block):
		return BlockType.HEADING
	elif block.startswith("```") and block.endswith("```"):
		return BlockType.CODE
	elif isQuote(block):
		return BlockType.QUOTE
	elif isUnorderedList(block):
		return BlockType.UNORDERED_LIST
	elif isOrderedList(block):
		return BlockType.ORDERED_LIST
	else:
		return BlockType.PARAGRAPH

def isQuote(block):
	lines = block.split('\n')
	for line in lines:
		if not line.startswith('>'):
			return False
	return True

def isUnorderedList(block):
	lines = block.split('\n')
	for line in lines:
		if not line.startswith('- '):
			return False
	return True

def isOrderedList(block):
	lines = block.split('\n')
	for line in lines:
		if not re.match(re_ordered, block):
			return False
	return True

def block_to_paragraph(block):
	lines = block.split("\n")
	unified = " ".join(lines)
	textNodes = convert_line_to_textnodes(unified)
	children = []
	for node in textNodes:
		children.append(text_node_to_html_node(node))
	return ParentNode("p", children)

# TODO: figure out how to handle whitespace on each line of code
def block_to_code(block):
	unquoted = block[3:-3]
	lines = unquoted.split('\n')
	normalized = [line.strip() for line in lines]
	filtered = [line for line in lines if line != ""]
	cleaned = "\n".join(filtered)
	children = [LeafNode("code", cleaned)]
	return ParentNode("pre", children)

def block_to_heading(block):
	"""
	1. split string into (hashpart, remainder)
	2. count hashes
	3. create textnode(s) using convert_line_to_textnodes
	4. create a list of Leafnodes from the textnodes
	5. create parent node (h*, children)
	"""
	split_block = block.split(" ", maxsplit=1)
	heading_depth = len(split_block[0])
	unified = " ".join(split_block[1].split("\n"))
	textNodes = convert_line_to_textnodes(unified)
	children = []
	for node in textNodes:
		children.append(text_node_to_html_node(node))
	return ParentNode(f"h{heading_depth}", children)

def block_to_list(block, ordered):
	if ordered:
		main_tag = "ol"
	else:
		main_tag = "ul"
	children = []
	list_items = block.split("\n")

	for line in list_items:
		children.append(line_to_list_item(line))

	return ParentNode(main_tag, children)

def line_to_list_item(line):
	text = line.split(" ", maxsplit=1)[1]
	children = []
	textNodes = convert_line_to_textnodes(text)
	for node in textNodes:
		children.append(text_node_to_html_node(node))
	return ParentNode("li", children)

def block_to_quote(block):
	lines = block.split("\n")
	normalized = [strip_quote_prefix(line) for line in lines]
	text = " ".join(normalized)
	children = [LeafNode("blockquote", text)]
	return ParentNode("pre", children)

QUOTE_PREFIX_RE = re.compile(r"^>\s*(.*)$")
def strip_quote_prefix(line: str) -> str:
	match = QUOTE_PREFIX_RE.match(line)
	if match:
		return match.group(1)
	return line  # fallback, in case something slips through