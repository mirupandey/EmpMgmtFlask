from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, MetaData
from sqlalchemy.dialects import mysql


def create_tables_and_insert_dummy_data(meta, engine):
    """
        A method to create database tables and insert dummy datas
    :return: None
    """
    admin = Table(
        'admin', meta,
        Column('username', String, primary_key=True, nullable=False),
        Column('password', String, nullable=False)
    )

    employee = Table(
        'employee', meta,
        Column('employee_id', String, nullable=False, unique=True, primary_key=True),
        Column('password', String, nullable=False),
        Column('first_name', String, nullable=False),
        Column('last_name', String, nullable=False),
        Column('dept_id', Integer, ForeignKey("dept.dept_id"), nullable=False),
        Column('gender', String(1), nullable=False),
        Column('mobile_no', mysql.INTEGER(10), nullable=False, unique=True),
        Column('dob', Date, nullable=False)
    )

    dept = Table(
        'dept', meta,
        Column('dept_id', Integer, unique=True, nullable=False, primary_key=True),
        Column('dept_name', String, nullable=False, unique=True)
    )

    meta.create_all(engine)

    admin_insert(admin, 'admin', 'admin123')

    emp_insert(employee, 123, 'miru123', 'Mrinal', 'Pandey', 101, 'Female', '9784314332',
               datetime.strptime('1995-06-06', "%Y-%m-%d").date())

    emp_insert(employee, 124, 'aayu123', 'Aayushi', 'Priya', 102, 'Female', 9887908868,
               datetime.strptime('1996-11-08', "%Y-%m-%d").date())

    dept_insert(dept, 101, 'Development')
    dept_insert(dept, 102, 'Support')
    dept_insert(dept, 103, 'Testing')
    dept_insert(dept, 104, 'Maintenance')


def emp_insert(emp, employee_id, password, first_name, last_name, dept_id, gender, mobile_no, dob):

    employee_login_insert = emp.insert()
    employee_login_insert.execute(employee_id=employee_id, password=password, first_name=first_name,
                                  last_name=last_name, dept_id=dept_id, gender=gender, mobile_no=mobile_no,
                                  dob=dob)


def admin_insert(admin, username, password):

    admin_login_insert = admin.insert()
    admin_login_insert.execute(username=username, password=password)


def dept_insert(dept, dept_id, dept_name):

    department_insert = dept.insert()
    department_insert.execute(dept_id=dept_id, dept_name=dept_name)
