from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin


def open_url(url):
    try:
        page = urlopen(url)
    except Exception as e:
        return None
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_sentence(page, query):
    query = query.lower()

    if page is not None:
        doc = page.get_text().lower()
        # if query in doc or query in title:
        # doc = ' '.join(doc.split())
        # sentences = doc.split('.')
        sentences = doc.split('\n')
        for s in sentences:
            s = s.strip()
            if query in s:
                yield s


def get_links_url(url):
    urls = []
    soup = open_url(url)
    for a in soup.find_all('a'):
        path = a.get('href')
        if path and path.startswith('/'):
            path = urljoin(url, path)
        urls.append(path)
    return urls
