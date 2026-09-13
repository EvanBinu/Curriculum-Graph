import networkx as nx
import pytest

from graph.editor import GraphEditor


def create_graph():

    graph = nx.DiGraph()

    graph.add_node(
        "topic_a",
        type="Topic"
    )

    graph.add_node(
        "topic_b",
        type="Topic"
    )

    graph.add_node(
        "topic_c",
        type="Topic"
    )

    graph.add_edge(
        "topic_a",
        "topic_b",
        type="Prerequisite"
    )

    return graph


def test_valid_edge_is_accepted():

    graph = create_graph()

    editor = GraphEditor(graph)

    result = editor.add_edge(
        "topic_b",
        "topic_c",
        "Prerequisite"
    )

    assert result is True

    assert graph.has_edge(
        "topic_b",
        "topic_c"
    )


def test_duplicate_edge_is_rejected():

    graph = create_graph()

    editor = GraphEditor(graph)

    with pytest.raises(
        ValueError,
        match="already exists"
    ):
        editor.add_edge(
            "topic_a",
            "topic_b",
            "Prerequisite"
        )


def test_cycle_is_rejected_and_rolled_back():

    graph = create_graph()

    editor = GraphEditor(graph)

    with pytest.raises(
        ValueError,
        match="rolled back"
    ):
        editor.add_edge(
            "topic_b",
            "topic_a",
            "Prerequisite"
        )

    # Original relationship remains
    assert graph.has_edge(
        "topic_a",
        "topic_b"
    )

    # Invalid relationship was removed
    assert not graph.has_edge(
        "topic_b",
        "topic_a"
    )


def test_nonexistent_source_is_rejected():

    graph = create_graph()

    editor = GraphEditor(graph)

    with pytest.raises(
        ValueError,
        match="does not exist"
    ):
        editor.add_edge(
            "topic_unknown",
            "topic_b",
            "Prerequisite"
        )


def test_nonexistent_target_is_rejected():

    graph = create_graph()

    editor = GraphEditor(graph)

    with pytest.raises(
        ValueError,
        match="does not exist"
    ):
        editor.add_edge(
            "topic_a",
            "topic_unknown",
            "Prerequisite"
        )


def test_invalid_edge_type_is_rejected():

    graph = create_graph()

    editor = GraphEditor(graph)

    with pytest.raises(
        ValueError,
        match="Invalid edge type"
    ):
        editor.add_edge(
            "topic_b",
            "topic_c",
            "RandomEdge"
        )