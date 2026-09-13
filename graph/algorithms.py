import networkx as nx


class CurriculumAlgorithms:

    def __init__(self, graph):
        self.graph = graph

    # -------------------------------------------------
    # 1. TOPOLOGICAL SORT
    # -------------------------------------------------

    def learning_order(self):
        """
        Returns topics in a valid prerequisite order.

        Only Prerequisite edges are considered.
        """

        prerequisite_graph = nx.DiGraph()

        # Add only Topic nodes
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "Topic":
                prerequisite_graph.add_node(node, **data)

        # Add only prerequisite relationships
        for source, target, data in self.graph.edges(data=True):

            if data.get("type") != "Prerequisite":
                continue

            if (
                self.graph.nodes[source].get("type") == "Topic"
                and self.graph.nodes[target].get("type") == "Topic"
            ):
                prerequisite_graph.add_edge(source, target)

        try:
            order = list(nx.topological_sort(prerequisite_graph))
            return order

        except nx.NetworkXUnfeasible:
            raise ValueError(
                "Cannot compute learning order: prerequisite cycle detected."
            )

    # -------------------------------------------------
    # 2. BFS
    # -------------------------------------------------

    def bfs(self, start_topic, depth=None):
        """
        Breadth-First Search over the prerequisite graph.

        Only Topic -> Topic Prerequisite relationships
        are traversed.
        """

        prerequisite_graph = self._build_prerequisite_graph()

        if start_topic not in prerequisite_graph:
            raise ValueError(
                f"Topic '{start_topic}' does not exist."
            )

        visited = []

        queue = [(start_topic, 0)]

        seen = {start_topic}

        while queue:

            current, current_depth = queue.pop(0)

            if current != start_topic:
                visited.append(current)

            if depth is not None and current_depth >= depth:
                continue

            for neighbor in prerequisite_graph.successors(current):

                if neighbor not in seen:

                    seen.add(neighbor)

                    queue.append(
                        (neighbor, current_depth + 1)
                    )

        return visited

    # -------------------------------------------------
    # 3. DFS
    # -------------------------------------------------

    def dfs(self, start_topic, depth=None):
        """
        Depth-First Search over the prerequisite graph.

        Only Topic -> Topic Prerequisite relationships
        are traversed.
        """

        prerequisite_graph = self._build_prerequisite_graph()

        if start_topic not in prerequisite_graph:
            raise ValueError(
                f"Topic '{start_topic}' does not exist."
            )

        visited = []

        stack = [(start_topic, 0)]

        seen = {start_topic}

        while stack:

            current, current_depth = stack.pop()

            if current != start_topic:
                visited.append(current)

            if depth is not None and current_depth >= depth:
                continue

            neighbors = list(
                prerequisite_graph.successors(current)
            )

            for neighbor in reversed(neighbors):

                if neighbor not in seen:

                    seen.add(neighbor)

                    stack.append(
                        (neighbor, current_depth + 1)
                    )

        return visited

    # -------------------------------------------------
    # 4. DEGREE CENTRALITY
    # -------------------------------------------------

    def degree_centrality(self):
        """
        Calculates degree centrality for Topic nodes.

        Uses the prerequisite graph only.
        """

        prerequisite_graph = self._build_prerequisite_graph()

        centrality = nx.degree_centrality(
            prerequisite_graph
        )

        return centrality

    # -------------------------------------------------
    # 5. BETWEENNESS CENTRALITY
    # -------------------------------------------------

    def betweenness_centrality(self):
        """
        Finds topics that act as bridges between
        other topics.
        """

        prerequisite_graph = self._build_prerequisite_graph()

        centrality = nx.betweenness_centrality(
            prerequisite_graph
        )

        return centrality

    # -------------------------------------------------
    # 6. PAGERANK
    # -------------------------------------------------

    def pagerank(self):
        """
        Calculates PageRank importance of topics.
        """

        prerequisite_graph = self._build_prerequisite_graph()

        if len(prerequisite_graph) == 0:
            return {}

        return nx.pagerank(
            prerequisite_graph
        )

    # -------------------------------------------------
    # HELPER
    # -------------------------------------------------

    def _build_prerequisite_graph(self):
        """
        Creates a graph containing only:

            Topic --Prerequisite--> Topic
        """

        prerequisite_graph = nx.DiGraph()

        for node, data in self.graph.nodes(data=True):

            if data.get("type") == "Topic":
                prerequisite_graph.add_node(
                    node,
                    **data
                )

        for source, target, data in self.graph.edges(data=True):

            if data.get("type") != "Prerequisite":
                continue

            if (
                self.graph.nodes[source].get("type") == "Topic"
                and self.graph.nodes[target].get("type") == "Topic"
            ):
                prerequisite_graph.add_edge(
                    source,
                    target
                )

        return prerequisite_graph
    def get_prerequisites(self, target_topic):
        """
        Return all prerequisite topics required before the target topic.
        """

        G = self._build_prerequisite_graph()

        if target_topic not in G:
            raise ValueError(f"Topic not found: {target_topic}")

        # Reverse graph:
        # A -> B means A is prerequisite of B
        # Reverse gives B -> A
        reverse_graph = G.reverse(copy=True)

        # Find all ancestors of target
        prerequisites = nx.ancestors(G, target_topic)

        # Subgraph containing only prerequisites
        prereq_graph = G.subgraph(prerequisites).copy()

        # Add target so we can get a valid ordering
        prereq_graph.add_node(target_topic)

        # Topological ordering ensures prerequisites appear first
        ordered = list(nx.topological_sort(prereq_graph))

        # Remove target itself
        ordered.remove(target_topic)

        return ordered