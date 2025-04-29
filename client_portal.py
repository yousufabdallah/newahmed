from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect('management.db')
    c = conn.cursor()
    
    # Create clients table
    c.execute('''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        phone TEXT,
        email TEXT
    )''')
    
    # Create government entities table
    c.execute('''CREATE TABLE IF NOT EXISTS government_entities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    
    # Create services table
    c.execute('''CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_id INTEGER,
        service_name TEXT NOT NULL,
        government_fee REAL,
        office_fee REAL,
        FOREIGN KEY (entity_id) REFERENCES government_entities (id),
        UNIQUE(entity_id, service_name)
    )''')
    
    # Create tasks table
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        description TEXT,
        cost REAL,
        profit REAL,
        status TEXT,
        creation_date TEXT,
        completion_date TEXT,
        receipt_path TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )''')
    
    # Create task services table
    c.execute('''CREATE TABLE IF NOT EXISTS task_services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        service_id INTEGER,
        FOREIGN KEY (task_id) REFERENCES tasks (id),
        FOREIGN KEY (service_id) REFERENCES services (id)
    )''')
    
    conn.commit()
    conn.close()

def update_db_schema():
    conn = sqlite3.connect('management.db')
    c = conn.cursor()
    
    # إضافة عمود receipt_path إلى جدول tasks إذا لم يكن موجود
    try:
        c.execute('ALTER TABLE tasks ADD COLUMN receipt_path TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        # العمود موجود بالفعل
        pass
    
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('management.db')
    conn.row_factory = sqlite3.Row
    return conn

# تهيئة قاعدة البيانات عند بدء التطبيق
init_db()
update_db_schema()  # تحديث هيكل قاعدة البيانات بعد init_db مباشرة

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    
    if not name or not phone:
        flash('جميع الحقول مطلوبة', 'error')
        return redirect(url_for('register'))
    
    conn = get_db_connection()
    try:
        # التحقق من عدم وجود رقم الهاتف مسبق
        existing_client = conn.execute('SELECT * FROM clients WHERE phone = ?', (phone,)).fetchone()
        if existing_client:
            flash('رقم الهاتف مسجل مسبق', 'error')
            return redirect(url_for('register'))
        
        # إضافة العميل الجديد
        conn.execute('INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)',
                    (name, phone, email))
        conn.commit()
        flash('تم التسجيل بنجاح. يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('login'))
        
    except sqlite3.Error as e:
        flash('حدث خطأ أثناء التسجيل. الرجاء المحاولة مرة أخرى', 'error')
        return redirect(url_for('register'))
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login_post():
    phone = request.form.get('phone')
    
    if not phone:
        flash('الرجاء إدخال رقم الهاتف', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM clients WHERE phone = ?', (phone,)).fetchone()
    conn.close()
    
    if client:
        session['client_id'] = client['id']
        session['client_name'] = client['name']
        return redirect(url_for('show_entities'))  # تم تصحيح اسم المسار هنا
    else:
        flash('رقم الهاتف غير مسجل', 'error')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'client_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    tasks = conn.execute('''
        SELECT tasks.*, services.service_name 
        FROM tasks 
        JOIN task_services ON tasks.id = task_services.task_id 
        JOIN services ON task_services.service_id = services.id 
        WHERE tasks.client_id = ? 
        ORDER BY tasks.creation_date DESC
    ''', (session['client_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', 
                         client_name=session['client_name'],
                         tasks=tasks)

@app.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('login'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'client_id' not in session:
            flash('الرجاء تسجيل الدخول أولاً', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/entities')
@login_required
def show_entities():
    conn = get_db_connection()
    entities = conn.execute('SELECT * FROM government_entities').fetchall()
    conn.close()
    return render_template('entities.html', entities=entities)

@app.route('/entity_services/<int:entity_id>')
@login_required
def show_entity_services(entity_id):
    conn = get_db_connection()
    services = conn.execute('''
        SELECT services.*, government_entities.name as entity_name 
        FROM services 
        JOIN government_entities ON services.entity_id = government_entities.id 
        WHERE entity_id = ?
    ''', (entity_id,)).fetchall()
    conn.close()
    return render_template('services.html', services=services)

@app.route('/service_details/<int:service_id>')
@login_required
def service_details(service_id):
    conn = get_db_connection()
    service = conn.execute('''
        SELECT services.*, government_entities.name as entity_name 
        FROM services 
        JOIN government_entities ON services.entity_id = government_entities.id 
        WHERE services.id = ?
    ''', (service_id,)).fetchone()
    conn.close()
    return render_template('service_details.html', service=service)

@app.route('/submit_request/<int:service_id>', methods=['POST'])
def submit_request(service_id):
    if 'client_id' not in session:
        return redirect(url_for('login'))
    
    if 'receipt' not in request.files:
        flash('لم يتم تحميل الإيصال', 'error')
        return redirect(url_for('service_details', service_id=service_id))
    
    file = request.files['receipt']
    if file.filename == '':
        flash('لم يتم اختيار ملف', 'error')
        return redirect(url_for('service_details', service_id=service_id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        conn = get_db_connection()
        try:
            # الحصول على معلومات الخدمة
            service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
            
            # التعامل مع القيم الصفرية
            government_fee = service['government_fee'] if service['government_fee'] is not None else 0
            office_fee = service['office_fee'] if service['office_fee'] is not None else 0
            total_cost = government_fee + office_fee
            
            # إدخال المهمة الجديدة
            c = conn.execute('''
                INSERT INTO tasks 
                (client_id, status, creation_date, receipt_path, description, cost)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                session['client_id'],
                'pending',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                filename,
                f"طلب خدمة جديد - {service['service_name']}",
                total_cost
            ))
            
            task_id = c.lastrowid
            
            # ربط المهمة بالخدمة
            conn.execute('''
                INSERT INTO task_services (task_id, service_id)
                VALUES (?, ?)
            ''', (task_id, service_id))
            
            conn.commit()
            flash('تم تقديم الطلب بنجاح', 'success')
            return redirect(url_for('my_requests'))
            
        except Exception as e:
            conn.rollback()
            flash('حدث خطأ أثناء تقديم الطلب', 'error')
            return redirect(url_for('service_details', service_id=service_id))
        finally:
            conn.close()

@app.route('/confirm_completion/<int:task_id>', methods=['POST'])
def confirm_completion(task_id):
    if 'client_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    try:
        # Get task details before updating
        task = conn.execute('''
            SELECT tasks.*, services.government_fee, services.office_fee
            FROM tasks 
            JOIN task_services ON tasks.id = task_services.task_id
            JOIN services ON task_services.service_id = services.id
            WHERE tasks.id = ? AND tasks.client_id = ?
        ''', (task_id, session['client_id'])).fetchone()
        
        if not task:
            flash('الطلب غير موجود', 'error')
            return redirect(url_for('my_requests'))
        
        # Calculate total cost and profit, handling NULL values
        government_fee = task['government_fee'] if task['government_fee'] is not None else 0
        office_fee = task['office_fee'] if task['office_fee'] is not None else 0
        
        total_cost = government_fee + office_fee
        profit = office_fee  # الربح هو رسوم المكتب فقط
        
        # Update task status and add completion details
        current_date = datetime.now().strftime('%Y-%m-%d')
        conn.execute('''
            UPDATE tasks 
            SET status = 'منجزة',
                completion_date = ?,
                cost = ?,
                profit = ?
            WHERE id = ?
        ''', (current_date, total_cost, profit, task_id))
        
        conn.commit()
        flash('تم تأكيد إنجاز المهمة بنجاح', 'success')
        
    except Exception as e:
        conn.rollback()
        flash('حدث خطأ أثناء تأكيد إنجاز المهمة', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('my_requests'))

@app.route('/my_requests')
@login_required
def my_requests():
    conn = get_db_connection()
    tasks = conn.execute('''
        SELECT tasks.*, services.service_name, services.government_fee, services.office_fee,
               government_entities.name as entity_name
        FROM tasks 
        JOIN task_services ON tasks.id = task_services.task_id 
        JOIN services ON task_services.service_id = services.id 
        JOIN government_entities ON services.entity_id = government_entities.id
        WHERE tasks.client_id = ? 
        ORDER BY tasks.creation_date DESC
    ''', (session['client_id'],)).fetchall()
    conn.close()
    
    return render_template('my_requests.html', tasks=tasks)  # تأكد من وجود ملف my_requests.html

if __name__ == '__main__':
    # تأكد من وجود مجلد التحميلات
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # تشغيل التطبيق في وضع التطوير
    app.run(debug=True)


