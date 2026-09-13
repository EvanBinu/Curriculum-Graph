import json

import networkx as nx
import streamlit as st
from pyvis.network import Network

from graph.algorithms import CurriculumAlgorithms
from graph.validator import GraphValidator


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="SafePath AI - Curriculum Graph",
    page_icon="🧠",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD GRAPH
# ---------------------------------------------------------

@st.cache_resource
def load_graph():

    with open(
        "data/curriculum.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    graph = nx.DiGraph()

    for node in data["nodes"]:

        graph.add_node(
            node["id"],
            **node
        )

    for edge in data["edges"]:

        graph.add_edge(
            edge["source"],
            edge["target"],
            **edge
        )

    return graph


graph = load_graph()

algorithms = CurriculumAlgorithms(graph)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("🧠 SafePath AI")

st.sidebar.caption(
    "Curriculum Knowledge Graph"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Course Explorer",
        "Topic Explorer",
        "Learning Order",
        "Centrality Analysis",
        "Graph Visualization"
    ]
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def get_nodes_by_type(node_type):

    return [
        (node, data)
        for node, data in graph.nodes(data=True)
        if data.get("type") == node_type
    ]


def get_course_topics(course_id):

    topics = []

    for target in graph.successors(course_id):

        edge = graph.get_edge_data(
            course_id,
            target
        )

        if edge.get("type") == "Contains":

            topics.append(target)

    return topics


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if page == "Dashboard":

    st.title("🧠 SafePath AI")
    st.markdown("### Curriculum Knowledge Graph")

    st.write(
        "Explore courses, topics, prerequisite relationships, "
        "learning order and graph analytics."
    )

    # -----------------------------------------
    # GRAPH VALIDATION
    # -----------------------------------------

    validator = GraphValidator(graph)

    try:
        validator.validate()
        graph_status = True
    except ValueError as e:
        graph_status = False
        validation_error = str(e)

    # -----------------------------------------
    # NODE COUNTS
    # -----------------------------------------

    courses = get_nodes_by_type("Course")
    topics = get_nodes_by_type("Topic")

    # -----------------------------------------
    # EDGE COUNTS
    # -----------------------------------------

    prerequisite_edges = sum(
        1
        for _, _, data in graph.edges(data=True)
        if data.get("type") == "Prerequisite"
    )

    contains_edges = sum(
        1
        for _, _, data in graph.edges(data=True)
        if data.get("type") == "Contains"
    )

    # -----------------------------------------
    # GRAPH HEALTH
    # -----------------------------------------

    st.divider()

    if graph_status:
        st.success("✓ Graph Integrity: PASSED")
    else:
        st.error(
            f"✗ Graph Integrity: FAILED — {validation_error}"
        )

    # -----------------------------------------
    # CURRICULUM OVERVIEW
    # -----------------------------------------

    st.subheader("Curriculum Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Courses",
            len(courses)
        )

    with col2:
        st.metric(
            "Topics",
            len(topics)
        )

    # -----------------------------------------
    # GRAPH STATISTICS
    # -----------------------------------------

    st.divider()

    st.subheader("Graph Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Nodes",
            graph.number_of_nodes()
        )

    with col2:
        st.metric(
            "Total Relationships",
            graph.number_of_edges()
        )

    with col3:
        st.metric(
            "Prerequisite Relationships",
            prerequisite_edges
        )

    # -----------------------------------------
    # RELATIONSHIP BREAKDOWN
    # -----------------------------------------

    st.divider()

    st.subheader("Relationship Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Course → Topic",
            contains_edges
        )

    with col2:
        st.metric(
            "Topic → Topic",
            prerequisite_edges
        )

    # -----------------------------------------
    # AVAILABLE OPERATIONS
    # -----------------------------------------

    st.divider()

    st.subheader("Available Graph Operations")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            **Academic Planning**

            - Prerequisite discovery
            - Valid learning order
            - Course topic exploration
            """
        )

    with col2:

        st.markdown(
            """
            **Graph Traversal**

            - BFS
            - DFS
            - Depth-limited traversal
            - Related topic discovery
            """
        )

    with col3:

        st.markdown(
            """
            **Graph Analytics**

            - Degree Centrality
            - Betweenness Centrality
            - PageRank
            """
        )

# ---------------------------------------------------------
# COURSE EXPLORER
# ---------------------------------------------------------

elif page == "Course Explorer":

    st.title("📚 Course Explorer")

    courses = get_nodes_by_type("Course")

    course_options = {
        data.get("name", node): node
        for node, data in courses
    }

    selected_name = st.selectbox(
        "Select a course",
        list(course_options.keys())
    )

    course_id = course_options[selected_name]

    # -----------------------------------------
    # COURSE INFORMATION
    # -----------------------------------------

    st.subheader(selected_name)

    st.caption(f"Course Code: {course_id}")

    topics = get_course_topics(course_id)

    col1, col2 = st.columns(2)

    col1.metric(
        "Topics",
        len(topics)
    )

    col2.metric(
        "Course ID",
        course_id
    )

    st.divider()

    # -----------------------------------------
    # COURSE TOPICS
    # -----------------------------------------

    st.subheader("📖 Course Topics")

    if not topics:

        st.info("No topics are connected to this course.")

    else:

        for index, topic_id in enumerate(topics, start=1):

            topic_data = graph.nodes[topic_id]

            topic_name = topic_data.get(
                "name",
                topic_id
            )

            with st.expander(
                f"{index}. {topic_name}"
            ):

                st.caption(
                    f"Topic ID: {topic_id}"
                )

                # -----------------------------------------
                # PREREQUISITES
                # -----------------------------------------

                try:

                    prerequisites = algorithms.get_prerequisites(
                        topic_id
                    )

                except ValueError:

                    prerequisites = []

                st.write("**Prerequisites**")

                if not prerequisites:

                    st.info(
                        "No prerequisite topics found."
                    )

                else:

                    for prerequisite_id in prerequisites:

                        prerequisite_name = graph.nodes[
                            prerequisite_id
                        ].get(
                            "name",
                            prerequisite_id
                        )

                        st.write(
                            f"⬅️ {prerequisite_name}"
                        )

                        st.caption(
                            f"Topic ID: {prerequisite_id}"
                        )


# ---------------------------------------------------------
# TOPIC EXPLORER
# ---------------------------------------------------------

elif page == "Topic Explorer":

    st.title("🔎 Topic Explorer")

    topics = get_nodes_by_type("Topic")

    topic_options = {
        data.get("name", node): node
        for node, data in topics
    }

    selected_name = st.selectbox(
        "Select a topic",
        list(topic_options.keys())
    )

    topic_id = topic_options[selected_name]

    st.subheader(selected_name)

    st.caption(f"Topic ID: {topic_id}")

    st.divider()

    # -----------------------------------------
    # PREREQUISITES
    # -----------------------------------------

    st.write("### ⬅️ Prerequisites")

    try:
        prerequisites = algorithms.get_prerequisites(
            topic_id
        )
    except ValueError:
        prerequisites = []

    if prerequisites:

        for prerequisite_id in prerequisites:

            prerequisite_name = graph.nodes[
                prerequisite_id
            ].get(
                "name",
                prerequisite_id
            )

            st.write(
                f"• {prerequisite_name}"
            )

            st.caption(
                f"Topic ID: {prerequisite_id}"
            )

    else:

        st.info(
            "No prerequisite topics found."
        )

    st.divider()

    # -----------------------------------------
    # DEPENDENT TOPICS
    # -----------------------------------------

    st.write("### ➡️ Dependent Topics")

    prerequisite_graph = algorithms._build_prerequisite_graph()

    dependent_topics = list(
        prerequisite_graph.successors(topic_id)
    )

    if dependent_topics:

        for dependent_id in dependent_topics:

            dependent_name = graph.nodes[
                dependent_id
            ].get(
                "name",
                dependent_id
            )

            st.write(
                f"• {dependent_name}"
            )

            st.caption(
                f"Topic ID: {dependent_id}"
            )

    else:

        st.info(
            "No topics directly depend on this topic."
        )

    st.divider()

    # -----------------------------------------
    # RELATED TOPICS
    # -----------------------------------------

    st.write("### 🔗 Related Topics")

    depth = st.slider(
        "Relationship depth",
        min_value=1,
        max_value=3,
        value=1
    )

    related_topics = algorithms.bfs(
        topic_id,
        depth=depth
    )

    # Remove topics already displayed as direct
    # dependents from the general related list.
    related_topics = [
        topic
        for topic in related_topics
        if topic not in dependent_topics
    ]

    if related_topics:

        for related_id in related_topics:

            related_name = graph.nodes[
                related_id
            ].get(
                "name",
                related_id
            )

            st.write(
                f"• {related_name}"
            )

            st.caption(
                f"Topic ID: {related_id}"
            )

    else:

        st.info(
            "No additional related topics found."
        )


# ---------------------------------------------------------
# LEARNING ORDER
# ---------------------------------------------------------

elif page == "Learning Order":

    st.title("🎯 Learning Path")

    st.write(
        "Select a target topic to determine the prerequisite "
        "topics that should be learned first."
    )

    st.caption(
        "Topological sorting is used to produce a valid order "
        "from prerequisites to the selected topic."
    )

    st.divider()

    # -----------------------------------------
    # BUILD PREREQUISITE GRAPH
    # -----------------------------------------

    prerequisite_graph = algorithms._build_prerequisite_graph()

    # -----------------------------------------
    # TOPIC SELECTION
    # -----------------------------------------

    topics = get_nodes_by_type("Topic")

    topic_options = {
        data.get("name", node): node
        for node, data in topics
    }

    selected_name = st.selectbox(
        "🎯 Select target topic",
        list(topic_options.keys()),
        key="learning_path_topic"
    )

    target_topic = topic_options[selected_name]

    st.caption(
        f"Target Topic ID: {target_topic}"
    )

    st.divider()

    # -----------------------------------------
    # FIND ALL PREREQUISITES
    # -----------------------------------------

    try:

        prerequisites = algorithms.get_prerequisites(
            target_topic
        )

    except ValueError as e:

        st.error(str(e))
        st.stop()

    # -----------------------------------------
    # TARGET HAS NO PREREQUISITES
    # -----------------------------------------

    if not prerequisites:

        st.success(
            f"'{selected_name}' is a foundation topic "
            "with no prerequisite topics."
        )

    else:

        st.subheader("📚 Required Learning Path")

        st.write(
            f"**{len(prerequisites)} prerequisite topics** "
            f"must appear before **{selected_name}**."
        )

        st.divider()

        # -----------------------------------------
        # CREATE SUBGRAPH
        # -----------------------------------------

        path_nodes = set(prerequisites)
        path_nodes.add(target_topic)

        path_graph = prerequisite_graph.subgraph(
            path_nodes
        ).copy()

        # -----------------------------------------
        # TOPOLOGICAL ORDER
        # -----------------------------------------

        ordered_path = list(
            nx.topological_sort(path_graph)
        )

        # -----------------------------------------
        # DISPLAY PATH
        # -----------------------------------------

        for index, topic_id in enumerate(
            ordered_path,
            start=1
        ):

            topic_name = graph.nodes[
                topic_id
            ].get(
                "name",
                topic_id
            )

            if topic_id == target_topic:

                st.success(
                    f"🎯 {index}. {topic_name}"
                )

                st.caption(
                    "Target topic"
                )

            else:

                st.info(
                    f"📘 {index}. {topic_name}"
                )

                st.caption(
                    f"Prerequisite — {topic_id}"
                )

            if index < len(ordered_path):

                st.markdown(
                    "↓"
                )

    st.divider()

    # -----------------------------------------
    # GRAPH RELATIONSHIP SUMMARY
    # -----------------------------------------

    st.subheader("🔗 Dependency Summary")

    direct_prerequisites = list(
        prerequisite_graph.predecessors(
            target_topic
        )
    )

    dependent_topics = list(
        prerequisite_graph.successors(
            target_topic
        )
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Direct Prerequisites",
        len(direct_prerequisites)
    )

    col2.metric(
        "Topics Depending On It",
        len(dependent_topics)
    )
# ---------------------------------------------------------
# CENTRALITY
# ---------------------------------------------------------

elif page == "Centrality Analysis":

    st.title("📊 Centrality Analysis")

    st.write(
        "Centrality measures identify structurally important "
        "topics in the prerequisite graph."
    )

    st.caption(
        "Higher values indicate greater structural importance "
        "according to the selected graph metric."
    )

    st.divider()

    # -----------------------------------------
    # CALCULATE CENTRALITY
    # -----------------------------------------

    degree = algorithms.degree_centrality()

    betweenness = algorithms.betweenness_centrality()

    pagerank = algorithms.pagerank()

    # -----------------------------------------
    # BUILD RESULTS
    # -----------------------------------------

    rows = []

    for topic_id in degree:

        topic_name = graph.nodes[
            topic_id
        ].get(
            "name",
            topic_id
        )

        rows.append(
            {
                "Topic ID": topic_id,
                "Topic": topic_name,
                "Degree Centrality": degree.get(
                    topic_id,
                    0
                ),
                "Betweenness Centrality": betweenness.get(
                    topic_id,
                    0
                ),
                "PageRank": pagerank.get(
                    topic_id,
                    0
                )
            }
        )

    # -----------------------------------------
    # TOP TOPICS
    # -----------------------------------------

    st.subheader("🏆 Most Important Topics")

    col1, col2, col3 = st.columns(3)

    # Highest Degree

    top_degree = max(
        rows,
        key=lambda x: x["Degree Centrality"]
    )

    col1.metric(
        "Highest Degree",
        top_degree["Topic"]
    )

    # Highest Betweenness

    top_betweenness = max(
        rows,
        key=lambda x: x["Betweenness Centrality"]
    )

    col2.metric(
        "Top Bridge Topic",
        top_betweenness["Topic"]
    )

    # Highest PageRank

    top_pagerank = max(
        rows,
        key=lambda x: x["PageRank"]
    )

    col3.metric(
        "Highest PageRank",
        top_pagerank["Topic"]
    )

    st.divider()

    # -----------------------------------------
    # METRIC EXPLANATION
    # -----------------------------------------

    st.subheader("📖 Understanding the Metrics")

    with st.expander("Degree Centrality"):

        st.write(
            "Measures how connected a topic is within the "
            "prerequisite graph."
        )

        st.write(
            "A highly connected topic may have relationships "
            "with many other topics."
        )

    with st.expander("Betweenness Centrality"):

        st.write(
            "Measures how often a topic lies on shortest paths "
            "between other topics."
        )

        st.write(
            "A high value can indicate a bridge topic that "
            "connects different parts of the curriculum."
        )

    with st.expander("PageRank"):

        st.write(
            "Measures structural importance based on the "
            "connections surrounding a topic."
        )

        st.write(
            "It can help identify topics that have greater "
            "importance within the overall prerequisite network."
        )

    st.divider()
    # -----------------------------------------
    # NUMERICAL INTERPRETATION
    # -----------------------------------------

    st.subheader("📐 How to Interpret the Values")

    st.write(
        "Centrality values should primarily be compared "
        "with other topics in the same curriculum graph. "
        "There is no universal ideal value."
    )

    with st.expander("📌 Degree Centrality — Range: 0 to 1"):   

        st.write(
            "**0** means the topic has no connections in "
            "the prerequisite graph."
        )

        st.write(
            "Values closer to **1** indicate that the topic "
            "is highly connected."
        )

        st.write(
            "**Higher = more structurally connected**, "
            "but not necessarily academically better."
        )

        st.markdown(
            """
            **General interpretation**

            - `0` → No connections
            - `0.01–0.10` → Low
            - `0.10–0.30` → Moderate
            - `0.30+` → High
            - `1.0` → Maximum possible connectivity
            """
        )

    with st.expander(
        "📌 Betweenness Centrality — Range: 0 to 1"
    ):

        st.write(
            "**0** means the topic does not significantly "
            "act as a bridge between other topics."
        )

        st.write(
            "Higher values indicate that the topic appears "
            "more frequently on shortest paths between "
            "other topics."
        )

        st.write(
            "**Higher = stronger bridge/connector role.**"
        )

        st.markdown(
            """
            **General interpretation**

            - `0` → No bridge role
            - `0–0.10` → Low
            - `0.10–0.30` → Moderate
            - `0.30+` → High
            - `1.0` → Extremely strong bridge position
            """
        )

    with st.expander(
        "📌 PageRank — Values sum to approximately 1"
    ):

        st.write(
            "PageRank distributes importance across the "
            "entire prerequisite graph."
        )

        st.write(
            "A higher value means the topic has greater "
            "structural importance according to the PageRank "
            "calculation."
        )

        st.write(
            "There is no universal value that is considered "
            "'good' or 'bad'. Compare the topic against the "
            "other topics in this curriculum."
        )

        st.markdown(
            """
            **Interpretation**

            - Very low → Relatively low structural importance
            - Moderate → Typical/medium importance
            - High relative to other topics → Important topic
            - Highest values → Most highly ranked topics
            """
        )

    st.info(
        "⚠️ Centrality does not measure teaching quality, "
        "difficulty, or student performance. It measures "
        "structural properties of the curriculum graph."
    )
    # -----------------------------------------
    # SORTING
    # -----------------------------------------

    st.subheader("🔍 Explore Centrality Rankings")

    metric = st.selectbox(
        "Rank topics by",
        [
            "Degree Centrality",
            "Betweenness Centrality",
            "PageRank"
        ]
    )

    sorted_rows = sorted(
        rows,
        key=lambda x: x[metric],
        reverse=True
    )

    # -----------------------------------------
    # DISPLAY TOP 15
    # -----------------------------------------

    st.write("### Top 15 Topics")

    top_rows = sorted_rows[:15]

    st.dataframe(
        top_rows,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------------------
    # SELECT TOPIC
    # -----------------------------------------

    st.subheader("🎯 Inspect a Topic")

    topic_options = {
        row["Topic"]: row["Topic ID"]
        for row in rows
    }

    selected_name = st.selectbox(
        "Select a topic",
        list(topic_options.keys()),
        key="centrality_topic"
    )

    selected_id = topic_options[selected_name]

    selected_row = next(
        row
        for row in rows
        if row["Topic ID"] == selected_id
    )

    st.caption(
        f"Topic ID: {selected_id}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Degree",
        f"{selected_row['Degree Centrality']:.4f}"
    )

    col2.metric(
        "Betweenness",
        f"{selected_row['Betweenness Centrality']:.4f}"
    )

    col3.metric(
        "PageRank",
        f"{selected_row['PageRank']:.4f}"
    )

    # -----------------------------------------
    # PREREQUISITE INFORMATION
    # -----------------------------------------

    prerequisites = algorithms.get_prerequisites(
        selected_id
    )

    direct_dependents = list(
        algorithms._build_prerequisite_graph().successors(
            selected_id
        )
    )

    st.write("### 🔗 Topic Relationships")

    col1, col2 = st.columns(2)

    col1.metric(
        "Prerequisite Topics",
        len(prerequisites)
    )

    col2.metric(
        "Direct Dependent Topics",
        len(direct_dependents)
    )

# ---------------------------------------------------------
# GRAPH VISUALIZATION
# ---------------------------------------------------------

elif page == "Graph Visualization":

    st.title("🕸️ Curriculum Graph Visualization")

    st.write(
        "Explore prerequisite relationships around a selected "
        "curriculum topic."
    )

    st.caption(
        "Edges shown here represent Topic → Topic prerequisite "
        "relationships."
    )

    st.divider()

    # -----------------------------------------
    # BUILD PREREQUISITE GRAPH
    # -----------------------------------------

    prerequisite_graph = algorithms._build_prerequisite_graph()

    topics = get_nodes_by_type("Topic")

    topic_options = {
        data.get("name", node): node
        for node, data in topics
    }

    # -----------------------------------------
    # SELECT TOPIC
    # -----------------------------------------

    selected_name = st.selectbox(
        "🎯 Select a topic",
        list(topic_options.keys()),
        key="visualization_topic"
    )

    selected_topic = topic_options[selected_name]

    # -----------------------------------------
    # GRAPH DIRECTION
    # -----------------------------------------

    direction = st.radio(
        "Relationship direction",
        [
            "Prerequisites",
            "Dependent Topics",
            "Both"
        ],
        horizontal=True
    )

    depth = st.slider(
        "Relationship depth",
        min_value=1,
        max_value=3,
        value=1
    )

    st.divider()

    # -----------------------------------------
    # DETERMINE VISIBLE NODES
    # -----------------------------------------

    visible_nodes = {selected_topic}

    if direction in ["Prerequisites", "Both"]:

        prerequisite_nodes = set(
            nx.ancestors(
                prerequisite_graph,
                selected_topic
            )
        )

        # Limit using shortest-path distance
        for node in prerequisite_nodes:

            try:

                distance = nx.shortest_path_length(
                    prerequisite_graph,
                    node,
                    selected_topic
                )

                if distance <= depth:
                    visible_nodes.add(node)

            except nx.NetworkXNoPath:

                pass

    if direction in ["Dependent Topics", "Both"]:

        dependent_nodes = set(
            nx.descendants(
                prerequisite_graph,
                selected_topic
            )
        )

        # Limit using shortest-path distance
        for node in dependent_nodes:

            try:

                distance = nx.shortest_path_length(
                    prerequisite_graph,
                    selected_topic,
                    node
                )

                if distance <= depth:
                    visible_nodes.add(node)

            except nx.NetworkXNoPath:

                pass

    # -----------------------------------------
    # GRAPH STATISTICS
    # -----------------------------------------

    visible_edges = []

    for source, target in prerequisite_graph.edges():

        if (
            source in visible_nodes
            and target in visible_nodes
        ):

            visible_edges.append(
                (source, target)
            )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Visible Topics",
        len(visible_nodes)
    )

    col2.metric(
        "Visible Relationships",
        len(visible_edges)
    )

    col3.metric(
        "Depth",
        depth
    )

    st.divider()

    # -----------------------------------------
    # PYVIS GRAPH
    # -----------------------------------------

    net = Network(
        height="650px",
        width="100%",
        directed=True
    )

    # -----------------------------------------
    # ADD NODES
    # -----------------------------------------

    for node_id in visible_nodes:

        node_data = graph.nodes[node_id]

        node_name = node_data.get(
            "name",
            node_id
        )

        if node_id == selected_topic:

            label = f"🎯 {node_name}"

        else:

            label = node_name

        net.add_node(
            node_id,
            label=label,
            title=f"{node_name}\nID: {node_id}"
        )

    # -----------------------------------------
    # ADD EDGES
    # -----------------------------------------

    for source, target in visible_edges:

        net.add_edge(
            source,
            target,
            label="Prerequisite"
        )

    # -----------------------------------------
    # VISUALIZATION OPTIONS
    # -----------------------------------------

    net.set_options(
        """
        {
        "physics": {
            "enabled": true,
            "stabilization": {
            "iterations": 300
            },
            "barnesHut": {
            "gravitationalConstant": -8000,
            "centralGravity": 0.1,
            "springLength": 250,
            "springConstant": 0.02,
            "damping": 0.09,
            "avoidOverlap": 1
            }
        },

        "nodes": {
            "margin": 20
        },

        "edges": {
            "arrows": {
            "to": {
                "enabled": true
            }
            },
            "smooth": {
            "enabled": true
            }
        },

        "interaction": {
            "hover": true,
            "navigationButtons": true,
            "zoomView": true
        }
        }
        """
    )

    # -----------------------------------------
    # RENDER GRAPH
    # -----------------------------------------

    net.save_graph(
        "graph.html"
    )

    with open(
        "graph.html",
        "r",
        encoding="utf-8"
    ) as f:

        html = f.read()

    st.components.v1.html(
        html,
        height=700,
        scrolling=True
    )

    st.divider()

    # -----------------------------------------
    # GRAPH LEGEND
    # -----------------------------------------

    st.subheader("📖 How to Read the Graph")

    st.write(
        "**Arrow direction:** Prerequisite → Dependent Topic"
    )

    st.write(
        "**Selected topic:** The topic marked with 🎯"
    )

    st.write(
        "**Depth:** Maximum number of prerequisite/dependent "
        "relationships displayed from the selected topic."
    )

    st.info(
        "The visualization uses only actual prerequisite "
        "relationships stored in the curriculum graph."
    )