import json
import networkx as nx

from graph.algorithms import CurriculumAlgorithms
from graph.validator import GraphValidator
from graph.editor import GraphEditor

def load_graph():
    with open("data/curriculum.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = nx.DiGraph()

    # Add nodes
    for node in data["nodes"]:
        graph.add_node(
            node["id"],
            **node
        )

    # Add edges
    for edge in data["edges"]:
        graph.add_edge(
            edge["source"],
            edge["target"],
            **edge
        )

    return graph


def main():

    # Load graph
    graph = load_graph()

    print("\nDEBUG: Prerequisite edges")
    print("-" * 40)

    prerequisite_edges = [
        (source, target)
        for source, target, data in graph.edges(data=True)
        if data.get("type") == "Prerequisite"
    ]

    print(f"Total prerequisite edges: {len(prerequisite_edges)}")

    for source, target in prerequisite_edges:
        print(f"{source} -> {target}")

    print("=" * 60)
    print("             CURRICULUM GRAPH TEST")
    print("=" * 60)

    # -----------------------------------------
    # GRAPH VALIDATION
    # -----------------------------------------

    validator = GraphValidator(graph)

    try:
        validator.validate()
        print("\nGraph validation: PASSED")

    except ValueError as e:
        print("\nGraph validation: FAILED")
        print(e)
        return

    # -----------------------------------------
    # ALGORITHMS
    # -----------------------------------------

    algorithms = CurriculumAlgorithms(graph)

    target_topic = "topic_23CSE203_graph_traversal"

    print("\nTarget Topic:")
    print(target_topic)

    try:
        prerequisites = algorithms.get_prerequisites(target_topic)

        print("\nPrerequisites:")
        print("-" * 40)

        if not prerequisites:
            print("No prerequisites found.")
        else:
            for i, topic in enumerate(prerequisites, 1):
                print(f"{i}. {topic}")

    except ValueError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")

    # -----------------------------------------
    # GRAPH EDIT + ROLLBACK TEST
    # -----------------------------------------

    print("\n" + "=" * 60)
    print("             GRAPH EDIT TEST")
    print("=" * 60)

    editor = GraphEditor(graph)

    source = "topic_23CSE203_graph_traversal"
    target = "topic_23CSE203_graphs"

    print("\nAttempting invalid edit:")
    print(f"{source} -> {target}")

    try:
        editor.add_edge(
            source,
            target,
            "Prerequisite"
        )

        print("Edit succeeded.")

    except ValueError as e:
        print("\nEdit failed:")
        print(e)

    print("\nChecking graph after failed edit...")

    try:
        GraphValidator(graph).validate()
        print("Graph validation after rollback: PASSED")

    except ValueError as e:
        print("Graph validation after rollback: FAILED")
        print(e)
if __name__ == "__main__":
    main()