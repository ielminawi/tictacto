from openai import OpenAI
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import json, os, time
import networkx as nx
from pyvis.network import Network
import webbrowser

# Robust extraction (SDK 2.x)
def extract_json_text(r):
    if hasattr(r, "output_text"):
        return r.output_text
    for item in getattr(r, "output", []) or []:
        for c in getattr(item, "content", []) or []:
            if getattr(c, "type", "") in ("output_text", "input_text"):
                if hasattr(c, "text"): return c.text
    raise ValueError("No JSON text found in response.")

class Entity(BaseModel):
    id: str
    name: str
    information: str
    payment: str
    logistics: str
    health: str
    preferences: str
    red_flags: str
    label: Optional[Literal["ORG","PERSON","PRODUCT","PROCESS","TOOL","GPE","OTHER"]] = "OTHER"

class Relation(BaseModel):
    head: str  # entity id
    rel: str   # e.g., PARTNERED_WITH, USES, ACQUIRED
    tail: str  # entity id
    page: Optional[int] = None
    evidence: Optional[str] = Field(default=None, description="Short quote/sentence")

class KnowledgeGraph(BaseModel):
    entities: List[Entity] = Field(default_factory=list)
    relations: List[Relation] = Field(default_factory=list)

create_json = 1
if create_json:
    client = OpenAI(api_key="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")  # or OpenAI(api_key="sk-...")

    PDF_PATH = "pdf_test2.pdf"

    # 1) Upload PDF
    pdf = client.files.create(file=open(PDF_PATH, "rb"), purpose="assistants")

    prompt = (
        "From the attached PDF, extract ENTITIES and RELATIONS for a knowledge graph. "
        "Prefer Companies and People and try to find out their relation. " \
        "For People, try to extract information about their position, their preferences and red flags"
        "For Organisations, try to extract information about payments, logistics and the health of relationship"
        "Return ONLY fields that fit the provided schema. "
        "For relations, include a short evidence. "
        "For rel in relations, try to summarize the evidence in a few words. "
        "If uncertain, omit and fill with zeros."
    )

    response = client.responses.parse(               # ← Pydantic-parsed output
        model="gpt-5", # gpt-4o-2024-08-06
        #reasoning={ "effort": "low" },
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_file", "file_id": pdf.id}
            ]
        }],
        text_format=KnowledgeGraph,                  # ← your Pydantic model
        max_output_tokens=10000
    )

    kg_obj: KnowledgeGraph = response.output_parsed

    kg = kg_obj.model_dump()

    # # Optional: save JSON output
    # os.makedirs("out", exist_ok=True)
    # stamp = time.strftime("%Y%m%d-%H%M%S")
    # json_path = f"out/kg_{stamp}.json"

    # with open(json_path, "w", encoding="utf-8") as f:
    #     json.dump(kg_obj.model_dump(), f, ensure_ascii=False, indent=2)

    # print("Saved:", json_path)

G = nx.MultiDiGraph()  # keeps multiple edges with evidence

# Add nodes
for e in kg.get("entities", []):
    eid = e.get("id") or e["name"].lower().strip()
    G.add_node(
        eid,
        name=e.get("name", ""),
        label=e.get("label", ""),
        information=e.get("information", ""),
        payment=e.get("payment", ""),
        logistics=e.get("logistics", ""),
        health=e.get("health", ""),
        preferences=e.get("preferences", ""),
        red_flags=e.get("red_flags", "")
    )

# Add edges with evidence + page
for r in kg.get("relations", []):
    head = r["head"]; tail = r["tail"]
    G.add_edge(
        head, tail,
        rel=r.get("rel","REL"),
        page=r.get("page"),
        evidence=r.get("evidence","")
    )

# Export graph files
nx.write_graphml(G, "out/kg.graphml")
nx.write_gexf(G, "out/kg.gexf")

# Quick interactive HTML (hover shows evidence)
net = Network(height="720px", width="100%", directed=True, bgcolor="#ffffff")

# size nodes by degree, color by label (optional)
deg = dict(G.degree())
palette = {"ORG":"#6aa9ff","PERSON":"#ffb866","PROCESS":"#9fe29f","PRODUCT":"#d6b3ff"}
for n, attrs in G.nodes(data=True):
    # build tooltip text with all your extended fields
    lines = [
        f"Name: {attrs.get('name','')}",
        f"Label: {attrs.get('label','')}",
        f"Information: {attrs.get('information','')}",
        f"Payment: {attrs.get('payment','')}",
        f"Logistics: {attrs.get('logistics','')}",
        f"Health: {attrs.get('health','')}",
        f"Preferences: {attrs.get('preferences','')}",
        f"Red Flags: {attrs.get('red_flags','')}",
    ]
    tooltip = "\n".join([s for s in lines if s and not s.endswith(': ')])  # no empty fieldsd

    net.add_node(
        n,
        label=attrs.get("name", n),
        title=tooltip,                # ← this is the hover text
        shape="dot",
        color="#6aa9ff" if attrs.get("label") == "ORG" else "#ffb366"
    )
for u, v, d in G.edges(data=True):
    net.add_edge(
        u, v,
        label=d.get('rel',''),
        title=f"p.{d.get('page','?')}: {d.get('evidence','')}"
    )

# Configure physics for better layout
# forceAtlas2Based parameters:
# gravitationalConstant = more negative → stronger repulsion
# spring_length = length of connecting arrows
# centralGravity = pull to center; lower → more spread
# springConstant = weaker spring → more spacing
net.set_options("""
{
  "layout": { "randomSeed": 42 },
  "nodes": {
    "shape": "dot",
    "scaling": { "min": 8, "max": 36 },
    "font": { "size": 14 }
  },
  "edges": {
    "arrows": { "to": { "enabled": true, "scaleFactor": 0.7 } },
    "smooth": { "enabled": true, "type": "dynamic"}
  },
  "physics": {
    "solver": "forceAtlas2Based",
    "stabilization": { "iterations": 300 },
    "forceAtlas2Based": {
      "gravitationalConstant": -80,
      "centralGravity": 0.01,
      "springLength": 250,   
      "springConstant": 0.01,
      "damping": 0.85,
      "avoidOverlap": 1
    }
  }
}
""")

# Generate Knowledge Graph HTML
net.write_html("knowledge_graph.html", notebook=False, local=True)
webbrowser.open('file://' + os.path.abspath("knowledge_graph.html"))


