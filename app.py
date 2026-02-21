from flask import Flask, render_template, request, redirect, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"
DB = "bookings.db"

# ----------------------------

# DATABASE INIT

# ----------------------------

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    certificate TEXT,
    status TEXT,
    slot TEXT,
    remarks TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ----------------------------

# HOME

# ----------------------------

@app.route("/")
def home():
    return render_template("login.html")

# ----------------------------

# STUDENT LOGIN

# ----------------------------

@app.route("/student_login", methods=["POST"])
def student_login():
    roll = request.form.get("roll")
    password = request.form.get("password")


    if roll and password and roll == password:
        session.clear()
        session["student"] = roll
        return redirect("/student")

    return "Invalid student credentials"


# ----------------------------

# ADMIN LOGIN

# ----------------------------

@app.route("/admin_login", methods=["POST"])
def admin_login():
    aid = request.form.get("aid")
    apass = request.form.get("password")


    if aid == "admin" and apass == "123":
        session.clear()
        session["admin"] = True
        return redirect("/admin")

    return "Invalid admin credentials"


# ----------------------------

# STUDENT DASHBOARD

# ----------------------------

@app.route("/student")
def student_dash():
    if "student" not in session:
        return redirect("/")


    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM requests WHERE student=? ORDER BY id DESC",
        (session["student"],)
    )
    data = cursor.fetchall()
    conn.close()

    return render_template("student.html", requests=data)


# ----------------------------

# SUBMIT REQUEST

# ----------------------------

@app.route("/submit_request", methods=["POST"])
def submit_request():
    if "student" not in session:
     return redirect("/")

    
    cert = request.form.get("certificate")
    if not cert:
        return redirect("/student")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO requests (student, certificate, status, slot, remarks)
        VALUES (?, ?, 'Pending', '-', '-')
        """,
        (session["student"], cert)
    )
    conn.commit()
    conn.close()

    flash("✅ Request submitted successfully.", "success")
    return redirect("/student")


# ----------------------------

# ADMIN DASHBOARD (PENDING ONLY)

# ----------------------------

@app.route("/admin")
def admin_dash():
    if "admin" not in session:
        return redirect("/")


    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM requests WHERE status='Pending' ORDER BY id DESC"
    )
    data = cursor.fetchall()
    conn.close()

    return render_template("admin.html", requests=data)
    # ----------------------------

# APPROVE WITH CONFLICT CHECK

# ----------------------------

@app.route("/approve/<int:req_id>", methods=["POST"])
def approve(req_id):
    if "admin" not in session:
        return redirect("/")

    
    slot = request.form.get("slot")
    if not slot:
        flash("Slot is required.", "error")
        return redirect("/admin")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    # 🔥 conflict check
    cursor.execute(
        "SELECT id FROM requests WHERE slot=? AND status='Approved'",
        (slot,)
    )
    conflict = cursor.fetchone()

    if conflict:
        conn.close()
        flash("❌ Slot already booked. Choose another time.", "error")
        return redirect("/admin")

    # ✅ approve
    cursor.execute(
        """
        UPDATE requests
        SET status='Approved',
            slot=?,
            remarks='Approved'
        WHERE id=?
        """,
        (slot, req_id)
    )

    conn.commit()
    conn.close()

    flash("✅ Slot approved successfully.", "success")
    return redirect("/admin")
    
# ----------------------------

# REJECT

# ----------------------------

@app.route("/reject/<int:req_id>", methods=["POST"])
def reject(req_id):
    if "admin" not in session:
        return redirect("/")

    
    remark = request.form.get("remark")
    if not remark:
        flash("Remark is required.", "error")
        return redirect("/admin")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE requests
        SET status='Rejected',
            remarks=?,
            slot='-'
        WHERE id=?
        """,
        (remark, req_id)
    )
    conn.commit()
    conn.close()

    flash("❌ Request rejected.", "error")
    return redirect("/admin")
    

    # ----------------------------

    # LOGOUT

    # ----------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
