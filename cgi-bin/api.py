#!/usr/bin/env python3
# ============================================================
# PCIM — Private Credit Intelligence Monitor | Backend API
# © 2026 ReviveERM™ — a subsidiary of Spiritus Partners, Inc.,
# a Delaware corporation. All rights reserved.
# ============================================================
import json, os, sys, sqlite3, uuid
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pcim.db")

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS cards (
        id TEXT PRIMARY KEY,
        title TEXT,
        source TEXT,
        type TEXT DEFAULT 'article',
        date TEXT,
        domain TEXT,
        signal TEXT,
        agent TEXT DEFAULT 'A1',
        tags TEXT DEFAULT '[]',
        summary TEXT,
        url TEXT DEFAULT '',
        xs INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS queue (
        id TEXT PRIMARY KEY,
        title TEXT,
        source TEXT,
        type TEXT DEFAULT 'article',
        date TEXT,
        domain TEXT,
        signal TEXT,
        agent TEXT DEFAULT 'A1',
        tags TEXT DEFAULT '[]',
        summary TEXT,
        url TEXT DEFAULT '',
        xs INTEGER DEFAULT 0,
        status TEXT DEFAULT 'queued',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    db.commit()
    return db

def row_to_dict(row):
    d = dict(row)
    if 'tags' in d:
        try:
            d['tags'] = json.loads(d['tags'])
        except:
            d['tags'] = []
    d['xs'] = bool(d.get('xs', 0))
    return d

def send(status_code, data):
    print(f"Status: {status_code}")
    print("Content-Type: application/json")
    print()
    print(json.dumps(data))

method = os.environ.get("REQUEST_METHOD", "GET")
path = os.environ.get("PATH_INFO", "")
query = os.environ.get("QUERY_STRING", "")
content_length = int(os.environ.get("CONTENT_LENGTH", 0) or 0)

body = {}
if content_length > 0:
    raw = sys.stdin.read(content_length)
    try:
        body = json.loads(raw)
    except:
        body = {}

db = get_db()

def parse_qs(qs):
    params = {}
    for part in qs.split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            params[k] = v
    return params

params = parse_qs(query)

try:
    if path == "/cards":
        if method == "GET":
            rows = db.execute("SELECT * FROM cards WHERE status='active' ORDER BY created_at DESC").fetchall()
            send(200, [row_to_dict(r) for r in rows])
        elif method == "POST":
            card_id = body.get("id", f"u{uuid.uuid4().hex[:6]}")
            tags = body.get("tags", [])
            if isinstance(tags, list):
                tags_json = json.dumps(tags)
            else:
                tags_json = json.dumps([t.strip() for t in str(tags).split(",") if t.strip()])
            db.execute(
                "INSERT OR REPLACE INTO cards (id, title, source, type, date, domain, signal, agent, tags, summary, url, xs, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                [card_id, body.get("title",""), body.get("source",""), body.get("type","article"),
                 body.get("date", datetime.now().strftime("%Y-%m-%d")), body.get("domain","CreditMarkets"),
                 body.get("signal","Monitor"), body.get("agent","A1"), tags_json,
                 body.get("summary",""), body.get("url",""), int(body.get("xs", False)), "active"]
            )
            db.commit()
            row = db.execute("SELECT * FROM cards WHERE id=?", [card_id]).fetchone()
            send(201, row_to_dict(row))
        else:
            send(405, {"error": "Method not allowed"})

    elif path == "/queue":
        if method == "GET":
            rows = db.execute("SELECT * FROM queue WHERE status='queued' ORDER BY created_at DESC").fetchall()
            send(200, [row_to_dict(r) for r in rows])
        elif method == "POST":
            q_id = body.get("id", f"q{uuid.uuid4().hex[:6]}")
            tags = body.get("tags", [])
            if isinstance(tags, list):
                tags_json = json.dumps(tags)
            else:
                tags_json = json.dumps([t.strip() for t in str(tags).split(",") if t.strip()])
            db.execute(
                "INSERT OR REPLACE INTO queue (id, title, source, type, date, domain, signal, agent, tags, summary, url, xs, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                [q_id, body.get("title",""), body.get("source",""), body.get("type","article"),
                 body.get("date", datetime.now().strftime("%Y-%m-%d")), body.get("domain","CreditMarkets"),
                 body.get("signal","Monitor"), body.get("agent","A1"), tags_json,
                 body.get("summary",""), body.get("url",""), int(body.get("xs", False)), "queued"]
            )
            db.commit()
            row = db.execute("SELECT * FROM queue WHERE id=?", [q_id]).fetchone()
            send(201, row_to_dict(row))
        elif method == "DELETE":
            q_id = params.get("id", "")
            if q_id:
                db.execute("UPDATE queue SET status='dismissed' WHERE id=?", [q_id])
                db.commit()
            send(200, {"ok": True})
        else:
            send(405, {"error": "Method not allowed"})

    elif path == "/approve":
        if method == "POST":
            q_id = params.get("id", "")
            if not q_id:
                send(400, {"error": "Missing id"})
            else:
                row = db.execute("SELECT * FROM queue WHERE id=?", [q_id]).fetchone()
                if not row:
                    send(404, {"error": "Not found"})
                else:
                    d = dict(row)
                    card_id = f"a{uuid.uuid4().hex[:6]}"
                    db.execute(
                        "INSERT INTO cards (id, title, source, type, date, domain, signal, agent, tags, summary, url, xs, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        [card_id, d["title"], d["source"], d["type"], d["date"], d["domain"],
                         d["signal"], d["agent"], d["tags"], d["summary"], d["url"], d["xs"], "active"]
                    )
                    db.execute("UPDATE queue SET status='approved' WHERE id=?", [q_id])
                    db.commit()
                    new_row = db.execute("SELECT * FROM cards WHERE id=?", [card_id]).fetchone()
                    send(200, row_to_dict(new_row))
        else:
            send(405, {"error": "Method not allowed"})

    else:
        send(404, {"error": "Unknown endpoint", "path": path})

except Exception as e:
    send(500, {"error": str(e)})
finally:
    db.close()