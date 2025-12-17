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
	block = "\n".join(filtered)
	return block
