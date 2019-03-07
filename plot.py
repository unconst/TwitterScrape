import requests
from bs4 import BeautifulSoup
from re import findall
import logging as logme
import random
import time
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import os.path
from concurrent.futures import ThreadPoolExecutor
import threading


def plot_graph(graph):
    options = {
        'node_color': 'black',
        'node_size': 1,
        'line_color': 'grey',
        'linewidths': 0,
        'width': 0.1,
    }
    nx.draw(graph, **options)
    plt.show()

if __name__ == "__main__":
    if not os.path.isfile('twitter.gpickle'):
        graph = nx.Graph()
        graph.add_node('unconst1')
        nx.write_gpickle(graph, 'twitter.gpickle')
        del graph

    graph = nx.read_gpickle("twitter.gpickle")
    plot_graph(graph)
    nx.write_gpickle(graph, 'twitter.gpickle')

