import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        text = old_node.text
        images = extract_markdown_images(text)
        if not images:
            split_nodes.append(old_node)

        else:
            for alt, url in images:
                full_markdown = f"![{alt}]({url})"
                before, after = text.split(full_markdown, 1)

                if before:
                    split_nodes.append(TextNode(before, TextType.TEXT))

                split_nodes.append(TextNode(alt, TextType.IMAGE, url))

                text = after
            if text:
                split_nodes.append(TextNode(text, TextType.TEXT))
                
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        text = old_node.text
        links = extract_markdown_links(text)
        if not links:
            split_nodes.append(old_node)

        else:
            for alt, url in links:
                full_markdown = f"[{alt}]({url})"
                before, after = text.split(full_markdown, 1)

                if before:
                    split_nodes.append(TextNode(before, TextType.TEXT))

                split_nodes.append(TextNode(alt, TextType.LINK, url))

                text = after
            if text:
                split_nodes.append(TextNode(text, TextType.TEXT))
                
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(markdown):
    stripped_blocks = []
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        b = blocks[i]
        if b:
            stripped_blocks.append("".join(b.strip()))
    return stripped_blocks