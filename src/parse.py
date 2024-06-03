from langchain_community.document_loaders import UnstructuredHTMLLoader
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import os
from src.utils import (generate_name_html, return_splitter, return_vector_store)

BASE_URL = """https://u.ae/en/information-and-services"""


def parse(path):
    loader = UnstructuredHTMLLoader(path)
    document = loader.load()
    return document


def pre_process(document):
    splitter = return_splitter()
    documents = splitter.split_documents(document)
    print(documents[0].page_content)
    vector_store = return_vector_store()
    vector_store.add_documents(documents)


class Scrape:
    def __init__(self):
        self.html = None
        self.links = []
        self.path = "./htmls"

        path_to_create = Path(self.path)
        path_to_create.mkdir(parents=True, exist_ok=True)

    def fetch_html(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.html = response.content
            path = self.save_html(html=self.html, url=url)
            return path
        except Exception as e:
            print(e)

    def save_html(self, html, url):
        path = os.path.join(self.path, f"{generate_name_html(url)}.html".replace("/",''))
        with open(path, 'w', encoding='utf-8') as file:
            file.write(html.decode('utf-8'))
        return path

    def extract_links_from_html(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        div = soup.find('div', class_='row ui-filter-items row-flex')
        links = []
        if div:
            a_tags = div.find_all('a')
            for a in a_tags:
                href = a.get('href')
                links.append({'href': urljoin(BASE_URL, href)})
        self.links = links
        print(links)

    def child_htmls(self):
        for i in range(len(self.links)):
            path = self.fetch_html(self.links[i]["href"])
            print(self.links[i]["href"])
            document = parse(path)
            pre_process(document)
