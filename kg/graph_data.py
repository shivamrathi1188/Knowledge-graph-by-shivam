"""Structured facts extracted (by hand, from the 35 corpus files) for the knowledge graph.

Every fact below is stated in energy_research_corpus/corpus/*.txt, except the items
flagged INFERRED, which are implied rather than stated.
"""

COUNTRIES = ["Norway", "Germany", "India", "Canada", "Belgium"]

# name, short, type, city, country, founded, source file
ORGANIZATIONS = [
    ("Halvorsen Institute of Technology", "HIT", "University", "Trondheim", "Norway", 1962),
    ("Rhine Valley University", "RVU", "University", "Karlsruhe", "Germany", 1957),
    ("Southern Peninsula Institute of Science", "SPIS", "University", "Chennai", "India", 1985),
    ("Maple Ridge University", "MRU", "University", "Vancouver", "Canada", 1968),
    ("Lumen Storage Systems", "Lumen", "Company", "Munich", "Germany", 2014),
    ("Fjordgrid AS", "Fjordgrid", "Utility", "Bergen", "Norway", None),
    ("Deccan Power Corporation", "Deccan", "Utility", "Hyderabad", "India", None),
    ("Pacific Cell Technologies", "Pacific Cell", "Company", "Vancouver", "Canada", 2017),
    ("European Clean Energy Council", "ECEC", "FundingAgency", "Brussels", "Belgium", 2010),
    ("National Science Endowment of India", "NSEI", "FundingAgency", "New Delhi", "India", None),
    ("Canadian Innovation Fund", "CIF", "FundingAgency", "Ottawa", "Canada", None),
]

# name, start, end, topic
PROJECTS = [
    ("ALPINE", 2021, 2025), ("MONSOON", 2022, 2027),
    ("CASCADE", 2022, 2025), ("RECLAIM", 2022, 2027),
]

# funder, project, amount, currency
FUNDING = [
    ("European Clean Energy Council", "ALPINE", 4_200_000, "EUR"),
    ("European Clean Energy Council", "RECLAIM", 3_100_000, "EUR"),
    ("National Science Endowment of India", "MONSOON", 380_000_000, "INR"),
    ("Canadian Innovation Fund", "CASCADE", 2_800_000, "CAD"),
]

# organization, project, role, contribution
PARTICIPATION = [
    ("Halvorsen Institute of Technology", "ALPINE", "coordinator", "Coordinated the consortium"),
    ("Rhine Valley University", "ALPINE", "materials", "Developed solid-state electrolytes"),
    ("Lumen Storage Systems", "ALPINE", "manufacturing", "Manufactured the cells"),
    ("Fjordgrid AS", "ALPINE", "pilot operation", "Operated the pilot"),
    ("Southern Peninsula Institute of Science", "MONSOON", "coordinator", "Leads the project"),
    ("Deccan Power Corporation", "MONSOON", "utility partner", "Grid connection and operational data"),
    ("Maple Ridge University", "MONSOON", "modelling", "Contributes modelling expertise"),
    ("Maple Ridge University", "CASCADE", "coordinator", "Leads the project"),
    ("Pacific Cell Technologies", "CASCADE", "software integration", "Integrated algorithms into commercial software"),
    ("Halvorsen Institute of Technology", "CASCADE", "degradation models", "Provided battery degradation models"),
    ("Rhine Valley University", "RECLAIM", "coordinator", "Leads the project"),
    ("Lumen Storage Systems", "RECLAIM", "industrial partner", "Supplies production scrap and used cells"),
]

# name, title/role
PEOPLE = [
    ("Ingrid Solberg", "Professor"),
    ("Markus Weber", "Professor"),
    ("Priya Raghunathan", "Associate Professor"),
    ("Daniel Okafor", "Professor"),
    ("Elena Voss", "Chief Technology Officer"),
    ("Tomas Berg", "Lead storage engineer"),
    ("Katarina Novak", "Senior researcher"),
    ("Li Wei", "Research scientist"),
    ("Hannah Brooks", "Head of software division"),
    ("Sofia Lindqvist", "Doctoral student"),   # affiliation INFERRED: supervised by Solberg at HIT (docs 16, 27)
    ("Arjun Menon", "Doctoral student"),
    ("Rahul Venkatesan", "Project manager"),
]

