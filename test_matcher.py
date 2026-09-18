import pytest
from matcher import extract_skills

def test_extract_skills_whole_word_c():
    """Test extracting 'c' as a standalone word."""
    text = "I have experience with C programming."
    skills = extract_skills(text)
    assert "c" in skills

def test_extract_skills_false_positive_c():
    """Test that 'c' is not matched inside other words like 'experience'."""
    text = "I have great experience in car driving and architecture."
    skills = extract_skills(text)
    assert "c" not in skills

def test_extract_skills_special_characters():
    """Test extracting skills with special characters like C++, C#, Node.js."""
    text = "I use C++ and C# and Node.js daily."
    skills = extract_skills(text)
    assert "c++" in skills
    assert "c#" in skills
    assert "node.js" in skills

def test_extract_skills_case_insensitive():
    """Test that skill extraction is case-insensitive."""
    text = "PYTHON, jAvAsCrIpT, and React"
    skills = extract_skills(text)
    assert "python" in skills
    assert "javascript" in skills
    assert "react" in skills

def test_extract_skills_boundary_punctuation():
    """Test extracting skills bounded by punctuation."""
    text = "Skills: python, java. Also c++!"
    skills = extract_skills(text)
    assert "python" in skills
    assert "java" in skills
    assert "c++" in skills

def test_extract_skills_empty():
    """Test extraction on empty string."""
    assert extract_skills("") == []

def test_extract_skills_multiple_occurrences():
    """Test that extracted skills are unique and sorted."""
    text = "Python is great. I love python. PYTHON!"
    skills = extract_skills(text)
    assert skills.count("python") == 1

def test_extract_skills_no_skills_found():
    """Test extraction when text contains no predefined skills."""
    text = "I am a very hard worker and a team player."
    skills = extract_skills(text)
    assert skills == []
