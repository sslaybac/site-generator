from htmlnode import HTMLNode


class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if not self.tag:
			raise ValueError("Node does not have a tag.")
		if not self.children:
			raise ValueError("Parent node does not have children.")
		output_string = f"<{self.tag}{self.props_to_html()}>"
		for child in self.children:
			output_string += child.to_html()
		output_string += f"</{self.tag}>"

		return output_string

	def to_raw_text(self):
		children_text = [child.to_raw_text() for child in self.children]
		return ''.join(children_text)