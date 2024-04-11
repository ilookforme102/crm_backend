from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'f33924fea4dd7123a0daa9d2a7213679'
# Replace the following values with your database connection details
username = 'sql_dabanhtructi'
password = 'sql_dabanhtructi'
host = '128.199.228.235'
database = 'sql_dabanhtructi'
port = 3306
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.route('/')
def home():
    return "Home page"

@app.route('/index')
def index():
    return {"name":"sang"}
if __name__ == '__main__':
    app.run(port=5000, debug=True)