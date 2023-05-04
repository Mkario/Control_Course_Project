import networkx as nx
import matplotlib.pyplot as plt
import sys

from GainIP import GainIP
from MainWindow import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QDialog, QLabel


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Input Dialog')
        self.label = QLabel('Enter Gain:', self)
        self.line_edit = QLineEdit(self)
        self.ok_button = QPushButton('OK', self)
        self.cancel_button = QPushButton('Cancel', self)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def get_text(self):
        text, ok = self.line_edit.text(), self.result() == QDialog.Accepted
        return text if ok and text != '' else None

class Grapher:
    GDraw = nx.DiGraph()
    G = nx.DiGraph()
    input_dialogue = InputDialog()
    from_node = None
    to_node = None
    gainWindow = GainIP()
    noNodes = 0
    weight = 0

    @classmethod
    def add_node(cls, event):

        if event.button == 1 and cls.noNodes > 0:  # left mouse button
            x, y = event.xdata, event.ydata
            node = len(cls.GDraw)
            cls.GDraw.add_node(node, pos=(x, y))
            cls.G.add_node(node, pos=(x, y))
            cls.noNodes = cls.noNodes - 1
            cls.draw_graph()

        if event.button == 3:  # right mouse button
            if cls.from_node is None:
                cls.from_node = cls.get_closest_node(event.xdata, event.ydata)
                if cls.from_node is not None:
                    nx.draw_networkx_nodes(cls.GDraw, pos=nx.get_node_attributes(cls.GDraw, 'pos'), node_color='red',
                                           nodelist=[cls.from_node])
                    print("from node is: ",cls.from_node)
                    plt.draw()

            elif cls.to_node is None:
                cls.to_node = cls.get_closest_node(event.xdata, event.ydata)
                if cls.to_node is not None:
                    print("to node is: ",cls.to_node)
                    if not cls.G.has_edge(cls.from_node, cls.to_node):
                        cls.G.add_edge(cls.from_node, cls.to_node)
                        cls.set_weight()
                        cls.draw_graph()
                    else:
                        cls.set_weight()
                    cls.from_node = None
                    cls.to_node = None

    # @classmethod
    # def input_weight(cls, fromNode, toNode):
    #     cls.window = QtWidgets.QDialog()
    #     cls.gainWindow.setupUi(cls.window, fromNode, toNode)
    #     cls.window.show()
    #     cls.gainWindow.addGain.clicked.connect(cls.set_weight)

    @classmethod
    def set_weight(cls):
        QtCore.pyqtRemoveInputHook()
        cls.weight = cls.get_input()
        while cls.weight is None:
            cls.weight = cls.get_input()
        cls.G[cls.from_node][cls.to_node]['weight'] = cls.weight
        pos = nx.get_node_attributes(cls.GDraw,'pos')
        nx.draw_networkx_edges(cls.GDraw, pos, edgelist=[(cls.from_node, cls.to_node, cls.weight)],
                               connectionstyle='arc3,rad=0.5')
        edge_labels = nx.get_edge_attributes(cls.G, 'weight')
        nx.draw_networkx_edge_labels(cls.G, pos, edge_labels=edge_labels, label_pos=0.5,
                                     horizontalalignment='center', verticalalignment='bottom')
        plt.show()
        print("Adj list", cls.G.adj)

    @classmethod
    def get_closest_node(cls, x, y):
        pos = nx.get_node_attributes(cls.GDraw, 'pos')
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
        pos = nx.get_node_attributes(cls.GDraw, 'pos')
        nx.draw_networkx(cls.GDraw, pos=pos)
        edge_labels = nx.get_edge_attributes(cls.GDraw, 'weight')
        if edge_labels:
            nx.draw_networkx_edge_labels(cls.GDraw, pos=pos, edge_labels=edge_labels, node_size=500)
        plt.draw()

    @classmethod
    def clear_graph(cls):
        cls.GDraw.clear()
        cls.from_node = None
        cls.to_node = None
        cls.draw_graph()

    @classmethod
    def get_input(self):
        self.input_dialogue.exec_()
        return self.input_dialogue.get_text()


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