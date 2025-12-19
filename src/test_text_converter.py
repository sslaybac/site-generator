import unittest

from leafnode import LeafNode
from text_converter import BlockType, identify_block_type, markdown_to_blocks, markdown_to_html_node

class TestTextConverter(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
			This is **bolded** paragraph

			This is another paragraph with _italic_ text and `code` here
			This is the same paragraph on a new line

			- This is a list
			- with items
			"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)

	def test_identify_heading(self):
		input = "# This is a heading"
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.HEADING)
		input = "####### This is a false heading"
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.PARAGRAPH)

	def test_identify_code(self):
		input = """
			```
			def hello():
			print("Hello, world!")
			```
		"""
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.CODE)
		input = """
			```
			def hello():
			```
			print("Hello, world!")
		"""
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.PARAGRAPH)

	def test_identify_quote(self):
		input = """
			> This is a quote
			> It spans multiple lines
			> Every line starts with >
		"""
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.QUOTE)
		input = """
			> This is a quote
			It spans multiple lines
			> Every line starts with >
		"""
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.PARAGRAPH)

	def test_identify_unordered_list(self):
		input = """
			- First item
			- Second item
			- Third item
		"""
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.UNORDERED_LIST)

	def test_paragraphs(self):
		md = """
	This is **bolded** paragraph
	text in a p
	tag here

	This is another paragraph with _italic_ text and `code` here

	"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)