import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("p", "hello world", None, None)
		node2 = HTMLNode("p", "hello world", None, None)
		self.assertEqual(node, node2)

	def test_props_conversion(self):
		props = {"class": "p_class", "id": "p_id"}
		node = HTMLNode("p", "hello_world", None, props)
		self.assertEqual(node.props_to_html(), ' class="p_class" id="p_id"')

	def test_eq_rev_props(self):
		props = {"class": "p_class", "id": "p_id"}
		props2 = {"id": "p_id", "class": "p_class"}
		node = HTMLNode("p", "hello world", None, props)
		node2 = HTMLNode("p", "hello world", None, props2)
		self.assertEqual(node, node2)