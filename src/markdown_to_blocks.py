from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    stripped_blocks = []
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        b = blocks[i]
        if b:
            stripped_blocks.append("".join(b.strip()))
    return stripped_blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    quote, unordered, ordered, total_lines = 0, 0, 0, 0
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith(">"):
            quote += 1
        if line.startswith("- "):
            unordered += 1
        if line.startswith(f"{i+1}. "):
            ordered += 1
        total_lines += 1

    if quote == total_lines:
        return BlockType.QUOTE
    
    if unordered == total_lines:
        return BlockType.UNORDERED_LIST
    
    if ordered == total_lines:
        return BlockType.ORDERED_LIST
    
    else:
        return BlockType.PARAGRAPH
