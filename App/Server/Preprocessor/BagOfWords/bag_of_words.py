from typing import List, Dict, Set
import nltk
import pandas
from collections import defaultdict
from termcolor import cprint
from sklearn.feature_extraction.text import CountVectorizer
from App.Server.Preprocessor.TextCleaner import text_cleaner

nltk.download('punkt')
nltk.download('stopwords')

COLOR = "blue"


class BagOfWords:
    """
    BagOfWords class to extract features form raw text

    Args:
        col_names_features (List[str]): Data frame columns names to extract from the raw sample_data
        max_features (int): Maximum possible number of features to extract

    Attributes:
        col_names_features (List[str]): Data frame columns names to extract from the raw sample_data
        max_features (int): Maximum possible number of features to extract
        __cleaned_text_data (List[str]): Corpus of cleaned texts to get the features and vectors
        __stemmed_words_dict (Dict[str, Set]): All the stemmed words as keys and their original words
        __stemmed_words_features_dict (Dict[str, Set]): Stemmed words (only the features) as keys and their original words
        __bow_features (List[str]): The N-most frequent words on the corpus
        __bow_vectors (List[List[int]]): Vector for each cleaned text
        __vectorizer (CountVectorizer): CountVectorizer object used to transform cleaned text to vector representation
    """

    def __init__(self, col_names_features: List[str], max_features: int):
        self.col_names_features = col_names_features
        self.max_features = max_features
        self.__cleaned_text_data: List[str] = []
        self.__stemmed_words_dict: Dict[str, Set] = defaultdict(set)
        self.__stemmed_words_features_dict: Dict[str, Set] = dict()
        self.__bow_features: List[str] = []
        self.__bow_vectors: List[List[int]] = []
        self.__vectorizer: CountVectorizer = None

    def build(self, df: pandas.DataFrame, filter_col_name: str) -> None:
        """
        Extracts the text from a sample_data frame and creates the bow features and vectors from the whole corpus

        Args:
            df (pandas.DataFrame): Data frame to extract the text
            filter_col_name (str): Column name to filter sample_data

        Returns:
            None
        """
        # Get clean stemmed sample_data
        cprint(f"Cleaning and stemming the sample_data...", COLOR)
        for col_name in self.col_names_features:
            filtered_data = df.loc[df[filter_col_name], col_name]
            diet_texts = filtered_data.astype(str).values.tolist()
            self.__cleaned_text_data += self.stem_raw_text_list(
                diet_texts, feed_stem_dict=True)
        # Get Bag of Words
        cprint(f"Building the BoW model...", COLOR)
        self.__vectorizer = CountVectorizer(max_features=self.max_features)
        self.__bow_vectors = self.__vectorizer.fit_transform(self.__cleaned_text_data).toarray()
        self.__bow_features = self.__vectorizer.get_feature_names()

        # Keep only the features names in the dict
        cprint(f"Keeping the stemmed words of the features...", COLOR)
        for feature in self.__bow_features:
            self.__stemmed_words_features_dict[feature] = self.__stemmed_words_dict[feature]

    def get_stemmed_words_dict(self) -> Dict[str, Set]:
        """
        Gets all the stemmed words as keys and their original words

        Args:
            None

        Returns:
            stem_words_dict (Dict[str, Set]): All the stemmed words as keys and their original words
        """
        return self.__stemmed_words_dict

    def get_stemmed_words_features_dict(self) -> Dict[str, Set]:
        """
        Gets the stemmed features as keys and their original words as a values

        Args:
            None

        Returns:
            Dict[str, Set]: Stemmed features as keys and their original word
        """
        return self.__stemmed_words_features_dict

    def get_features(self) -> List[str]:
        """
        Gets the the N-most frequent words on the corpus

        Args:
            None

        Returns:
            bow_features (List[str]): The N-most frequent words on the corpus
        """
        return self.__bow_features

    def get_vectors(self) -> List[List[int]]:
        """
        Gets the vectors obtained after fit and transform the corpus to BoW

        Args:
            None

        Returns:
            bow_vectors (List[List[int]]): Vector for each cleaned text used in the corpus
        """
        return self.__bow_vectors

    def get_vectorizer(self) -> CountVectorizer:
        """
        Gets the CountVectorizer object used to transform cleaned text to vector representation

        Args:
            None

        Returns:
            vectorizer (CountVectorizer): CountVectorizer object used to transform cleaned text to vector representation
        """
        return self.__vectorizer

    def stem_raw_text_list(self, text_list: List[str], feed_stem_dict: bool = False) -> List[str]:
        """
        Transforms a list of raw text into a list of clean stemmed text for vectorize

        Args:
            text_list (List[str]): List of raw text
            feed_stem_dict (bool): Flag to feed the stemmed dictionary

        Returns:
            stem_text_list (List[str]): List of stemmed text for vectorize
        """
        clean_text_list: List[str] = []
        for text in text_list:
            # Preprocessor
            text = text.strip().lower()
            text = text_cleaner.add_space_between_number_and_chars(text)
            text = text_cleaner.remove_unwanted_characters(text)
            text = text_cleaner.remove_non_alphabetic_chars(text)
            # Stemming
            tokens = text_cleaner.get_tokens_word(text)
            clean_tokens = text_cleaner.remove_stop_words(tokens)
            stem_clean_tokens = text_cleaner.get_base_words(clean_tokens)

            if feed_stem_dict:
                for token, stemmed_token in zip(clean_tokens, stem_clean_tokens):
                    self.__stemmed_words_dict[stemmed_token].add(token)

            final_text = " ".join(stem_clean_tokens)
            clean_text_list.append(final_text)
        return clean_text_list

    def vectorize_raw_data(self, raw_texts: List[str], print_result: bool = False) -> List[List[int]]:
        """
        Vectorizes a list of raw text

        Args:
            raw_texts (List[str]): List of raw text
            print_result (bool): Flag to print the results

        Returns:
            vectors (List[List[int]]): Vectors for each input list row
        """
        clean_texts = self.stem_raw_text_list(raw_texts)
        vectors = self.__vectorizer.transform(clean_texts).toarray()
        if print_result:
            cprint(f"\nBoW Features:\n{self.__bow_features}", 'blue')
            for idx, texts in enumerate(zip(raw_texts, clean_texts)):
                raw_text, clean_text = texts
                vector = vectors[idx]
                cprint(f'Raw Text: "{raw_text}"', 'magenta')
                cprint(f'Clean Text: "{clean_text}"', 'cyan')
                print(f'{vector}\n')
        return vectors

    def print_results(self) -> None:
        cprint(f'{self.__cleaned_text_data}\n Len: {len(self.__cleaned_text_data)}\n', 'green')
        cprint(f'{self.__stemmed_words_features_dict}\n Len: {len(self.__stemmed_words_features_dict)}\n', 'yellow')
        cprint(self.__bow_features, 'blue')
        cprint(self.__bow_vectors, 'blue')
        cprint(f'Size: {len(self.__bow_vectors)} * {len(self.__bow_vectors[0])}', 'blue')
