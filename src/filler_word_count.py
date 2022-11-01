# adapted from MRJob example
from mrjob.job import MRJob
import re

class WordCount(MRJob): #inheritance
    
    FILES = ['input-words.txt']

    def mapper_init(self):
        stop_words_path = 'input-words.txt'
        with open(stop_words_path) as f:
            self.input_words = set(line.strip() for line in f)
    
    def mapper(self, _, line):
        line = line.lower()
        # substitute group separators and dashes with spaces ('--')
        group_seperator_regex = re.compile('--')
        line = group_seperator_regex.sub(' ', line)
        # filter out all characters except alphabetical and apostrophes
        word_regex = re.compile(r"[a-z]+'?[a-z]+")
        line = word_regex.findall(line)
        for word in line:
            if word in self.input_words:
                yield(word, 1)

    """the combiner offers no advantage when using the local runner, but we've included it 
    to speed up execution when using a Hadoop runner
    """
    def combiner(self, word, counts):
        yield(word, sum(counts))


    def reducer(self, word, counts):
        yield(word, sum(counts))

  
if __name__ == '__main__':
    WordCount.run()

"""
To run this file as a standalone:
python3 WordCount.py -r local <input filepath> > <output filepath>
python3 WordCount.py -r local ../input-files/small.txt > output-wordcount.txt
"""