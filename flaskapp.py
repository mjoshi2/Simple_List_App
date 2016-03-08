from flask.ext.mysql import MySQL

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

from contextlib import closing

app = Flask(__name__)
app.config.from_object(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'manapp'
app.config['MYSQL_DATABASE_PASSWORD'] = 'new_password'
app.config['MYSQL_DATABASE_DB'] = 'flaskdb'
app.config['MYSQL_DATABASE_HOST'] = '192.168.114.136'
mysql.init_app(app)

def connect_db():
    return mysql.connect()

def init_db():
    cur = mysql.connect().cursor()
    cur.execute('drop table if exists entries;')
    cur.execute('create table entries (item_no int not null auto_increment, description varchar(100) not null, to_be_done_by varchar(50) not null, primary key (item_no));')

@app.before_request
def before_request():
#    cur = mysql.connect().cursor
    cur = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(mysql, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/show', methods=['GET','POST'])
def show_entries():
    cur = mysql.connect().cursor()
    cur.execute('select item_no, description, to_be_done_by from entries order by item_no asc')
    entries = [dict(item_no=row[0], description=row[1], to_be_done_by=row[2]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['GET','POST'])
def add_entry():
  #  cur = mysql.connect().cursor()
    error = None
    if request.form['description'] == '' or request.form['to_be_done_by'] == '':
        error = 'Invalid Entry'
    else:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute('insert into entries (description, to_be_done_by) values (%s,%s)',
                [request.form['description'], request.form['to_be_done_by']])
        conn.commit()
    return redirect(url_for('show_entries'))

@app.route('/delete/<int:item_no>')
def del_entry(item_no):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute('delete from entries where item_no= %d' % item_no)
    conn.commit()
    return redirect(url_for('show_entries'))

@app.route('/clear')
def clear_list():
    init_db()
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')

