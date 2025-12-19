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

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children = []
	for block in blocks:
		b_type = identify_block_type(block)
		match b_type:
			case BlockType.PARAGRAPH:
				children.append(markdown_to_paragraph(block))
			case BlockType.HEADING:
				pass
			case BlockType.CODE:
				children.append(markdown_to_code(block))
			case BlockType.QUOTE:
				pass
			case BlockType.UNORDERED_LIST:
				pass
			case BlockType.ORDERED_LIST:
				pass
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
		return BlockType.UNORDERED_LIST
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

def markdown_to_paragraph(block):
	lines = block.split("\n")
	unified = " ".join(lines)
	textNodes = convert_line_to_textnodes(unified)
	children = []
	for node in textNodes:
		children.append(text_node_to_html_node(node))
	return ParentNode("p", children)

def markdown_to_code(block):
	unquoted = block[3:-3]
	lines = unquoted.split('\n')
	normalized = [line.strip() for line in lines]
	filtered = [line for line in lines if line != ""]
	cleaned = "\n".join(filtered) + "\n"
	children = [LeafNode("code", cleaned)]
	return ParentNode("pre", children)