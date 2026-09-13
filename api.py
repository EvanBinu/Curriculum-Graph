import json
import networkx as nx

from fastapi import FastAPI, HTTPException

from graph.algorithms import CurriculumAlgorithms
from graph.validator import GraphValidator
from graph.editor import GraphEditor
from pydantic import BaseModel

class EdgeRequest(BaseModel):
    source: str
    target: str
    edge_type: str

app = FastAPI(
    title="SafePath Curriculum Graph API",
    description="API for curriculum knowledge graph operations",
    version="1.0.0"
)


# -------------------------------------------------
# LOAD GRAPH
# -------------------------------------------------

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


graph = load_graph()


# -------------------------------------------------
# GET PREREQUISITES
# -------------------------------------------------

@app.get("/topics/{topic_id}/prerequisites")
def get_prerequisites(topic_id: str):

    algorithms = CurriculumAlgorithms(graph)

    try:
        prerequisites = algorithms.get_prerequisites(topic_id)

        return {
            "topic": topic_id,
            "prerequisites": prerequisites
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
# -------------------------------------------------
# GET RELATED TOPICS
# -------------------------------------------------

@app.get("/topics/{topic_id}/related")
def get_related_topics(
    topic_id: str,
    depth: int = 1
):

    if depth < 1:
        raise HTTPException(
            status_code=400,
            detail="Depth must be at least 1."
        )

    algorithms = CurriculumAlgorithms(graph)

    try:
        related_topics = algorithms.bfs(
            topic_id,
            depth=depth
        )

        return {
            "topic": topic_id,
            "depth": depth,
            "related_topics": related_topics
        }

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
# -------------------------------------------------
# GET LEARNING ORDER
# -------------------------------------------------

@app.get("/learning-order")
def get_learning_order():

    algorithms = CurriculumAlgorithms(graph)

    try:
        order = algorithms.learning_order()

        return {
            "learning_order": order,
            "total_topics": len(order)
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
# -------------------------------------------------
# GET CENTRALITY
# -------------------------------------------------

@app.get("/centrality")
def get_centrality():

    algorithms = CurriculumAlgorithms(graph)

    try:
        degree = algorithms.degree_centrality()
        betweenness = algorithms.betweenness_centrality()
        pagerank = algorithms.pagerank()

        topics = set(degree) | set(betweenness) | set(pagerank)

        result = []

        for topic in topics:
            result.append({
                "topic": topic,
                "degree": degree.get(topic, 0),
                "betweenness": betweenness.get(topic, 0),
                "pagerank": pagerank.get(topic, 0)
            })

        # Sort by PageRank
        result.sort(
            key=lambda x: x["pagerank"],
            reverse=True
        )

        return {
            "centrality": result,
            "total_topics": len(result)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# -------------------------------------------------
# GET COURSES
# -------------------------------------------------

@app.get("/courses")
def get_courses():

    courses = []

    for node, data in graph.nodes(data=True):

        if data.get("type") == "Course":

            courses.append({
                "id": node,
                "name": data.get("name", node)
            })

    return {
        "courses": courses,
        "total_courses": len(courses)
    }
@app.get("/courses/{course_id}/topics")
def get_course_topics(course_id: str):

    if course_id not in graph:
        raise HTTPException(
            status_code=404,
            detail=f"Course '{course_id}' does not exist."
        )

    if graph.nodes[course_id].get("type") != "Course":
        raise HTTPException(
            status_code=400,
            detail=f"'{course_id}' is not a Course node."
        )

    algorithms = CurriculumAlgorithms(graph)

    topics = []

    for target in graph.successors(course_id):

        edge = graph.get_edge_data(course_id, target)

        if edge.get("type") != "Contains":
            continue

        topic_data = graph.nodes[target]

        try:
            prerequisites = algorithms.get_prerequisites(target)
        except ValueError:
            prerequisites = []

        topics.append({
            "id": target,
            "name": topic_data.get("name", target),
            "prerequisites": prerequisites
        })

    return {
        "course": course_id,
        "topics": topics,
        "total_topics": len(topics)
    }

@app.post("/graph/edge")
def add_graph_edge(request: EdgeRequest):

    editor = GraphEditor(graph)

    try:
        editor.add_edge(
            request.source,
            request.target,
            request.edge_type
        )

        return {
            "status": "accepted",
            "source": request.source,
            "target": request.target,
            "type": request.edge_type
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )