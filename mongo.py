# mongo.py
import requests
from werkzeug.utils import redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import Flask, request, jsonify, url_for, render_template, flash, json

app = Flask(__name__, template_folder='templates')

'''
app.config['MONGO_DBNAME'] = "EmpMgmt"
app.config['MONGO_URI'] = "mongodb://localhost:27017/EmpMgmt"
'''

mongo = PyMongo(app, uri='mongodb://localhost:27017/EmpMgmt')


@app.route('/', methods=['GET'])
def home():
    return render_template('welcome.html')


@app.route('/user', methods=['GET'])
def get_all_users():
    output = []
    for s in emp.find():
        output.append({'emp_id': s['emp_id'], 'first_name': s['first_name'], 'last_name': s['last_name'],
                       'dept_name': s['dept_name'], 'gender': s['gender'], 'dob': s['dob'],
                       'salary': s['salary'], 'country_code': s['country_code'], 'mobile_no': s['mobile_no']})
    print("Output:", output)
    return render_template('user.html', emps=output)


@app.route('/search_user', methods=['GET', 'POST'])
def search_users():
    if request.method == 'POST':
        emp_id = int(request.form.get('emp_id'))
        output = []
        for s in emp.find({'emp_id': int(emp_id)}):
            output.append({'emp_id': s['emp_id'], 'first_name': s['first_name'], 'last_name': s['last_name'],
                           'dept_name': s['dept_name'], 'gender': s['gender'], 'dob': s['dob'],
                           'salary': s['salary'], 'country_code': s['country_code'], 'mobile_no': s['mobile_no']})
        print("Output:", output)
        return render_template('search_user.html', emps=output[0])
    return render_template('search_user.html', emps=None)


@app.route('/delete/<emp_id>', methods=['GET', 'DELETE'])
def delete_user(emp_id):
    if request.method == 'DELETE':
        emp.delete_one({'emp_id' : emp_id})
        return render_template('user.html')
    return 'You made it'


@app.route('/update_user/<emp_id>', methods=['GET', 'POST', 'DELETE'])
def update_user(emp_id):
    print("Employee ID:", emp_id)
    #output = emp.find({'emp_id': emp_id})
    output = []
    for s in emp.find({'emp_id': int(emp_id)}):
        output.append({'emp_id': s['emp_id'], 'first_name': s['first_name'], 'last_name': s['last_name'],
                       'dept_name': s['dept_name'], 'gender': s['gender'], 'dob': s['dob'],
                       'salary': s['salary'], 'country_code': s['country_code'], 'mobile_no': s['mobile_no']})
    print("Output:", output)
    if request.method == 'POST':
        if not request.form.get['emp_id'] or not request.form.get['first_name'] or not request.form.get['last_name'] \
                or not request.form.get['dept_name'] or not request.form.get['gender'] or not request.form.get['dob'] \
                or not request.form.get['salary'] or not request.form['country_code'] \
                or not request.form.get['mobile_no']:
            flash('Please enter all the fields', 'error')
        else:
            emp_id = int(request.form.get('emp_id'))
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            dept_name = request.form.get('dept_name')
            gender = request.form.get('gender')
            dob = request.form.get('dob')
            salary = float(request.form.get('salary'))
            country_code = int(request.form['country_code'])
            mobile_no = int(request.form.get('mobile_no'))
            emp.update_one({"emp_id": emp_id, "first_name": first_name, "last_name": last_name,
                            "dept_name": dept_name, "gender": gender, "dob": dob, "salary": salary,
                            "country_code": country_code, "mobile_no": mobile_no})
            flash('Employee Updated')
            return redirect('user.html')
    if request.method == 'DELETE':
        emp.delete_one({'emp_id': emp_id})
        return render_template('user.html')
    return render_template('update_user.html', emp_id=emp_id, output=output[0])


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        if not request.form.get('emp_id') or not request.form.get('first_name') \
                or not request.form.get('last_name') or not request.form.get('dept_name') \
                or not request.form.get('gender') or not request.form.get('dob') or not request.form.get('salary') \
                or not request.form['country_code'] or not request.form.get('mobile_no'):
            flash('Please enter all the fields', 'error')
        else:
            emp_id = int(request.form.get('emp_id'))
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            dept_name = request.form.get('dept_name')
            gender = request.form.get('gender')
            dob = request.form.get('dob')
            salary = float(request.form.get('salary'))
            country_code = int(request.form['country_code'])
            mobile_no = int(request.form.get('mobile_no'))
            emp.insert_one({"emp_id" : emp_id, "first_name" : first_name, "last_name" : last_name,
                            "dept_name" : dept_name, "gender" : gender, "dob" : dob, "salary" : salary,
                            "country_code" : country_code, "mobile_no" : mobile_no})
            return render_template('user.html')
            # return jsonify({'result' : output})
    return render_template('new_user.html')


if __name__ == '__main__':
    emp = mongo.db.Employee
    app.run(debug=True)