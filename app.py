from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import numpy as np
import os


app = Flask(__name__)
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'electoral_bonds'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT DISTINCT(`Name of the Political Party`) FROM eb_party;')
        parties = (("Any",),) + cur.fetchall()
        cur.execute('SELECT DISTINCT(`Name of the Purchaser`) FROM eb_company;')
        names = (("Any",),) + cur.fetchall()

        return render_template('search.html', parties=parties, names=names)

    else:
        bond_number = request.form['bond_number']
        party = request.form['party']
        company = request.form['company']

        print(bond_number, party, company)

        query = 'select `Reference No (URN)`, `Name of the Political Party`, `Name of the Purchaser`, `Bond Number` from eb_company join eb_party using(`Bond Number`) where '
        if bond_number != "":
            query += f'`Bond Number`={bond_number} and '

        if party != 'Any':
            query += f'`Name of the Political Party`="{party}" and '

        if company != 'Any':
            query += f'`Name of the Purchaser`="{company}" and '

        query = query.strip(' and ') + ';'

        cur = mysql.connection.cursor()
        cur.execute(query)

        results = cur.fetchall()
        return render_template("search_results.html", results=list(results))


if __name__ == '__main__':
    app.run(debug=True)
