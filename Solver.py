from typing import List
from sympy import sympify


class Loop:
    def __init__(self, loop, gain):
        self.loop = loop
        self.gain = gain
        self.id = None


#  ID added after appending to unique_loops
def filterLoops(loops):
    unique_loops = []

    for loop_obj in loops:
        loop = loop_obj.loop
        if len(loop) not in [len(l.loop) for l in unique_loops]:
            unique_loops.append(loop_obj)
            loop_obj.id = len(unique_loops)
        else:
            found = False
            for ul in unique_loops:
                if set(ul.loop) == set(loop):
                    found = True
                    break
            if not found:
                unique_loops.append(loop_obj)
                loop_obj.id = len(unique_loops)

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
            gain = ''
            for i in range(len(loop)):
                current_node = loop[i]
                next_node = loop[(i + 1) % len(loop)]
                gain += f"{adj_list[current_node][next_node]['weight']} * "
            loops.append(Loop(loop, f'({gain[:-3]})'))
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
        rest = lst[i + 1:]
        for comb in string_combinations(rest, length - 1):
            result.append(f'{lst[i].gain} * {comb}')
    return result


def int_combinations(loops: List[Loop], length):
    if length == 0:
        return [1]
    result = []
    for i in range(len(loops)):
        rest = loops[i + 1:]
        for comb in int_combinations(rest, length - 1):
            result.append(loops[i].gain * comb)
    return result


def combination(lst: List[Loop], length):
    if len(lst) == 0:
        return '0'
    # if isinstance(lst[0].gain, str):
    result = '( '
    products = string_combinations(lst, length)
    for i in range(0, len(products) - 1):
        result += products[i] + ' + '
    result += products[-1]
    result = result[:-3]
    result += ' )'
    return result
    # else:
    #     result = 0
    #     products = int_combinations(lst, length)
    #     for p in products:
    #         result += p
    #     return result


class ForwardPath:
    def __init__(self, path, gain):
        self.path = path
        self.gain = gain

    isloated_notTouchingLoops: List[List[Loop]] = []
    isolated_loops: List[Loop] = []

    def extract_isolatedLoop(self, loops: List[Loop]):
        self.isolated_loops = []
        for loop in loops:
            if not lists_overlap(self.path, loop.loop):
                self.isolated_loops.append(loop)

    def extract_notTouching_isolatedLoops(self, nonTouching_loops: List[List[Loop]]):
        self.isloated_notTouchingLoops = []
        for group in nonTouching_loops:
            newGroup: List[Loop] = []
            for loop in group:
                if loop in self.isolated_loops:
                    newGroup.append(loop)
            if len(newGroup) > 1:
                self.isloated_notTouchingLoops.append(newGroup)


