from graph import WebGraph
from utils.web import *
from ranking import *
import time
import warnings

warnings.filterwarnings("ignore")


class Crawler:
    def __init__(self, start_url, query, horizontal_depth=50):
        self.url = start_url
        self.visited_urls = []
        self.query = query
        self.graph = WebGraph(breadth=horizontal_depth)

    def traverse_urls(self, n_pages=10, parallel=True):
        if parallel:
            self.graph.transition_matrix = None
            data = self.graph.ParallelBFTraverse(self.url, self.query)
            # for k, v in data.items():
            #     print(k, v)
            filtered = {k: v for k, v in data.items() if v['sentences'][0] is not None}
            data.clear()
            data.update(filtered)

        else:
            data = self.graph.BFTraverse(self.url, self.query, n_pages)
            rank = self.rank_page()
            data = rank_pages(rank, data)

        return data

    def rank_page(self):
        trans_mat = self.graph.transition_matrix
        print(trans_mat)
        final_rank = pagerank(trans_mat)
        return final_rank


def main(url, query, json_out, html_out, hd, n_pages, parallel=True):
    c = Crawler(url, query=query, horizontal_depth=hd)
    start = time.time()
    info = c.traverse_urls(n_pages, parallel)
    to_json(info, json_out)
    to_html(json_out, html_out)
    end = time.time()
    print(f'Crawling in {end - start} seconds')


if __name__ == "__main__":
    # hyperparameters
    link = 'https://stackoverflow.com/questions/72575288/how-to-reduce-memory-size-of-pygame-array-to-allow-passing' \
           '-to-stable-baselines3 '
    q = 'robot'
    out_json = 'output/output.json'
    out_html = 'output/output.html'
    d = 2
    n_urls = 20
    p = True

    main(link, q, out_json, out_html, d, n_urls, p)
