# Load nltk 
import nltk
nltk.download('punkt')
import numpy as np
from matplotlib import pyplot as plt

papers = {
    'Madison': [10, 14, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
    'Hamilton': [1, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 21, 22, 23, 24, 
                 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 59, 60,
                 61, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 
                 78, 79, 80, 81, 82, 83, 84, 85],
    'Jay': [2, 3, 4, 5],
    'Shared': [18, 19, 20],
    'Disputed': [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 62, 63],
    'TestCase': [64]
}
# A function that compiles all of the text files associated with a single author into a single string
def read_files_into_string(filenames):
    strings = []
    for filename in filenames:
        with open(f'../../a_DataAquisition/stylometry-federalist/data/federalist_{filename}.txt') as f:
            strings.append(f.read())
    return '\n'.join(strings)
	
# Make a dictionary out of the authors' corpora
federalist_by_author = {}  
for author, files in papers.items():
    federalist_by_author[author] = read_files_into_string(files)
	
for author in papers:
    print(federalist_by_author[author][:100])
# Compare the disputed papers to those written by everyone, 
# including the shared ones. 
authors = ("Hamilton", "Madison", "Disputed", "Jay", "Shared")

# Transform the authors' corpora into lists of word tokens
federalist_by_author_tokens = {}
federalist_by_author_length_distributions = {}
for author in authors:
    tokens = nltk.word_tokenize(federalist_by_author[author])
    
    # Filter out punctuation
    federalist_by_author_tokens[author] = ([token for token in tokens 
                                            if any(c.isalpha() for c in token)])
   
    # Get a distribution of token lengths
    token_lengths = [len(token) for token in federalist_by_author_tokens[author]]
    federalist_by_author_length_distributions[author] = nltk.FreqDist(token_lengths)
    federalist_by_author_length_distributions[author].plot(15,title=author)
	
# Who are the authors we are analyzing?
authors = ("Hamilton", "Madison")

# Lowercase the tokens so that the same word, capitalized or not, 
# counts as one word
for author in authors:
    federalist_by_author_tokens[author] = (
        [token.lower() for token in federalist_by_author_tokens[author]])
federalist_by_author_tokens["Disputed"] = (
    [token.lower() for token in federalist_by_author_tokens["Disputed"]])

# Calculate chisquared for each of the two candidate authors
for author in authors:
   
    # First, build a joint corpus and identify the 500 most frequent words in it
    joint_corpus = (federalist_by_author_tokens[author] + 
                    federalist_by_author_tokens["Disputed"])
    joint_freq_dist = nltk.FreqDist(joint_corpus)
    most_common = list(joint_freq_dist.most_common(500))

    # What proportion of the joint corpus is made up 
    # of the candidate author's tokens?
    author_share = (len(federalist_by_author_tokens[author]) 
                    / len(joint_corpus))
    
    # Now, let's look at the 500 most common words in the candidate 
    # author's corpus and compare the number of times they can be observed 
    # to what would be expected if the author's papers 
    # and the Disputed papers were both random samples from the same distribution.
    chisquared = 0
    for word,joint_count in most_common:
        
        # How often do we really see this common word?
        author_count = federalist_by_author_tokens[author].count(word)
        disputed_count = federalist_by_author_tokens["Disputed"].count(word)
        
        # How often should we see it?
        expected_author_count = joint_count * author_share
        expected_disputed_count = joint_count * (1-author_share)
        
        # Add the word's contribution to the chi-squared statistic
        chisquared += ((author_count-expected_author_count) * 
                       (author_count-expected_author_count) / 
                       expected_author_count)
                    
        chisquared += ((disputed_count-expected_disputed_count) *
                       (disputed_count-expected_disputed_count) 
                       / expected_disputed_count)
        
    print("The Chi-squared statistic for candidate", author, "is", chisquared)