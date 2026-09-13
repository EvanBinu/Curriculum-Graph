import networkx as nx


class GraphValidator:

    ALLOWED_EDGE_TYPES = {
        "Prerequisite",
        "Develops",
        "RequiredFor",
        "Contains"
    }

    def __init__(self, graph):
        self.graph = graph

    def validate(self):
        """
        Run all graph integrity checks.
        Returns True if graph is valid.
        Raises ValueError if an integrity violation is found.
        """

        self.check_orphan_relationships()
        self.check_invalid_edge_types()
        self.check_self_loops()
        self.check_prerequisite_cycles()

        return True

    def check_orphan_relationships(self):
        """
        Ensure every edge references nodes that actually exist.
        """

        for source, target, data in self.graph.edges(data=True):

            if source not in self.graph:
                raise ValueError(
                    f"Orphan relationship: source node '{source}' does not exist."
                )

            if target not in self.graph:
                raise ValueError(
                    f"Orphan relationship: target node '{target}' does not exist."
                )

    def check_invalid_edge_types(self):
        """
        Ensure every relationship uses a recognized edge type.
        """

        for source, target, data in self.graph.edges(data=True):

            edge_type = data.get("type")

            if edge_type not in self.ALLOWED_EDGE_TYPES:
                raise ValueError(
                    f"Invalid edge type '{edge_type}' "
                    f"for relationship {source} -> {target}."
                )

    def check_self_loops(self):
        """
        Prerequisite self-loops are not allowed.
        """

        for source, target, data in self.graph.edges(data=True):

            if (
                source == target
                and data.get("type") == "Prerequisite"
            ):
                raise ValueError(
                    f"Invalid prerequisite self-loop: {source} -> {target}"
                )

    def check_prerequisite_cycles(self):
        """
        Ensure the prerequisite graph is acyclic.
        """

        prerequisite_graph = nx.DiGraph()

        for node, data in self.graph.nodes(data=True):

            if data.get("type") == "Topic":
                prerequisite_graph.add_node(node)

        for source, target, data in self.graph.edges(data=True):

            if data.get("type") != "Prerequisite":
                continue

            if (
                self.graph.nodes[source].get("type") == "Topic"
                and self.graph.nodes[target].get("type") == "Topic"
            ):
                prerequisite_graph.add_edge(source, target)

        if not nx.is_directed_acyclic_graph(prerequisite_graph):

            cycle = nx.find_cycle(prerequisite_graph)

            raise ValueError(
                f"Prerequisite cycle detected: {cycle}"
            )