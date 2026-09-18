import pytest
from app import allowed_file

@pytest.mark.parametrize(
    "filename, expected",
    [
        # Happy paths
        ("resume.pdf", True),
        ("resume.PDF", True),
        ("resume.PdF", True),
        ("my.resume.pdf", True),
        ("some_other_file_name.123.pdf", True),

        # Negative cases
        ("resume", False),
        ("resume.doc", False),
        ("resume.docx", False),
        ("resume.pdf.doc", False),
        ("resume.", False),
        ("", False),
        ("pdf", False),

        # Edge cases
        (".pdf", True), # hidden file with pdf extension
        ("resume..pdf", True), # multiple dots
    ]
)
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected
