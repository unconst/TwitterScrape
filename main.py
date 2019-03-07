import requests
from bs4 import BeautifulSoup
from re import findall
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os.path
from concurrent.futures import ThreadPoolExecutor
import threading
import logging

def log(string):
    logging.info(str(string))

def update(graph, args):

    log('start...')
    start = time.time()
    mutex = threading.Lock()

    def followers(user):
        base_url = f"https://mobile.twitter.com/{user}/following?lang=en"
        cursor_index = None
        while True:
            url = base_url + (" " if not cursor_index else f"&cursor={cursor_index}")
            log(url)

            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            follow = soup.find_all("td", "info fifty screenname")
            cursor = soup.find_all("div", "w-button-more")

            edges = []
            for next_user in follow:
                next_username = next_user.find("a")["name"]
                edges.append((user, next_username))

            with mutex:
                graph.add_edges_from(edges)
                nx.write_gpickle(graph, 'twitter.gpickle')


            try:
                cursor_index = findall(r'cursor=(.*?)">', str(cursor))[0]
            except IndexError:
                break


    while (time.time() - start) < args.duration:
        with ThreadPoolExecutor(max_workers=3) as executor:
            for _ in range(3):
                user = random.choice(list(graph.nodes()))
                future = executor.submit(followers, (user))
                log(user)

    log('stop.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scape Twitter into nx Graph.')
    parser.add_argument('--duration', type=int, default=100,  help='scrape duration.')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    if not os.path.isfile('twitter.gpickle'):
        log('Creating new twitter.gpickle file')
        graph = nx.Graph()
        graph.add_node('unconst1')
        nx.write_gpickle(graph, 'twitter.gpickle')
        del graph

    log('loading twitter.gpickle')
    graph = nx.read_gpickle("twitter.gpickle")
    update(graph, args)

