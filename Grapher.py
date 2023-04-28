import networkx as nx
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets

from GainIP import GainIP


class Grapher:
    G = nx.DiGraph()
    from_node = None
    to_node = None
    gainWindow = GainIP()
    noNodes = 0

    @classmethod
    def add_node(cls, event):

        if event.button == 1 and cls.noNodes > 0:  # left mouse button
            x, y = event.xdata, event.ydata
            node = len(cls.G)
            cls.G.add_node(node, pos=(x, y))
            cls.noNodes = cls.noNodes - 1
            cls.draw_graph()

        if event.button == 3:  # right mouse button
            if cls.from_node is None:
                cls.from_node = cls.get_closest_node(event.xdata, event.ydata)
                if cls.from_node is not None:
                    nx.draw_networkx_nodes(cls.G, pos=nx.get_node_attributes(cls.G, 'pos'), node_color='red',
                                           nodelist=[cls.from_node])
                    plt.draw()

            elif cls.to_node is None:
                cls.to_node = cls.get_closest_node(event.xdata, event.ydata)
                if cls.to_node is not None:
                    if cls.G.has_edge(cls.from_node, cls.to_node):
                        cls.set_weight()
                    else:
                        cls.G.add_edge(cls.from_node, cls.to_node)
                        cls.draw_graph()
                    cls.from_node = None
                    cls.to_node = None

    # @classmethod
    # def input_weight(cls, fromNode, toNode):
        # cls.window = QtWidgets.QDialog()
        # cls.gainWindow.setupUi(cls.window, fromNode, toNode)
        # cls.window.show()
        # cls.gainWindow.addGain.clicked.connect(cls.set_weight)

    @classmethod
    def set_weight(cls):
        # weight = int(cls.gainWindow.gainIP.text())
        weight = input(f"Enter gain from node {cls.from_node} to node {cls.to_node}: ")
        cls.G[cls.from_node][cls.to_node]['weight'] = weight
        cls.draw_graph()

    @classmethod
    def get_closest_node(cls, x, y):
        pos = nx.get_node_attributes(cls.G, 'pos')
        min_dist = float('inf')
        closest_node = None
        for node, (nx_, ny_) in pos.items():
            dist = (nx_ - x) ** 2 + (ny_ - y) ** 2
            if dist < min_dist:
                min_dist = dist
                closest_node = node
        if min_dist <= 0.01:
            return closest_node
        else:
            return None

    @classmethod
    def draw_graph(cls):
        pos = nx.get_node_attributes(cls.G, 'pos')
        nx.draw_networkx(cls.G, pos=pos)
        edge_labels = nx.get_edge_attributes(cls.G, 'weight')
        if edge_labels:
            nx.draw_networkx_edge_labels(cls.G, pos=pos, edge_labels=edge_labels)
        plt.draw()

    @classmethod
    def clear_graph(cls, event):
        cls.G.clear()
        cls.from_node = None
        cls.to_node = None
        cls.draw_graph()


# Create a Matplotlib figure and axes
fig, ax = plt.subplots()

# Set the limits of the axes
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Register the event handler function for mouse clicks
cid = fig.canvas.mpl_connect('button_press_event', Grapher.add_node)

# Register the event handler function for closing the window
cid_close = fig.canvas.mpl_connect('close_event', Grapher.clear_graph)

# Draw the initial empty graph
Grapher.draw_graph()

plt.show()
