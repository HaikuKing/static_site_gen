def markdown_to_blocks(markdown):
    stripped_blocks = []
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        b = blocks[i]
        if b:
            stripped_blocks.append("".join(b.strip()))
    return stripped_blocks