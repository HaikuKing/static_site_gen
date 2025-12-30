from enum import Enum
from textnode import (
    text_node_to_html_node
)
from htmlnode import (
    HTMLNode
)
from inline_markdown import (
    text_to_textnodes
)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADER_ONE = "header one"
    HEADER_TWO = "header two"
    HEADER_THREE = "header three"
    HEADER_FOUR = "header four"
    HEADER_FIVE = "header five"
    HEADER_SIX = "header six"
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
    if block.startswith("# "):
        return BlockType.HEADER_ONE
    
    if block.startswith("## "):
        return BlockType.HEADER_TWO
    
    if block.startswith("### "):
        return BlockType.HEADER_THREE
    
    if block.startswith("#### "):
        return BlockType.HEADER_FOUR
    
    if block.startswith("##### "):
        return BlockType.HEADER_FIVE
    
    if block.startswith("###### "):
        return BlockType.HEADER_SIX

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

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = []
    for node in nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BlockType.HEADER_ONE:
        text = block.lstrip("#").strip()
        return HTMLNode("h1", text)
    elif block_type == BlockType.HEADER_TWO:
        text = block.lstrip("#").strip()
        return HTMLNode("h2", text)
    elif block_type == BlockType.HEADER_THREE:
        text = block.lstrip("#").strip()
        return HTMLNode("h3", text)
    elif block_type == BlockType.HEADER_FOUR:
        text = block.lstrip("#").strip()
        return HTMLNode("h4", text)
    elif block_type == BlockType.HEADER_FIVE:
        text = block.lstrip("#").strip()
        return HTMLNode("h5", text)
    elif block_type == BlockType.HEADER_SIX:
        text = block.lstrip("#").strip()
        return HTMLNode("h6", text)
    

    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            new_lines.append(line.lstrip(">").strip())
        new_block = "\n".join(new_lines)
        children = text_to_children(new_block)
        return HTMLNode("blockquote", None, children)
    
    elif block_type == BlockType.PARAGRAPH:
        # turn internal newlines into spaces before inline parsing
        normalized = " ".join(block.split("\n"))
        children = text_to_children(normalized)
        return HTMLNode("p", None, children)
    
    elif block_type == BlockType.CODE:
        if "\n" not in block:
            code = block[3:-3]
        else:
            lines = block.split("\n")
            code_lines = lines[1:-1]
            cleaned = [line.lstrip() for line in code_lines]
            code = "\n".join(cleaned) + "\n"
        code_node = HTMLNode("code", code)
        return HTMLNode("pre", None, [code_node])

    elif block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            stripped_line = line.lstrip("-").strip()
            items.append(HTMLNode("li", None, text_to_children(stripped_line)))
        return HTMLNode("ul", None, items)
    
    elif block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            stripped_line = line.lstrip("1234567890.").strip()
            items.append(HTMLNode("li", None, text_to_children(stripped_line)))
        return HTMLNode("ol", None, items)

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return HTMLNode("div", None, children)