# person, org, kind, seq (chronological order for that person), from, to (None = open / unstated)
AFFILIATIONS = [
    ("Ingrid Solberg", "Rhine Valley University", "study", 1, None, 2005),
    ("Ingrid Solberg", "Halvorsen Institute of Technology", "employment", 2, 2008, None),
    ("Markus Weber", "Rhine Valley University", "employment", 1, None, None),
    ("Priya Raghunathan", "Southern Peninsula Institute of Science", "employment", 1, None, None),
    ("Priya Raghunathan", "Maple Ridge University", "visiting", 2, 2019, 2019),
    ("Daniel Okafor", "Maple Ridge University", "employment", 1, None, None),
    ("Elena Voss", "Rhine Valley University", "postdoc", 1, 2015, 2019),
    ("Elena Voss", "Lumen Storage Systems", "employment", 2, 2019, None),
    ("Tomas Berg", "Halvorsen Institute of Technology", "study", 1, None, 2016),
    ("Tomas Berg", "Fjordgrid AS", "employment", 2, 2016, None),
    ("Katarina Novak", "Rhine Valley University", "employment", 1, None, None),
    ("Li Wei", "Maple Ridge University", "employment", 1, None, None),
    ("Hannah Brooks", "Maple Ridge University", "study", 1, None, 2018),
    ("Hannah Brooks", "Pacific Cell Technologies", "employment", 2, 2018, None),
    ("Sofia Lindqvist", "Halvorsen Institute of Technology", "study", 1, None, None),
    ("Arjun Menon", "Southern Peninsula Institute of Science", "study", 1, None, None),
    ("Rahul Venkatesan", "Deccan Power Corporation", "employment", 1, None, None),
]

# supervisor, student, kind, year (graduation year, None if ongoing)
SUPERVISION = [
    ("Markus Weber", "Ingrid Solberg", "doctoral", 2005),
    ("Ingrid Solberg", "Tomas Berg", "doctoral", 2016),
    ("Ingrid Solberg", "Sofia Lindqvist", "doctoral", None),
    ("Daniel Okafor", "Hannah Brooks", "doctoral", 2018),
    ("Priya Raghunathan", "Arjun Menon", "doctoral", None),
    ("Markus Weber", "Elena Voss", "postdoc", 2019),
]

PRINCIPAL_INVESTIGATORS = [
    ("Ingrid Solberg", "ALPINE"), ("Priya Raghunathan", "MONSOON"),
    ("Daniel Okafor", "CASCADE"), ("Markus Weber", "RECLAIM"),
]

TECHNOLOGIES = [
    "Sodium-ion battery", "Thermal management", "Load forecasting",
    "Battery recycling", "Solid-state electrolyte", "Battery degradation",
]

# key, title, year, journal, project, [(author, affiliation-at-publication)], [technologies]
PAPERS = [
    ("P22", "Sodium-Ion Cell Degradation Under Variable Grid Loads", 2023,
     "Journal of Energy Storage Engineering", "ALPINE",
     [("Ingrid Solberg", "Halvorsen Institute of Technology"),
      ("Sofia Lindqvist", "Halvorsen Institute of Technology"),
      ("Tomas Berg", "Fjordgrid AS")],
     ["Sodium-ion battery", "Battery degradation"]),
    ("P23", "Sodium-Ion Cathode Stability in Solid-State Electrolytes", 2022,
     "Advanced Electrochemical Materials", "ALPINE",
     [("Katarina Novak", "Rhine Valley University"),
      ("Ingrid Solberg", "Halvorsen Institute of Technology"),
      ("Elena Voss", "Lumen Storage Systems")],
     ["Sodium-ion battery", "Solid-state electrolyte"]),
    ("P24", "Thermal Management Strategies for Stationary Batteries in Hot Climates", 2024,
     "International Journal of Thermal Energy Systems", "MONSOON",
     [("Priya Raghunathan", "Southern Peninsula Institute of Science"),
      ("Arjun Menon", "Southern Peninsula Institute of Science"),
      ("Daniel Okafor", "Maple Ridge University")],
     ["Thermal management", "Sodium-ion battery"]),
    ("P25", "Probabilistic Load Forecasting with Gradient-Boosted Models", 2023,
     "Transactions on Smart Grid Analytics", "CASCADE",
     [("Daniel Okafor", "Maple Ridge University"),
      ("Li Wei", "Maple Ridge University"),
      ("Hannah Brooks", "Pacific Cell Technologies")],
     ["Load forecasting"]),
    ("P26", "Hydrometallurgical Recovery of Sodium-Ion Cathode Materials", 2024,
     "Journal of Sustainable Materials Processing", "RECLAIM",
     [("Markus Weber", "Rhine Valley University"),
      ("Katarina Novak", "Rhine Valley University")],
     ["Battery recycling", "Sodium-ion battery"]),
    ("P27", "Forecast-Aware Dispatch of Grid Batteries", 2025,
     "Energy Systems Control Letters", "CASCADE",
     [("Hannah Brooks", "Pacific Cell Technologies"),
      ("Sofia Lindqvist", "Halvorsen Institute of Technology"),
      ("Daniel Okafor", "Maple Ridge University")],
     ["Load forecasting", "Battery degradation"]),
]