class MasonSolver:
    adj_list = {}
    start_node: any
    end_node: any

    forwardPaths: List[ForwardPath] = []  # forward paths
    loops: List[Loop] = []  # All loops
    nonTouching_loops: List[List[Loop]] = []  # All non-touching loops combinations
    nonTouching_loops_map = {}  # {'13': (G1*H1)+(G3*H3)}
    deltas = []  # all deltas n

    # Can be changed into None to ignore data type
    transferFunction: str = ''  # C/R

    delta: int = 0  # Whole delta

    def __init__(self, graph, start_node, end_node):
        self.adj_list = graph
        self.start_node = start_node
        self.end_node = end_node

        self.forwardPaths = self.__find_forwardPaths(self.start_node, self.end_node)
        self.__find_loops()
        self.__generate_nonTouchingLoops()

        for path in self.forwardPaths:
            path.extract_isolatedLoop(self.loops)
            path.extract_notTouching_isolatedLoops(self.nonTouching_loops)
            path.gain = f'({path.gain[:-3]})'

        self.form_nonTouching_loops_map()
        self.form_deltas()
        self.delta = self.__delta()

    def form_deltas(self):
        for path in self.forwardPaths:
            self.deltas.append(self.__delta_path(path))

    def form_nonTouching_loops_map(self):
        for i in range(len(self.nonTouching_loops)):
            loopId = ''
            combinationGain = None
            for loop in self.nonTouching_loops[i]:
                loopId += 'L' + str(loop.id)
                if isinstance(loop.gain, int):
                    if combinationGain is None:
                        combinationGain = 1
                    combinationGain *= loop.gain  # handles numbers only
                else:
                    if combinationGain is None:
                        combinationGain = ''
                        combinationGain += loop.gain
                    else:
                        combinationGain += '*' + loop.gain
            self.nonTouching_loops_map[loopId] = combinationGain

    def calculate_transferFunction(self):
        transferFunction: str = '( '
        for i in range(0, len(self.forwardPaths) - 1):
            transferFunction += f'( {self.forwardPaths[i].gain} * {self.__delta_path(self.forwardPaths[i])} ) + '
        transferFunction += f'( {self.forwardPaths[-1].gain} * {self.__delta_path(self.forwardPaths[-1])} ) )'
        transferFunction += f' / ( {self.delta} )'
        self.transferFunction = sympify(transferFunction)
        return self.transferFunction

    def __find_forwardPaths(self, start_node, end_node, path=None):
        # Initialize path and gain if not provided
        if path is None:
            path = []
        path = path + [start_node]
        gain = ''

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
                new_paths = self.__find_forwardPaths(neighbor, end_node, path)
                for new_path in new_paths:
                    # Multiply the gain by the weight of the edge between start_node and neighbor
                    edge_weight = self.adj_list[start_node][neighbor]['weight']
                    new_path.gain += f'{edge_weight} * '
                    paths.append(new_path)

        # Return the list of paths
        return paths

    def __find_loops(self):
        loops = []
        visited = set()  # keep track of visited nodes
        path = []  # current path being explored
        for start_node in self.adj_list.keys():
            getLoopsHelper(self.adj_list, start_node, visited, start_node, path, loops)
        self.loops = filterLoops(loops)
        return self.loops

    def __generate_nonTouchingLoops(self):
        groups: List[List[Loop]] = []
        for i in range(0, len(self.loops)):
            for j in range(i, len(self.loops)):
                if not lists_overlap(self.loops[i].loop, self.loops[j].loop):
                    groups.append([self.loops[i], self.loops[j]])
        for length in range(2, len(self.loops)):
            for loop in self.loops:
                for group in groups:
                    if len(group) != length or loop in group:
                        continue
                    overlap: bool = False
                    for gp_loop in group:
                        if lists_overlap(gp_loop.loop, loop.loop):
                            overlap = True
                            break
                    if not overlap:
                        newGroup = group[:]
                        newGroup.append(loop)
                        groups.append(newGroup)

        self.nonTouching_loops = groups
        return groups

    def __deltaHelper_nonTouchingLoops(self, nonTouching_loops: List[List[Loop]]):
        if len(nonTouching_loops) == 0:
            return '0'

        # if isinstance(nonTouching_loops[0][0].gain, str):
        result = '( '
        for group in nonTouching_loops:

            if group != nonTouching_loops[0]:
                if len(group) % 2 == 0:
                    result += ' + '
                else:
                    result += ' - '

            result += '('
            for loop in group:
                result += f'{loop.gain} * '
            result = f'{result[:-3]})'

        return f'{result} )'
        # else:
        #     result = 0
        #     for length in range(2, maxLength + 1) :   
        #         temp = 0
        #         for group in nonTouching_loops:
        #             if len(group) < length:
        #                 continue
        #             temp += combination(group, length)
        #         result += temp * pow(-1, length)

        #     return result

    def __deltaHelper_isolatedLoop(self, loops: List[Loop]):
        if len(loops) == 0:
            return '0'
        # if isinstance(loops[0].gain, str):
        result = '( '
        for loop in loops:
            result += f'{loop.gain} + '
        result = result[:-3]
        result += ' )'
        return result
        # else:
        #     result = 0
        #     for loop in loops:
        #         result += loop.gain

    def __delta(self):
        return f'(1 - {self.__deltaHelper_isolatedLoop(self.loops)} + {self.__deltaHelper_nonTouchingLoops(self.nonTouching_loops)})'

    def __delta_path(self, path: ForwardPath):
        return f'(1 - {self.__deltaHelper_isolatedLoop(path.isolated_loops)} + {self.__deltaHelper_nonTouchingLoops(path.isloated_notTouchingLoops)})'


if __name__ == "__main__":
    nigga = {
        'r': {'y1': {'weight': 'G1'}, 'y4': {'weight': 'G5'}},
        'y1': {'y2': {'weight': 'G2'}},
        'y2': {'y3': {'weight': 'G3'}, 'y1': {'weight': 'H2'}},
        'y3': {'c': {'weight': 'G4'}, 'y2': {'weight': 'H3'}},
        'y4': {'y5': {'weight': 'G6'}},
        'y5': {'y6': {'weight': 'G7'}, 'y4': {'weight': 'H6'}},
        'y6': {'c': {'weight': 'G8'}, 'y5': {'weight': 'H7'}},
        'c': {}
    }
    solve = MasonSolver(nigga, 'r', 'c')
    for path in solve.forwardPaths:
        print(path.path)
        print(path.gain)

    for loop in solve.loops:
        print("")

    for nonTouching in solve.nonTouching_loops:
        print("")

    print(solve.calculate_transferFunction())
