from pagerank import *

corpus = {
    "1.html": {"2.html", "3.html"}, 
    "2.html": {"3.html"}, 
    "3.html": {"2.html"},
    # "4.html": {}
    }
page = "1.html"
damping_factor = 0.85


# print(transition_model(corpus, page, damping_factor))
# print(sample_pagerank(corpus, damping_factor, 10 ** 5))
# print(corpus.key)

print(iterate_pagerank(corpus, 0.85))