from flask import Flask, jsonify, request, session, make_response,redirect, url_for,Blueprint
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
from sqlalchemy import Date, and_
from datetime import datetime, timezone, timedelta
import json

app = Flask(__name__)
# CORS(app)
app.secret_key = 'f33924fea4dd7123a0daa9d2a7213679'
# Replace the following values with your database connection details
db_username = 'crm'
db_password = 'LSciYCtCK7tZXAxL'
db_host = '23.226.8.83'
db_database = 'crm'
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
###################################################################################
#######################Data model for dropdown list display as an option for data fill-in
#List BO code    
class BO(db.Model):
    __tablename__ = 'db_vn168_crm_bo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bo_code = db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.bo_code
#List category
class Category(db.Model):
    __tablename__ = 'db_vn168_crm_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.category
#List contact node
class Contact_Note(db.Model):
    __tablename__ = 'db_vn168_crm_contact_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note = db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.note
#List of call note
class Call_Note(db.Model):
    __tablename__ = 'db_vn168_crm_call_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    call_note = db.Column(db.String(255), primary_key = True,unique = True, nullable = False)
    def __repr__(self):
        return self.call_note
#########
class Zalo_Note(db.Model):
    __tablename__ = 'db_vn168__crm_zalo_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zalo_note= db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.zalo_note
class Tele_Note(db.Model):
    __tablename__ = 'db_vn168__crm_tele_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tele_note= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.tele_note
class SMS_Note(db.Model):
    __tablename__ = 'db_vn168__crm_sms_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sms_note= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.sms_note
class Social_Note(db.Model):
    __tablename__ = 'db_vn168__crm_social_note'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    social_note= db.Column(db.String(255), unique = True, nullable = False)
    def __repr__(self):
        return self.social_note
class Interactive_Content(db.Model): #Something called Nội dung tương tác
    __tablename__ = 'db_vn168__interactive_content'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.interaction_content
class Interactive_Result(db.Model): #Something called Nội dung tương tác
    __tablename__ = 'db_vn168__crm_interactive_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    result= db.Column(db.String(255),unique = True, nullable = False)
    def __repr__(self):
        return self.result 
class Customers(db.Model):
    __tablename__ = 'db_vn168__crm_customer'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    username = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = False)
    contact_note = db.Column(db.String(255), nullable = False)
    call_note = db.Column(db.String(255), nullable = False)
    zalo_note = db.Column(db.String(255), nullable = False)
    tele_note = db.Column(db.String(255),nullable = False)
    sms_note = db.Column(db.String(255),nullable = False)
    social_note = db.Column(db.String(255),nullable = False)
    interaction_content = db.Column(db.String(255), nullable = False)
    interaction_result = db.Column(db.String(255), nullable = False)
    person_in_charge = db.Column(db.String(255), nullable = False)
    filled_date = db.Column(Date, nullable = False)
    assistant = db.Column(db.String(255))
    def __repr__(self):
        return self.code
class Edit_Customer_Records(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime,  nullable=False, default = datetime.timestamp(datetime.now()))
    code = db.Column(db.String(255),  nullable = False)
    username = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    bo_code = db.Column(db.String(255), nullable = False)
    call_note = db.Column(db.String(255), nullable = False)
    zalo_note = db.Column(db.String(255), nullable = False)
    tele_note = db.Column(db.String(255),nullable = False)
    sms_note = db.Column(db.String(255),nullable = False)
    social_note = db.Column(db.String(255),nullable = False)
    interaction_content = db.Column(db.String(255), nullable = False)
    interaction_result = db.Column(db.String(255), nullable = False)
    person_in_charge = db.Column(db.String(255), nullable = False)
    filled_date = db.Column(Date, nullable = False)
    assistant = db.Column(db.String(255))
    def __repr__(self):
        return self.created_at
####Data model for tools management
#####SIM########
class Sim(db.Model):
    __tablename__ = 'db_vn168_crm_sim'
    sim_code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    number = db.Column(db.String(255), nullable = False)
    provider = db.Column(db.String(255))
    status = db.Column(db.String(255)) #Trạng thái
    package = db.Column(db.String(255))
    zalo_status = db.Column(db.String(255))
    tele_status = db.Column(db.String(255))
    tik_face_status = db.Column(db.String(255))
    sms_status = db.Column(db.String(255))
    storage_address = db.Column(db.String(255))
    sim_note = db.Column(db.String(255))
    def __repr__(self):
        return self.sim_code
