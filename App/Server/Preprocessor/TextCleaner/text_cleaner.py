import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from autocorrect import Speller
from typing import List


def remove_stop_words(tokens: List[str], language="english") -> List[str]:
    """
    Gets the a list of tokens that not includes stop words

    Args:
        tokens (List[str]): List of tokens
        language (str): Language to use

    Returns:
        tokens (List[str]): List of tokens that not includes stop words
    """
    return [word for word in tokens if word not in stopwords.words(language)]


def get_base_words(tokens: List[str], stem_lang="english", spell_lang="en") -> List[str]:
    """
    Gets a list of stemmed tokens (base word for each token)

    Args:
        tokens (List[str]): List of tokens
        stem_lang (str): Language to use on the stem process
        spell_lang (str): Language to use on the spell check process

    Returns:
        stemmed_tokens (List[str]): List of stemmed tokens
    """
    stemmer = SnowballStemmer(stem_lang)
    spell = Speller(lang=spell_lang)
    return [spell(stemmer.stem(word))
            for word in tokens]


def add_space_between_number_and_chars(word: str) -> str:
    """
    Adds space between char and number (and vice versa) if they are together.
    i.e. Adds space between number and chars 3pcs ... 3 pcs

    Args:
        word (str): word to apply the change

    Returns:
        new_word (str): New word with space between char and number (and vice cversa) if they are together
    """
    return re.sub(r'(\d+(\.\d+)?)', r' \1 ', word)


def remove_non_alphabetic_chars(word: str) -> str:
    """
    Gets a new string with only alphabetic characters

    Args:
        word (str): Word to apply the change

    Returns:
        new_word (str): String with only alphabetic characters
    """
    return re.sub('[^A-Za-z]', ' ', word)


def remove_unwanted_characters(word: str) -> str:
    """
    Replaces abbreviations in a text and removes unwanted characters. i.e: 'pc' -> 'piece'

    Args:
        word (str): Word to apply the change

    Returns:
        new_word (str): String with no abbreviations
    """
    word = word.replace('*', '').replace('+', 'and')
    return re.sub('pc', 'piece', word)


def get_tokens_word(word: str, language="english") -> List[str]:
    """
    Gets the a list of tokes given a word

    Args:
        word (str): Word to tokenize
        language (str): Language to use

    Returns:
        tokens (List[str]): List of tokens obtained from the word
    """
    return word_tokenize(word, language)
