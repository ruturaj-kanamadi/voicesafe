from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# DATABASE CONNECTION

def get_db_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="#rrk2007",
        database="voicesafe"
    )


# HOME PAGE

@app.route('/')
def home():

    return render_template('index.html')


# ABOUT PAGE

@app.route('/about')
def about():

    return render_template('about.html')


# CONTACT PAGE

@app.route('/contact')
def contact():

    return render_template('contact.html')


# SUBMIT MANUAL COMPLAINT

@app.route('/submit', methods=['POST'])
def submit():

    ctype = request.form['type']
    location = request.form['location']
    description = request.form['description']

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO complaints
    (type, location, description, source, status)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        ctype,
        location,
        description,
        'User',
        'Pending'
    )

    cursor.execute(sql, values)

    conn.commit()
    conn.close()

    return redirect('/dashboard')


# PUBLIC DASHBOARD

@app.route('/dashboard')
def dashboard():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    )

    complaints = cursor.fetchall()

    conn.close()

    return render_template(
        'dashboard.html',
        complaints=complaints
    )


# ADMIN DASHBOARD

@app.route('/admin')
def admin():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    )

    complaints = cursor.fetchall()

    conn.close()

    return render_template(
        'admin.html',
        complaints=complaints
    )


# RESOLVE COMPLAINT

@app.route('/resolve/<int:id>')
def resolve(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE complaints SET status='Resolved' WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


# DELETE COMPLAINT

@app.route('/delete/<int:id>')
def delete(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM complaints WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')


# AUTO SENSOR COMPLAINT

@app.route('/auto-complaint', methods=['POST'])
def auto_complaint():

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO complaints
    (type, location, description, source, status)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        data['type'],
        data['location'],
        data['description'],
        'Sensor',
        'Pending'
    )

    cursor.execute(sql, values)

    conn.commit()
    conn.close()

    return {
        "message": "Auto complaint registered"
    }


# RUN APP

if __name__ == '__main__':

    app.run(debug=True)