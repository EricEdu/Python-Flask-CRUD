from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'IVN'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM item")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', item=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfullly")
        Tipo = request.form['Tipo']
        Modelo = request.form['Modelo']
        Marca = request.form['Marca']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO item (Tipo, Modelo, Marca) VALUES (%s, %s, %s)", (Tipo, Modelo, Marca))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:Patrimonio_data>', methods = ['GET'])
def delete(Patrimonio_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM item WHERE Patrimonio=%s", (Patrimonio_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        Patrimonio_data = request.form['Patrimonio']
        Tipo = request.form['Tipo']
        Modelo = request.form['Modelo']
        Marca = request.form['Marca']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE item SET Tipo=%s, Modelo=%s, Marca=%s
        WHERE Patrimonio=%s
        """, (Tipo, Modelo, Marca, Patrimonio_data))
        flash("Data Updated Suceefully")
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)