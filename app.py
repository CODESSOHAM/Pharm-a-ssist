import time
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Soham@2006',
        database='medicine_db'
    )

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create admins table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    ''')
    
    # Ensure at least one admin exists
    cursor.execute("SELECT * FROM admins WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admins (username, password) VALUES ('admin', 'admin123')")
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order_medicine', methods=['GET', 'POST'])
def order_medicine():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        email = request.form['email']
        address = request.form['address']
        medicine_name = request.form['medicine_name']
        contact_no = request.form['contact_no']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (name, date, email, address, medicine_name, contact_no) VALUES (%s, %s, %s, %s, %s, %s)',
                       (name, date, email, address, medicine_name, contact_no))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('order_medicine.html')

@app.route('/doctors')
def doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch distinct categories
    cursor.execute('SELECT DISTINCT category FROM doctors')
    categories = cursor.fetchall()

    # Fetch all doctors
    cursor.execute('SELECT * FROM doctors')
    doctors = cursor.fetchall()

    conn.close()
    return render_template('doctors.html', categories=categories, doctors=doctors)


@app.route('/doctor/<int:id>')
def doctor_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM doctors WHERE id = %s', (id,))
    doctor = cursor.fetchone()
    conn.close()
    return render_template('doctor_details.html', doctor=doctor)


import time  # Ensure time is imported

import time
import random
import string

@app.route('/book_appointment/<int:doctor_id>', methods=['GET', 'POST'])
def book_appointment(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch doctor details
    cursor.execute('SELECT * FROM doctors WHERE id = %s', (doctor_id,))
    doctor = cursor.fetchone()

    if not doctor:
        conn.close()
        return "Doctor not found", 404

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        address = request.form['address']
        email = request.form['email']
        contact_no = request.form['contact_no']
        age = request.form['age']
        date = request.form['date']

        # ✅ Generate a unique alphanumeric token
        token = f"T-{doctor_id}-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # ✅ Insert appointment details
        cursor.execute('''
            INSERT INTO appointments (doctor_id, doctor_name, patient_name, address, email, contact_no, age, date, token)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (doctor_id, doctor['name'], patient_name, address, email, contact_no, age, date, token))
        conn.commit()

        # ✅ Retrieve the generated token
        cursor.execute('SELECT token FROM appointments WHERE doctor_id = %s AND patient_name = %s ORDER BY id DESC LIMIT 1',
                       (doctor_id, patient_name))
        appointment = cursor.fetchone()

        conn.close()

        if appointment and appointment['token']:
            return render_template('appointment_success.html', 
                                   token=appointment['token'], 
                                   date=date, 
                                   doctor_fee=doctor['fee'])  # ✅ Pass doctor’s fee
        else:
            return "Error: Token not retrieved from database."

    conn.close()
    return render_template('book_appointment.html', doctor=doctor)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        conn.close()
        if admin:
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials'
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')

@app.route('/orders')
def orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/appointments')
def appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM appointments')
    appointments = cursor.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/contact_pharmacy')
def contact_pharmacy():
    return render_template('contact_pharmacy.html')

@app.route('/nearby_hospitals')
def nearby_hospitals():
    return render_template('nearby_hospitals.html')



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
