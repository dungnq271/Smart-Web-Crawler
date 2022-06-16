import concurrent.futures
import requests
import threading
import time
from bs4 import BeautifulSoup


thread_local = threading.local()


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def download_site(url):
    urls = []
    session = get_session()
    with session.get(url) as response:
        soup = BeautifulSoup(response.content, "html.parser")
        print(f"Read {len(response.content)} from {url}")
        for a in soup.find_all('a'):
            urls.append(a.get('href'))
    return urls


def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        found = executor.map(download_site, sites)
    return found


if __name__ == "__main__":
    sites = [
                "https://stackoverflow.com/",
                "https://pytorch.org/",
            ] * 5
    start_time = time.time()
    f = download_all_sites(sites)
    for i in f:
        print(i)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
