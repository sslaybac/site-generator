import unittest

from leafnode import LeafNode
from text_converter import BlockType, extract_title, identify_block_type, markdown_to_blocks, markdown_to_html_node

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

	def test_identify_ordered_list(self):
		input = """
			1. First item
			2. Second item
			3. Third item
		"""
		self.assertEqual(identify_block_type(markdown_to_blocks(input)[0]), BlockType.ORDERED_LIST)

	def test_paragraphs(self):
		md = """
	This is **bolded** paragraph
	text in a p
	tag here

	This is another paragraph with _italic_ text and `code` here

	"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
		self.assertEqual(html, expected)

	def test_codeblock(self):
		md = """
		```
		This is text that _should_ remain
		the **same** even with inline stuff
		```
		"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
		self.assertEqual(html, expected)

	def test_heading(self):
		md = """
		# This is a heading
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><h1>This is a heading</h1></div>"
		self.assertEqual(html, expected)

		md = """
		## This is a heading with **bold** text
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><h2>This is a heading with <b>bold</b> text</h2></div>"
		self.assertEqual(html, expected)

		md = """
		### This is a heading
		across multiple lines
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><h3>This is a heading across multiple lines</h3></div>"
		self.assertEqual(html, expected)

	def test_list(self):
		md = """
		- unordered list item 1
		- unordered list item 2
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><ul><li>unordered list item 1</li><li>unordered list item 2</li></ul></div>"
		self.assertEqual(html, expected)

		md = """
		1. ordered list item 1
		2. ordered list item 2
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><ol><li>ordered list item 1</li><li>ordered list item 2</li></ol></div>"
		self.assertEqual(html, expected)

		md = """
		- unordered list item with **bold**
		- unordered _italic_ list item
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><ul><li>unordered list item with <b>bold</b></li><li>unordered <i>italic</i> list item</li></ul></div>"
		self.assertEqual(html, expected)

	def test_quote(self):
		md = """
		>One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed.
		> He lay on his armour-like back.
		>   His many legs, pitifully thin, waved about helplessly as he looked.
		>	His room, a proper human room although a little too small, lay peacefully between its four familiar walls.
		"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = "<div><pre><quote>One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed. He lay on his armour-like back. His many legs, pitifully thin, waved about helplessly as he looked. His room, a proper human room although a little too small, lay peacefully between its four familiar walls.</quote></pre></div>"
		self.assertEqual(html, expected)

	def test_multiblock_md(self):
		md = """
			# This is an **important** heading

			###### This heading is
			far less important

			This is a simple
			multiline paragraph with
			_italic_ text

			1. First _ordered_ list item
			2. Second _ordered_ list item

			- First _unordered_ list item
			- Second _unordered_ list item

			> It was the **best** of times
			>It was the _worst_ of times

			```
			def test():
				print("testing")
				# this is **not** parsed and _stays_ `the same
			```
			"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		expected = '<div><h1>This is an <b>important</b> heading</h1><h6>This heading is far less important</h6><p>This is a simple multiline paragraph with <i>italic</i> text</p><ol><li>First <i>ordered</i> list item</li><li>Second <i>ordered</i> list item</li></ol><ul><li>First <i>unordered</i> list item</li><li>Second <i>unordered</i> list item</li></ul><pre><quote>It was the **best** of times It was the _worst_ of times</quote></pre><pre><code>def test():\nprint("testing")\n# this is **not** parsed and _stays_ `the same</code></pre></div>'
		self.assertEqual(html, expected)

	def test_extract_title(self):
		md = """
			# This is an **important** heading

			###### This heading is
			far less important

			This is a simple
			multiline paragraph with
			_italic_ text

			1. First _ordered_ list item
			2. Second _ordered_ list item

			- First _unordered_ list item
			- Second _unordered_ list item

			> It was the **best** of times
			>It was the _worst_ of times

			```
			def test():
				print("testing")
				# this is **not** parsed and _stays_ `the same
			```
			"""

		title = extract_title(md)
		expected = "This is an important heading"
		self.assertEqual(title, expected)