#####IP###############
class IP(db.Model):
    __tablename__ = 'db_vn168_crm_ip'
    ip_code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    ip_info = db.Column(db.String(255), nullable = False)
    expired_date = db.Column(db.String(255))
    country = db.Column(db.String(255))
    provider = db.Column(db.String(255))
    status = db.Column(db.String(255))
    day_until_expiration = db.Column(db.String(255))
    zalo_note = db.Column(db.String(255))
    ip_note = db.Column(db.String(255))
#######Phone##################
class Phone(db.Model):
    __tablename__ = 'db_vn168_crm_phone'
    device_code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    num_zalo_acc_created = db.Column(db.String(255))
    num_zalo_acc_active = db.Column(db.String(255))
    num_zalo_acc_active = db.Column(db.String(255))
    online = db.Column(db.String(255))
    online_cls = db.Column(db.String(255))
    online_nkb = db.Column(db.String(255))
    online_agency = db.Column(db.String(255))
    num_sim = db.Column(db.Integer)
    number1 = db.Column(db.String(255))
    number2 = db.Column(db.String(255))
    phone_note = db.Column(db.String(255))
    
#######Data model for all contact method including zalo, tele, faceboook , tiktok
######Tool######################################################################
class Tool_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_tool_mgt'
    code = db.Column(db.String(255), primary_key = True, unique = True, nullable = False)
    category = db.Column(db.String(255))
    person_in_charge = db.Column(db.String(255))
    acc_note = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    acc_info = db.Column(db.String(255))
    ip_address = db.Column(db.String(255))
    note = db.Column(db.String(255))
####Employee session management table#########################
class Session_Mgt(db.Model):
    __tablename__ = 'db_vn168_crm_session_mgt'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    checkin_time = db.Column(Date, nullable = False)
    checkout_time = db.Column(Date, nullable = False)
#####Using Flask Blueprints to create hierarchical API endpoints#####
#Declare blueprint for CRM team
crm_bp = Blueprint('crm_bp', __name__, url_prefix='/crm')
social_bp = Blueprint('social_bp', __name__, url_prefix='/social')
dev_bp = Blueprint('dev_bp', __name__, url_prefix='/dev')
seo_bp = Blueprint('seo_bp', __name__, url_prefix='/seo')

##################################################
##Create aall tables that defined above
@app.route('/create_tables')
def create_tables():
    with app.app_context():
        db.create_all() 
    return 'All tables are created successfully'
#############################################################
@crm_bp.route('/show-record')
def show_records():
    records = Customers.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    dates = [{'filled_date':record.filled_date ,"end date":(datetime.now().date()-timedelta(days=10)),"Start date":datetime.strptime("2024-04-23", '%Y-%m-%d').date()} for record in records]
    return dates    
