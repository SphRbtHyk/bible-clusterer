"""
Tests the LXXClusterer class.
"""
import unittest
from lxx_nlp_utils import clusterer
import numpy as np
import pandas as pd
from lxx_nlp_utils.clusterer import LXXClusterer


class TextLXXClusterer(unittest.TestCase):
    """
    Test the LXX Clusterer class.
    """

    def setUp(self):
        self.lxx_clusterer = LXXClusterer()

    def test_clean(self):
        """
        Tests that the cleaning method works as expected.
        """
        test_corpus = ["titi is tall", "toto is small", "tutu is big"]
        stop_words = ["is"]
        expected_cleaned_corpus = ["titi tall", "toto small", "tutu big"]
        cleaned_corpus = self.lxx_clusterer.clean(test_corpus, stop_words)
        self.assertEqual(expected_cleaned_corpus, cleaned_corpus)

    def test_tf_idf_vectorizer(self):
        """
        Check if tf idf vectorizer works properly.
        """
        test_corpus = ["titi tall", "toto tall", "tall"]
        tf_idf_vectorized = self.lxx_clusterer.tf_idf_vectorizer(test_corpus)
        # Check that last corpus value sums to 1
        self.assertEqual(tf_idf_vectorized.iloc[2].sum(), 1)

    def test_reduce(self):
        """
        Test that the PCA reducing works as expected.
        """
        test_corpus = ["titi tall", "toto tall", "tall"]
        tf_idf_vectorized = self.lxx_clusterer.tf_idf_vectorizer(test_corpus)
        test_dataframe = self.lxx_clusterer.reduce(
            tf_idf_vectorized, dimension=2)
        expected_reduced_dataframe = np.array([[6.08845099e-01, -2.60815602e-01],
                                              [-6.08845099e-01, -2.60815602e-01],
                                              [4.77971549e-17, 5.21631204e-01]])
        np.testing.assert_almost_equal(
            test_dataframe, expected_reduced_dataframe)

    def test_clusterize(self):
        """
        Tests that the clusterization method behaves as expected.
        """
        np.random.seed(5)
        df = pd.DataFrame(np.random.randint(
            0, 100, size=(3, 4)), columns=list('ABCD'))
        clusters = self.lxx_clusterer.clusterize(
            df, ["tutu", "titi", "toto"], n_cluster=2)
        np.testing.assert_equal(clusters.label.values, [
                                "tutu", "titi", "toto"])

    def test_pipeline(self):
        """
        Test the whole clustering pipeline.
        """
        result = self.lxx_clusterer.pipeline(
            {"Mt": "titi is small", "Lk": "titi is big"}, n_clusters=2)
        self.assertEqual(result["labels"], ["Mt", "Lk"])


if __name__ == "__main__":
    unittest.main()
