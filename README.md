# galactacto

A collection of utilities for processing PDFs and generating interactive visualizations and videos using OpenAI APIs.

## Projects

### 1. Knowledge Graph Generator (kg4.py)
Extracts a simple knowledge graph from a PDF using the OpenAI Responses API, builds a NetworkX graph, and renders an interactive visualization as HTML.

**What kg4.py does:**
- Uploads a PDF to the OpenAI Files API and asks the model to extract entities and relations into a typed Pydantic schema.
- Builds a MultiDiGraph (NetworkX) from the extracted entities and relations (keeps evidence and page numbers).
- Exports graph files (out/kg.graphml and out/kg.gexf).
- Renders an interactive HTML visualization (knowledge_graph.html) using pyvis and opens it in your browser.

**Outputs:**
- knowledge_graph.html — interactive visualization (saved to repo root and opened automatically).
- out/kg.graphml, out/kg.gexf — graph exports.
- Optionally out/kg_<timestamp>.json if saving raw parsed output.

### 2. Instagram Reel Generator (reels.py) 🎬
**⚠️ IMPORTANT: This script contains HARDCODED PROMPTS and is designed for direct PDF-to-video generation.**

Generates 15-second Instagram Reels directly from PDF content using OpenAI's Sora video generation API.

**What reels.py does:**
- Extracts key information from PDFs (focuses on persons, companies, and their relations)
- Creates a single optimized video prompt for 15-second Instagram Reels
- Generates a direct video using Sora API (vertical format, 1080x1920)
- Creates a simple HTML preview with video player

**Key Features:**
- **15-second maximum duration** - Optimized for Instagram Reels
- **Direct PDF to video** - No intermediate script generation
- **Vertical format** - Instagram Reels optimized (9:16 aspect ratio)
- **Single video output** - One `direct_sora_reel.mp4` file

**⚠️ HARDCODED PROMPTS:**
The script contains hardcoded video generation prompts and may not work with all PDF content types. The prompts are optimized for business/company content with persons and relationships.

**Outputs:**
- `direct_sora_reel.mp4` - The generated 15-second video
- `video_prompt.txt` - The prompt used for Sora
- `reel_preview.html` - Simple preview page

## Requirements
- Python 3.9+
- Install dependencies:
  ```bash
  pip install openai networkx pyvis pydantic
  ```
- For reels.py video generation:
  ```bash
  pip install -r requirements_reels.txt
  ```

## Configuration
- Provide an OpenAI API key. The scripts currently accept an OpenAI client creation call; prefer setting an environment variable and updating the scripts to read it:
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```
- **Remove any hardcoded API keys before committing.**

## Run

### Knowledge Graph Generator
1. Place the PDF you want to process (default in script: `pdf_test2.pdf`) next to the script or update `PDF_PATH`.
2. Run:
   ```bash
   python3 kg4.py
   ```
3. The script will create `knowledge_graph.html` and open it in your default browser.

### Instagram Reel Generator
1. Place the PDF you want to process (default: `pdf_test2.pdf`) next to the script.
2. Run:
   ```bash
   python3 reels.py
   ```
3. The script will generate a 15-second video and open a preview in your browser.

## Notes
- The repo .gitignore is configured so only `kg4.py`, `knowledge_graph.html`, and `.gitignore` are kept at the root — other files are ignored.
- **reels.py contains hardcoded prompts** - may need customization for different content types.
- Inspect and sanitize any saved JSON outputs before sharing (may contain extracted text).
- Video generation requires OpenAI Sora API access.