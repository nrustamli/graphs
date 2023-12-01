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
    G = nx.Graph()

    num_nodes = len(matrix)
    G.add_nodes_from(range(num_nodes))

    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if matrix[i][j] == 1:
                edges.append((i, j))

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=1.0, edge_color='gray')

    labels = {i: str(i) for i in range(num_nodes)}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color='black')

    plt.axis('off')
    plt.show()

def main():
    n = int(input("Введите размерность матрицы (n*n): "))

    if 2 <= n <= 10:
        matrix = []
        for i in range(n):
            row = input(f"Введите строку {i + 1} через пробел: ").split()
            if len(row) != n:
                print("Ошибка: Введите ровно n элементов в строке.")
                return
            matrix.append(list(map(int, row)))

        while True:
            print("\nВыберите параметр для проверки:")
            print("1. Направленность графа")
            print("2. Связность графа")
            print("3. Взвешенность графа")
            print("4. Полнота графа")
            print("5. Проверка наличия полного подграфа")
           
            print("7. Уникурсальность графа")
            print("8. Количество связных компонентов")
            print("9. Классификация графа")
            print("10. Визуализация графа")
            print("11. Минимальное остовное дерево (Краскал)")
            print("0. Выход")

            choice = input("Введите номер выбранного параметра (0-11): ")

            if choice == "0":
                break
            elif choice == "1":
                # Проверка направленности графа
                if is_symmetric(matrix):
                    print("Это ненаправленный граф.")
                else:
                    print("Это направленный граф.")
            elif choice == "2":
                # Проверка связности графа
                if is_connected(matrix):
                    print("Граф связный.")
                else:
                    print("Граф несвязный.")
            elif choice == "3":
                # Проверка взвешенности графа
                if is_weighted(matrix):
                    print("Граф взвешенный.")
                else:
                    print("Граф не взвешенный.")
            elif choice == "4":
                # Проверка полноты графа
                if is_complete_graph(matrix):
                    print("Граф полный.")
                else:
                    print("Граф не полный.")
            elif choice == "5":
                # Проверка наличия полного подграфа
                k = int(input("Введите размерность k для проверки на полный подграф: "))
                if has_complete_subgraph(matrix, k):
                    print(f"Существует полный подграф с {k} вершинами.")
                else:
                    print(f"Нет полного подграфа с {k} вершинами.")
            elif choice == "6":
                # Проверка наличия циклов в графе
                if has_cycle(matrix):
                    print("Граф содержит циклы.")
                else:
                    print("Граф не содержит циклов.")
            elif choice == "7":
                # Проверка уникурсальности графа
                if is_unicyclic(matrix):
                    print("Граф уникурсальный.")
                else:
                    print("Граф не уникурсальный.")
            elif choice == "8":
                # Количество связных компонентов
                components = count_connected_components(matrix)
                print(f"Количество связных компонентов: {components}")
            elif choice == "9":
                # Классификация графа
                print("Тип графа:", classify_graph(matrix))
            elif choice == "10":
                # Визуализация графа
                visualize_graph(matrix)
            elif choice == "11":
                # Минимальное остовное дерево (Краскал)
                result = kruskal(matrix)
                print("Минимальное остовное дерево (Краскал) (рёбра):", result)
            else:
                print("Ошибка: Неверный выбор. Введите число от 0 до 10.")
    else:
        print("Ошибка: Размерность матрицы должна быть от 2 до 10.")

if __name__ == "__main__":
    main()
