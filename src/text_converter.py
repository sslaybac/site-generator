import re
from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

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