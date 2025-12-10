import unittest

from markdown_to_blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
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
            BlockType.HEADING,
        )

    def test_block_to_block_type_two(self):
        block = "#### This is a heading."
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
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

if __name__ == "__main__":
    unittest.main()
