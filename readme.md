Absolutely. For GitHub, I’d make the README **technical enough to demonstrate the engineering work**, but structured so that someone reviewing the repository can understand the project quickly.

Below is a complete `README.md` you can use.

````markdown
# SafePath AI — Curriculum Knowledge Graph

A curriculum-aware Knowledge Graph module for **SafePath AI**, designed to represent academic topics, prerequisite dependencies, and course-topic relationships in a structured directed graph.

The module provides:

- Curriculum graph construction
- Course → Topic mapping
- Topic → Prerequisite → Topic relationships
- Prerequisite-aware learning-order computation
- BFS and DFS graph traversal
- Degree Centrality
- Betweenness Centrality
- PageRank
- Graph integrity validation
- Cycle and self-loop detection
- Invalid relationship and orphan-reference rejection
- Transaction-like graph editing with rollback
- REST APIs using FastAPI
- Interactive curriculum exploration using Streamlit
- Interactive graph visualization using PyVis
- Automated testing using pytest

> **Current implementation:** 8 courses, 210 topics, 218 nodes, and 298 relationships, including 90 prerequisite relationships.

> **Note:** Skills and Role nodes are supported by the graph schema but are not populated in the current dataset.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Role in SafePath AI](#role-in-safepath-ai)
- [Key Features](#key-features)
- [Graph Model](#graph-model)
- [Architecture](#architecture)
- [Methodology](#methodology)
- [Algorithms](#algorithms)
- [Graph Integrity and Validation](#graph-integrity-and-validation)
- [Current Dataset](#current-dataset)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [REST API](#rest-api)
- [Streamlit Interface](#streamlit-interface)
- [Testing](#testing)
- [Example Workflow](#example-workflow)
- [Design Decisions](#design-decisions)
- [Scope and Limitations](#scope-and-limitations)
- [Future Improvements](#future-improvements)
- [Team Contribution](#team-contribution)
- [Contributing](#contributing)
- [License](#license)

---

# Overview

SafePath AI is intended to provide students with intelligent, personalized academic and career guidance.

The **Curriculum Knowledge Graph** acts as the structural layer of SafePath AI by representing curriculum information as a graph rather than as a simple list of courses and topics.

A traditional curriculum representation might look like:

```text
Course A
Course B
Course C
````

The Knowledge Graph instead represents relationships:

```text
Course
   |
   | Contains
   v
 Topic A
   |
   | Prerequisite
   v
 Topic B
   |
   | Prerequisite
   v
 Topic C
```

This allows the system to reason about:

* What topics belong to a course?
* What must be learned before a particular topic?
* What is a valid learning sequence?
* Which topics are connected?
* Which topics act as structural bridges?
* Which topics have high graph centrality?
* Would a proposed graph modification introduce an invalid dependency?

The graph therefore provides the **structural knowledge layer** that can be used by other SafePath AI components.

---

# Problem Statement

Traditional curriculum structures usually organize academic content according to:

* Course
* Semester
* Unit
* Topic

However, this representation does not explicitly capture dependencies between topics.

For example:

```text
Graphs
   ↓
Graph Traversal
   ↓
Advanced Graph Algorithms
```

A student who attempts to learn Graph Traversal without understanding Graphs may encounter unnecessary difficulty.

The Curriculum Knowledge Graph addresses this problem by explicitly representing prerequisite relationships.

Instead of treating topics as independent items, the system models them as a directed dependency graph.

This enables SafePath AI to determine prerequisite-aware learning sequences and perform structural analysis of the curriculum.

---

# Objectives

The primary objectives of this module are:

### 1. Represent Curriculum Structure

Represent courses and topics as nodes and their relationships as directed edges.

### 2. Model Topic Prerequisites

Represent prerequisite dependencies between topics.

### 3. Compute Learning Order

Use topological sorting to calculate a valid prerequisite-aware learning sequence.

### 4. Support Graph Traversal

Provide BFS and DFS traversal for exploring topic relationships.

### 5. Analyze Topic Importance

Calculate:

* Degree Centrality
* Betweenness Centrality
* PageRank

### 6. Maintain Graph Integrity

Prevent invalid graph modifications such as:

* prerequisite cycles
* prerequisite self-loops
* invalid relationship types
* orphan relationships

### 7. Support Other SafePath Modules

Provide structural curriculum information that can be consumed by:

* Academic Planning
* Contextual Routing
* Skill Development
* Goal-Based Planning
* Other personalization components

---

# Role in SafePath AI

The Curriculum Knowledge Graph serves as the **structural backbone** of the SafePath AI architecture.

Conceptually:

```text
                         SafePath AI
                              |
          +-------------------+-------------------+
          |                   |                   |
          v                   v                   v
 Student Digital       Curriculum Graph      Goal-Based
      Twin                   |                Planning
                             |
                 +-----------+-----------+
                 |                       |
                 v                       v
          Prerequisite Graph       Graph Metrics
                 |                       |
                 v                       v
          Learning Order         Centrality Analysis
                 |                       |
                 +-----------+-----------+
                             |
                             v
                    Academic Planning
```

The Curriculum Graph does not make all student-level decisions itself.

Instead, it provides structured curriculum knowledge that other components can use for reasoning and recommendation.

---

# Key Features

## Curriculum Representation

The graph currently represents:

* Course nodes
* Topic nodes
* Course → Topic relationships
* Topic → Topic prerequisite relationships

---

## Prerequisite-Aware Learning Order

The system uses topological sorting to calculate a valid ordering of topics.

For example:

```text
Programming Fundamentals
          ↓
Data Structures
          ↓
Graphs
          ↓
Graph Traversal
```

The prerequisite graph ensures that prerequisite topics occur before their dependent topics.

---

## Graph Traversal

The system supports:

### Breadth-First Search (BFS)

Explores neighboring topics level by level.

Useful for:

* finding nearby dependencies
* finding downstream topics within a given depth
* related-topic exploration

### Depth-First Search (DFS)

Explores one dependency branch before moving to another.

Useful for:

* dependency exploration
* graph traversal
* structural analysis

---

## Centrality Analysis

The system implements three centrality measures.

### Degree Centrality

Measures how connected a topic is within the prerequisite graph.

A higher value indicates greater direct connectivity.

It does **not** mean that the topic is academically better, harder, or more important to a student.

### Betweenness Centrality

Measures how frequently a topic lies on shortest paths between other topics.

A topic with high betweenness can act as a structural bridge between different parts of the curriculum.

For example:

```text
Foundation Topics
        |
        v
   Bridge Topic
        |
        v
Advanced Topics
```

### PageRank

Measures the relative structural importance of nodes based on graph connectivity.

PageRank is useful for ranking topics relative to one another.

> Centrality metrics describe the **structural position of a topic in the graph**. They do not directly measure teaching quality, difficulty, student performance, or learning effectiveness.

---

# Graph Model

The curriculum is represented as a directed graph using NetworkX.

## Node Types

### Course

Represents a curriculum course.

Example:

```json
{
  "id": "23CSE203",
  "type": "Course",
  "name": "Course Name"
}
```

The course ID is retained as the actual Course node ID.

### Topic

Represents an individual curriculum topic.

Example:

```json
{
  "id": "topic_23CSE203_graphs",
  "type": "Topic",
  "name": "Graphs"
}
```

Topic IDs are implementation identifiers used to uniquely represent topics in the graph.

---

# Relationship Types

The graph schema supports four relationship types:

| Relationship   | Meaning                                  |
| -------------- | ---------------------------------------- |
| `Prerequisite` | A topic is required before another topic |
| `Develops`     | A topic develops a skill                 |
| `RequiredFor`  | A skill is required for a role           |
| `Contains`     | A course contains a topic                |

The currently populated relationships are primarily:

```text
Course ──Contains──────> Topic

Topic ──Prerequisite───> Topic
```

The `Develops` and `RequiredFor` relationship types are supported by the graph validator but are not populated in the current dataset.

---

# Architecture

The implementation follows a layered architecture:

```text
             Curriculum / Syllabus
                       |
                       v
              curriculum.json
                       |
                       v
              Graph Loading Layer
                       |
                       v
                NetworkX DiGraph
                       |
          +------------+------------+
          |            |            |
          v            v            v
      Algorithms    Validator     Editor
          |            |            |
          +------------+------------+
                       |
             +---------+---------+
             |                   |
             v                   v
          FastAPI            Streamlit
             |                   |
             v                   v
        REST Clients       Human Users
```

## Data Layer

Stores structured curriculum information in:

```text
data/curriculum.json
```

## Graph Layer

Contains:

* graph algorithms
* graph validation
* graph editing

## API Layer

FastAPI exposes graph operations through REST endpoints.

## UI Layer

Streamlit provides interactive exploration.

PyVis provides interactive graph visualization.

## Test Layer

pytest provides automated regression testing.

---

# Methodology

The implementation follows the following pipeline:

```text
1. Curriculum / Syllabus
           |
           v
2. Curriculum Data Extraction
           |
           v
3. Structured JSON Representation
           |
           v
4. NetworkX Graph Construction
           |
           v
5. Graph Validation
           |
           v
6. Algorithmic Analysis
           |
           v
7. FastAPI Services
           |
           v
8. Streamlit Visualization
           |
           v
9. Automated Testing
```

### Step 1 — Curriculum Source

Course and topic information is obtained from the curriculum/syllabus source.

### Step 2 — Data Structuring

Curriculum information is converted into a structured JSON representation.

### Step 3 — Graph Construction

The JSON representation is loaded into a NetworkX directed graph.

### Step 4 — Validation

The graph is checked for structural integrity.

### Step 5 — Algorithmic Analysis

Graph algorithms operate on the prerequisite graph.

### Step 6 — API Exposure

FastAPI exposes the graph functionality to external clients.

### Step 7 — Visualization

Streamlit and PyVis provide interactive exploration.

### Step 8 — Testing

pytest validates the implemented functionality.

---

# Algorithms

## 1. Topological Sort

Topological sorting calculates a valid ordering of a directed acyclic graph.

Given:

```text
A → B
B → C
```

a valid ordering is:

```text
A
B
C
```

For prerequisite relationships, this represents:

```text
Prerequisite
     ↓
Dependent Topic
```

Therefore topological sorting provides a valid prerequisite-aware learning sequence.

### Cycle Requirement

Topological sorting requires the prerequisite graph to be acyclic.

For example:

```text
A → B
B → C
C → A
```

cannot produce a valid learning order.

The implementation detects this condition and raises an error.

---

# 2. Breadth-First Search

BFS explores a graph level by level.

Example:

```text
Topic A
   |
   +── Topic B
   |
   +── Topic C
          |
          +── Topic D
```

At depth `1`:

```text
B
C
```

At depth `2`:

```text
D
```

This is useful for exploring topics within a limited dependency distance.

---

# 3. Depth-First Search

DFS explores a graph branch before moving to another branch.

Example:

```text
A
|
B
|
C
|
D
```

DFS can traverse deeply through the dependency chain before exploring alternative branches.

---

# 4. Degree Centrality

Degree Centrality measures direct graph connectivity.

Conceptually:

```text
Degree Centrality
=
Direct Connections
/
Maximum Possible Connections
```

NetworkX provides the normalization used by the implementation.

Higher degree centrality indicates greater connectivity.

---

# 5. Betweenness Centrality

Betweenness Centrality identifies nodes that frequently occur on shortest paths between other nodes.

For example:

```text
A ──> B ──> D
      ^
      |
      C
```

If `B` lies on many paths between different parts of the graph, it may have high betweenness centrality.

This makes it useful for identifying structural bridge topics.

---

# 6. PageRank

PageRank assigns a relative importance score to nodes based on graph connectivity.

The scores can be used to produce a ranking such as:

```text
1. Topic A
2. Topic B
3. Topic C
...
```

The values are most useful for relative comparison within the graph.

---

# 7. Cycle Detection

Prerequisite cycles are detected using directed acyclic graph validation.

For example:

```text
A → B
B → C
C → A
```

is invalid because there is no possible learning order satisfying all three dependencies.

The graph validator detects this condition and rejects the graph.

---

# Graph Integrity and Validation

Graph modifications are validated before being accepted.

The validator performs several checks.

## 1. Orphan Relationship Detection

Every relationship must reference existing nodes.

Invalid:

```text
ExistingTopic → MissingTopic
```

The edit is rejected.

---

## 2. Invalid Edge-Type Detection

Only supported edge types are accepted:

```text
Prerequisite
Develops
RequiredFor
Contains
```

An arbitrary edge type is rejected.

---

## 3. Prerequisite Self-Loop Detection

A topic cannot be its own prerequisite.

Invalid:

```text
Graphs
  |
  +── Prerequisite ──> Graphs
```

The validator rejects the relationship.

---

## 4. Prerequisite Cycle Detection

A prerequisite graph must be acyclic.

Invalid:

```text
A
↓
B
↓
C
↘
 ↑
```

More explicitly:

```text
A → B
B → C
C → A
```

The graph is rejected.

---

# Transactional Graph Editing

Graph modifications use a snapshot-based rollback mechanism.

The process is:

```text
             Graph Edit Request
                     |
                     v
              Create Snapshot
                     |
                     v
                Apply Edit
                     |
                     v
              Validate Graph
                     |
                     v
        Recompute Graph Algorithms
                     |
              +------+------+
              |             |
             PASS          FAIL
              |             |
              v             v
           Commit        Rollback
              |             |
              v             v
        Updated Graph   Original Graph
```

If validation or downstream algorithmic recomputation fails:

1. The edit is rejected.
2. The graph is restored to its previous state.
3. An error is returned.

This prevents an invalid edit from leaving the graph in an inconsistent state.

---

# Current Dataset

The current implementation contains:

| Metric                         |      Value |
| ------------------------------ | ---------: |
| Courses                        |          8 |
| Topics                         |        210 |
| Total Nodes                    |        218 |
| Total Relationships            |        298 |
| Course → Topic (`Contains`)    |        208 |
| Topic → Topic (`Prerequisite`) |         90 |
| Automated Tests                | 20 passing |

Graph composition:

```text
218 Nodes
│
├── 8 Courses
└── 210 Topics
```

Relationship composition:

```text
298 Relationships
│
├── 208 Course → Topic
└── 90 Topic → Topic Prerequisite
```

Skills and Roles are not included in the current dataset counts.

---

# Project Structure

```text
SafePath-AI-Curriculum-Graph/
│
├── data/
│   └── curriculum.json
│
├── graph/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── editor.py
│   └── validator.py
│
├── tests/
│   ├── conftest.py
│   └── ...
│
├── app.py
├── api.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## File Responsibilities

### `data/curriculum.json`

Contains the structured curriculum graph data.

### `graph/algorithms.py`

Contains:

* topological learning order
* prerequisite extraction
* BFS
* DFS
* Degree Centrality
* Betweenness Centrality
* PageRank

### `graph/validator.py`

Contains:

* orphan-reference validation
* edge-type validation
* prerequisite self-loop detection
* prerequisite cycle detection

### `graph/editor.py`

Handles graph modifications and rollback.

### `api.py`

Implements the FastAPI REST API.

### `app.py`

Implements the Streamlit dashboard and interactive graph exploration.

### `main.py`

Provides a command-line entry point for loading and testing the graph.

### `tests/`

Contains automated tests for graph functionality.

---

# Technology Stack

| Technology | Purpose                             |
| ---------- | ----------------------------------- |
| Python     | Core implementation                 |
| NetworkX   | Graph representation and algorithms |
| FastAPI    | REST API                            |
| Uvicorn    | ASGI server                         |
| Streamlit  | Interactive dashboard               |
| PyVis      | Interactive graph visualization     |
| pytest     | Automated testing                   |
| JSON       | Curriculum data storage             |

---

# Installation

## Prerequisites

Recommended:

* Python 3.10+
* pip
* Git

Check Python:

```bash
python --version
```

Check pip:

```bash
pip --version
```

---

# Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd SafePath-AI-Curriculum-Graph
```

---

# Create a Virtual Environment

## Windows PowerShell

```powershell
python -m venv venv
venv\Scripts\activate
```

## Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

The core dependencies include:

```text
fastapi
uvicorn
networkx
streamlit
pyvis
pytest
numpy
```

---

# Running the Project

## Command-Line Graph Test

Run:

```bash
python main.py
```

This loads the curriculum graph, validates it, and demonstrates prerequisite retrieval.

---

# Running the FastAPI Server

Start the server:

```bash
uvicorn api:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to test all available API endpoints.

---

# REST API

The current implementation provides seven primary endpoints.

## 1. Topic Prerequisites

```http
GET /topics/{topic_id}/prerequisites
```

Example:

```text
GET /topics/topic_23CSE203_graph_traversal/prerequisites
```

Example response:

```json
{
  "topic": "topic_23CSE203_graph_traversal",
  "prerequisites": [
    "topic_23CSE203_graphs"
  ]
}
```

---

## 2. Related Topics

```http
GET /topics/{topic_id}/related?depth=1
```

Returns downstream topics within the requested graph depth.

---

## 3. Learning Order

```http
GET /learning-order
```

Returns a prerequisite-aware topological ordering of topics.

---

## 4. Centrality

```http
GET /centrality
```

Returns structural centrality information.

The API supports:

* Degree Centrality
* Betweenness Centrality
* PageRank

---

## 5. Courses

```http
GET /courses
```

Returns the courses represented in the curriculum graph.

---

## 6. Course Topics

```http
GET /courses/{course_id}/topics
```

Example:

```text
GET /courses/23CSE203/topics
```

The course ID corresponds to the actual Course node ID.

The endpoint returns the topics contained in the course and their prerequisite information.

---

## 7. Add Graph Relationship

```http
POST /graph/edge
```

Example request:

```json
{
  "source": "topic_A",
  "target": "topic_B",
  "edge_type": "Prerequisite"
}
```

The relationship is accepted only if:

1. The source node exists.
2. The target node exists.
3. The edge type is valid.
4. The relationship does not already exist.
5. The graph passes validation.
6. The prerequisite graph remains acyclic.
7. Required downstream algorithm computations succeed.

Otherwise the edit is rejected and rolled back.

> **Current limitation:** API graph edits are currently in-memory and are not persisted back to `data/curriculum.json`.

---

# Streamlit Interface

Run the dashboard:

```bash
streamlit run app.py
```

The interface provides multiple graph exploration modes.

---

## Dashboard

The dashboard displays current graph statistics:

```text
Courses                 8
Topics                210
Total Nodes           218
Relationships         298
Course → Topic        208
Prerequisites          90
Graph Integrity      PASSED
```

---

# Course Explorer

The Course Explorer allows users to:

1. Select a course.
2. View the course code/name.
3. View topics contained by the course.
4. Inspect prerequisites for each topic.

Example:

```text
23CSE203
   |
   +── Complexity Analysis
   |
   +── Asymptotic Analysis
   |
   +── Graphs
   |
   +── Graph Traversal
```

---

# Topic Explorer

The Topic Explorer allows users to inspect a selected topic.

It provides:

* prerequisites
* direct dependent topics
* downstream related topics

This allows the user to explore the dependency structure around an individual topic.

---

# Learning Path

The Learning Path interface allows a user to select a target topic.

The system:

1. Finds its prerequisite topics.
2. Builds the relevant prerequisite subgraph.
3. Performs topological sorting.
4. Displays the resulting learning sequence.

Conceptually:

```text
Prerequisite 1
      ↓
Prerequisite 2
      ↓
Prerequisite 3
      ↓
Target Topic
```

This provides a graph-derived prerequisite learning path.

---

# Centrality Analysis

The Centrality Analysis interface provides:

* Degree Centrality
* Betweenness Centrality
* PageRank
* ranked topic lists
* topic inspection

Example:

```text
Rank  Topic                    Score
-------------------------------------
1     Topic A                  0.31
2     Topic B                  0.27
3     Topic C                  0.24
```

The values should be interpreted as structural graph metrics rather than academic quality scores.

---

# Graph Visualization

The graph visualization uses PyVis to display prerequisite relationships interactively.

The user can select:

* a topic
* prerequisite direction
* dependent-topic direction
* both directions
* graph depth

The visualization operates on the prerequisite graph to keep dependency relationships clear.

The interface also displays the number of nodes and edges currently shown.

---

# Testing

The project uses pytest for automated testing.

Run:

```bash
pytest -v
```

Current result:

```text
20 tests passed
```

The tests cover functionality including:

* prerequisite retrieval
* learning-order computation
* BFS traversal
* DFS traversal
* centrality calculations
* cycle detection
* self-loop rejection
* invalid edge-type rejection
* orphan-reference validation
* graph editing
* rollback behavior

---

# Example Workflow

Consider the following prerequisite relationship:

```text
Graphs
   |
   v
Graph Traversal
```

Represented in the graph as:

```text
topic_23CSE203_graphs
        |
        | Prerequisite
        v
topic_23CSE203_graph_traversal
```

Request:

```http
GET /topics/topic_23CSE203_graph_traversal/prerequisites
```

Response:

```json
{
  "topic": "topic_23CSE203_graph_traversal",
  "prerequisites": [
    "topic_23CSE203_graphs"
  ]
}
```

Now suppose a user attempts to add the reverse relationship:

```text
Graph Traversal
       |
       v
     Graphs
```

The resulting graph would contain:

```text
Graphs
   ↕
Graph Traversal
```

This creates a prerequisite cycle.

The graph editor rejects the edit and restores the previous graph state.

The resulting API response is an error rather than an invalid graph.

---

# Design Decisions

## Why NetworkX?

NetworkX provides mature implementations of the graph operations required by the project:

* directed graphs
* topological sorting
* BFS/DFS traversal
* centrality algorithms
* cycle detection

It also keeps the prototype lightweight and easy to maintain.

---

## Why a Directed Graph?

Prerequisites have an inherent direction.

If:

```text
A → B
```

represents:

```text
A is a prerequisite of B
```

then the relationship cannot be represented correctly using an undirected graph.

A directed graph preserves this dependency information.

---

## Why Separate the Prerequisite Graph?

The complete curriculum graph can contain multiple relationship types:

```text
Contains
Prerequisite
Develops
RequiredFor
```

Learning-order computation should only consider:

```text
Topic → Prerequisite → Topic
```

Otherwise relationships such as:

```text
Course → Contains → Topic
```

could incorrectly influence prerequisite ordering.

Therefore the implementation constructs a dedicated prerequisite subgraph for prerequisite algorithms.

---

## Why Validate Before Commit?

An invalid graph can break downstream functionality.

For example, a prerequisite cycle can make topological sorting impossible.

Therefore graph edits follow:

```text
Edit
 ↓
Validation
 ↓
Algorithm Recalculation
 ↓
Commit / Rollback
```

This ensures that the graph remains structurally consistent.

---

# Scope and Limitations

## Included

The current implementation includes:

* Course nodes
* Topic nodes
* Course → Topic relationships
* Topic prerequisite relationships
* Topological sorting
* BFS
* DFS
* Degree Centrality
* Betweenness Centrality
* PageRank
* Cycle detection
* Self-loop validation
* Edge-type validation
* Orphan-reference validation
* Graph edit rollback
* FastAPI
* Streamlit
* PyVis
* Automated testing

---

## Skills and Roles

The graph schema supports:

```text
Topic → Develops → Skill
Skill → RequiredFor → Role
```

However, Skills and Roles are not populated in the current dataset.

They should therefore not be treated as available graph entities in the current implementation.

---

## API Persistence

Graph edits made through:

```text
POST /graph/edge
```

are currently maintained in memory.

They are not automatically written back to:

```text
data/curriculum.json
```

Persistent graph editing is a future improvement.

---

## Semantic Validation

The current validation layer performs structural validation.

For example, it can detect:

```text
A → B
B → C
C → A
```

as a cycle.

However, it does not determine whether a prerequisite relationship is academically meaningful.

For example, it does not independently determine whether:

```text
Linear Algebra
      ↓
Operating Systems
```

is a valid academic prerequisite.

Such semantic validation would require additional domain knowledge.

---

## Curriculum Version Management

Curriculum version information is part of the broader graph design.

A complete multi-version curriculum lifecycle is outside the current prototype scope.

---

## Graph Embeddings

Graph embeddings and advanced semantic graph representations are not included in the current implementation.

---

# Future Improvements

## 1. Persistent Graph Editing

Store validated graph modifications permanently.

Possible future architecture:

```text
FastAPI
   |
   v
Graph Service
   |
   v
Persistent Graph Store
```

---

## 2. Skill and Role Integration

Populate:

```text
Topic
  |
  | Develops
  v
Skill
  |
  | RequiredFor
  v
Role
```

This would connect curriculum learning with career-oriented skill requirements.

---

## 3. Curriculum Version Management

Support multiple curriculum versions and controlled version transitions.

For example:

```text
2023 Curriculum
       |
       v
2024 Curriculum
       |
       v
2025 Curriculum
```

---

## 4. Semantic Prerequisite Validation

Future versions could combine:

* domain knowledge
* semantic similarity
* expert validation
* language models

to evaluate whether prerequisite relationships are meaningful.

---

## 5. Graph Database Backend

For significantly larger graphs, the JSON + NetworkX architecture could be extended with a graph database such as Neo4j.

A possible architecture:

```text
FastAPI
   |
   v
Graph Service
   |
   v
Graph Database
   |
   +── Nodes
   +── Relationships
   +── Properties
```

---

## 6. Personalized Learning Paths

The graph could eventually be combined with student-specific information such as:

* completed courses
* completed topics
* current skills
* academic goals
* career goals

to generate personalized prerequisite-aware learning paths.

---

## 7. Graph Embeddings

Graph embeddings could be introduced for:

* semantic topic similarity
* related-topic recommendation
* curriculum clustering
* advanced graph reasoning

---

# Team Contribution

SafePath AI is divided into several major modules.

| Team Member  | Module                     |
| ------------ | -------------------------- |
| Chola Chetan | Student Digital Twin       |
| Evan Binu    | Curriculum Knowledge Graph |
| Jacob Isaac  | Goal-Based Planning        |
| David        | Dynamic Topic Retrieval    |

This repository focuses specifically on the **Curriculum Knowledge Graph** module.

---

# Contributing

When modifying the curriculum graph:

1. Preserve the existing graph schema.
2. Use supported node and relationship types.
3. Do not introduce prerequisite cycles.
4. Do not create prerequisite self-loops.
5. Ensure every referenced node exists.
6. Run the automated tests before committing.
7. Keep curriculum information traceable to its source.
8. Do not fabricate prerequisite relationships without an appropriate source or explicit domain justification.

Before submitting changes:

```bash
pytest -v
```

Verify the command-line application:

```bash
python main.py
```

Verify the API:

```bash
uvicorn api:app --reload
```

Verify the UI:

```bash
streamlit run app.py
```

---

# Quick Start

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd SafePath-AI-Curriculum-Graph
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the graph test:

```bash
python main.py
```

Run the API:

```bash
uvicorn api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Run the Streamlit interface in another terminal:

```bash
streamlit run app.py
```

Run the tests:

```bash
pytest -v
```

---

# Summary

The SafePath AI Curriculum Knowledge Graph transforms curriculum information into a structured, prerequisite-aware directed graph.

The implementation pipeline is:

```text
Curriculum / Syllabus
        ↓
Structured JSON
        ↓
NetworkX Directed Graph
        ↓
Graph Validation
        ↓
Graph Algorithms
        ↓
FastAPI
        ↓
Streamlit + PyVis
        ↓
Interactive Curriculum Analysis
```

The current implementation contains:

```text
8 Courses
210 Topics
218 Nodes
298 Relationships
90 Prerequisite Relationships
20 Passing Tests
```

The primary purpose of the module is not simply to store curriculum information.

It provides SafePath AI with the ability to **reason about curriculum structure**, particularly:

* prerequisite dependencies
* valid learning order
* topic connectivity
* downstream topic relationships
* structural bridge topics
* graph centrality
* graph integrity

This structural knowledge can then serve as a foundation for personalized academic planning and other SafePath AI components.


