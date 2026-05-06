# Literary Themes Ontology Knowledge Graph

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)

##  Project Overview & Goal
The **Literary Themes Ontology Knowledge Graph** is a project aimed at modeling a literary themes ontology and applying it to a corpus of annotated stories. 

The primary goal is to structurally represent literary themes, their hierarchical relationships (sub-themes / super-themes), as well as their occurrences and significance within literary works. The final output is a machine-readable Knowledge Graph that combines both the ontological structure and the story annotations.

##  Data Source
This project utilizes data from the publicly available [Theme Ontology Project](https://github.com/theme-ontology/theming). It includes:
* A defined ontology of several thousand literary themes.
* An annotated corpus of literary stories linked to these themes.

For this project, we are processing a reduced subset of this data to build our Knowledge Graph.

##  Basic Approach & Data Structure (Concept)
1. **Ontology Modeling:** Themes are modeled with their hierarchical relationships.
2. **Annotation Linking:** Stories are connected to specific themes.
3. **Enrichment:** Connections are enriched with weights (e.g., major vs. minor themes) and textual justifications.

##  Workflow & Data Flow
1. **Data Ingestion:** Raw data (themes and annotations) is loaded from the `literature/` directory.
2. **Graph Construction:** The `KG.py` script parses the data and builds the nodes (Themes, Stories) and edges (Relationships, Occurrences).
3. **Graph Export/Query:** The resulting Knowledge Graph is exported into a standardized format for further analysis or querying.

