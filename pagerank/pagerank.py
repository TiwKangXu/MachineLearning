import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_count = len(corpus)

    if len(corpus[page]) == 0:
        return dict.fromkeys(corpus, 1 / page_count)
    
    base_prob = (1 - damping_factor) / page_count
    ans = dict.fromkeys(corpus, base_prob)

    children = corpus[page]
    child_prob = damping_factor / len(children)
    for child in children:
        ans[child] += child_prob
    
    return ans
        
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ans = dict.fromkeys(corpus, 0)
    prob = 1 / n
    page_list = list(corpus.keys())
    curr = random.choice(page_list)
    ans[curr] += prob
    for i in range(n - 1):
        trans_dict = transition_model(corpus, curr, damping_factor)
        curr = random.choices(page_list, weights=list(trans_dict.values()))[0]
        ans[curr] += prob
    return ans


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    parent_page = {page: set() for page in corpus}

    for parent in corpus:
        if len(corpus[parent]) == 0:
            corpus[parent] = set(corpus.keys())
        for child in corpus[parent]:
            parent_page[child].add(parent)

    page_count = len(corpus)
    prev = dict.fromkeys(corpus, 1 / page_count)
    ans = dict.fromkeys(corpus, 1 / page_count)
    can_continue = True
    loop_count = 0
    while(can_continue):
        loop_count += 1
        can_continue = False
        for key in list(ans.keys()):
            parents = parent_page[key]
            sigma = sum(prev[parent] / len(corpus[parent]) for parent in parents)
            ans[key] = (1 - damping_factor) / page_count + damping_factor * sigma
            can_continue = can_continue or abs(ans[key] - prev[key]) >= 0.001
        prev = ans.copy()
    return ans

if __name__ == "__main__":
    main()