# citing, cited
CITATIONS = [("P22", "P23"), ("P24", "P22"), ("P26", "P23"), ("P27", "P25"), ("P27", "P22")]

# name, country, commissioned, project, [operators], [cell suppliers/software], patent id or None, capacity
SITES = [
    ("Vestfjord Pilot Site", "Norway", 2024, "ALPINE",
     ["Fjordgrid AS", "Halvorsen Institute of Technology"], "Lumen Storage Systems",
     "LSS-PAT-2020-114", "2 MWh sodium-ion"),
    ("Tiruvallur Test Bed", "India", 2025, "MONSOON",
     ["Southern Peninsula Institute of Science", "Deccan Power Corporation"], "Lumen Storage Systems",
     "LSS-PAT-2020-114", "1.5 MWh sodium-ion"),
    ("Fraser Valley Demonstration Site", "Canada", 2024, "CASCADE",
     ["Maple Ridge University", "Pacific Cell Technologies"], None,
     None, "800 kWh lithium iron phosphate"),
]

SITE_MANAGERS = [("Tomas Berg", "Vestfjord Pilot Site"), ("Rahul Venkatesan", "Tiruvallur Test Bed")]

PATENT = {
    "id": "LSS-PAT-2020-114",
    "title": "Layered Sodium-Ion Cell with Composite Electrolyte Interface",
    "filed": 2020, "granted": 2022,
    "holder": "Lumen Storage Systems",
    "inventors": ["Elena Voss", "Katarina Novak"],
    "described_in_paper": "P23",
}

# name, year, host org, location
EVENTS = [
    ("Nordic Storage Symposium 2023", 2023, "Halvorsen Institute of Technology", "Trondheim"),
    ("Asian Battery Safety Workshop 2024", 2024, "Southern Peninsula Institute of Science", "Chennai"),
]

# person, event, role
EVENT_ROLES = [
    ("Ingrid Solberg", "Nordic Storage Symposium 2023", "keynote"),
    ("Elena Voss", "Nordic Storage Symposium 2023", "industry panel"),
    ("Daniel Okafor", "Nordic Storage Symposium 2023", "presenter"),
    ("Markus Weber", "Nordic Storage Symposium 2023", "invited guest"),
]
PAPERS_PRESENTED = [("P22", "Nordic Storage Symposium 2023"), ("P25", "Nordic Storage Symposium 2023")]

# org, org, relation (non-project institutional links stated in the corpus)
ORG_LINKS = [
    ("Rhine Valley University", "Lumen Storage Systems", "COLLABORATION_AGREEMENT"),
    ("Southern Peninsula Institute of Science", "Maple Ridge University", "EXCHANGE_AGREEMENT"),
    ("Pacific Cell Technologies", "Halvorsen Institute of Technology", "COLLABORATES_WITH"),
    ("Pacific Cell Technologies", "Maple Ridge University", "LICENSES_FROM"),
]
