from networkx import DiGraph
from typing import List

class Loop:
    def __init__(self, loop, gain):
        self.loop = loop
        self.gain = gain

class ForwardPath:
    def __init__(self, path, gain):
        self.path = path
        self.gain = gain

    isloated_notTouchingLoops: List[List[Loop]] = []
    isolated_loops: List[Loop] = []

    def generate_isolatedLoop(self, loops: List[Loop]):
        self.isolated_loops = []
        for loop in loops:
            if not lists_overlap(self.path, loop.loop):
                self.isolated_loops.append(loop)

    def generate_notTouching_isolatedLoops(self, nonTouching_loops: List[List[Loop]]):
        for group in nonTouching_loops:
            newGroup: List[Loop] = []
            for loop in group:
                if loop in self.isolated_loops:
                    newGroup.append(loop)
            if len(newGroup) > 1:
                self.isloated_notTouchingLoops.append(newGroup)


def filterLoops(loops):
    unique_loops = []
    
    for loop_obj in loops:
        loop = loop_obj.loop
        if len(loop) not in [len(l.loop) for l in unique_loops]:
            unique_loops.append(loop_obj)
        else:
            found = False
            for ul in unique_loops:
                if set(ul.loop) == set(loop):
                    found = True
                    break
            if not found:
                unique_loops.append(loop_obj)
    
    return unique_loops

def getLoopsHelper(adj_list, node, visited, start_node, path, loops):
    visited.add(node)
    path.append(node)
    for neighbor_tuple in adj_list[node].items():
        neighbor = neighbor_tuple[0]
        if neighbor not in path:
            getLoopsHelper(adj_list, neighbor, visited, start_node, path, loops)
        elif neighbor == start_node:
            loop = path[path.index(neighbor):]
            gain = 1
            for i in range(len(loop)):
                current_node = loop[i]
                next_node = loop[(i+1) % len(loop)]
                gain *= adj_list[current_node][next_node]['weight']
            loops.append(Loop(loop, gain))
    path.pop()
    visited.remove(node)

def lists_overlap(a: List, b: List):
    sb = set(b)
    return any(el in sb for el in a)

def string_combinations(lst: List[Loop], length):
    if length == 0:
        return ['']
    result = []
    for i in range(len(lst)):
        rest = lst[i+1:]
        for comb in string_combinations(rest, length-1):
            result.append(lst[i].gain + comb)
    return result

def int_combinations(loops: List[Loop], length):
    if length == 0:
        return [1]
    result = []
    for i in range(len(loops)):
        rest = loops[i+1:]
        for comb in int_combinations(rest, length-1):
            result.append(loops[i].gain * comb)
    return result
    
def combination(lst: List[Loop], length):
    if len(lst) == 0:
        return
    if isinstance(lst[0].gain, str):
        result = ''
        products = string_combinations(lst, length)
        for p in products:
            result += p + ' + '
        return result[:-3]
    else:
        result = 0
        products = int_combinations(lst, length)
        for p in products:
            result += p
        return result

class MasonSolver:
    adj_list = {}
    start: any
    end: any

    forwardPaths: List[ForwardPath] = []
    loops: List[Loop] = []
    nonTouching_loops: List[List[Loop]] = []

    def __init__(self, graph):
        self.adj_list = graph
    
    def get_forwardPaths(self, start_node, end_node, path=None):
        # Initialize path and gain if not provided
        if path is None:
            path = []
        path = path + [start_node]
        gain = 1

        # If the start_node is the end_node, return the path and gain as an ForwardPath object
        if start_node == end_node:
            return [ForwardPath(path, gain)]

        # If the start_node is not in the adjacency list, return an empty list
        if start_node not in self.adj_list:
            return []

        # Initialize the list of paths
        paths = []

        # Loop through the neighbors of start_node
        for neighbor in self.adj_list[start_node]:
            if neighbor not in path:
                # Recursively find paths from neighbor to end_node
                new_paths = self.get_forwardPaths(neighbor, end_node, path)
                for new_path in new_paths:
                    # Multiply the gain by the weight of the edge between start_node and neighbor
                    edge_weight = self.adj_list[start_node][neighbor]['weight']
                    new_path.gain *= edge_weight
                    paths.append(new_path)

        # Return the list of paths
        self.forwardPaths = paths
        return paths

    def get_loops(self):
        loops = []
        visited = set()  # keep track of visited nodes
        path = []  # current path being explored
        for start_node in self.adj_list.keys():
            getLoopsHelper(self.adj_list, start_node, visited, start_node, path, loops)
        self.loops = filterLoops(loops)
        return self.loops

    def get_nonTouchingLoops(self):
        groups = []

        for loop_obj in self.loops:
            current = loop_obj.loop
            found = False
            for group in groups:
                found = False
                for loop in group:
                    if lists_overlap(loop.loop, current):
                        found = True
                        break
                if not found:
                    group.append(loop_obj)
            if found or len(groups) == 0:
                groups.append([loop_obj])
                    
        self.nonTouching_Loops = [group for group in groups]
        return self.nonTouching_Loops
 
    def deltaHelper_nonTouchingLoops(self):
        if len(self.nonTouching_loops) == 0:
            return
        maxLength = 0
        for group in self.nonTouching_loops:
            if len(group) > maxLength:
                maxLength = len(group)
        if isinstance(self.nonTouching_loops[0][0].gain, str):
            result = '('
            for length in range(2, maxLength + 1) :       
                for group in self.nonTouching_loops:
                    if len(group) < length:
                        continue
                    result += combination(group, length) + ' + '
                
                result = result[:-3]
                result += ')'
                if(length % 2 == 0):
                    result += ' - '
                else:
                    result += ' + '
                result += '('
                    
            return result[:-3]
        else:
            result = 0
            for length in range(2, maxLength + 1) :   
                temp = 0
                for group in self.nonTouching_loops:
                    if len(group) < length:
                        continue
                    temp += combination(group, length)
                result += temp * pow(-1, length)
                    
            return result
            
    def deltaHelper_isolatedLoop(self):
        if len(self.loops) == 0:
            return
        if isinstance(self.loops[0].gain, str):
            result = ''
            for loop in self.loops:
                result += loop.gain + ' + '
        else:
            result = 0
            for loop in self.loops:
                result += loop.gain
        return result
    
    def delta(self):
        return 1 - self.deltaHelper_isolatedLoop() + self.deltaHelper_nonTouchingLoops()

if __name__ == "__main__":
    nigga = {
    'y1': {'y2': {'weight': 1}},
    'y2': {'y3': {'weight': 2}, 'y4': {'weight': 8}, 'y7': {'weight': 9}},
    'y3': {'y4': {'weight': 3}, 'y2': {'weight': 1}},
    'y4': {'y5': {'weight': 4}, 'y3': {'weight': 2}},
    'y5': {'y6': {'weight': 5}, 'y8': {'weight': 10}, 'y4': {'weight': 3}},
    'y6': {'y7': {'weight': 6}, 'y5': {'weight': 4}},
    'y7': {'y8': {'weight': 7}, 'y6': {'weight': 5}},
    'y8': {}
    }
    solve = MasonSolver(nigga)

    solve.get_forwardPaths('y1', 'y8')
    
    solve.get_loops()

    solve.get_nonTouchingLoops()

    for path in solve.forwardPaths:
        print(path.generate_isolatedLoop(solve.loops))