import json
import networkx as nx

from graph.algorithms import CurriculumAlgorithms


def load_graph():
    with open("data/curriculum.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = nx.DiGraph()

    for node in data["nodes"]:
        graph.add_node(node["id"], **node)

    for edge in data["edges"]:
        graph.add_edge(
            edge["source"],
            edge["target"],
            **edge
        )

    return graph


def test_learning_order():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    order = algorithms.learning_order()

    assert len(order) > 0
    assert len(order) == len(set(order))


def test_prerequisites():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    prerequisites = algorithms.get_prerequisites(
        "topic_23CSE203_graph_traversal"
    )

    assert "topic_23CSE203_graphs" in prerequisites


def test_bfs():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    result = algorithms.bfs(
        "topic_23CSE203_graphs",
        depth=1
    )

    assert "topic_23CSE203_graph_traversal" in result


def test_dfs():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    result = algorithms.dfs(
        "topic_23CSE203_graphs",
        depth=1
    )

    assert "topic_23CSE203_graph_traversal" in result


def test_degree_centrality():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    result = algorithms.degree_centrality()

    assert len(result) > 0


def test_betweenness_centrality():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    result = algorithms.betweenness_centrality()

    assert len(result) > 0


def test_pagerank():
    graph = load_graph()

    algorithms = CurriculumAlgorithms(graph)

    result = algorithms.pagerank()

    assert len(result) > 0