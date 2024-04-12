from flask import Flask, jsonify, request, session, make_response,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, and_
import datetime
app = Flask(__name__)
app.secret_key = 'f33924fea4dd7123a0daa9d2a7213679'
# Replace the following values with your database connection details
db_username = 'sql_dabanhtructi'
db_password = 'FKb75AYJzFMJET8F'
db_host = '128.199.228.235'
db_database = 'sql_dabanhtructi'
db_port = 3306
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
###########SQL Query#############
# INSERT INTO `db_vn168_user` (`username`, `password`, `company_id`, `role`, `team`) VALUES ('shang168', 'admin', 'f0732', 'admin', 'IT');
class User(db.Model):
    __tablename__ = 'db_vn168_user'
    username =  db.Column(db.String(255), primary_key = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    company_name = db.Column(db.String(255), nullable = False)
    company_id = db.Column(db.String(255), nullable = False, unique = True)
    role = db.Column(db.String(255), nullable = False)
    team = db.Column(db.String(255), nullable = False)
    def __repr__(self):
        return f'<User {self.username}>'
    
class BO(db.Model):
    __tablename__ = 'db_vn168_crm_bo'
    bo_code = db.Column(db.String(255), primary_key = True,unique = True, nullable = False)
    def __repr__(self):
        return self.bo_code
class Category(db.Model):
    __tablename__ = 'db_vn168_crm_category'
    category = db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.category
class Contact_Note(db.Model):
    __tablename__ = 'db_vn168_crm_contact_note'
    note = db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.note
class Call_Note(db.Model):
    __tablename__ = 'db_vn168_crm_call_note'
    call_note = db.Column(db.String(255), primary_key = True,unique = True, nullable = False)
    def __repr__(self):
        return self.call_note
class Zalo_Note(db.Model):
    __tablename__ = 'db_vn168__crm_zalo_note'
    zalo_note= db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.zalo_note
class Tele_Note(db.Model):
    __tablename__ = 'db_vn168__crm_tele_note'
    tele_note= db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.tele_note
class SMS_Note(db.Model):
    __tablename__ = 'db_vn168__crm_sms_note'
    sms_note= db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.sms_note
class Social_Note(db.Model):
    __tablename__ = 'db_vn168__crm_social_note'
    social_note= db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.social_note
class Interaction_Content(db.Model): #Something called Nội dung tương tác
    __tablename__ = 'db_vn168__interaction_content'
    interaction_content= db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.interaction_content
class Interaction_Result(db.Model): #Something called Nội dung tương tác
    __tablename__ = 'db_vn168__crm_interaction_result'
    result= db.Column(db.String(255),primary_key = True, unique = True, nullable = False)
    def __repr__(self):
        return self.result 
class Customers(db.Model):
    __tablename__ = 'db_vn168__crm_customer'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    username = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = False)
    call_note = db.Column(db.String(255), nullable = False)
    zalo_note = db.Column(db.String(255), nullable = False)
    tele_note = db.Column(db.String(255),nullable = False)
    social_note = db.Column(db.String(255),nullable = False)
    interaction_content = db.Column(db.String(255), nullable = False)
    interaction_result = db.Column(db.String(255), nullable = False)
    person_in_charge = db.Column(db.String(255), nullable = False)
    filled_date = db.Column(Date, nullable = False)
    assistant = db.Column(db.String(255))
    def __repr__(self):
        return self.result
@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all() 
    return 'Hello world'
@app.route('/get_all_users')
def get_all_users():
    # users = Customers.query.all()
    customers = Customers.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    customer_data = [{'code':customer.code, 'username':customer.username,'bo code':customer.bo_code,'zalo note':customer.zalo_note,'tele note':customer.tele_note,'date': customer.filled_date.isoformat()} for customer in customers]
    return customer_data
