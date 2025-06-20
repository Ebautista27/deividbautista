from flask import Flask, render_template_string, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'database.db'

SCHEMA = '''
CREATE TABLE IF NOT EXISTS clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS reset_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    click_count INTEGER
);
'''

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM clicks')
    count = cur.fetchone()[0]
    conn.close()
    return render_template_string(TEMPLATE, count=count)

@app.route('/click', methods=['POST'])
def click():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO clicks(timestamp) VALUES(?)', (datetime.utcnow().isoformat(),))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM clicks')
    count = cur.fetchone()[0]
    if count > 0:
        conn.execute('INSERT INTO reset_history(timestamp, click_count) VALUES(?, ?)', (datetime.utcnow().isoformat(), count))
        conn.execute('DELETE FROM clicks')
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/history')
def history():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT timestamp, click_count FROM reset_history ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return render_template_string(HISTORY_TEMPLATE, history=rows)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Click App</title>
</head>
<body>
    <h1>Clicks: {{ count }}</h1>
    <form action="{{ url_for('click') }}" method="post">
        <button type="submit">Click me!</button>
    </form>
    <form action="{{ url_for('reset') }}" method="post" style="margin-top:10px;">
        <button type="submit">Reset</button>
    </form>
    <a href="{{ url_for('history') }}">View history</a>
</body>
</html>
'''

HISTORY_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Click History</title>
</head>
<body>
    <h1>Reset History</h1>
    <a href="{{ url_for('index') }}">Back</a>
    <ul>
    {% for ts, count in history %}
        <li>{{ ts }} - {{ count }} clicks</li>
    {% else %}
        <li>No history</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
