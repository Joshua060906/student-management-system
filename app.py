from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# =========================
# DATABASE INITIALIZATION
# =========================

def init_db():

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            roll_number TEXT UNIQUE,

            name TEXT,

            email TEXT,

            course TEXT,

            year TEXT,

            phone TEXT
        )
    ''')

    conn.commit()
    conn.close()


# =========================
# HOME PAGE + SEARCH
# =========================

@app.route('/')
def index():

    search = request.args.get('search', '')

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    # SEARCH FEATURE

    if search:

        cursor.execute(
            '''
            SELECT * FROM students

            WHERE

            roll_number LIKE ?
            OR name LIKE ?
            OR email LIKE ?
            OR course LIKE ?
            OR year LIKE ?
            OR phone LIKE ?
            ''',

            (
                f'%{search}%',
                f'%{search}%',
                f'%{search}%',
                f'%{search}%',
                f'%{search}%',
                f'%{search}%'
            )
        )

    else:

        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    total_students = len(students)

    conn.close()

    return render_template(
        'index.html',
        students=students,
        total_students=total_students
    )


# =========================
# ADD STUDENT
# =========================

@app.route('/add', methods=['GET', 'POST'])
def add_student():

    error = ""

    if request.method == 'POST':

        roll_number = request.form['roll_number']
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        year = request.form['year']
        phone = request.form['phone']

        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        # CHECK DUPLICATE ROLL NUMBER

        cursor.execute(
            "SELECT * FROM students WHERE roll_number=?",
            (roll_number,)
        )

        existing_student = cursor.fetchone()

        if existing_student:

            error = "Roll Number already exists!"

        else:

            cursor.execute(
                '''
                INSERT INTO students

                (roll_number, name, email, course, year, phone)

                VALUES (?, ?, ?, ?, ?, ?)
                ''',

                (
                    roll_number,
                    name,
                    email,
                    course,
                    year,
                    phone
                )
            )

            conn.commit()
            conn.close()

            return redirect('/')

        conn.close()

    return render_template(
        'add_student.html',
        error=error
    )


# =========================
# DELETE STUDENT
# =========================

@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# =========================
# EDIT STUDENT
# =========================

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        roll_number = request.form['roll_number']
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        year = request.form['year']
        phone = request.form['phone']

        cursor.execute(
            '''
            UPDATE students

            SET

            roll_number=?,
            name=?,
            email=?,
            course=?,
            year=?,
            phone=?

            WHERE id=?
            ''',

            (
                roll_number,
                name,
                email,
                course,
                year,
                phone,
                id
            )
        )

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_student.html',
        student=student
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == '__main__':

    init_db()

    app.run(debug=True)