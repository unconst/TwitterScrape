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

def update(graph, args):

    start = time.time()
    mutex = threading.Lock()

    def followers(user):
        base_url = f"https://mobile.twitter.com/{user}/following?lang=en"
        cursor_index = None
        while True:
            url = base_url + (" " if not cursor_index else f"&cursor={cursor_index}")
            print (url)

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

            try:
                cursor_index = findall(r'cursor=(.*?)">', str(cursor))[0]
            except IndexError:
                break

    with ThreadPoolExecutor(max_workers=3) as executor:
        while (time.time() - start) > args.duration:
            user = random.choice(list(graph.nodes()))
            future = executor.submit(followers, (user))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scape Twitter into nx Graph.')
    parser.add_argument('--duration', type=int, default=100,  help='scrape duration.')
    args = parser.parse_args()

    if not os.path.isfile('twitter.gpickle'):
        graph = nx.Graph()
        graph.add_node('unconst1')
        nx.write_gpickle(graph, 'twitter.gpickle')
        del graph

    graph = nx.read_gpickle("twitter.gpickle")
    update(graph, args)
    nx.write_gpickle(graph, 'twitter.gpickle')

