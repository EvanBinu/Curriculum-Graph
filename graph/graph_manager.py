import json
import networkx as nx


VALID_NODE_TYPES = {
    "Course",
    "Topic",
    "Skill",
    "Role"
}

VALID_EDGE_TYPES = {
    "Prerequisite",
    "Develops",
    "RequiredFor",
    "Contains"
}


class CurriculumGraph:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.curriculum_version = None

    def load_from_json(self, file_path):

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.curriculum_version = data["curriculum_version"]

        # Add nodes
        for node in data["nodes"]:
            self.add_node(
                node["id"],
                node["name"],
                node["type"],
                **{
                    key: value
                    for key, value in node.items()
                    if key not in {"id", "name", "type"}
                }
            )

        # Add edges
        for edge in data["edges"]:
            self.add_edge(
                edge["source"],
                edge["target"],
                edge["type"]
            )

    def add_node(self, node_id, name, node_type, **attributes):

        if node_type not in VALID_NODE_TYPES:
            raise ValueError(
                f"Invalid node type: {node_type}"
            )

        self.graph.add_node(
            node_id,
            name=name,
            type=node_type,
            **attributes
        )

    def add_edge(self, source, target, edge_type):

        if edge_type not in VALID_EDGE_TYPES:
            raise ValueError(
                f"Invalid edge type: {edge_type}"
            )

        if source not in self.graph:
            raise ValueError(
                f"Source node does not exist: {source}"
            )

        if target not in self.graph:
            raise ValueError(
                f"Target node does not exist: {target}"
            )

        self.graph.add_edge(
            source,
            target,
            relation=edge_type
        )

    def get_node(self, node_id):

        if node_id not in self.graph:
            return None

        return {
            "id": node_id,
            **self.graph.nodes[node_id]
        }

    def get_nodes_by_type(self, node_type):

        return [
            {
                "id": node_id,
                **self.graph.nodes[node_id]
            }
            for node_id in self.graph.nodes
            if self.graph.nodes[node_id]["type"] == node_type
        ]

    def get_edges_by_type(self, edge_type):

        return [
            {
                "source": source,
                "target": target,
                "relation": data["relation"]
            }
            for source, target, data
            in self.graph.edges(data=True)
            if data["relation"] == edge_type
        ]

    def get_course(self, course_id):

        node = self.get_node(course_id)

        if node is None:
            return None

        if node["type"] != "Course":
            return None

        return node

    def get_courses_by_semester(self, semester):

        return [
            {
                "id": node_id,
                **self.graph.nodes[node_id]
            }
            for node_id in self.graph.nodes
            if (
                self.graph.nodes[node_id]["type"] == "Course"
                and self.graph.nodes[node_id].get("semester") == semester
            )
        ]

    def summary(self):

        return {
            "curriculum_version": self.curriculum_version,
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "courses": len(
                self.get_nodes_by_type("Course")
            ),
            "topics": len(
                self.get_nodes_by_type("Topic")
            ),
            "skills": len(
                self.get_nodes_by_type("Skill")
            ),
            "roles": len(
                self.get_nodes_by_type("Role")
            )
        }
    def get_topics_for_course(self, course_id):

        if course_id not in self.graph:
            return []

        topics = []

        for target in self.graph.successors(course_id):

            edge_data = self.graph.get_edge_data(
                course_id,
                target
            )

            if edge_data["relation"] == "Contains":
                node = self.graph.nodes[target]

                topics.append({
                    "id": target,
                    **node
                })

        return topics