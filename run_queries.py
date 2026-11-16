"""Run every query from kg/queries.py against Aura and write results/query_results.csv."""
import csv
import json
import time
from pathlib import Path

from kg.db import get_client
from kg.queries import QUERIES

OUT = Path(__file__).parent / "results" / "query_results.csv"


def main():
    client = get_client()
    print("connected via", client.transport)
    OUT.parent.mkdir(exist_ok=True)
    out_rows = []
    for i, (question, cypher) in enumerate(QUERIES, 1):
        t0 = time.perf_counter()
        records = client.run(cypher)
        ms = (time.perf_counter() - t0) * 1000
        out_rows.append({
            "Question": question,
            "Cypher Query": cypher,
            "Answer": json.dumps(records, ensure_ascii=False, default=str),
            "Execution Time": f"{ms:.1f} ms",
        })
        print(f"Q{i}: {len(records)} rows, {ms:.1f} ms")
    # utf-8-sig so Excel displays non-ASCII characters correctly
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["Question", "Cypher Query", "Answer", "Execution Time"], lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    print("wrote", OUT)
    client.close()


if __name__ == "__main__":
    main()
