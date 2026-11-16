"""Create/refresh the knowledge graph in Neo4j Aura. Idempotent (MERGE); use --reset to wipe first."""
import sys
from kg.db import get_client
from kg import graph_data as d

CONSTRAINTS = [
    "CREATE CONSTRAINT org_name IF NOT EXISTS FOR (n:Organization) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (n:Person) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT project_name IF NOT EXISTS FOR (n:Project) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT paper_key IF NOT EXISTS FOR (n:Paper) REQUIRE n.key IS UNIQUE",
    "CREATE CONSTRAINT site_name IF NOT EXISTS FOR (n:Site) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT patent_id IF NOT EXISTS FOR (n:Patent) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT tech_name IF NOT EXISTS FOR (n:Technology) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT event_name IF NOT EXISTS FOR (n:Event) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT country_name IF NOT EXISTS FOR (n:Country) REQUIRE n.name IS UNIQUE",
]


PROJECT_LABELS = ["Organization", "Person", "Project", "Paper", "Site", "Patent", "Technology", "Event", "Country"]


def rows(keys, data):
    return [dict(zip(keys, r)) for r in data]


STEPS = [
    ("countries", "UNWIND $rows AS r MERGE (:Country {name:r.name})",
     [{"name": c} for c in d.COUNTRIES]),
    ("organizations",
     """UNWIND $rows AS r MERGE (o:Organization {name:r.name})
        SET o.short=r.short, o.type=r.type, o.city=r.city, o.founded=r.founded
        WITH o, r MATCH (c:Country {name:r.country}) MERGE (o)-[:LOCATED_IN]->(c)""",
     rows(["name", "short", "type", "city", "country", "founded"], d.ORGANIZATIONS)),
    ("projects", "UNWIND $rows AS r MERGE (p:Project {name:r.name}) SET p.start=r.start, p.end=r.end",
     rows(["name", "start", "end"], d.PROJECTS)),
    ("funding",
     """UNWIND $rows AS r MATCH (f:Organization {name:r.funder}), (p:Project {name:r.project})
        MERGE (f)-[x:FUNDS]->(p) SET x.amount=r.amount, x.currency=r.currency""",
     rows(["funder", "project", "amount", "currency"], d.FUNDING)),
    ("participation",
     """UNWIND $rows AS r MATCH (o:Organization {name:r.org}), (p:Project {name:r.project})
        MERGE (o)-[x:PARTICIPATES_IN]->(p) SET x.role=r.role, x.contribution=r.contribution""",
     rows(["org", "project", "role", "contribution"], d.PARTICIPATION)),
    ("people", "UNWIND $rows AS r MERGE (p:Person {name:r.name}) SET p.title=r.title",
     rows(["name", "title"], d.PEOPLE)),
    ("affiliations",
     """UNWIND $rows AS r MATCH (p:Person {name:r.person}), (o:Organization {name:r.org})
        MERGE (p)-[x:AFFILIATED_WITH {kind:r.kind}]->(o) SET x.seq=r.seq, x.start=r.start, x.end=r.end""",
     rows(["person", "org", "kind", "seq", "start", "end"], d.AFFILIATIONS)),
    ("supervision",
     """UNWIND $rows AS r MATCH (s:Person {name:r.sup}), (t:Person {name:r.stu})
        MERGE (s)-[x:SUPERVISED {kind:r.kind}]->(t) SET x.year=r.year""",
     rows(["sup", "stu", "kind", "year"], d.SUPERVISION)),
    ("principal investigators",
     """UNWIND $rows AS r MATCH (p:Person {name:r.person}), (j:Project {name:r.project})
        MERGE (p)-[:PRINCIPAL_INVESTIGATOR_OF]->(j)""",
     rows(["person", "project"], d.PRINCIPAL_INVESTIGATORS)),
    ("technologies", "UNWIND $rows AS r MERGE (:Technology {name:r.name})",
     [{"name": t} for t in d.TECHNOLOGIES]),
    ("papers",
     """UNWIND $rows AS r MERGE (p:Paper {key:r.key}) SET p.title=r.title, p.year=r.year, p.journal=r.journal
        WITH p, r MATCH (j:Project {name:r.project}) MERGE (p)-[:PRODUCED_IN]->(j)
        WITH p, r UNWIND r.techs AS t MATCH (x:Technology {name:t}) MERGE (p)-[:ABOUT]->(x)""",
     [dict(zip(["key", "title", "year", "journal", "project", "authors", "techs"], p)) for p in d.PAPERS]),
    ("authorship",
     """UNWIND $rows AS r MATCH (p:Paper {key:r.key}), (a:Person {name:r.author})
        MERGE (a)-[x:AUTHORED]->(p) SET x.position=r.pos, x.affiliation=r.aff""",
     [{"key": p[0], "author": a, "aff": aff, "pos": i + 1}
      for p in d.PAPERS for i, (a, aff) in enumerate(p[5])]),
    ("citations",
     "UNWIND $rows AS r MATCH (a:Paper {key:r.a}), (b:Paper {key:r.b}) MERGE (a)-[:CITES]->(b)",
     [{"a": a, "b": b} for a, b in d.CITATIONS]),
    ("patent", None, None),  # handled separately (scalar params)
    ("sites",
     """UNWIND $rows AS r MERGE (s:Site {name:r.name}) SET s.commissioned=r.year, s.system=r.system
        WITH s, r MATCH (c:Country {name:r.country}) MERGE (s)-[:LOCATED_IN]->(c)
        WITH s, r MATCH (j:Project {name:r.project}) MERGE (s)-[:BUILT_UNDER]->(j)
        WITH s, r UNWIND r.operators AS op MATCH (o:Organization {name:op}) MERGE (s)-[:OPERATED_BY]->(o)""",
     [{"name": s[0], "country": s[1], "year": s[2], "project": s[3], "operators": s[4],
       "system": s[7]} for s in d.SITES]),
    ("site cells and patent usage",
     """UNWIND $rows AS r MATCH (s:Site {name:r.name}), (o:Organization {name:r.supplier})
        MERGE (o)-[:SUPPLIED_CELLS_TO]->(s)
        WITH s, r WHERE r.patent IS NOT NULL MATCH (t:Patent {id:r.patent}) MERGE (s)-[:USES_PATENT]->(t)""",
     [{"name": s[0], "supplier": s[5], "patent": s[6]} for s in d.SITES if s[5]]),
    ("site managers",
     "UNWIND $rows AS r MATCH (p:Person {name:r.p}), (s:Site {name:r.s}) MERGE (p)-[:MANAGES]->(s)",
     [{"p": p, "s": s} for p, s in d.SITE_MANAGERS]),
    ("events",
     """UNWIND $rows AS r MERGE (e:Event {name:r.name}) SET e.year=r.year, e.location=r.loc
        WITH e, r MATCH (o:Organization {name:r.host}) MERGE (o)-[:HOSTED]->(e)""",
     rows(["name", "year", "host", "loc"], d.EVENTS)),
    ("event roles",
     """UNWIND $rows AS r MATCH (p:Person {name:r.p}), (e:Event {name:r.e})
        MERGE (p)-[x:PARTICIPATED_IN]->(e) SET x.role=r.role""",
     [{"p": p, "e": e, "role": ro} for p, e, ro in d.EVENT_ROLES]),
    ("papers presented",
     "UNWIND $rows AS r MATCH (p:Paper {key:r.p}), (e:Event {name:r.e}) MERGE (p)-[:PRESENTED_AT]->(e)",
     [{"p": p, "e": e} for p, e in d.PAPERS_PRESENTED]),
    ("org links",
     """UNWIND $rows AS r MATCH (a:Organization {name:r.a}), (b:Organization {name:r.b})
        MERGE (a)-[x:INSTITUTIONAL_LINK {type:r.t}]->(b)""",
     [{"a": a, "b": b, "t": t} for a, b, t in d.ORG_LINKS]),
]

