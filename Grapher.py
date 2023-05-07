import math
from typing import *
import tkinter as tk
from tkinter import simpledialog


class Node:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Edge:
    def __init__(self, src, dst, gain):
        self.src = src
        self.dst = dst
        self.gain = gain

class Graph:
    def __init__(self, num_nodes):
        self.nodes = []
        self.edges = []
        self.adj_list: Dict[str, Dict[str, Dict[str, str]]] = {}
        start = 135
        interval = 1650 / (num_nodes - 1)
        for i in range(num_nodes):
            self.adj_list[str(i + 1)] = {}
            self.nodes.append(Node(i + 1, start + i * interval, 500))

    def add_edge(self, src_id, dst_id, gain):
        src_node = self.get_node(src_id)
        dst_node = self.get_node(dst_id)
        self.adj_list[str(src_id)][str(dst_id)] = {'weight': gain}
        self.edges.append(Edge(src_node, dst_node, gain))

    def get_node(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return None


class SignalFlowGraph:
    graph: Graph = None

    def __init__(self, master, num_nodes):
        self.selected_node = None
        self.graph = Graph(num_nodes)
        self.canvas = tk.Canvas(master, width=1920, height=1080)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_graph()

    def draw_graph(self):
        for edge in self.graph.edges:
            x1, y1 = edge.src.x, edge.src.y
            x2, y2 = edge.dst.x, edge.dst.y
            gain = edge.gain
            dist = (x2 - x1) / 3.5
            if dist > 0:
                self.draw_forward_edge(x1, y1, x2, y2, gain, dist)
            elif dist < 0:
                self.draw_backward_edge(x1, y1, x2, y2, gain, dist)
            else:
                self.draw_self_edge(x1, y1, gain)
        for node in self.graph.nodes:
            self.canvas.create_oval(node.x - 40, node.y - 40, node.x + 40, node.y + 40, fill="white", width=4)
            self.canvas.create_text(node.x, node.y, text=node.id, font=("Helvetica", 18))

    def draw_forward_edge(self, x1, y1, x2, y2, gain, dist):
        self.canvas.create_arc(x1, y1 - dist, x2, y2 + dist, start=0, extent=180,
                               width=2, style='arc', outline='black')
        self.draw_arrow((x1 + x2) / 2, (y1 - dist), 10, gain)

    def draw_backward_edge(self, x1, y1, x2, y2, gain, dist):
        self.canvas.create_arc(x1, y1 - dist, x2, y2 + dist, start=180, extent=180,
                               width=2, style='arc', outline='black')
        self.draw_arrow((x1 + x2) / 2, (y1 - dist), -10, gain)

    def draw_self_edge(self, x, y, gain):
        dist = 75
        self.canvas.create_arc(x - dist / 3, y - dist / 3, x + dist / 3, y - dist, start=270, extent=340,
                               width=2, style='arc', outline='black')
        self.draw_arrow(x, y - dist, 10, gain)

    def draw_arrow(self, x, y, r, g):
        x1 = x + r
        y1 = y
        x2 = x - r / 2
        y2 = y + r * math.sqrt(3) / 2
        x3 = x2
        y3 = y - r * math.sqrt(3) / 2
        self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="white", width=2, outline='black')
        self.canvas.create_text(x, y + 2 * r, text=g, font=("default", 13))

    def on_click(self, event):
        node_id = self.get_node_id(event.x, event.y)
        if node_id is not None:
            if self.selected_node is None:
                self.selected_node = node_id
            else:
                gain = simpledialog.askstring(title="Gain", prompt="Please enter the gain:")
                if gain is not None and gain != "":
                    found = False
                    for edge in self.graph.edges:
                        if edge.src.id == self.selected_node and edge.dst.id == node_id:
                            try:
                                edge.gain = str(float(edge.gain) + float(gain)).replace(".0", "")
                                self.graph.adj_list[str(edge.src.id)][str(edge.dst.id)] = {'weight': edge.gain}
                            except ValueError:
                                edge.gain += ' + ' + gain
                                self.graph.adj_list[str(edge.src.id)][str(edge.dst.id)] = {'weight': edge.gain}
                            found = True
                            break
                    if not found:
                        self.graph.add_edge(self.selected_node, node_id, gain)
                self.canvas.delete("all")
                self.selected_node = None
                self.draw_graph()

    def get_node_id(self, x, y):
        for node in self.graph.nodes:
            if (x - node.x) ** 2 + (y - node.y) ** 2 < 1600:
                return node.id
        if self.selected_node is not None:
            self.selected_node = None
        return None


def run(num_nodes):
    root = tk.Tk(className=" Signal Flow Graph")
    graph = SignalFlowGraph(root, num_nodes)
    root.mainloop()
    return graph