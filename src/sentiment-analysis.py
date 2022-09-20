"""
Citation for VADER:
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import glob
import csv
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer

# # --- examples -------
# sentences = ["VADER is smart, handsome, and funny.",      # positive sentence example
#             "VADER is not smart, handsome, nor funny.",   # negation sentence example
#             "VADER is smart, handsome, and funny!",       # punctuation emphasis handled correctly (sentiment intensity adjusted)
#             "VADER is very smart, handsome, and funny.",  # booster words handled correctly (sentiment intensity adjusted)
#             "VADER is VERY SMART, handsome, and FUNNY.",  # emphasis for ALLCAPS handled
#             "VADER is VERY SMART, handsome, and FUNNY!!!",# combination of signals - VADER appropriately adjusts intensity
#             "VADER is VERY SMART, uber handsome, and FRIGGIN FUNNY!!!",# booster words & punctuation make this close to ceiling for score
#             "The book was good.",                                     # positive sentence
#             "The book was kind of good.",                 # qualified positive sentence is handled correctly (intensity adjusted)
#             "The plot was good, but the characters are uncompelling and the dialog is not great.", # mixed negation sentence
#             "At least it isn't a horrible book.",         # negated negative sentence with contraction
#             "Make sure you :) or :D today!",              # emoticons handled
#             "Today SUX!",                                 # negative slang with capitalization emphasis
#             "Today only kinda sux! But I'll get by, lol"  # mixed sentiment example with slang and constrastive conjunction "but"
#              ]

def dict_mean(dict_list):
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict

overall_scores = []
# path = "../../data/IBM-Debater-DR-EMNLP-2019.r4.full/full/speeches/trs.txt/*.txt"
path = "../../data/IBM-Debater-DR-ACL-2020.r5.no_wavs/no_wavs/trs.txt/*.txt"
for filename in glob.glob(path):
    with open(filename, 'r') as f:
        sentences = f.readlines()

    vs_scores = []
    analyzer = SentimentIntensityAnalyzer()
    for sentence in sentences:
        vs = analyzer.polarity_scores(sentence)
        vs_scores.append(vs)

    vs_mean = dict_mean(vs_scores)
    # print(vs_mean)
    overall_scores.append(vs_mean)

print("-----------------------------------------------------")
# write overall_scores (scores for each speech) to file
keys = overall_scores[0].keys()

with open('vader.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(overall_scores)

overall_vs = dict_mean(overall_scores)
print(overall_vs)