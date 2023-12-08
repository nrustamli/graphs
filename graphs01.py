import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

def is_symmetric(matrix):
    return all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix[0])))

def is_connected(matrix):
    num_nodes = len(matrix)
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in range(num_nodes):
            if matrix[node][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)

    dfs(0)
    return len(visited) == num_nodes

def is_weighted(matrix):
    return any(matrix[i][j] > 1 for i in range(len(matrix)) for j in range(len(matrix[0])))

def is_complete_graph(matrix):
    num_nodes = len(matrix)
    return all(matrix[i][j] == 1 for i in range(num_nodes) for j in range(i + 1, num_nodes))

def has_complete_subgraph(matrix, k):
    G = nx.Graph()
    
    num_nodes = len(matrix)
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if matrix[i][j] == 1:
                G.add_edge(i, j)

    # Проверка всех подграфов
    for nodes_combination in combinations(G.nodes, k):
        subgraph = G.subgraph(nodes_combination)
        if subgraph.number_of_edges() == k * (k - 1) // 2:
            return True

    return False

def has_cycle(matrix):
    num_nodes = len(matrix)
    visited = [False] * num_nodes

    def dfs(node, parent):
        visited[node] = True
        for neighbor in range(num_nodes):
            if matrix[node][neighbor] == 1:
                if not visited[neighbor]:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
        return False

    for node in range(num_nodes):
        if not visited[node]:
            if dfs(node, -1):
                return True

    return False

def is_unicyclic(matrix):
    num_nodes = len(matrix)
    visited = [False] * num_nodes

    def dfs(node, parent):
        visited[node] = True
        for neighbor in range(num_nodes):
            if matrix[node][neighbor] == 1:
                if not visited[neighbor]:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
        return False

    for node in range(num_nodes):
        if not visited[node]:
            if dfs(node, -1):
                return True

    return False

def classify_graph(matrix):
    if is_complete_graph(matrix):
        return "Полный граф"
    elif is_connected(matrix):
        return "Связный граф"
    else:
        return "Несвязный граф"
def kruskal(graph):
    edges = []
    for u in range(len(graph)):
        for v in range(u + 1, len(graph[u])):
            if graph[u][v] != 0:
                edges.append((u, v, graph[u][v]))

    edges.sort(key=lambda edge: edge[2])  # Сортируем рёбра по весу

    n = len(graph)
    parent = [i for i in range(n)]
    minimum_spanning_tree = []

    def find(u):
        if u != parent[u]:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)

        if root_u != root_v:
            parent[root_v] = root_u

    for edge in edges:
        u, v, weight = edge
        if find(u) != find(v):
            union(u, v)
            minimum_spanning_tree.append(edge)

    return minimum_spanning_tree

def visualize_graph(matrix):
    G = nx.Graph() if is_symmetric(matrix) else nx.DiGraph()  # Use DiGraph for directed graph

    num_nodes = len(matrix)
    G.add_nodes_from(range(num_nodes))

    edges = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            if matrix[i][j] == 1:
                edges.append((i, j))

    pos = nx.spring_layout(G)

    if is_symmetric(matrix):
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color="#ff7518")
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=2.0, edge_color='#18a2ff', arrows=False)
    else:
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='#ff7518')
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=2.0, edge_color='#18a2ff', arrowsize=30, arrowstyle='->')

    labels = {i: str(i) for i in range(num_nodes)}
    nx.draw_networkx_labels(G, pos, labels, font_size=16, font_color='black')

    plt.axis('off')
    plt.show()


def main():
    n = int(input("Enter the dimension of the matrix (n*n): " ))

    if 2 <= n <= 10:
        matrix = []
        for i in range(n):
            row = input(f"Enter row {i + 1} separated by space: ").split()
            if len(row) != n:
                print("Error: Enter exactly n elements in the row.")
                return
            matrix.append(list(map(int, row)))

        while True:
            print("\nChoose the property to check:")
            print("1. Directed or Undirected Graph")
            print("2. Connectivity of the Graph")
            print("3. Weighted or Unweighted Graph")
            print("4. Completeness of the Graph")
            print("5. Check for a Complete Subgraph")
            print("6. Unicyclic Graph Check")
            print("7. Number of Connected Components")
            print("8. Graph Classification")
            print("9. Visualize the Graph")
            print("10.Minimum Spanning Tree (Kruskal's Algorithm)")
            print("0. Exit")
            

            choice = input(" Enter the number of the chosen property (0-11): ")

            if choice == "0":
                break
            elif choice == "1":
                # Check for the directionality of the graph
                if is_symmetric(matrix):
                    print("This is an undirected graph.")
                else:
                    print("This is a directed graph.")
            elif choice == "2":
                # Check for the connectivity of the graph
                if is_connected(matrix):
                    print("The graph is connected.")
                else:
                    print("The graph is disconnected.")
            elif choice == "3":
                # Check for the weightedness of the graph
                if is_weighted(matrix):
                    print("The graph is weighted.")
                else:
                    print("The graph is unweighted.")
            elif choice == "4":
               # Check for the completeness of the graph
               if is_complete_graph(matrix):
                    print("The graph is complete.")
               else:
                    print("The graph is not complete.")
            elif choice == "5":
                # Check for the presence of a complete subgraph
                k = int(input("Enter the dimension k for checking a complete subgraph: "))
                if has_complete_subgraph(matrix, k):
                    print(f"A complete subgraph with {k} vertices exists.")
                else:
                    print(f"No complete subgraph with {k} vertices.")
            elif choice == "6":
                # Check for the unicyclicity of the graph
                if is_unicyclic(matrix):
                    print("The graph is unicyclic.")
                else:
                    print("The graph is not unicyclic.")
            elif choice == "7":
                # Количество связных компонентов
                components = count_connected_components(matrix)
                print(f"Number of connected components: {components}")
            elif choice == "8":
                # Классификация графа
                print("Graph type:", classify_graph(matrix))
            elif choice == "9":
                # Визуализация графа
                visualize_graph(matrix)
            elif choice == "10":
                # Минимальное остовное дерево (Краскал)
                result = kruskal(matrix)
                print("Minimum Spanning Tree (Prim's Algorithm) (edges):", result)
            else:
                print("Error: Invalid choice. Enter a number from 0 to 10.")
    else:
        print("Error: The matrix dimension should be between 2 and 10.")

if __name__ == "__main__":
    main()
