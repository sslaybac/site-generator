import unittest

from textnode import TextNode, TextType, split_nodes_image, split_nodes_link, text_node_to_html_node, convert_line_to_textnodes
from textnode import extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_eq_none(self):
		node = TextNode("This is a text node", None)
		node2 = TextNode("This is a text node", None)
		self.assertEqual(node, node2)

	def test_ne_type(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)

	def test_plaintext(self):
		node = TextNode("This is a text node", TextType.PLAIN)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a bold node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold node")

	def test_italic(self):
		node = TextNode("This is a italic node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is a italic node")

	def test_code(self):
		node = TextNode("This is a code node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code node")

	def test_link(self):
		node = TextNode("This is a link node", TextType.LINK, "www.link.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link node")
		self.assertEqual(html_node.props["href"], "www.link.com")

	def test_img(self):
		node = TextNode("This is a image node", TextType.IMAGE, "www.image.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props["alt"], "This is a image node")
		self.assertEqual(html_node.props["src"], "www.image.com")

	def test_line_to_bold_simple(self):
		md_line = "this is a **bold** test message"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.BOLD)
		self.assertEqual(nodes[1].text, "bold")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

		md_line2 = "**bold** at the beginning"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.BOLD)
		self.assertEqual(nodes[1].text, "bold")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

		md_line3 = "line ends in **bold**"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.BOLD)
		self.assertEqual(nodes[1].text, "bold")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

	def test_line_to_italic_simple(self):
		md_line = "this is a _italic_ test message"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.ITALIC)
		self.assertEqual(nodes[1].text, "italic")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

		md_line2 = "_italic_ at the beginning"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.ITALIC)
		self.assertEqual(nodes[1].text, "italic")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

		md_line3 = "line ends in _italic_"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.ITALIC)
		self.assertEqual(nodes[1].text, "italic")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

	def test_line_to_code_simple(self):
		md_line = "this is a `code` test message"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.CODE)
		self.assertEqual(nodes[1].text, "code")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

		md_line2 = "`code` at the beginning"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.CODE)
		self.assertEqual(nodes[1].text, "code")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

		md_line3 = "line ends in `code`"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 3)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.CODE)
		self.assertEqual(nodes[1].text, "code")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)

	def test_double_bold(self):
		md_line = "testing **bold** two **bold** sections"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 5)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.BOLD)
		self.assertEqual(nodes[1].text, "bold")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)
		self.assertEqual(nodes[3].text_type, TextType.BOLD)
		self.assertEqual(nodes[3].text, "bold")
		self.assertEqual(nodes[4].text_type, TextType.PLAIN)

	def test_double_italic(self):
		md_line = "testing _italic_ two _italic_ sections"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 5)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.ITALIC)
		self.assertEqual(nodes[1].text, "italic")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)
		self.assertEqual(nodes[3].text_type, TextType.ITALIC)
		self.assertEqual(nodes[3].text, "italic")
		self.assertEqual(nodes[4].text_type, TextType.PLAIN)

	def test_double_code(self):
		md_line = "testing `code` two `code` sections"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 5)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.CODE)
		self.assertEqual(nodes[1].text, "code")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)
		self.assertEqual(nodes[3].text_type, TextType.CODE)
		self.assertEqual(nodes[3].text, "code")
		self.assertEqual(nodes[4].text_type, TextType.PLAIN)

	def test_mixed_line(self):
		md_line = "testing **bold** then _italic_ then `code` line"
		nodes = convert_line_to_textnodes(md_line)
		self.assertEqual(len(nodes), 7)
		self.assertEqual(nodes[0].text_type, TextType.PLAIN)
		self.assertEqual(nodes[1].text_type, TextType.BOLD)
		self.assertEqual(nodes[1].text, "bold")
		self.assertEqual(nodes[2].text_type, TextType.PLAIN)
		self.assertEqual(nodes[3].text_type, TextType.ITALIC)
		self.assertEqual(nodes[3].text, "italic")
		self.assertEqual(nodes[4].text_type, TextType.PLAIN)
		self.assertEqual(nodes[5].text_type, TextType.CODE)
		self.assertEqual(nodes[5].text, "code")
		self.assertEqual(nodes[6].text_type, TextType.PLAIN)

	def test_image_extractor(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
		self.assertEqual(extract_markdown_images(text), expected)

		text = "no images here"
		expected = []
		self.assertEqual(extract_markdown_images(text), expected)
		

	def test_link_extractor(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		expected = [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
		self.assertEqual(extract_markdown_links(text), expected)

		text = "no links here"
		expected = []
		self.assertEqual(extract_markdown_images(text), expected)

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.PLAIN,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.PLAIN),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.PLAIN),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes,
		)

	def test_split_links(self):
		node = TextNode(
			"This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
			TextType.PLAIN,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.PLAIN),
				TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.PLAIN),
				TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
			],
			new_nodes,
		)

	def test_split_all(self):
		input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		actual = convert_line_to_textnodes(input)
		expected = [
			TextNode("This is ", TextType.PLAIN),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.PLAIN),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.PLAIN),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.PLAIN),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.PLAIN),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		self.assertListEqual(expected, actual)


if __name__ == "__main__":
	unittest.main()