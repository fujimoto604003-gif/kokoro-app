import sqlite3
import datetime

DB_NAME = "diary.db"

def init_db():
    """Initializes the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create table: date as Primary Key (YYYY-MM-DD), comment, and q1-q15 columns
    # We will store date as TEXT in ISO format
    columns = ["entry_date TEXT PRIMARY KEY", "comment TEXT"]
    for i in range(1, 16):
        columns.append(f"q{i} INTEGER")
    
    create_sql = f"CREATE TABLE IF NOT EXISTS diary_entries ({', '.join(columns)})"
    c.execute(create_sql)
    conn.commit()
    conn.close()

def save_entry(entry_date, comment, answers):
    """
    Saves or updates a diary entry.
    entry_date: datetime.date object
    comment: str
    answers: dict mapping 'Q1'..'Q15' to int scores
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    date_str = entry_date.strftime("%Y-%m-%d")
    
    # Prepare values
    # We use REPLACE INTO to handle both Insert and Update (Upsert)
    # Be careful, REPLACE deletes old row and inserts new one, so if we had other columns they'd be lost.
    # Here we update all columns anyway, so it's fine.
    
    cols = ["entry_date", "comment"] + [f"q{i}" for i in range(1, 16)]
    placeholders = ["?"] * len(cols)
    
    vals = [date_str, comment]
    for i in range(1, 16):
        qid = f"Q{i}"
        vals.append(answers.get(qid, 3)) # Default to 3 if missing
        
    sql = f"REPLACE INTO diary_entries ({', '.join(cols)}) VALUES ({', '.join(placeholders)})"
    
    c.execute(sql, vals)
    conn.commit()
    conn.close()

def get_entry(entry_date):
    """
    Retrieves an entry for a specific date.
    Returns a dict with 'comment' and 'answers' (dict of Qid->score), or None if not found.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    date_str = entry_date.strftime("%Y-%m-%d")
    
    # Dynamic column selection to be safe
    cols = ["comment"] + [f"q{i}" for i in range(1, 16)]
    sql = f"SELECT {', '.join(cols)} FROM diary_entries WHERE entry_date = ?"
    
    c.execute(sql, (date_str,))
    row = c.fetchone()
    conn.close()
    
    if row:
        comment = row[0]
        answers = {}
        for i in range(1, 16):
            answers[f"Q{i}"] = row[i]
        return {"comment": comment, "answers": answers}
    else:
        return None

def get_all_entry_dates():
    """Returns a list of all dates that have entries."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT entry_date FROM diary_entries ORDER BY entry_date DESC")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_all_entries():
    """
    Retrieves all entries (date, comment, answers).
    Returns a list of dicts.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Dynamic column selection
    cols = ["entry_date", "comment"] + [f"q{i}" for i in range(1, 16)]
    sql = f"SELECT {', '.join(cols)} FROM diary_entries ORDER BY entry_date DESC"
    
    c.execute(sql)
    rows = c.fetchall()
    conn.close()
    
    entries = []
    for row in rows:
        entry_date = row[0]
        comment = row[1]
        answers = {}
        for i in range(1, 16):
            # Column index starts at 2 (0=date, 1=comment)
            answers[f"Q{i}"] = row[i+1]
        entries.append({
            "date": entry_date,
            "comment": comment,
            "answers": answers
        })
    return entries
