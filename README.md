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
1. **Data Ingestion:** Raw annotation files (`.txt` format, currently focused on "plays") are loaded from the `literature/` directory.
2. **Data Extraction:** The `KG.py` script parses the text files to extract the title of the work and identifies associated themes categorized as major, minor, or choice themes.
3. **Edge List Generation:** The extracted relationships are exported into an `output.csv` file. This CSV serves as the foundational edge list (Work -> Theme, with the Type as the relationship property) for building the actual Knowledge Graph in the next steps.
4. **RDF Generation:** Based on the generated edge list (`output.csv`), the next step was to transform the extracted relationships into a machine-readable RDF representation. For this purpose, a second Python script (`rdf_script.py`) was developed using the **RDFLib** library. The script reads the generated CSV file and creates an RDF graph from the extracted data.

A unique **URI (Uniform Resource Identifier)** is created for every literary work and every literary theme. URIs ensure that each entity within the knowledge graph can be uniquely identified and referenced. This is a fundamental requirement for RDF-based knowledge graphs and enables further use in technologies such as SPARQL or integration with other knowledge graphs.
For each row in the CSV file, RDF triples are generated. The relationship between a literary work and one of its themes is represented by the property **`hasTheme`**. Additionally, the thematic importance is stored using the property **`themeType`**, indicating whether a theme is classified as **major**, **minor**, or **choice**.

The thematic weights are interpreted as follows:
- **minor** – The theme is present in the story but plays only a secondary role.
- **major** – The theme is important to the plot.
- **choice** – The theme is central to the story and significantly shapes its overall meaning.

Finally, the generated RDF graph is exported as an RDF/XML file named **`knowledge_graph.rdf`**, providing a machine-readable representation of the Literary Theme Knowledge Graph.
### Example
```text
Hamlet ── hasTheme ──► Revenge
Hamlet ── themeType ─► major
```
--- 

5. **Visualization in Wikibase** 

The data extraction process was initially tested using only the **play** category. This made it possible to verify that the Python script correctly extracted the titles of the literary works together with their associated **major**, **minor**, and **choice** themes and stored them in the generated `output.csv` file.

After this initial validation, the script was extended to process the complete literature dataset. In addition to **plays**, it now also extracts information from **novels**, **operas**, **short stories**, and **writings**. All extracted relationships are combined into a single `output.csv` file, providing a comprehensive basis for constructing the knowledge graph.

The next step was to import the generated RDF graph into **Wikibase Docker** in order to visualize the knowledge graph. Although the RDF file was imported successfully, the contained entities and relationships were not available within Wikibase as expected.

Therefore, an alternative approach was explored. Instead of importing the RDF file directly, the previously generated `output.csv` file was used as the basis for importing the data into **Wikibase Cloud**. This approach enables the extracted literary works, themes, and their relationships to be represented in Wikibase and serves as the foundation for the further development and visualization of the knowledge graph.
