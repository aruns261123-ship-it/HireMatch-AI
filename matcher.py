import re
import math
from collections import Counter
from functools import lru_cache


# ============================================================
# HIREMATCH AI
# NLP-Based Resume and Job Matching Engine
# ============================================================


SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "flask",
    "django",
    "fastapi",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "sqlite",
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "rest api",
    "data analysis",
    "data science",
    "power bi",
    "tableau"
]


STOP_WORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "but",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "from",
    "is",
    "are",
    "was",
    "were",
    "be",
    "this",
    "that",
    "as",
    "by",
    "we",
    "our",
    "you",
    "your",
    "will",
    "have",
    "has",
    "had",
    "it",
    "they",
    "their"
}


@lru_cache(maxsize=128)
def clean_text(text):
    """
    Basic NLP text preprocessing.
    Optimized with lru_cache to prevent redundant processing of the same text
    (e.g., job descriptions across multiple candidates).
    """

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


@lru_cache(maxsize=128)
def tokenize(text):
    """
    Tokenize text and remove stop words.
    Optimized with lru_cache to avoid re-tokenizing the same text multiple times.
    """

    text = clean_text(text)

    words = text.split()

    words = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    return words


def calculate_tfidf(documents):
    """
    Calculate TF-IDF vectors manually.

    TF  = Term Frequency
    IDF = Inverse Document Frequency
    """

    tokenized_documents = [
        tokenize(document)
        for document in documents
    ]

    document_count = len(
        tokenized_documents
    )

    vocabulary = set()

    for document in tokenized_documents:

        vocabulary.update(document)

    vocabulary = sorted(vocabulary)

    tfidf_vectors = []

    for document in tokenized_documents:

        word_count = Counter(document)

        total_words = len(document)

        vector = {}

        for word in vocabulary:

            if total_words == 0:

                tf = 0

            else:

                tf = (
                    word_count[word]
                    / total_words
                )

            document_frequency = sum(
                1
                for doc in tokenized_documents
                if word in doc
            )

            idf = math.log(
                (document_count + 1)
                /
                (document_frequency + 1)
            ) + 1

            vector[word] = tf * idf

        tfidf_vectors.append(vector)

    return tfidf_vectors


def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    words = set(vector_a.keys()) | set(
        vector_b.keys()
    )

    dot_product = sum(
        vector_a.get(word, 0)
        *
        vector_b.get(word, 0)
        for word in words
    )

    magnitude_a = math.sqrt(
        sum(
            value ** 2
            for value in vector_a.values()
        )
    )

    magnitude_b = math.sqrt(
        sum(
            value ** 2
            for value in vector_b.values()
        )
    )

    if magnitude_a == 0 or magnitude_b == 0:

        return 0

    return (
        dot_product
        /
        (magnitude_a * magnitude_b)
    )


def calculate_similarity(
    resume_text,
    job_description
):
    """
    Calculate TF-IDF cosine similarity.
    """

    vectors = calculate_tfidf(
        [
            resume_text,
            job_description
        ]
    )

    return cosine_similarity(
        vectors[0],
        vectors[1]
    )


@lru_cache(maxsize=128)
def extract_skills(text):
    """
    Extract technical skills using whole-word matching.
    This prevents false positives such as detecting
    'c' inside words like 'experience'.
    Optimized with lru_cache to avoid re-extracting skills for the same text.
    """

    text = clean_text(text)

    found_skills = []

    for skill in SKILLS:

        # Escape special characters such as +, # and .
        escaped_skill = re.escape(
            skill.lower()
        )

        # Whole-word / phrase matching
        pattern = r"(?<!\w)" + escaped_skill + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(set(found_skills))


def calculate_match(
    resume_text,
    job_description
):
    """
    Complete HireMatch AI analysis.
    """

    similarity = calculate_similarity(
        resume_text,
        job_description
    )

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    matching_skills = [
        skill
        for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in job_skills
        if skill not in resume_skills
    ]

    if job_skills:

        skill_score = (
            len(matching_skills)
            /
            len(job_skills)
        )

    else:

        skill_score = 0

    final_score = (
        (similarity * 60)
        +
        (skill_score * 40)
    )

    final_score = round(
        final_score,
        2
    )

    return {
        "match_score": final_score,

        "similarity_score": round(
            similarity * 100,
            2
        ),

        "skill_score": round(
            skill_score * 100,
            2
        ),

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "matching_skills": matching_skills,

        "missing_skills": missing_skills
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    resume = """
    Python developer with experience in
    machine learning, Flask, SQL, Pandas
    and REST APIs.
    """

    job = """
    We are looking for a Python developer
    with experience in machine learning,
    Flask, SQL, REST APIs and Docker.
    """

    print("\n==============================")
    print("       HIREMATCH AI")
    print("==============================\n")

    result = calculate_match(
        resume,
        job
    )

    print(
        "Match Score:",
        result["match_score"],
        "%"
    )

    print(
        "TF-IDF Similarity:",
        result["similarity_score"],
        "%"
    )

    print(
        "Skill Match:",
        result["skill_score"],
        "%"
    )

    print("\nMatching Skills:")

    for skill in result["matching_skills"]:

        print("  ✓", skill)

    print("\nMissing Skills:")

    for skill in result["missing_skills"]:

        print("  ✗", skill)

    print("\n==============================\n")


# ============================================================
# MULTI-CANDIDATE RANKING
# ============================================================

def rank_candidates(
    candidates,
    job_description
):
    """
    Analyze and rank multiple candidates
    against one job description.
    """

    ranked_candidates = []

    for candidate in candidates:

        result = calculate_match(
            candidate["text"],
            job_description
        )

        ranked_candidates.append({

            "filename": candidate["filename"],

            "match_score": result["match_score"],

            "similarity_score": result["similarity_score"],

            "skill_score": result["skill_score"],

            "matching_skills": result["matching_skills"],

            "missing_skills": result["missing_skills"],

            "resume_skills": result["resume_skills"]

        })

    # Highest match score first

    ranked_candidates.sort(
        key=lambda candidate: candidate["match_score"],
        reverse=True
    )

    # Assign ranking numbers

    for index, candidate in enumerate(
        ranked_candidates,
        start=1
    ):

        candidate["rank"] = index

    return ranked_candidates