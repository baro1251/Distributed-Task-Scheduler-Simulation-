from flask import Flask, request, render_template_string, send_file, redirect, url_for
import sqlite3
import uuid
from fpdf import FPDF
from datetime import datetime
import tempfile


app = Flask(__name__)

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id TEXT PRIMARY KEY, number INTEGER, status TEXT, result INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# HTML
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Distributed Task Scheduler</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; padding: 20px; }
        h1 { text-align: center; }
        form { text-align: center; margin-bottom: 20px; }
        input[type=number] { padding: 8px; width: 200px; }
        button { padding: 8px 15px; background: #28a745; color: white; border: none; border-radius: 5px; margin: 5px; }
        table { width: 80%; margin: 20px auto; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background: #007bff; color: white; }
    </style>
</head>
<body>
    <h1>Distributed Task Scheduler</h1>
    <form method="POST" action="/add_task">
        <input type="number" name="number" placeholder="Enter a number" required>
        <button type="submit">Add Task</button>
    </form>
    <div style="text-align:center;">
        <form action="/generate_pdf" method="GET" style="display:inline;">
            <button type="submit">Generate PDF Report</button>
        </form>
        <form action="/reset" method="POST" style="display:inline;">
            <button type="submit" style="background:red;">Reset Database</button>
        </form>
    </div>
    <table>
        <tr><th>Task ID</th><th>Number</th><th>Status</th><th>Result</th></tr>
        {% for row in tasks %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td>{{ row[3] if row[3] else '...' }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template_string(HTML_PAGE, tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    number = int(request.form['number'])
    task_id = str(uuid.uuid4())
    result = sum(range(1, number + 1))  # تنفيذ فوري بدلاً من Celery
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (id, number, status, result) VALUES (?, ?, ?, ?)",
              (task_id, number, 'DONE', result))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# دالة لتوليد ملف PDF (بدون route)
def create_pdf(tasks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Tasks Report", ln=True, align="C")

    # إضافة التاريخ والوقت
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)

    # إنشاء الجدول
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Task ID", 1, 0, "C")
    pdf.cell(30, 10, "Number", 1, 0, "C")
    pdf.cell(30, 10, "Status", 1, 0, "C")
    pdf.cell(40, 10, "Result", 1, 1, "C")

    pdf.set_font("Arial", size=12)
    for row in tasks:
        pdf.cell(50, 10, row[0][:8], 1, 0, "C")  # ID مختصر
        pdf.cell(30, 10, str(row[1]), 1, 0, "C")
        pdf.cell(30, 10, row[2], 1, 0, "C")
        pdf.cell(40, 10, str(row[3]), 1, 1, "C")

    # حفظ في ملف مؤقت
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# هذا هو الـ Route الوحيد
@app.route('/generate_pdf')
def generate_pdf():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    pdf_file = create_pdf(tasks)

    # إرجاع ملف PDF للتنزيل
    return send_file(pdf_file, as_attachment=True, download_name="tasks_report.pdf")



@app.route('/reset', methods=['POST'])
def reset_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)



