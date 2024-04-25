from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'duauth'  # Replace with your MySQL database name

mysql = MySQL(app)

# Set secret key for session
app.secret_key = 'super_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'cell_number' not in session:
        return redirect(url_for('index'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE cell_number = %s", [session['cell_number']])
    user = cur.fetchone()
    cur.close()
    return render_template('dashboard.html', user=user)


@app.route('/verify', methods=['POST'])
def verify():
    cell_number = request.form['cell_number']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE cell_number = %s", [cell_number])
    user = cur.fetchone()
    cur.close()

    if user:
        session['cell_number'] = cell_number
        return render_template('nic.html')
    else:
        return "Cell number not found in the database."


@app.route('/verify_nic', methods=['POST'])
def verify_nic():
    cnic = request.form['cnic']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE cell_number = %s AND cnic = %s", (session['cell_number'], cnic))
    user = cur.fetchone()
    cur.close()

    if user:
        return redirect(url_for('dashboard'))
    else:
        return "Invalid NIC number."


if __name__ == '__main__':
    app.run(debug=True)
