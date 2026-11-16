# Energy Research Knowledge Graph (Neo4j Aura)

Builds a knowledge graph from the 35 text files in `energy_research_corpus/corpus/` and answers the ten
questions in `queries.txt` with Cypher. The graded deliverable is **`results/query_results.csv`**
(columns: `Question`, `Cypher Query`, `Answer`, `Execution Time`).

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # Windows: copy .env.example .env
# edit .env with your Neo4j Aura credentials (this file is git-ignored, never commit it)

python build_graph.py              # idempotent load (MERGE); add --reset to rebuild from scratch
python run_queries.py              # writes results/query_results.csv
```

## Project layout
| Path | Purpose |
|---|---|
| `energy_research_corpus/corpus/*.txt` | Source documents (organizations, projects, people, papers, sites, patent, technologies, event) |
| `kg/graph_data.py` | Facts extracted from the corpus (entities and relationships) |
| `kg/db.py` | Neo4j connection layer (Bolt, with automatic HTTPS Query API fallback) |
| `build_graph.py` | Creates uniqueness constraints and loads the graph |
| `kg/queries.py` | One self-contained Cypher query per question |
| `run_queries.py` | Runs the queries, records answers and timings |
| `queries.txt` | The ten questions |
| `results/query_results.csv` | Deliverable: Question, Cypher Query, Answer, Execution Time |
| `.env.example` | Template for credentials |

## Graph model
Nodes: `Organization` (type: University / Company / Utility / FundingAgency), `Person`, `Project`, `Paper`,
`Site`, `Patent`, `Technology`, `Event`, `Country`.

Relationships: `FUNDS`, `PARTICIPATES_IN {role}`, `AFFILIATED_WITH {kind, seq, start, end}`,
`SUPERVISED {kind, year}`, `PRINCIPAL_INVESTIGATOR_OF`, `AUTHORED {position, affiliation}`, `PRODUCED_IN`,
`ABOUT`, `CITES`, `BUILT_UNDER`, `OPERATED_BY`, `SUPPLIED_CELLS_TO`, `USES_PATENT`, `HELD_BY`, `INVENTOR_OF`,
`DESCRIBES_BACKGROUND_OF`, `MANAGES`, `HOSTED`, `PARTICIPATED_IN`, `PRESENTED_AT`, `INSTITUTIONAL_LINK`, `LOCATED_IN`.

## Assumptions
- Transport: uses Bolt when port 7687 is reachable, otherwise Aura's HTTPS Query API (port 443).
- Execution Time is client-side wall time per query, including network round trip.
- Sofia Lindqvist's HIT affiliation is inferred (supervised by Solberg; linked to HIT in the 2025 paper).
- "Collaboration hops" count shared participation in a project; funding agencies are excluded.
- "Co-author country" uses the author's affiliation at the time of each paper.
- Academic lineage follows `kind = 'doctoral'` supervision only (Elena Voss's postdoc hosting is excluded).
- Priya Raghunathan's 2019 stay at Maple Ridge is a temporary sabbatical visit; it is shown as a move to
  `Maple Ridge University (visiting)` in the Mobility answer.

## Security
`.env` holds live database credentials and is excluded by `.gitignore`. Never commit or share it.
