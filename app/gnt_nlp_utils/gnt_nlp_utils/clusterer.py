from typing import Dict, List
import pandas as pd
from scipy.sparse import data
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from gnt_nlp_utils import STOP_WORDS


class GNTClusterer:
    """
    Class to perform the clustering of gnt data, using the following workflow:

    - Remove stop words from text
    - Perform tf-idf transformation using sklearn
    - Perform PCA on transformed data
    - Run clustering algorithm on the reduced data
    - Perform 3D projection of results using PCA
    """

    @ staticmethod
    def clean(text_corpus: List[str], stop_words: List[str]) -> List[str]:
        """
        Given a list of strings, remove the words located in stop_words.
        """
        clean_corpus = []
        for text in text_corpus:
            clean_text = ""
            for word in text.split(" "):
                if word not in stop_words:
                    clean_text += " " + word
            clean_corpus.append(clean_text.strip())
        return clean_corpus

    @ staticmethod
    def tf_idf_vectorizer(text_corpus: List[str]) -> pd.DataFrame:
        """
        Compute the vectorization of the text.

        Args:
            text_corpus (list of strings): texts to perform the clustering on.

        Returns:
            A pandas dataframe containing the projected data.
        """
        tf_idf_vectorizer = TfidfVectorizer(norm="l2", use_idf=True)
        X = tf_idf_vectorizer.fit(text_corpus)
        return pd.DataFrame(X.transform(text_corpus).todense())

    @ staticmethod
    def reduce(dataframe: pd.DataFrame, dimension: int = 3) -> pd.DataFrame:
        """
        Reduce a pandas data frame using PCA transformation
        within dimension 'dimensions'.

        Args:
            dataframe (pd.DataFrame): dataframe to perform the
                reducing on.
            dimension (int): dimensions to perform the reduce
                on.

        Returns:
            A dataframe projected in a reduced dimension.
        """
        dimension = min(dimension, dataframe.shape[0])
        pca = PCA(n_components=dimension)
        return pca.fit_transform(dataframe)

    def clusterize(self, dataframe: pd.DataFrame, name: List[str], n_cluster: int = 10, ground_truth: List[str] = None) -> pd.DataFrame:
        """
        Perform clustering on an input dataframe using kmeans.

        Args:
            dataframe (pd.DataFrame): dataframe to perform the
                reducing on.
            name (Iterable): List of the values to use in final dataframe.
            n_cluster (int): Number of clusters to compute.

        Returns:
            A dataframe with the column labels and the corresponding index
            of labels.
        """
        n_cluster = min(n_cluster, dataframe.shape[0])
        kmeans = KMeans(n_clusters=n_cluster)
        kmeans.fit(dataframe)
        if not ground_truth:
            return pd.DataFrame(
                {"label": name, "cluster": kmeans.labels_})
        else:
            return pd.DataFrame(
                {"label": name,
                 "cluster": kmeans.labels_,
                 "ground_truth": ground_truth})

    def pipeline(self, text_corpus: List[str], n_clusters: int = 10, names: List[str] = [], ground_truth: List[str] = None):
        """
        Perform all the required transformation on the pipeline.

        Args:
            text_corpus (dict): Dictionary containing the books and
                their labels.
            n_clusters (int): Number of clusters to use.
        """
        if len(text_corpus) < 3:
            return {"projection":
                    {'x': [],
                     'y': [],
                     "z": []},
                    "clusters": [],
                    "labels": []}
        # Clean up corpus
        cleaned_corpus = self.clean(
            text_corpus, stop_words=STOP_WORDS)
        # Vectorized data
        vectorized_matrix = self.tf_idf_vectorizer(cleaned_corpus)
        # Reduce data before clustering
        reduced_vectorized_matrix = self.reduce(
            vectorized_matrix, dimension=15)
        # Cluster data
        clustered_data = self.clusterize(
            reduced_vectorized_matrix, name=names, n_cluster=n_clusters, ground_truth=ground_truth)
        # Perform final transformation
        data_3D = pd.DataFrame(self.reduce(
            reduced_vectorized_matrix, dimension=3))
        data_3D.columns = ["x", "y", "z"]
        # Send data back as a list of dictionary (per cluster)
        projections = []
        for cluster in pd.unique(clustered_data.ground_truth):
            sub_clustered_data = clustered_data[clustered_data.ground_truth == cluster]
            sub_3d_data = data_3D[clustered_data.ground_truth == cluster]
            projections.append(
                {"projection":
                 {'x': sub_3d_data.x.values.tolist(),
                  'y': sub_3d_data.y.values.tolist(),
                  "z": sub_3d_data.z.values.tolist()},
                 "clusters": sub_clustered_data.cluster.values.tolist(),
                 "labels": sub_clustered_data.label.values.tolist(),
                 "ground_truth": sub_clustered_data.ground_truth.values.tolist(),
                 "markers": {"color": "blue"}}
            )
        return projections
