from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_student():
    return render_template('student.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                # CREATE TABLE hanya jika belum ada
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nm TEXT,
                        address TEXT,
                        city TEXT,
                        pin TEXT
                    )
                ''')

                cur.execute('''
                    INSERT INTO students (nm, address, city, pin)
                    VALUES (?, ?, ?, ?)''', (nm, addr, city, pin))

                con.commit()
                msg = "Record successfully added"
        except sql.Error as e:
            con.rollback()
            msg = f"Error in insert operation: {e}"
        finally:
            con.close()  # Pindahkan ini ke luar blok try-except
            return render_template("result.html", msg=msg)

@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()
    con.close()  # Tutup koneksi setelah menggunakan

    return render_template("list.html", rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
