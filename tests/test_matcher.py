import unittest
from src.matcher import tfidf_similarity, skill_coverage, calculate_match

class TestMatcher(unittest.TestCase):
    def test_identical_text(self):
        score = tfidf_similarity("python machine learning", "python machine learning")
        self.assertAlmostEqual(score, 1.0, places=5)

    def test_skill_coverage(self):
        score = skill_coverage(["Python", "SQL"], ["Python", "SQL", "AWS"])
        self.assertAlmostEqual(score, 2/3, places=5)

    def test_calculate_match_range(self):
        result = calculate_match(
            "python sql machine learning",
            "python sql machine learning aws",
            ["Python", "SQL", "Machine Learning"],
            ["Python", "SQL", "AWS"],
            2, 2
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 1)

if __name__ == "__main__":
    unittest.main()
