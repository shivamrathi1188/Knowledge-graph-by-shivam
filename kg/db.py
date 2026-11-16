"""Neo4j connection layer.

Tries the Bolt driver first. If port 7687 is blocked (common on corporate networks) it falls back to
Aura's HTTPS Query API (port 443), so the rest of the project only ever calls `client.run(cypher, **params)`.
"""
import base64
import json
import os
import socket
import urllib.request
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()


def database():
    return os.getenv("NEO4J_DATABASE", "neo4j")


class HttpClient:
    """Minimal client for the Neo4j Query API v2 (POST /db/<db>/query/v2)."""
    transport = "https (Query API, port 443)"

    def __init__(self, host, user, pwd, db):
        self.url = f"https://{host}/db/{db}/query/v2"
        token = base64.b64encode(f"{user}:{pwd}".encode()).decode()
        self.headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json",
                        "Accept": "application/json"}

    def run(self, cypher, **params):
        body = json.dumps({"statement": cypher, "parameters": params}).encode()
        req = urllib.request.Request(self.url, data=body, headers=self.headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                payload = json.load(resp)
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Neo4j error {e.code}: {e.read().decode()[:800]}") from None
        data = payload.get("data", {})
        fields = data.get("fields", [])
        return [dict(zip(fields, row)) for row in data.get("values", [])]

    def close(self):
        pass


class BoltClient:
    transport = "bolt (port 7687)"

    def __init__(self, uri, user, pwd, db):
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(uri, auth=(user, pwd))
        self.driver.verify_connectivity()
        self.db = db

    def run(self, cypher, **params):
        with self.driver.session(database=self.db) as s:
            return [r.data() for r in s.run(cypher, **params)]

    def close(self):
        self.driver.close()


def get_client():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME", "neo4j")
    pwd = os.getenv("NEO4J_PASSWORD")
    if not uri or not pwd:
        raise SystemExit("Set NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD in .env (see .env.example)")
    host = urlparse(uri).hostname
    mode = os.getenv("NEO4J_TRANSPORT", "auto")  # auto | bolt | http
    if mode != "http":
        try:
            socket.create_connection((host, 7687), timeout=5).close()
            return BoltClient(uri, user, pwd, database())
        except OSError:
            if mode == "bolt":
                raise
    return HttpClient(host, user, pwd, database())
