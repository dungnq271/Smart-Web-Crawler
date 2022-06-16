from collections import defaultdict
from utils.utils import *
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import logging


class WebGraph:
    def __init__(self, breadth=2):
        self.transition_matrix = None
        self.visited = defaultdict(dict)
        self.br = breadth
        format = "%(message)s"
        logging.basicConfig(format=format, level=logging.INFO)

    def add_info(self, p, t, u, query):
        print(t)
        self.visited[t]['link'] = u
        self.visited[t]['sentences'] = []
        for sentence in get_sentence(p, query):
            self.visited[t]['sentences'].append(sentence)
        # if query not found in page
        if len(self.visited[t]['sentences']) == 0:
            self.visited[t]['sentences'].append(None)

    def traverse_each_link(self, u, queue, query):
        page = open_url(u)
        # if url is valid
        if page is not None:
            title = page.title.string
            # if url not visited yet
            if len(self.visited[title]) == 0:
                # append to queue and append url with sentences to list visited
                queue.append(u)
                self.add_info(page, title, u, query)
        return self.visited

    def ParallelBFTraverse(self, s, query):
        # Append start vertex to queue
        queue = []
        queue.append(s)
        b = 0

        while queue:
            if b >= self.br:
                break
            s = queue.pop(0)
            page = open_url(s)
            if page is not None:
                name = page.title.string
                self.add_info(page, name, s, query)

            hrefs = get_links_url(s)
            logging.info(f'The page above has {len(hrefs)} links to other pages')

            n_threads = 12
            with ThreadPoolExecutor(n_threads) as executor:
                _ = [executor.submit(self.traverse_each_link, url, queue, query)
                           for url in hrefs]

            b += 1
        return self.visited

    def BFTraverse(self, s, query, n_pages):
        self.transition_matrix = np.zeros((n_pages, n_pages))

        # Append start vertex to queue
        queue = []
        queue.append(s)
        b = 0

        while queue:
            s = queue.pop(0)
            page = open_url(s)
            if page is not None:
                name = page.title.string
                self.add_info(page, name, s, query)

            hrefs = get_links_url(s)
            print(f'The page above has {len(hrefs)} links to other pages')

            for u in hrefs:
                page = open_url(u)
                # if url is valid
                if page is not None and page.title is not None:
                    title = page.title.string
                    # if url not visited yet
                    if len(self.visited[title]) == 0:
                        # append to queue and append url with sentences to list visited
                        queue.append(u)
                        self.add_info(page, title, u, query)

                    list_urls = list(self.visited.keys())
                    if len(list_urls) >= n_pages:
                        return self.visited

                    self.transition_matrix[list_urls.index(name), list_urls.index(title)] += 1

        return self.visited