################################################
##Save new record of customer to the Customer table
@app.route('/record', methods=['POST'])
def add_record():
    if not request.form:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.form
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    social_note = data.get('social_note')
    person_in_charge = data.get('person_in_charge')
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    assistant = data.get('assistant')
    # Check if the user already exists
    if Customers.query.filter((Customers.code == code)).first():
        return jsonify({"error": "Code is already existed, please try again"}), 409
    new_customer = Customers(code= code, username=username,category=category,bo_code=bo_code,call_note=call_note,zalo_note=zalo_note,tele_note=tele_note,social_note=social_note,person_in_charge = person_in_charge,interaction_content=interaction_content, interaction_result = interaction_result,assistant = assistant)
    db.session.add(new_customer)
    try:
        db.session.commit()
        return "User added successfully!"
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e)
#####Edit value for a specific code in Customer table
@app.route('/record/<string:code>',methods = ['PUT'])
def edit_record(code):
    #######################
    # Get method perform a query filtering on the primary key
    record = Customers.query.get(code)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    data = request.form
    record.username = data.get('username')
    record.category = data.get('category')
    record.bo_code = data.get('bo_code')
    record.call_note = data.get('call_note')
    record.zalo_note = data.get('zalo_note')
    record.tele_note = data.get('tele_note')
    record.social_note = data.get('social_note')
    record.person_in_charge = data.get('person_in_charge')
    record.interaction_content = data.get('interaction_content')
    record.interaction_result = data.get('interaction_result')
    record.assistant = data.get('assistant')
    db.session.commit()
    return jsonify({
        'message': 'Customer updated successfully',
        'record': {
            'code': record.code,
            'username': record.username,
            'category' : record.category,
            'bo_code' : record.bo_code,
            'call_note' : record.call_note,
            'zalo_note' : record.zalo_note,
            'tele_note' : record.tele_note,
            'social_note' : record.social_note,
            'person_in_charge' : record.person_in_charge,
            'interaction_content' : record.interaction_content,
            'interaction_result' : record.interaction_result,
            'assistant' : record.assistant,
        }
    }), 200
@app.route('/filter_data', methods=['POST'])
def filter_data():
    if not request.form:
        return jsonify({"error": "Please fill in the form for searching"}), 400
    data = request.form
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    social_note = data.get('social_note')
    person_in_charge = data.get('person_in_charge')
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    assistant = data.get('assistant')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    # Check if the user already exists
    if not username:
        return jsonify({'error': 'Missing username'}), 400

    try:
        # Parse the date string into a date object
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Query the database for customers matching the username and date
    customers = Customers.query.filter(and_(Customers.username == username,
                                            Customers.category == category,
                                            Customers.bo_code == bo_code,
                                            Customers.call_note == call_note,
                                            Customers.zalo_note == zalo_note,
                                            Customers.tele_note == tele_note,
                                            Customers.social_note == social_note,
                                            Customers.person_in_charge == person_in_charge,
                                            Customers.interaction_content == interaction_content,
                                            Customers.interaction_result == interaction_result,
                                            Customers.assistant == assistant,
                                            Customers.code == code,
                                            Customers.filled_date == end_date,
                                            Customers.filled_date == end_date)).all()

    # Format results
    results = [{'username': customer.username, 'registration_date': customer.filled_date.isoformat()} for customer in customers]

    return jsonify(results)
@app.route('/test', methods = ['POST'])
def test():
    data = request.form
    date_string  = data.get('date')
    date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    customers = Customers.query.filter(Customers.username == 'shangđasdasđsd')
    test_list = [{'username': customer.username, 'datre': customer.filled_date >= date_obj} for customer in customers]
    # return {'str':date_obj}
    return test_list
@app.route('/')
def home():
    return "Home Page"
@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)
@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Implement logic to fetch users from the database
        return "<a href='dantri.com'>"
    elif request.method == 'POST':
        # Implement logic to create a new user in the database
        pass
@app.route('/index')
def index():
    return {"name":"sang"}
if __name__ == '__main__':
    app.run(port=5000, debug=True)