#Show all record
@crm_bp.route('/record')
def get_records():
    # users = Customers.query.all()
    query = Customers.query
    data = request.args
    page = int(data.get('page','1'))
    per_page = int(data.get('per_page','10'))
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    contact_note = data.get('contact_note')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    sms_note = data.get('sms_note')
    social_note = data.get('social_note')
    person_in_charge = data.get('person_in_charge')
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    assistant = data.get('assistant')
    start_date_str = data.get('start_date_str')
    end_date_str = data.get('end_date_str')
    try:
        # Parse the date string into a date object
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    except TypeError:
        start_date = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
        end_date = datetime.now().date()+ timedelta(days=10)
    # Query the database for customers matching the username and date
    param_mapping = {
            'username': Customers.username.like(f'%{username}%'),
            'category':Customers.category.like(f'%{category}%'),
            'bo_code':Customers.bo_code.like(f'%{bo_code}%'),
            'contact_note':Customers.contact_note.like(f'%{contact_note}%'),
            'call_note':Customers.call_note.like(f'%{call_note}%'),
            'zalo_note':Customers.zalo_note.like(f'%{zalo_note}%'),
            'tele_note':Customers.tele_note.like(f'%{tele_note}%'),
            'sms_note':Customers.sms_note.like(f'%{sms_note}%'),
            'social_note':Customers.social_note.like(f'%{social_note}%'),
            'person_in_charge':Customers.person_in_charge.like(f'%{person_in_charge}%'),
            'interaction_content':Customers.interaction_content.like(f'%{interaction_content}%'),
            'interaction_result':Customers.interaction_result.like(f'%{interaction_result}%'),
            'assistant':Customers.assistant.like(f'%{assistant}%'),
            'code':Customers.code.like(f'%{code}%'),
            'end_date':Customers.filled_date <= end_date,
            'start_date':Customers.filled_date >= start_date
    }
    for key, value in param_mapping.items():
        if key in data:
            query = query.filter(value)

    customers =  query.all()
    # customers = Customers.query.filter(
    #     and_(
    #         Customers.username.like(f'%{username}%'),
    #         Customers.category.like(f'%{category}%'),
    #         Customers.bo_code.like(f'%{bo_code}%'),
    #         Customers.call_note.like(f'%{call_note}%'),
    #         Customers.zalo_note.like(f'%{zalo_note}%'),
    #         Customers.tele_note.like(f'%{tele_note}%'),
    #         Customers.social_note.like(f'%{social_note}%'),
    #         Customers.person_in_charge.like(f'%{person_in_charge}%'),
    #         Customers.interaction_content.like(f'%{interaction_content}%'),
    #         Customers.interaction_result.like(f'%{interaction_result}%'),
    #         Customers.assistant.like(f'%{assistant}%'),
    #         Customers.code.like(f'%{code}%'),
    #         Customers.filled_date <= end_date,
    #         Customers.filled_date >= start_date)).all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    # customer_data = [{'code':customer.code, 'username':customer.username,'bo code':customer.bo_code,'zalo note':customer.zalo_note,'tele note':customer.tele_note,'date': customer.filled_date.isoformat()} for customer in customers]
    customer_data = [{'code':customer.code, 'username':customer.username,'category':customer.category,'bo_code':customer.bo_code,'contact_note':customer.contact_note,'call_note':customer.call_note,'zalo_note':customer.zalo_note,'tele_note':customer.tele_note,'sms_note': customer.sms_note,'social_note':customer.social_note,'interaction_content':customer.interaction_content,'interaction_result':customer.interaction_result,'person_in_charge':customer.person_in_charge,'filled_date': customer.filled_date.isoformat(),'assistant':customer.assistant} for customer in customers]
    paginated_data = customer_data[start_index:end_index]
    paginated_data = customer_data[start_index:end_index]

    return jsonify({'items': paginated_data, 'page': page, 'per_page': per_page, 'total_items': len(customer_data)})

    # return customer_data
################################################
##Save new record of customer to the Customer table
@crm_bp.route('/record', methods=['POST'])
def add_record():
    if not request.form:
        return jsonify({"error": "Missing JSON in request"}), 400
    data = request.form
    code = data.get('code')
    username = data.get('username')
    category = data.get('category')
    bo_code = data.get('bo_code')
    contact_note = data.get('contact_note')
    call_note = data.get('call_note')
    zalo_note = data.get('zalo_note')
    tele_note = data.get('tele_note')
    sms_note = data.get('sms_note')
    social_note = data.get('social_note')
    person_in_charge = data.get('person_in_charge')
    interaction_content = data.get('interaction_content')
    interaction_result = data.get('interaction_result')
    assistant = data.get('assistant')
    filled_date = datetime.now().strftime("%Y-%m-%d")
    # Check if the user already exists
    if Customers.query.filter((Customers.code == code)).first():
        return jsonify({"error": "Code is already existed, please try again"}), 409
    new_customer = Customers(code= code, username=username,category=category,bo_code=bo_code,contact_note = contact_note,call_note=call_note,zalo_note=zalo_note,tele_note=tele_note,sms_note = sms_note,social_note=social_note,interaction_content=interaction_content, interaction_result = interaction_result, person_in_charge = person_in_charge,filled_date = filled_date,assistant = assistant)
    db.session.add(new_customer)
    try:
        db.session.commit()
        return "User added successfully!"
    except Exception as e:
        db.session.rollback()  # Roll back the transaction if an error occurs
        return str(e)
#####Edit value for a specific code in Customer table
@crm_bp.route('/record/<string:code>',methods = ['PUT'])
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
    record.sms_note = data.get('sms_note')
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
            'sms' : record.sms_note,
            'social_note' : record.social_note,
            'person_in_charge' : record.person_in_charge,
            'interaction_content' : record.interaction_content,
            'interaction_result' : record.interaction_result,
            'assistant' : record.assistant,
        }
    }), 200
