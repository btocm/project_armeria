from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config['MYSQL_HOST'] = 'Ivans-MacBook-Air.local'
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "im117"
app.config['MYSQL_PORT'] = 3308
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT user, host FROM mysql.user""")
    rv = cur.fetchall()
    return str(rv)

if __name__ == "__main__":
    app.run(debug=True)