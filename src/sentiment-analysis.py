"""
Citation for VADER:
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import glob
import csv
import os
    #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
    #from vaderSentiment import SentimentIntensityAnalyzer


def dict_mean(dict_list):
    mean_dict = {}
    for key in dict_list[0].keys():
        mean_dict[key] = sum(d[key] for d in dict_list) / len(dict_list)
    return mean_dict

def main():
    overall_scores = []
    relative_dir_path = input("Enter relative path to directory containing transcripts\n")
    # path = "../../data/IBM-Debater-DR-EMNLP-2019.r4.full/full/speeches/trs.txt/*.txt"
    # path = os.path.join(os.path.dirname(__file__), os.pardir, "dataset", "textFiles", "*.txt")
    path = os.path.join(os.path.abspath(relative_dir_path), "*.txt")
    for filename in glob.glob(path):
        with open(filename, 'r') as f:
            sentences = f.readlines()

        vs_scores: list[dict[str, float]] = []
        analyzer: SentimentIntensityAnalyzer = SentimentIntensityAnalyzer()
        for sentence in sentences:
            vs: dict[str, float] = analyzer.polarity_scores(sentence)
            vs_scores.append(vs)

        vs_mean = dict_mean(vs_scores)
        vs_mean['filename'] = os.path.basename(filename)
        # print(vs_mean)
        overall_scores.append(vs_mean)

    print("-----------------------------------------------------")
    # write overall_scores (scores for each speech) to file
    # keys = overall_scores[0].keys()
    keys = ['filename','pos', 'neg', 'neu', 'compound']

    with open('vader.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(overall_scores)

    # overall_vs = dict_mean(overall_scores)
    # print(overall_vs)

if __name__ == "__main__":
    main()