# galactacto

A small utility that extracts a simple knowledge graph from a PDF using the OpenAI Responses API, builds a NetworkX graph, and renders an interactive visualization as HTML.

## What kg4.py does (summary)
- Uploads a PDF to the OpenAI Files API and asks the model to extract entities and relations into a typed Pydantic schema.
- Builds a MultiDiGraph (NetworkX) from the extracted entities and relations (keeps evidence and page numbers).
- Exports graph files (out/kg.graphml and out/kg.gexf).
- Renders an interactive HTML visualization (knowledge_graph.html) using pyvis and opens it in your browser.

## Outputs
- knowledge_graph.html — interactive visualization (saved to repo root and opened automatically).
- out/kg.graphml, out/kg.gexf — graph exports.
- Optionally out/kg_<timestamp>.json if saving raw parsed output.

## Requirements
- Python 3.9+
- Install dependencies:
  pip install openai networkx pyvis pydantic

## Configuration
- Provide an OpenAI API key. The script currently accepts an OpenAI client creation call; prefer setting an environment variable and updating the script to read it:
  export OPENAI_API_KEY="sk-..."
- Remove any hardcoded API key before committing.

## Run
1. Place the PDF you want to process (default in script: `pdf_test2.pdf`) next to the script or update `PDF_PATH`.
2. Run:
   python3 kg4.py
3. The script will create `knowledge_graph.html` and open it in your default browser.

## Notes
- The repo .gitignore is configured so only `kg4.py`, `knowledge_graph.html`, and `.gitignore` are kept at the root — other files are ignored.
- Inspect and sanitize any saved JSON outputs before sharing (may contain extracted text).