import os
from subprocess import call

import networkx as nx
import matplotlib.pyplot as plt

# Create an empty directed graph
G = nx.DiGraph()

# Create variables to hold the clicked nodes
from_node = None
to_node = None

# Create a function to add a node to the graph on click
def add_node(event):
    global from_node, to_node
    if event.button == 1:  # left mouse button
        x, y = event.xdata, event.ydata
        node = len(G)
        G.add_node(node, pos=(x, y))
        draw_graph()

    if event.button == 3:  # right mouse button
        if from_node is None:
            from_node = get_closest_node(event.xdata, event.ydata)
            if from_node is not None:
                nx.draw_networkx_nodes(G, pos=nx.get_node_attributes(G, 'pos'), node_color='red', nodelist=[from_node])
                plt.draw()

        elif to_node is None:
            to_node = get_closest_node(event.xdata, event.ydata)
            if to_node is not None:
                # Check if the selected nodes already form an edge
                if G.has_edge(from_node, to_node):
                    # Prompt the user to enter the weight for the edge
                    input_weight(from_node, to_node)
                else:
                    G.add_edge(from_node, to_node)
                    draw_graph()
                from_node = None
                to_node = None

def input_weight(from_node, to_node):
    # TODO show dialog box to enter weight --> needs updates
    current_dir = os.getcwd()
    main_window_path = os.path.join(current_dir, 'Dialog.py')
    call(["python", main_window_path])

    # Prompt the user to enter the weight for the edge
    # weight = input('Enter weight for the edge from node {} to node {}: '.format(from_node, to_node))
    # G[from_node][to_node]['weight'] = weight
    draw_graph()

def get_closest_node(x, y):
    pos = nx.get_node_attributes(G, 'pos')
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

def draw_graph():
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G, pos=pos)
    # Draw edge labels if edges have weights
    edge_labels = nx.get_edge_attributes(G, 'weight')
    if edge_labels:
        nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.draw()

def clear_graph(event):
    global G, from_node, to_node
    G.clear()
    from_node = None
    to_node = None
    draw_graph()

# TODO create window to: enter number of nodes, show graph window, calculate and show the results

# Create a Matplotlib figure and axes
fig, ax = plt.subplots()

# Set the limits of the axes
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])

# Register the event handler function for mouse clicks
cid = fig.canvas.mpl_connect('button_press_event', add_node)

# Register the event handler function for closing the window
cid_close = fig.canvas.mpl_connect('close_event', clear_graph)

# Draw the initial empty graph
draw_graph()

plt.show()