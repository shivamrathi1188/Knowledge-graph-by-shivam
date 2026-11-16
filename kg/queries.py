"""The ten questions from queries.txt, each paired with a self-contained Cypher query (no parameters)."""

QUERIES = [
    ("Consortium roles: Which organizations participate in the ALPINE project, what role does each play "
     "(coordinator, materials, manufacturing, pilot operation), and which agency funds it?",
     """MATCH (f:Organization)-[fund:FUNDS]->(p:Project {name:'ALPINE'})
MATCH (o:Organization)-[r:PARTICIPATES_IN]->(p)
RETURN o.name AS organization, r.role AS role, r.contribution AS contribution,
       f.name AS funding_agency, fund.amount AS amount, fund.currency AS currency
ORDER BY CASE r.role WHEN 'coordinator' THEN 0 ELSE 1 END, organization"""),

    ("Publication output: For each project, list its publications together with the authors and their affiliations.",
     """MATCH (pr:Project)<-[:PRODUCED_IN]-(pa:Paper)<-[w:AUTHORED]-(a:Person)
WITH pr, pa, a, w ORDER BY w.position
WITH pr, pa, collect(a.name + ' (' + w.affiliation + ')') AS authors
RETURN pr.name AS project, pa.title AS publication, pa.year AS year, pa.journal AS journal, authors
ORDER BY project, year, publication"""),

    ("Academic lineage: Trace the complete supervision chain for every doctoral researcher "
     "(e.g. who is the 'academic grandparent' of Sofia Lindqvist and Tomas Berg?).",
     """MATCH p = (root:Person)-[:SUPERVISED*1..]->(s:Person)
WHERE NOT EXISTS { (:Person)-[:SUPERVISED {kind:'doctoral'}]->(root) }
  AND ALL(r IN relationships(p) WHERE r.kind = 'doctoral')
WITH s, nodes(p) AS chain
RETURN s.name AS doctoral_researcher,
       [n IN chain | n.name] AS supervision_chain_oldest_to_researcher,
       chain[-2].name AS supervisor,
       CASE WHEN size(chain) >= 3 THEN chain[-3].name ELSE null END AS academic_grandparent,
       size(chain) - 1 AS generations_from_root
ORDER BY doctoral_researcher"""),

    ("Mobility: Which researchers have been affiliated with more than one organization (employment or study), "
     "and what was the direction of each move?",
     """MATCH (p:Person)-[a:AFFILIATED_WITH]->(o:Organization)
WITH p, a, o ORDER BY a.seq
WITH p, collect({org: o.name, kind: a.kind, start: a.start, end: a.end}) AS stops, count(DISTINCT o) AS orgs
WHERE orgs > 1
RETURN p.name AS researcher, orgs AS organizations_count,
       [i IN range(0, size(stops) - 2) |
         stops[i].org + ' (' + stops[i].kind + ') -> ' + stops[i+1].org + ' (' + stops[i+1].kind + ')'
         + CASE WHEN stops[i+1].start IS NULL THEN '' ELSE ', from ' + toString(stops[i+1].start) END] AS moves
ORDER BY researcher"""),

    ("Funding overview: For each funding agency, list the projects funded, amounts and currencies, "
     "and which companies and utilities take part in those projects.",
     """MATCH (f:Organization {type:'FundingAgency'})-[fund:FUNDS]->(p:Project)
OPTIONAL MATCH (c:Organization)-[:PARTICIPATES_IN]->(p) WHERE c.type IN ['Company', 'Utility']
WITH f, p, fund, collect(DISTINCT c.name + ' (' + c.type + ')') AS industry_participants
RETURN f.name AS funding_agency, p.name AS project, fund.amount AS amount, fund.currency AS currency,
       industry_participants
ORDER BY funding_agency, project"""),

    ("International reach: Rank researchers by the number of distinct countries represented among their "
     "co-authors (excluding their own).",
     """MATCH (a:Person) WHERE EXISTS { (a)-[:AUTHORED]->(:Paper) }
OPTIONAL MATCH (a)-[wa:AUTHORED]->(:Paper)<-[wb:AUTHORED]-(b:Person) WHERE b <> a
OPTIONAL MATCH (:Organization {name: wa.affiliation})-[:LOCATED_IN]->(own:Country)
OPTIONAL MATCH (:Organization {name: wb.affiliation})-[:LOCATED_IN]->(other:Country)
WITH a, collect(DISTINCT CASE WHEN other IS NOT NULL AND other <> own THEN other.name END) AS countries
WITH collect({name: a.name, n: size(countries), countries: countries}) AS rows
UNWIND rows AS r
RETURN size([x IN rows WHERE x.n > r.n]) + 1 AS rank, r.name AS researcher,
       r.n AS distinct_foreign_coauthor_countries, r.countries AS countries
ORDER BY rank, researcher"""),

    ("Citation influence: Which publications cite the 2022 cathode stability paper, directly or indirectly "
     "(transitive citation chain)?",
     """MATCH (target:Paper {title: 'Sodium-Ion Cathode Stability in Solid-State Electrolytes'})
MATCH path = (p:Paper)-[:CITES*1..]->(target)
WITH p, path ORDER BY length(path)
WITH p, collect(path)[0] AS shortest
RETURN p.title AS citing_publication, p.year AS year,
       CASE WHEN length(shortest) = 1 THEN 'direct' ELSE 'indirect' END AS citation_type,
       length(shortest) AS hops,
       [n IN nodes(shortest) | n.title] AS citation_chain
ORDER BY hops, year, citing_publication"""),

    ("Collaboration horizon: Starting from the Halvorsen Institute of Technology, which organizations are "
     "reachable within two project-collaboration hops, and through which projects?",
     """CALL () {
  MATCH (s:Organization {name: 'Halvorsen Institute of Technology'})-[:PARTICIPATES_IN]->(p:Project)
        <-[:PARTICIPATES_IN]-(o:Organization)
  WHERE o <> s
  RETURN o, 1 AS hops, s.name + ' -[' + p.name + ']- ' + o.name AS route, [p.name] AS projects
  UNION
  MATCH (s:Organization {name: 'Halvorsen Institute of Technology'})-[:PARTICIPATES_IN]->(p1:Project)
        <-[:PARTICIPATES_IN]-(m:Organization)-[:PARTICIPATES_IN]->(p2:Project)
        <-[:PARTICIPATES_IN]-(o:Organization)
  WHERE m <> s AND o <> s AND o <> m AND p1 <> p2
  RETURN o, 2 AS hops,
         s.name + ' -[' + p1.name + ']- ' + m.name + ' -[' + p2.name + ']- ' + o.name AS route,
         [p1.name, p2.name] AS projects
}
WITH o, hops, collect(route) AS routes
ORDER BY hops
WITH o, collect({hops: hops, routes: routes}) AS by_distance
RETURN o.name AS organization, by_distance[0].hops AS min_hops, by_distance[0].routes AS routes
ORDER BY min_hops, organization"""),

    ("Intellectual property to field: Which sites use technology covered by a patent held by Lumen Storage "
     "Systems, and which projects, operators and inventors are connected to them?",
     """MATCH (:Organization {name: 'Lumen Storage Systems'})<-[:HELD_BY]-(pt:Patent)<-[:USES_PATENT]-(s:Site)
OPTIONAL MATCH (s)-[:BUILT_UNDER]->(pr:Project)
OPTIONAL MATCH (s)-[:OPERATED_BY]->(op:Organization)
OPTIONAL MATCH (inv:Person)-[:INVENTOR_OF]->(pt)
RETURN s.name AS site, pt.id AS patent, collect(DISTINCT pr.name) AS projects,
       collect(DISTINCT op.name) AS operators, collect(DISTINCT inv.name) AS inventors
ORDER BY site"""),

    ("Collaborator recommendation: Suggest pairs of researchers who have never co-authored but share at least "
     "one common co-author, and whose work relates to the same technology area.",
     """MATCH (a:Person)-[:AUTHORED]->(:Paper)<-[:AUTHORED]-(c:Person)-[:AUTHORED]->(:Paper)<-[:AUTHORED]-(b:Person)
WHERE a.name < b.name AND c <> a AND c <> b
  AND NOT EXISTS { (a)-[:AUTHORED]->(:Paper)<-[:AUTHORED]-(b) }
WITH a, b, collect(DISTINCT c.name) AS common_coauthors
MATCH (a)-[:AUTHORED]->(:Paper)-[:ABOUT]->(t:Technology)<-[:ABOUT]-(:Paper)<-[:AUTHORED]-(b)
WITH a, b, common_coauthors, collect(DISTINCT t.name) AS shared_technology_areas
RETURN a.name AS researcher_1, b.name AS researcher_2, common_coauthors, shared_technology_areas
ORDER BY size(shared_technology_areas) DESC, size(common_coauthors) DESC, researcher_1, researcher_2"""),
]
