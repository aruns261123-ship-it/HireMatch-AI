import math
from matcher import cosine_similarity

def test_cosine_similarity_empty_vectors():
    assert cosine_similarity({}, {}) == 0
    assert cosine_similarity({"word": 1}, {}) == 0
    assert cosine_similarity({}, {"word": 1}) == 0

def test_cosine_similarity_zero_vectors():
    assert cosine_similarity({"word": 0}, {"word": 0}) == 0
    assert cosine_similarity({"word": 1}, {"word": 0}) == 0
    assert cosine_similarity({"word": 0}, {"word": 1}) == 0

def test_cosine_similarity_mixed_empty_zero():
    assert cosine_similarity({}, {"word": 0}) == 0
    assert cosine_similarity({"word": 0}, {}) == 0

def test_cosine_similarity_normal():
    vector_a = {"hello": 1, "world": 1}
    vector_b = {"hello": 1, "world": 0}
    # dot_product = 1
    # magnitude_a = sqrt(2)
    # magnitude_b = 1
    # similarity = 1 / sqrt(2)
    expected = 1 / math.sqrt(2)
    assert math.isclose(cosine_similarity(vector_a, vector_b), expected)
