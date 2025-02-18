# Group 21
# Edwin Cervantes, Sophia Nystrom, Vaibhav Vishnu Kovela
import networkx as nx

import heapq

# Create the weigh Graph representing the map
G = nx.Graph()

G.add_edge("Oradea", "Zerind", weight=71)
G.add_edge("Oradea", "Sibiu", weight=151)
G.add_edge("Zerind", "Arad", weight=75)
G.add_edge("Arad", "Sibiu", weight=140)
G.add_edge("Arad", "Timisoara", weight=118)
G.add_edge("Timisoara", "Lugoj", weight=111)
G.add_edge("Lugoj", "Mehadia", weight=70)
G.add_edge("Mehadia", "Drobeta", weight=75)
G.add_edge("Drobeta", "Craiova", weight=120)
G.add_edge("Craiova", "Rimnicu Vilcea", weight=146)
G.add_edge("Craiova", "Pitesti", weight=138)
G.add_edge("Rimnicu Vilcea", "Sibiu", weight=80)
G.add_edge("Pitesti", "Rimnicu Vilcea", weight=97)
G.add_edge("Sibiu", "Fagaras", weight=99)
G.add_edge("Fagaras", "Bucharest", weight=211)
G.add_edge("Bucharest", "Pitesti", weight=101)
G.add_edge("Bucharest", "Giurgiu", weight=90)
G.add_edge("Bucharest", "Urziceni", weight=85)
G.add_edge("Urziceni", "Hirsova", weight=98)
G.add_edge("Urziceni", "Vaslui", weight=142)
G.add_edge("Hirsova", "Eforie", weight=86)
G.add_edge("Vaslui", "Iasi", weight=92)
G.add_edge("Iasi", "Neamt", weight=87)


def find_path_dfs(graph, starting_node, ending_node):
    '''

    :param graph: A Networkx graph
    :param starting_node: Node you wish to begin at
    :param ending_node: Node you wish to end at
    :return: A path from starting node to end node and the weight of the path
    '''
    visited = []
    queue = [(starting_node, [starting_node])]

    # Since we are using dfs, we will always put the children of the current node
    # to the front of the queue
    while queue:
        # Get node from front of the queue
        node, path = queue.pop()
        if node not in visited:
            visited.append(node)
            if node == ending_node:
                weight = nx.path_weight(graph, path, 'weight')
                return path, weight
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    # No path existed
    return [], []
    

def find_path_bfs(graph, starting_node, ending_node):
    '''

    :param graph: A Networkx graph
    :param starting_node: Node you wish to begin at
    :param ending_node: Node you wish to end at
    :return: A path from starting node to end node and the weight of the path
    '''
    visited = []
    queue = [[starting_node]]

    # Since we are using bfs, we will always put the children of the current node
    # to the back of the queue
    while queue:
        # Get node from front of the queue
        path = queue.pop(0)
        node = path[-1]
        if node not in visited:
            neighbors = []
            visited.append(node)
            if node == ending_node:
                weight = nx.path_weight(graph, path, 'weight')
                return path, weight
            # Find what edges connects these two nodes and make them neighbors
            for edge in graph.edges:
                if edge[0] == node:
                    neighbors.append(edge[1])
                elif edge[1] == node:
                    neighbors.append(edge[0])

            # Add the neighbor to the path and add the path to the queue
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    # No path existed
    return [], []

# Define heuristic values for each city (straight-line distance to Bucharest).
heuristic = {
    'Arad': 366,
    'Zerind': 374,
    'Oradea': 380,
    'Timisoara': 329,
    'Lugoj': 244,
    'Mehadia': 241,
    'Drobeta': 242,
    'Sibiu': 253,
    'Rimnicu Vilcea': 193,
    'Fagaras': 176,
    'Pitesti': 100,
    'Craiova': 160,
    'Bucharest': 0,
    'Giurgiu': 77,
    'Urziceni': 80,
    'Hirsova': 151,
    'Eforie': 161,
    'Vaslui': 199,
    'Iasi': 226,
    'Neamt': 234
}


def Astar(graph, start, goal):
    came_from = {}
    open_set = [(heuristic[start], start)]  # Priority queue of nodes to explore
    g_score = {city: float('inf') for city in graph}  # Cost from start to each node
    g_score[start] = 0

    while open_set:
        
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct and return the path if the goal is reached
            path = []
            while current:
                path.append(current)
                current = came_from.get(current)
            return path[::-1], g_score[goal]
        
        for i in range(len(graph[current])):
            neighbor = list(graph[current])
            cost = [G[current][x]['weight'] for x in neighbor]
            tentative_g_score = g_score[current] + cost[i]
            if tentative_g_score < g_score[neighbor[i]]:
                came_from[neighbor[i]] = current
                g_score[neighbor[i]] = tentative_g_score
                f_score = tentative_g_score + heuristic[neighbor[i]]
                heapq.heappush(open_set, (f_score, neighbor[i]))

    return [],[]# No path found

bfs_path_1, bfs_weight_1 = find_path_bfs(G, "Oradea", "Bucharest")
bfs_path_2, bfs_weight_2 = find_path_bfs(G, "Timisoara", "Bucharest")
bfs_path_3, bfs_weight_3 = find_path_bfs(G, "Neamt", "Bucharest")
print("Path from Oradea to Bucharest via BFS: {}, weight: {}".format(bfs_path_1, bfs_weight_1))
print("Path from Timisoara to Bucharest via BFS: {}, weight: {}".format(bfs_path_2, bfs_weight_2))
print("Path from Neamt to Bucharest via BFS: {}, weight: {}".format(bfs_path_3, bfs_weight_3))
print('\n\n')
dfs_path_1, dfs_weight_1 = find_path_dfs(G, "Oradea", "Bucharest")
dfs_path_2, dfs_weight_2 = find_path_dfs(G, "Timisoara", "Bucharest")
dfs_path_3, dfs_weight_3 = find_path_dfs(G, "Neamt", "Bucharest")
print("Path from Oradea to Bucharest via DFS: {}, weight: {}".format(dfs_path_1, dfs_weight_1))
print("Path from Timisoara to Bucharest via DFS: {}, weight: {}".format(dfs_path_2, dfs_weight_2))
print("Path from Neamt to Bucharest via DFS: {}, weight: {}".format(dfs_path_3, dfs_weight_3))
print('\n\n')
aStar_path_1, aStar_weight_1 = Astar(G, "Oradea", "Bucharest")
aStar_path_2, aStar_weight_2 = Astar(G, "Timisoara", "Bucharest")
aStar_path_3, aStar_weight_3 = Astar(G, "Neamt", "Bucharest")
print("Path from Oradea to Bucharest via A*: {}, weight: {}".format(aStar_path_1, aStar_weight_1))
print("Path from Timisoara to Bucharest via A*: {}, weight: {}".format(aStar_path_2, aStar_weight_2))
print("Path from Neamt to Bucharest via A*: {}, weight: {}".format(aStar_path_3, aStar_weight_3))
