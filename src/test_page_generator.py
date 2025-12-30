import unittest
from page_generator import (
    extract_title
)

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        title = extract_title("# This is the title\n\nThis is a paragraph.")
        self.assertEqual(
            title,
            "This is the title"
        )

    def test_extract_title_two(self):
        title = extract_title("""# My Project Title

A brief description of what this project is about.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)

---

## Introduction
This project is designed to make your life easier by automating repetitive tasks.

---

## Features
- Easy to use  
- Fast and efficient  
- Secure and reliable  

---

## Installation
```bash
git clone https://github.com/username/project.git
cd project
npm install
""")
        self.assertEqual(
            title,
            "My Project Title"
        )

    def test_extract_title_three(self):
        title = extract_title("# This is the title\n\nThis is a paragraph.")
        self.assertNotEqual(
            title,
            "This is not the title"
        )

    def test_extract_title_four(self):
        title = extract_title("# This is the title\n\nThis is a paragraph.\n\n# This is another title")
        self.assertNotEqual(
            title,
            "This is another title"
        )

    def test_extract_title_trailing_space(self):
        title = extract_title("# This is the title \n\nThis is a paragraph.")
        self.assertEqual(
            title,
            "This is the title"
        )

if __name__ == "__main__":
    unittest.main()
