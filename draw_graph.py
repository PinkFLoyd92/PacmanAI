import threading
import time
import pygame
mport networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class myThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.file = open('data.txt', 'r')

    def run(self):
        pass

    def countLines(self):
        total_lines = 0
        for line in self.file:
            total_lines += 1
        return total_lines


    def update_image(self):
        total_lines = self.countLines()
        while 1:
            if(self.countLines()>total_lines):
                self.updateGraph()

    def updateGraph(self):
        pass