PATENT_CYPHER = """
MERGE (t:Patent {id:$id}) SET t.title=$title, t.filed=$filed, t.granted=$granted
WITH t MATCH (h:Organization {name:$holder}) MERGE (t)-[:HELD_BY]->(h)
WITH t MATCH (p:Paper {key:$paper}) MERGE (p)-[:DESCRIBES_BACKGROUND_OF]->(t)
WITH t UNWIND $inventors AS n MATCH (i:Person {name:n}) MERGE (i)-[:INVENTOR_OF]->(t)
"""


def main():
    client = get_client()
    print("connected via", client.transport)
    if "--reset" in sys.argv:
        # Only removes nodes created by this project (its own labels); never touches other data in the instance.
        client.run("MATCH (n) WHERE any(l IN labels(n) WHERE l IN $labels) DETACH DELETE n", labels=PROJECT_LABELS)
        print("removed previous knowledge-graph nodes (other data untouched)")
    for c in CONSTRAINTS:
        client.run(c)
    for name, cypher, data in STEPS:
        if name == "patent":
            p = d.PATENT
            client.run(PATENT_CYPHER, id=p["id"], title=p["title"], filed=p["filed"], granted=p["granted"],
                       holder=p["holder"], paper=p["described_in_paper"], inventors=p["inventors"])
        else:
            client.run(cypher, rows=data)
        print("loaded", name)
    n = client.run("MATCH (n) WHERE any(l IN labels(n) WHERE l IN $labels) RETURN count(n) AS c", labels=PROJECT_LABELS)[0]["c"]
    r = client.run("MATCH (a)-[r]->(b) WHERE any(l IN labels(a) WHERE l IN $labels) RETURN count(r) AS c", labels=PROJECT_LABELS)[0]["c"]
    print(f"knowledge graph: {n} nodes and {r} relationships")
    client.close()


if __name__ == "__main__":
    main()
