import unittest
from matcher import clean_text

class TestCleanText(unittest.TestCase):

    def test_lowercase_conversion(self):
        """Test that uppercase letters are converted to lowercase."""
        self.assertEqual(clean_text("HELLO WORLD"), "hello world")
        self.assertEqual(clean_text("Python Developer"), "python developer")

    def test_special_characters_removal(self):
        """Test that unwanted special characters are removed and replaced with spaces."""
        self.assertEqual(clean_text("hello@world!"), "hello world")
        self.assertEqual(clean_text("user_name$%^"), "user name")
        self.assertEqual(clean_text("React & Redux"), "react redux")

    def test_allowed_characters_retention(self):
        """Test that allowed characters like +, #, . are kept."""
        self.assertEqual(clean_text("C++ Developer"), "c++ developer")
        self.assertEqual(clean_text("C# Developer"), "c# developer")
        self.assertEqual(clean_text("Node.js, ASP.NET"), "node.js asp.net")

    def test_whitespace_handling(self):
        """Test that excess whitespaces are collapsed and edges are stripped."""
        self.assertEqual(clean_text("   too   many    spaces   "), "too many spaces")
        self.assertEqual(clean_text("tabs\tand\nnewlines"), "tabs and newlines")

    def test_empty_and_whitespace_only(self):
        """Test empty string and string with only whitespaces or special characters."""
        self.assertEqual(clean_text(""), "")
        self.assertEqual(clean_text("   \n \t "), "")
        self.assertEqual(clean_text("!@#$%^&*()"), "#")

    def test_only_disallowed_characters(self):
        """Test string with only disallowed characters."""
        self.assertEqual(clean_text("!@$%^&*()"), "")

if __name__ == "__main__":
    unittest.main()