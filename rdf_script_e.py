import csv
from rdflib import Graph, URIRef, Literal, Namespace
import re

# Create a new RDF graph
g = Graph()

# Define a custom namespace
# All entities in the knowledge graph will later receive a unique URI
# Example:
# http://example.org/Hamlet
# http://example.org/revenge
#
# RDF and Knowledge Graphs work with URIs
# so that every resource can be uniquely identified.
#
# This is important for:
# - RDF in general
# - SPARQL queries
# - Visualization in tools such as Protégé or Wikibase
# - Linking with other knowledge graphs
#
# EX is used as a shortcut for:
# http://example.org/
EX = Namespace("http://example.org/")

# Open the CSV file
with open("output.csv", "r", encoding="utf-8") as file:

    # Read the CSV file as a dictionary
    # This allows access via column names
    reader = csv.DictReader(file)

    # Iterate through each row in the CSV file
    for row in reader:

        # Retrieve values from the columns
        # .get() prevents errors if a column is missing
        # .strip() removes whitespace and line breaks
        work = (row.get("Work") or "").strip()
        theme = (row.get("Theme") or "").strip()
        theme_type = (row.get("Type") or "").strip()

        # Skip rows with missing work or theme values
        if not work or not theme:
            continue

        # Make names URI-safe
        # All special characters are replaced with "_"
        #
        # Example:
        # "love vs. career" -> "love_vs__career"
        #
        # This is necessary because some characters
        # are not allowed in RDF URIs
        work_name = re.sub(r'[^a-zA-Z0-9_]', '_', work)
        theme_name = re.sub(r'[^a-zA-Z0-9_]', '_', theme)

        # Create a URI for the literary work
        # Example:
        # http://example.org/Hamlet
        work_uri = URIRef(EX + work_name)

        # Create a URI for the theme
        # Example:
        # http://example.org/revenge
        theme_uri = URIRef(EX + theme_name)

        # Add RDF triple:
        # Work -> hasTheme -> Theme
        #
        # Example:
        # Hamlet -> hasTheme -> revenge
        g.add((work_uri, EX.hasTheme, theme_uri))

        # Add RDF triple:
        # Work -> themeType -> major/minor/choice
        #
        # Note:
        # This is a simplified modeling approach.
        # Currently, the theme type is directly assigned to the work.
        #
        # In a more advanced knowledge graph,
        # a separate intermediate entity for themes could be introduced.
        g.add((work_uri, EX.themeType, Literal(theme_type)))

# Save the RDF file
# format="xml" creates RDF/XML
g.serialize("knowledge_graph.rdf", format="xml")

print("RDF file has been created!")