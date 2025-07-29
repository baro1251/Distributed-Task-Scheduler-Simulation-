# 🖥️ Distributed Task Scheduler (Simulation)

A **simulation project for distributed task scheduling** using **Flask**, **SQLite**, and **FPDF** to generate PDF reports.  
This application allows you to add tasks (calculate the sum of numbers up to a given number), view all tasks, and generate downloadable PDF reports.

---

## ✅ Features:
✔ Simple web interface using Flask  
✔ Store tasks in SQLite database  
✔ Reset database option  
✔ Generate PDF report with all tasks  
✔ Simulated immediate task execution (instead of Celery)  

---

## ✅ Features in the UI
- **Add Task:** Input a number, and the system calculates the sum from 1 to that number.
- **View Tasks:** Table with (Task ID, Number, Status, Result).
- **Generate PDF Report:** Download a PDF report of all tasks.
- **Reset Database:** Clear all tasks.

---

## ⚠️ Notes
- This project is a **simulation only**, it does not use real distributed task execution or Celery.
- Can be extended to support **actual distributed scheduling** with Celery and Redis.

---

## 📌 Future Improvements
- 🎨 Add **Bootstrap UI** for a modern look.
- ⚡ Integrate **Celery** for true distributed task execution.
- 🔗 Provide **REST API** for integration with other systems.
  
---

## 🛠️ **Technologies Used**
- Python 3.x  
- Flask  
- SQLite3  
- FPDF (for PDF generation)  
- HTML + CSS  

---


## ✅ **Installation & Usage**

- main.py

### 1️⃣ Install dependencies:
```bash
pip install flask fpdf

- run the main.py

- open http://127.0.0.1:5000/




