import unittest
from htmlnode import(
    HTMLNode,
    LeafNode
)
from markdown_to_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    text_to_children,
    block_to_html_node,
    markdown_to_html_node
)


class TestMarkdownToBlocks(unittest.TestCase):

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

    def test_markdown_to_blocks_two(self):
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

    def test_markdown_to_blocks_three(self):
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

    def test_markdown_to_blocks_four(self):
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
                "- This is a list",
                "- with items",
            ],
        )

    def test_markdown_to_blocks_five(self):
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
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):

    def test_block_to_block_type(self):
        block = "# This is a heading."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADER_ONE,
        )

    def test_block_to_block_type_two(self):
        block = "## This is a heading."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADER_TWO,
        )

    def test_block_to_block_type_three(self):
        block = "```This is a code block.```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE,
        )

    def test_block_to_block_type_four(self):
        block = ">This is a quote block.\n>Every line needs to have\n>an arrow."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE,
        )

    def test_block_to_block_type_five(self):
        block = ">This is an incorrect quote block.\n>Every line needs to have an arrow.\nThis will flag as a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_six(self):
        block = "- This is an unordered list.\n- It has a dash at the start of each line.\n- This is the third line."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_block_type_seven(self):
        block = "1. This is an ordered list.\n2. It has a number and period at the start of each line.\n3. This is the third line."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_type_eight(self):
        block = "- This is an unordered list.\n- It has a dash at the start of each line.\nThis is the third line which makes it flag as a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )
    
    def test_block_to_block_type_nine(self):
        block = "1. This is an ordered list.\n2. It has a dash at the start of each line.\n- This is the third line which makes it flag as a paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_ten(self):
        block = "This is a paragraph.\nIt has multiple lines.\nIt is the last test as it is the last block type."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

class TestBlockToHtmlNode(unittest.TestCase):

    def test_block_to_html_node(self):
        block = "# some text here"
        node = block_to_html_node(block)
        self.assertEqual(node, HTMLNode("h1", "some text here"))

    def test_block_to_html_node_two(self):
        block = "## some text here"
        node = block_to_html_node(block)
        self.assertEqual(node.tag, "h2")
        self.assertEqual(node.value, "some text here")

    def test_block_to_html_node_code(self):
        block = "```some code here```"
        node = block_to_html_node(block)
        self.assertEqual(
            node,
            HTMLNode("pre", None, [
                    HTMLNode("code", "some code here")
            ])
        )
        
    def test_block_to_html_node_four(self):
        block = "just a random **paragraph** here"
        node = block_to_html_node(block)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.children, text_to_children(block))

    def test_block_to_html_node_quote(self):
        block = ">This is a quote block.\n>It has multiple lines.\n>We hope **this** works."
        node = block_to_html_node(block)
        self.assertEqual(node.tag, "blockquote")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, text_to_children("This is a quote block.\nIt has multiple lines.\nWe hope **this** works."))

    def test_block_to_html_node_unordered_list(self):
        block = "- This is an unordered list.\n- This is the **second** line.\n- This is the third."
        node = block_to_html_node(block)
        self.assertEqual(node.tag, "ul")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children,
            [
            LeafNode("li", "- This is an unordered list."),
            LeafNode("li", "- This is the **second** line."),
            LeafNode("li", "- This is the third."),
        ],
        )

    def test_block_to_html_node_ordered_list(self):
        block = "1. This is an ordered list.\n2. This is the **second** line.\n3. This is the third."
        node = block_to_html_node(block)
        self.assertEqual(node.tag, "ol")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children,
            [
            LeafNode("li", "1. This is an ordered list."),
            LeafNode("li", "2. This is the **second** line."),
            LeafNode("li", "3. This is the third."),
        ],
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_paragraphs_two(self):
        md = """
This is **bolded** paragraph
text in a p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
            
if __name__ == "__main__":
    unittest.main()
