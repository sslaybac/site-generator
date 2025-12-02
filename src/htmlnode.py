class HTMLNode:
	"""
	Docstring for HTMLNode constructor
	parameters:
	tag: the string representing the html tag
	value: text content of the html node
	children: any tagged html items within this node
	props: a dictionary of properties to be assigned in the opening tag.
	"""
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def __eq__(self, other):
		if self.tag != other.tag:
			return False
		if self.value != other.value:
			return False
		if self.children != other.children:
			return False
		if self.props != other.props:
			return False
		return True
	
	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		if not self.props:
			return ""
		props_string = ""
		for key in self.props:
			props_string += f' {key}="{self.props[key]}"'
		return props_string

	def __repr__(self):
		output_string = ""
		output_string += f"tag: {self.tag}\n"
		output_string += f"value: {self.value}\n"
		output_string += f"children: {self.children}\n"
		output_string += f"properties:{self.props_to_html()}\n"