#######Delete record#############
@crm_bp.route('/record/<string:code>',methods = ['DELETE'])
def remove_record(code):
    record = Customers.query.get(code)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'Record deleted successfully'})
    else:
        # If the user does not exist, return a 404 error
        return jsonify({'error': 'Record not found'}), 404

#####Filter data box
# @crm_bp.route('/record/search', methods=['POST'])
# def filter_data():
#     if not request.form:
#         return jsonify({"error": "Please fill in the form for searching"}), 400
#     data = request.form
#     code = data.get('code')
#     username = data.get('username')
#     category = data.get('category')
#     bo_code = data.get('bo_code')
#     call_note = data.get('call_note')
#     zalo_note = data.get('zalo_note')
#     tele_note = data.get('tele_note')
#     social_note = data.get('social_note')
#     person_in_charge = data.get('person_in_charge')
#     interaction_content = data.get('interaction_content')
#     interaction_result = data.get('interaction_result')
#     assistant = data.get('assistant')
#     start_date_str = data.get('start_date')
#     end_date_str = data.get('end_date')
#     # Check if the user already exists
#     if not username:
#         return jsonify({'error': 'Missing username'}), 400

#     try:
#         # Parse the date string into a date object
#         start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
#         end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
#     except ValueError:
#         return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

#     # Query the database for customers matching the username and date
#     customers = Customers.query.filter(
#         and_(
#             Customers.username.like(f'%{username}%'),
#             Customers.category.like(f'%{category}%'),
#             Customers.bo_code.like(f'%{bo_code}%'),
#             Customers.call_note.like(f'%{call_note}%'),
#             Customers.zalo_note.like(f'%{zalo_note}%'),
#             Customers.tele_note.like(f'%{tele_note}%'),
#             Customers.social_note.like(f'%{social_note}%'),
#             Customers.person_in_charge.like(f'%{person_in_charge}%'),
#             Customers.interaction_content.like(f'%{interaction_content}%'),
#             Customers.interaction_result.like(f'%{interaction_result}%'),
#             Customers.assistant.like(f'%{assistant}%'),
#             Customers.code.like(f'%{code}%'),
#             Customers.filled_date <= end_date,
#             Customers.filled_date >= start_date)).all()

#     # Format results
#     results = [{'username': customer.username,'category': customer.category, 'filled_date': customer.filled_date.isoformat()} for customer in customers]
#     sorted_results =  sorted(results, key =  lambda x: x['filled_date'], reverse= True)
#     return jsonify(sorted_results)
#############################################
#################Dropdown List###############
#/crm/bo
#/crm/bo [POST]
#/crm/bo [DELETE]
@crm_bp.route('/bo')
def get_bo():
    boes = BO.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    bo_data = [{'bo_code':bo.bo_code} for bo in boes]
    return bo_data

