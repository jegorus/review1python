from random import randrange
# https://www.ef.com/wwen/english-resources/english-vocabulary/top-1000-words/


class VocabularyClass:
    __vocabulary = None
    __vocabulary_length = None
    __initial_text_file = 'Vocabulary.txt'

    def __init__(self):
        with open(self.__initial_text_file, 'r') as vocabulary_file:
            vocabulary_string = vocabulary_file.read()
        self.__vocabulary = vocabulary_string.splitlines()
        self.__vocabulary_length = len(self.__vocabulary)

    def get_random_word(self):
        rand_voc_number = randrange(self.__vocabulary_length)
        return self.__vocabulary[rand_voc_number]
