
import argparse
from collections import defaultdict

########################################################################################################################
# Important Words Search
# Author: Barry Hykes Jr, bhykes@gmail.com
# version 1.0.0
########################################################################################################################


def word_search(text, k):
    """
    Search the text for words occurring at least k times and return array of words in order of occurrence in the original string
    At least one word meets the criteria
    the string is space separated
    :param text: text to search, str
    :param k: min number of occurrences, int
    """
    word_dict = defaultdict(int)
    words_array = []
    for word in text.split(' '):
        if not word_dict[word]:
            words_array.append(word)
        word_dict[word] += 1

    important_words = [word for word in words_array if word_dict[word] >= k]
    return important_words



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Important Words Search")
    parser.add_argument('-k', '--min_count', type=int, action="store", required=True, help="min occurrences of word")
    parser.add_argument('-s', '--search_string', type=str, action="store", required=True, help="phrase of words to search")
    parser_args = parser.parse_args()
    result = word_search(parser_args.search_string, parser_args.min_count)