#add multiple value to bo code
@crm_bp.route('/bo',methods = ['POST'])
def add_bo():
    try:
        data = request.json  # JSON payload containing data for new BO
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'}), 400

        for bo in data:
            # Validate data (e.g., check if bo_code is provided)
            if 'bo_code' not in bo:
                return jsonify({'error': 'bo_code is required for each BO'}), 400

            # Create a new BO object and add it to the session
            new_bo = BO(bo_code= bo['bo_code'])
            db.session.add(new_bo)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({'message': 'Users added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@crm_bp.route('/bo/<string:bo_code>',methods = ['DELETE'])
def remove_bo(bo_code):
    code = BO.query.get(bo_code)
    if code:
        db.session.delete(code)
        db.session.commit()
        return jsonify({'message':'bo code removed successfully'})
    else:
        return jsonify({'error':'bo code not found'}),404
#/crm/category
#/crm/category [POST]
#/crm/category [DELETE]
@crm_bp.route('/category')
def show_category():
    categories =  Category.query.all()
    categoy_data =  [{'category': category.category} for category in categories]
    return categoy_data
@crm_bp.route('/category', methods= ['POST'])
def add_category():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for category in data:
            if 'category'  not in category:
                return jsonify({'error':'category is require for each category table'})
            new_category = Category(category = category['category'])
            db.session.add(new_category)
        db.session.commit()
        return jsonify({'message':'Category added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/category/<string:category>', methods= ['DELETE'])
def remove_category(category):
    category_name = Category.query.filter(Category.category == category).first()
    if category_name:
        db.session.delete(category_name)
        db.session.commit()
        return jsonify({'message': 'Category removed successfully'})
    else:
        return jsonify({'error':'category not found'}),404
#/crm/contact_note
#/crm/contact_note [POST]
#/crm/contact_note [DELETE]
@crm_bp.route('/contact_note')
def show_contact_note():
    contact_notes = Contact_Note.query.all()
    contact_note_data = [{'contact_note': contact_note.note} for contact_note in contact_notes]
    return contact_note_data
@crm_bp.route('/contact_note', methods= ['POST'])
def add_contact_note():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for contact_note in data:
            if 'contact_note'  not in contact_note:
                return jsonify({'error':'contact_note is require for each contact_note table'})
            new_contact_note = Contact_Note(note = contact_note['contact_note'])
            db.session.add(new_contact_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/contact_note/<string:contact_note>', methods= ['DELETE'])
def remove_contact_note(contact_note):
    contact_note = Contact_Note.query.filter(Contact_Note.note == contact_note).first()
    if contact_note:
        db.session.delete(contact_note)
        db.session.commit()
        return jsonify({'message': 'contact_note removed successfully'})
    else:
        return jsonify({'error':'contact_note not found'}),404
#/crm/call_note 
#/crm/call_note [POST]
#/crm/call_note [DELETE]
@crm_bp.route("/call_note") #GET
def show_call_note():
    call_notes = Call_Note.query.all()
    call_note_data = [{'call_note': call_note.call_note} for call_note in call_notes]
    return call_note_data
@crm_bp.route('/call_note', methods= ['POST']) #POST
def add_call_note():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for call_note in data:
            if 'call_note'  not in call_note:
                return jsonify({'error':'call_note is require for each call_note table'})
            new_call_note = Call_Note(call_note = call_note['call_note'])
            db.session.add(new_call_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/call_note/<string:call_note>', methods= ['DELETE']) #DELETE
def remove_call_note(call_note):
    call_note = Call_Note.query.filter(Call_Note.call_note == call_note).first()
    if call_note:
        db.session.delete(call_note)
        db.session.commit()
        return jsonify({'message': 'call_note removed successfully'})
    else:
        return jsonify({'error':'call_note not found'}),404

#/crm/zalo_note
#/crm/zalo_note [POST]
#/crm/zalo_note [DELETE]

@crm_bp.route("/zalo_note") #GET
def show_zalo_note():
    zalo_notes = Zalo_Note.query.all()
    zalo_note_data = [{'zalo_note': zalo_note.zalo_note} for zalo_note in zalo_notes]
    return zalo_note_data
@crm_bp.route('/zalo_note', methods= ['POST']) #POST
def add_zalo_note():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for zalo_note in data:
            if 'zalo_note'  not in zalo_note:
                return jsonify({'error':'zalo_note is require for each call_note table'})
            new_zalo_note = Zalo_Note(zalo_note = zalo_note['zalo_note'])
            db.session.add(new_zalo_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/zalo_note/<string:zalo_note>', methods= ['DELETE']) #DELETE
def remove_zalo_note(zalo_note):
    zalo_note = Zalo_Note.query.filter(Zalo_Note.zalo_note == zalo_note).first()
    if zalo_note:
        db.session.delete(zalo_note)
        db.session.commit()
        return jsonify({'message': 'call_note removed successfully'})
    else:
        return jsonify({'error':'call_note not found'}),404
#/crm/tele_note 
#/crm/tele_note [POST]
#/crm/tele_note [DELETE]
@crm_bp.route("/tele_note") #GET
def show_tele_note():
    tele_notes = Tele_Note.query.all()
    tele_note_data = [{'tele_note': tele_note.tele_note} for tele_note in tele_notes]
    return tele_note_data
@crm_bp.route('/tele_note', methods= ['POST']) #POST
def add_tele_note():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for tele_note in data:
            if 'tele_note'  not in tele_note:
                return jsonify({'error':'tele_note is require for each tele_note table'})
            new_tele_note = Tele_Note(tele_note = tele_note['tele_note'])
            db.session.add(new_tele_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/tele_note/<string:tele_note>', methods= ['DELETE']) #DELETE
def remove_tele_note(tele_note):
    tele_note = Tele_Note.query.filter(Tele_Note.tele_note == tele_note).first()
    if tele_note:
        db.session.delete(tele_note)
        db.session.commit()
        return jsonify({'message': 'tele_note removed successfully'})
    else:
        return jsonify({'error':'tele_note not found'}),404
#/crm/sms_note 
#/crm/sms_note [POST]
#/crm/sms_note [DELETE    
@crm_bp.route("/sms_note") #GET
def show_sms_note():
    sms_notes = SMS_Note.query.all()
    sms_note_data = [{'sms_note': sms_note.sms_note} for sms_note in sms_notes]
    return sms_note_data
@crm_bp.route('/sms_note', methods= ['POST']) #POST
def add_sms_note():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for sms_note in data:
            if 'sms_note'  not in sms_note:
                return jsonify({'error':'sms_note is require for each sms_note table'})
            new_sms_note = SMS_Note(sms_note = sms_note['sms_note'])
            db.session.add(new_sms_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/sms_note/<string:sms_note>', methods= ['DELETE']) #DELETE
def remove_sms_note(sms_note):
    sms_note = SMS_Note.query.filter(SMS_Note.sms_note == sms_note).first()
    if sms_note:
        db.session.delete(sms_note)
        db.session.commit()
        return jsonify({'message': 'sms_note removed successfully'})
    else:
        return jsonify({'error':'sms_note not found'}),404

#/crm/social_note 
#/crm/social_note [POST]
#/crm/social_note [DELETE]
@crm_bp.route("/social_note") #GET
def show_social_note():
    social_notes = Social_Note.query.all()
    social_note_data = [{'social_note': social_note.social_note} for social_note in social_notes]
    return social_note_data
@crm_bp.route('/social_note', methods= ['POST']) #POST
def add_social_note():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for social_note in data:
            if 'social_note'  not in social_note:
                return jsonify({'error':'social_note is require for each social_note table'})
            new_social_note = Social_Note(social_note = social_note['social_note'])
            db.session.add(new_social_note)
        db.session.commit()
        return jsonify({'message':'Category(es) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/social_note/<string:social_note>', methods= ['DELETE']) #DELETE
def remove_social_note(social_note):
    social_note = Social_Note.query.filter(Social_Note.social_note == social_note).first()
    if social_note:
        db.session.delete(social_note)
        db.session.commit()
        return jsonify({'message': 'social_note removed successfully'})
    else:
        return jsonify({'error':'social_note not found'}),404
#/crm/interactive_content 
#/crm/interactive_content [POST]
#/crm/interactive_content [DELETE]
@crm_bp.route("/interactive_content") #GET
def show_interactive_content():
    contents = Interactive_Content.query.all()
    interactive_content_data = [{'content': content.content} for content in contents]
    return interactive_content_data
@crm_bp.route('/interactive_content', methods= ['POST']) #POST
def add_interactive_content():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for content in data:
            if 'content'  not in content:
                return jsonify({'error':'content is require for each content table'})
            new_interactive_content = Interactive_Content(content = content['content'])
            db.session.add(new_interactive_content)
        db.session.commit()
        return jsonify({'message':'interactive_content(s) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/interactive_content/<string:content>', methods= ['DELETE']) #DELETE
def remove_interactive_content(content):
    interactive_content = Interactive_Content.query.filter(Interactive_Content.content == content).first()
    if interactive_content:
        db.session.delete(interactive_content)
        db.session.commit()
        return jsonify({'message': 'content removed successfully'})
    else:
        return jsonify({'error':'content not found'}),404
#/crm/interactive_result 
#/crm/interactive_result [POST]
#/crm/interactive_result [DELETE]
@crm_bp.route("/interactive_result") #GET
def show_interactive_result():
    results = Interactive_Result.query.all()
    interactive_result_data = [{'result': result.result} for result in results]
    return interactive_result_data
@crm_bp.route('/interactive_result', methods= ['POST']) #POST
def add_interactive_result():
    try:
        data = request.json
        if not data or not isinstance(data, list):
            return jsonify({'error': 'Invalid JSON data'})
        for result in data:
            if 'result'  not in result:
                return jsonify({'error':'result is require for each result table'})
            result = Interactive_Result(result = result['result'])
            db.session.add(result)
        db.session.commit()
        return jsonify({'message':'interactive_result(s) added successfully'}),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),500
@crm_bp.route('/interactive_result/<string:result>', methods= ['DELETE']) #DELETE
def remove_interactive_result(result):
    result = Interactive_Result.query.filter(Interactive_Result.result == result).first()
    if result:
        db.session.delete(result)
        db.session.commit()
        return jsonify({'message': 'result removed successfully'})
    else:
        return jsonify({'error':'result not found'}),404



#######################################################################################################
#Skip to User Managemenet enpoints
@app.route('/user')
def show_users():
    users = User.query.all()
    # user_data = [{'username':user.username, 'role':user.role,'company_id':user.company_id,'nickname':user.company_name,'team':user.team} for user in users]
    user_data = {user.username: {'role': user.role,'company_id': user.company_id,'company_id': user.company_id,'company_name': user.company_name,'team': user.team} for user in users}
    return user_data
#Add user, not register
@app.route('/add_user', methods=['POST'])
def add_user():
    if 'role' in session and session['role'] == 'CEO':
        # users  =  get_users()
        if not request.form:
            return jsonify({"error": "Missing JSON in request"}), 400
        data = request.form
        username = data.get('username')
        password = data.get('username')
        company_name = data.get('company_name')
        company_id = data.get('company_id')
        role = data.get('role')
        team = data.get('team')
        # Check if the user already exists
        if User.query.filter((User.username == username)).first():
            return jsonify({"error": "User is already existed, please try again"}), 409
        new_user = User(username=username,password=password,company_name=company_name,company_id=company_id,role=role,team=team)
        db.session.add(new_user)
        try:
            db.session.commit()
            return "User added successfully!"
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if an error occurs
            return str(e)
@app.route('/user/<string:username>', methods = ['DELETE'])
def remove_user(username):
    if 'role' in session and session['role']:
        username = Customers.query.get(username)
        if username:
            db.session.delete(username)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'})
        else:
            # If the user does not exist, return a 404 error
            return jsonify({'error': 'Record not found'}), 404
    else:
        return  jsonify({'error': 'unauthenticated login'}), 401
# Middleware to check if the user is authenticated
@app.before_request
def check_authentication():
    session_cookie = request.cookies.get('session') 
    if request.endpoint != 'login' and 'username' not in session and session_cookie != True:
        return redirect(url_for('login'))

# Login endpoint

@app.route('/login', methods=['POST', 'GET'])
def login():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)
    user_data = User.query.all()
    users = {user.username: {'password': user.password} for user in user_data}

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        if username in users and users[username]['password'] == password:
            session['username'] = username
            role = User.query.get(session['username']).role
            session['role'] = role
            return jsonify({'message': 'Welcome, {},you are logging in as {}!'.format(session['username'],session['role'])})#session['username']
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    return  jsonify({'error': 'unauthenticated login'}), 401

# Logout endpoint
@app.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'logged out!'})

# Index page
# @app.route('/loggedin')
# def loggedin():
#     # role = User.query.get.filter(User.role == session['username'])
#     return jsonify({'message': 'Welcome, {},you are logging in as {}!'.format(session['username'],session['role'])})#session['username']


@crm_bp.route('/test')
def test():
    # data = request.form
    # date_string  = data.get('date')
    # date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    # customers = Customers.query.filter(Customers.username == 'shangđasdasđsd')
    # test_list = [{'username': customer.username, 'datre': customer.filled_date >= date_obj} for customer in customers]
    # # return {'str':date_obj}
    contact_note = Contact_Note.query.filter(Contact_Note.note == 'sda')
    notes =  [{'note': note.note} for note in contact_note]
    
    return notes
@crm_bp.route('/')
def home():
    return "Home Page"
@crm_bp.route('/api/data')
def get_data():
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)
@crm_bp.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Implement logic to fetch users from the database
        return "<a href='dantri.com'>"
    elif request.method == 'POST':
        # Implement logic to create a new user in the database
        pass
@crm_bp.route('/index')
def index():
    return {"name":"sang"}
app.register_blueprint(crm_bp)
app.register_blueprint(social_bp)
app.register_blueprint(dev_bp)
app.register_blueprint(seo_bp)
if __name__ == '__main__':
    app.run(port=5000, debug=True)