import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

def init_db():
    conn = sqlite3.connect('management.db')
    c = conn.cursor()
    
    # إنشاء جدول العملاء إذا لم يكن موجود
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL,
                  phone TEXT,
                  email TEXT)''')
    
    conn.commit()
    conn.close()

# استدعاء الدالة عند بدء التطبيق
init_db()

class ManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة المهام")
        # تصغير حجم النافذة الرئيسية
        self.root.geometry("800x600")
        
        # تعيين الألوان العصرية
        self.colors = {
            'primary': '#2196F3',  # أزرق فاتح
            'primary_dark': '#1976D2',  # أزرق غامق
            'accent': '#FF4081',  # وردي
            'white': '#FFFFFF',
            'gray_50': '#FAFAFA',
            'gray_100': '#F5F5F5',
            'gray_200': '#EEEEEE',
            'text_primary': '#212121',
            'text_secondary': '#757575',
            'shadow': '#00000020'
        }
        
        # تهيئة النمط
        self.setup_styles()
        
        # إنشاء قاعدة البيانات
        self.create_database()
        
        # تهيئة الواجهة الرئيسية
        self.setup_main_window()

    def clear_window(self):
        """مسح جميع العناصر من إطار المحتوى"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_back_button(self):
        """إنشاء زر العودة"""
        back_frame = ttk.Frame(self.content_frame, style='Main.TFrame')
        back_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        back_btn = ttk.Button(
            back_frame,
            text="العودة للقائمة الرئيسية",
            style='Secondary.TButton',
            command=self.show_main_menu
        )
        back_btn.pack(side=tk.RIGHT)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # تصغير حجم الخطوط والتباعد
        style.configure('Main.TFrame', 
            background=self.colors['gray_50']
        )
        
        style.configure('Card.TFrame',
            background=self.colors['white'],
            relief='flat'
        )
        
        # تصغير حجم الأزرار الرئيسية
        style.configure('Primary.TButton',
            background=self.colors['primary'],
            foreground=self.colors['white'],
            padding=(20, 10),  # تقليل التباعد
            font=('Helvetica', 10),  # تصغير حجم الخط
            borderwidth=0
        )
        style.map('Primary.TButton',
            background=[('active', self.colors['primary_dark'])]
        )
        
        # تصغير حجم الأزرار الثانوية
        style.configure('Secondary.TButton',
            background=self.colors['gray_100'],
            foreground=self.colors['text_primary'],
            padding=(15, 8),  # تقليل التباعد
            font=('Helvetica', 9),  # تصغير حجم الخط
            borderwidth=0
        )
        
        # تصغير حجم العناوين
        style.configure('Title.TLabel',
            background=self.colors['gray_50'],
            foreground=self.colors['text_primary'],
            font=('Helvetica', 20, 'bold'),  # تصغير حجم الخط
            padding=(0, 10)  # تقليل التباعد
        )
        
        # تصغير حجم العناوين الفرعية
        style.configure('Subtitle.TLabel',
            background=self.colors['white'],
            foreground=self.colors['text_secondary'],
            font=('Helvetica', 12),  # تصغير حجم الخط
            padding=(0, 5)  # تقليل التباعد
        )
        
        # تصغير حجم الجداول
        style.configure('Modern.Treeview',
            background=self.colors['white'],
            fieldbackground=self.colors['white'],
            foreground=self.colors['text_primary'],
            rowheight=30,  # تقليل ارتفاع الصفوف
            font=('Helvetica', 9)  # تصغير حجم الخط
        )
        style.configure('Modern.Treeview.Heading',
            background=self.colors['primary'],
            foreground=self.colors['white'],
            padding=(8, 6),  # تقليل التباعد
            font=('Helvetica', 10, 'bold')  # تصغير حجم الخط
        )
        style.map('Modern.Treeview',
            background=[('selected', self.colors['primary'] + '20')],
            foreground=[('selected', self.colors['text_primary'])]
        )
        
        # تنسيق حقول الإدخال
        style.configure('Modern.TEntry',
            padding=(15, 10),
            selectbackground=self.colors['primary']
        )
        
        # تنسيق القوائم المنسدلة
        style.configure('Modern.TCombobox',
            padding=(15, 10),
            selectbackground=self.colors['primary']
        )

    def setup_main_window(self):
        # إعداد الإطار الرئيسي
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط التنقل العلوي
        self.navbar = ttk.Frame(self.main_frame, style='Card.TFrame')
        self.navbar.pack(fill=tk.X, padx=0, pady=0)
        ttk.Label(
            self.navbar,
            text="نظام إدارة المهام",
            style='Title.TLabel'
        ).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # إطار المحتوى
        self.content_frame = ttk.Frame(self.main_frame, style='Main.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        
        #إطار البطاقات
        cards_frame = ttk.Frame(self.content_frame, style='Main.TFrame')
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # تعريف البطاقات
        cards = [
            {
                "title": "تسجيل العملاء",
                "icon": "👥",
                "command": self.show_clients
            },
            {
                "title": "الوزارات والجهات الحكومية",
                "icon": "🏛️",
                "command": self.show_government
            },
            {
                "title": "الطلبات الجديدة",  # إضافة قسم جديد
                "icon": "📨",
                "command": self.show_new_requests
            },
            {
                "title": "تسجيل المهام",
                "icon": "📝",
                "command": self.show_tasks
            },
            {
                "title": "المهام الغير منجزة",
                "icon": "⏳",
                "command": self.show_incomplete_tasks
            },
            {
                "title": "المهام المنجزة",
                "icon": "✅",
                "command": self.show_completed_tasks
            },
            {
                "title": "الأرباح",
                "icon": "💰",
                "command": self.show_profits
            }
        ]
        
        # إنشاء شبكة من البطاقات (2×3)
        for i, card in enumerate(cards):
            row = i // 3  # تغيير التخطيط إلى 3 بطاقات في كل صف
            col = i % 3
            
            #إطار البطاقة
            card_frame = ttk.Frame(cards_frame, style='Card.TFrame')
            card_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")  # تقليل التباعد
            
            # إضافة ظل للبطاقة
            card_frame.bind('<Enter>', lambda e, cf=card_frame: self.add_card_hover(cf))
            card_frame.bind('<Leave>', lambda e, cf=card_frame: self.remove_card_hover(cf))
            
            # أيقونة البطاقة
            ttk.Label(
                card_frame,
                text=card["icon"],
                font=('Segoe UI Emoji', 36),  # تصغير حجم الأيقونة
                background=self.colors['white']
            ).pack(pady=(10, 5))  # تقليل التباعد
            
            # عنوان البطاقة
            ttk.Label(
                card_frame,
                text=card["title"],
                style='Subtitle.TLabel'
            ).pack(pady=(0, 10))
            
            # زر البطاقة
            ttk.Button(
                card_frame,
                text="فتح",
                command=card["command"],
                style='Primary.TButton'
            ).pack(pady=(0, 10))
        
        # تكوين الشبكة
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(2, weight=1)  # إضافة العمود الثالث

    def add_card_hover(self, card):
        """إضافة تأثير التحويم على البطاقة"""
        card.configure(relief='solid', borderwidth=1)
        
    def remove_card_hover(self, card):
        """إزالة تأثير التحويم من البطاقة"""
        card.configure(relief='flat', borderwidth=0)

    def create_form_frame(self, title):
        """إنشاء إطار نموذج عصري"""
        form_frame = ttk.Frame(self.content_frame, style='Card.TFrame')
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # إضافة ظل للإطار
        form_frame.configure(relief='solid', borderwidth=1)
        
        # العنوان
        ttk.Label(
            form_frame,
            text=title,
            style='Subtitle.TLabel'
        ).pack(pady=15)
        
        return form_frame

    def create_data_table(self, parent, columns, headings):
        """إنشاء جدول عرض عصري"""
        #إطار الجدول
        table_frame = ttk.Frame(parent, style='Card.TFrame')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # إنشاء الجدول
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style='Modern.Treeview'
        )
        
        # إعداد أعمدة الجدول
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, anchor="center", minwidth=150)
        
        # إضافة شريط التمرير
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # تنسيق الجدول
        tree.pack(side="top", fill=tk.BOTH, expand=True)
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        
        return tree

    def show_clients(self):
        self.clear_window()
        self.create_back_button()
        
        # إطار رئيسي
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # إطار النموذج
        form_frame = ttk.LabelFrame(main_frame, text="تسجيل العملاء", padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # حقول الإدخال
        ttk.Label(form_frame, text="اسم العميل:").grid(row=0, column=1, pady=5, padx=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=0, pady=5, padx=5)
        
        ttk.Label(form_frame, text="رقم الهاتف:").grid(row=1, column=1, pady=5, padx=5)
        phone_entry = ttk.Entry(form_frame)
        phone_entry.grid(row=1, column=0, pady=5, padx=5)
        
        ttk.Label(form_frame, text="البريد الإلكتروني:").grid(row=2, column=1, pady=5, padx=5)
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=2, column=0, pady=5, padx=5)
        
        # جدول العملاء
        tree_frame = ttk.LabelFrame(main_frame, text="قائمة العملاء", padding="10")
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء الجدول مع شريط التمرير
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("name", "phone", "email"), show="headings",
                            yscrollcommand=tree_scroll.set)
        tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll.config(command=tree.yview)
        
        # تعيين عناوين الأعمدة
        tree.heading("name", text="اسم العميل")
        tree.heading("phone", text="رقم الهاتف")
        tree.heading("email", text="البريد الإلكتروني")
        
        # تعيين عرض الأعمدة
        tree.column("name", width=150)
        tree.column("phone", width=120)
        tree.column("email", width=200)
        
        def save_client():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
                return
                
            try:
                conn = sqlite3.connect('management.db')
                c = conn.cursor()
                c.execute("INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)",
                         (name, phone, email))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("نجاح", "تم تسجيل العميل بنجاح")
                name_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                update_table()
                
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "هذا العميل موجود مسبق<|im_start|>")
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ البيانات: {str(e)}")
        
        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("SELECT name, phone, email FROM clients ORDER BY name")
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        def delete_client():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("تنبيه", "الرجاء اختيار عميل للحذف")
                return
                
            if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا العميل؟"):
                client_name = tree.item(selected_item)['values'][0]
                conn = sqlite3.connect('management.db')
                c = conn.cursor()
                c.execute("DELETE FROM clients WHERE name=?", (client_name,))
                conn.commit()
                conn.close()
                update_table()
                messagebox.showinfo("نجاح", "تم حذف العميل بنجاح")
        
        # إطار الأزرار
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="حفظ", command=save_client).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="حذف", command=delete_client).pack(side=tk.LEFT, padx=5)
        
        # تحديث الجدول عند فتح النافذة
        update_table()

    def show_government(self):
        self.clear_window()
        self.create_back_button()
        
        # إنشاء الإطار الرئيسي
        main_frame = ttk.Frame(self.content_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء الإطارات الفرعية
        entity_frame = ttk.LabelFrame(main_frame, text="تسجيل جهة حكومية", padding="20")
        entity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        service_frame = ttk.LabelFrame(main_frame, text="تسجيل خدمة", padding="20")
        service_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # إضافة دالة تعديل الجهة الحكومية
        def edit_entity():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("تنبيه", "الرجاء اختيار جهة حكومية للتعديل")
                return
                
            entity_name = tree.item(selected_items[0])['values'][0]
            
            # إنشاء نافذة التعديل
            edit_window = tk.Toplevel(self.content_frame)
            edit_window.title("تعديل الجهة الحكومية")
            edit_window.geometry("400x150")
            
            ttk.Label(edit_window, text="الاسم الجديد:").pack(pady=5)
            new_name_entry = ttk.Entry(edit_window)
            new_name_entry.insert(0, entity_name)
            new_name_entry.pack(pady=5)
            
            def save_changes():
                new_name = new_name_entry.get().strip()
                if not new_name:
                    messagebox.showerror("خطأ", "يرجى إدخال اسم الجهة")
                    return
                    
                conn = sqlite3.connect('management.db')
                c = conn.cursor()
                try:
                    c.execute("UPDATE government_entities SET name = ? WHERE name = ?", 
                             (new_name, entity_name))
                    conn.commit()
                    messagebox.showinfo("نجاح", "تم تعديل اسم الجهة بنجاح")
                    edit_window.destroy()
                    update_entities()
                    update_services()
                except sqlite3.IntegrityError:
                    messagebox.showerror("خطأ", "هذا الاسم موجود مسبق<|im_start|>")
                finally:
                    conn.close()
            
            ttk.Button(edit_window, text="حفظ التغييرات", command=save_changes).pack(pady=10)

        # إضافة دالة تعديل الخدمة
        def edit_service():
            selected_items = tree.selection()
            if not selected_items:
                messagebox.showwarning("تنبيه", "الرجاء اختيار خدمة للتعديل")
                return
                
            service_data = tree.item(selected_items[0])['values']
            
            # إنشاء نافذة التعديل
            edit_window = tk.Toplevel(self.content_frame)
            edit_window.title("تعديل الخدمة")
            edit_window.geometry("400x300")
            
            ttk.Label(edit_window, text="اسم الخدمة:").pack(pady=5)
            service_name_entry = ttk.Entry(edit_window)
            service_name_entry.insert(0, service_data[1])
            service_name_entry.pack(pady=5)
            
            ttk.Label(edit_window, text="رسوم الخدمة الحكومية:").pack(pady=5)
            gov_fee_entry = ttk.Entry(edit_window)
            gov_fee_entry.insert(0, service_data[2])
            gov_fee_entry.pack(pady=5)
            
            ttk.Label(edit_window, text="رسوم المكتب:").pack(pady=5)
            office_fee_entry = ttk.Entry(edit_window)
            office_fee_entry.insert(0, service_data[3])
            office_fee_entry.pack(pady=5)
            
            def save_changes():
                new_name = service_name_entry.get().strip()
                new_gov_fee = gov_fee_entry.get().strip()
                new_office_fee = office_fee_entry.get().strip()
                
                if not all([new_name, new_gov_fee, new_office_fee]):
                    messagebox.showerror("خطأ", "يرجى إكمال جميع الحقول")
                    return
                    
                try:
                    new_gov_fee = float(new_gov_fee)
                    new_office_fee = float(new_office_fee)
                except ValueError:
                    messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للرسوم")
                    return
                    
                conn = sqlite3.connect('management.db')
                c = conn.cursor()
                try:
                    c.execute("""
                        UPDATE services 
                        SET service_name = ?, government_fee = ?, office_fee = ?
                        WHERE service_name = ? AND entity_id = (
                            SELECT id FROM government_entities WHERE name = ?
                        )
                    """, (new_name, new_gov_fee, new_office_fee, service_data[1], service_data[0]))
                    conn.commit()
                    messagebox.showinfo("نجاح", "تم تعديل الخدمة بنجاح")
                    edit_window.destroy()
                    update_services()
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ أثناء التعديل: {str(e)}")
                finally:
                    conn.close()
            
            ttk.Button(edit_window, text="حفظ التغييرات", command=save_changes).pack(pady=10)

        # إضافة أزرار التعديل
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Button(button_frame, text="تعديل الجهة المحددة", command=edit_entity).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="تعديل الخدمة المحددة", command=edit_service).pack(side=tk.LEFT, padx=5)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل جهة حكومية"
        ttk.Label(entity_frame, text="اسم الجهة:").grid(row=0, column=0, pady=5)
        entity_name = ttk.Entry(entity_frame)
        entity_name.grid(row=0, column=1, pady=5)
        
        def save_entity():
            name = entity_name.get()
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم الجهة")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO government_entities (name) VALUES (?)", (name,))
                conn.commit()
                messagebox.showinfo("نجاح", "تم تسجيل الجهة بنجاح")
                entity_name.delete(0, tk.END)
                update_entities()
                update_services()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "هذه الجهة موجودة مسبق<|im_start|>")
            conn.close()
        
        ttk.Button(entity_frame, text="حفظ الجهة", command=save_entity).grid(row=0, column=2, padx=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل خدمة"
        ttk.Label(service_frame, text="اختر الجهة:").grid(row=0, column=0, pady=5)
        entity_var = tk.StringVar()
        entity_combo = ttk.Combobox(service_frame, textvariable=entity_var)
        entity_combo.grid(row=0, column=1, pady=5)
        
        ttk.Label(service_frame, text="اسم الخدمة:").grid(row=1, column=0, pady=5)
        service_name = ttk.Entry(service_frame)
        service_name.grid(row=1, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم الخدمة الحكومية:").grid(row=2, column=0, pady=5)
        government_fee = ttk.Entry(service_frame)
        government_fee.grid(row=2, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم المكتب:").grid(row=3, column=0, pady=5)
        office_fee = ttk.Entry(service_frame)
        office_fee.grid(row=3, column=1, pady=5)
        
        def save_service():
            entity = entity_var.get()
            service = service_name.get()
            gov_fee = government_fee.get()
            off_fee = office_fee.get()
            
            if not all([entity, service, gov_fee, off_fee]):
                messagebox.showerror("خطأ", "يرجى إكمال جميع الحقول")
                return
            
            try:
                gov_fee = float(gov_fee)
                off_fee = float(off_fee)
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للرسوم")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("SELECT id FROM government_entities WHERE name=?", (entity,))
            entity_id = c.fetchone()[0]
            
            c.execute("""
                INSERT INTO services (entity_id, service_name, government_fee, office_fee) 
                VALUES (?, ?, ?, ?)
            """, (entity_id, service, gov_fee, off_fee))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجاح", "تم تسجيل الخدمة بنجاح")
            service_name.delete(0, tk.END)
            government_fee.delete(0, tk.END)
            office_fee.delete(0, tk.END)
            update_services()
        
        ttk.Button(service_frame, text="حفظ الخدمة", command=save_service).grid(row=3, column=2, padx=10)
        
        # إنشاء جدول الخدمات
        tree = ttk.Treeview(main_frame, columns=("entity", "service", "gov_fee", "office_fee"), show="headings")
        tree.heading("entity", text="الجهة الحكومية")
        tree.heading("service", text="الخدمة")
        tree.heading("gov_fee", text="رسوم الخدمة الحكومية")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def update_entities():
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            entities = [row[0] for row in c.execute("SELECT name FROM government_entities")]
            conn.close()
            entity_combo['values'] = entities
        
        def update_services():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT government_entities.name, services.service_name, 
                       services.government_fee, services.office_fee 
                FROM services 
                JOIN government_entities ON services.entity_id = government_entities.id
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_entities()
        update_services()

    def show_tasks(self):
        self.clear_window()
        self.create_back_button()
        
        # إنشاء الإطار الرئيسي
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # إطار الوزارات في الأعلى
        ministries_frame = ttk.LabelFrame(main_frame, text="الوزارات والجهات الحكومية", padding="10")
        ministries_frame.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # إنشاء أزرار للوزارات
        ministries_buttons_frame = ttk.Frame(ministries_frame)
        ministries_buttons_frame.pack(fill=tk.X)
        
        # تقسيم الشاشة إلى قسمين
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.LabelFrame(content_frame, text="الخدمات المتاحة", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        right_frame = ttk.LabelFrame(content_frame, text="تفاصيل المهمة", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # ====== تهيئة الجانب الأيمن (تفاصيل المهمة) ======
        # اختيار العميل
        client_frame = ttk.Frame(right_frame)
        client_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(client_frame, text="العميل:").pack(side=tk.LEFT)
        client_combo = ttk.Combobox(client_frame)
        client_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # الخدمات المختارة
        ttk.Label(right_frame, text="الخدمات المختارة:").pack(anchor=tk.W)
        selected_tree = ttk.Treeview(right_frame, columns=("service", "gov_fee", "office_fee", "total"), show="headings", height=5)
        selected_tree.heading("service", text="الخدمة")
        selected_tree.heading("gov_fee", text="الرسوم الحكومية")
        selected_tree.heading("office_fee", text="رسوم المكتب")
        selected_tree.heading("total", text="المجموع")
        selected_tree.pack(fill=tk.X, pady=(0, 10))
        
        # إجمالي التكلفة
        total_label = ttk.Label(right_frame, text="إجمالي التكلفة: 0")
        total_label.pack(anchor=tk.W, pady=(0, 10))
        
        # وصف المهمة
        ttk.Label(right_frame, text="وصف المهمة:").pack(anchor=tk.W)
        task_description = tk.Text(right_frame, height=4)
        task_description.pack(fill=tk.X, pady=(0, 10))
        
        # زر حفظ المهمة
        save_btn = ttk.Button(right_frame, text="حفظ المهمة", style='Primary.TButton')
        save_btn.pack(fill=tk.X)

        # ====== تهيئة الجانب الأيسر (قائمة الخدمات) ======
        # جدول الخدمات المتاحة
        services_tree = ttk.Treeview(left_frame, columns=("service", "gov_fee", "office_fee"), show="headings")
        services_tree.heading("service", text="الخدمة")
        services_tree.heading("gov_fee", text="الرسوم الحكومية")
        services_tree.heading("office_fee", text="رسوم المكتب")
        services_tree.pack(fill=tk.BOTH, expand=True)

        def update_total():
            total = sum(float(selected_tree.item(item)['values'][3]) for item in selected_tree.get_children())
            total_label.config(text=f"إجمالي التكلفة: {total:.2f}")

        def update_clients():
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            clients = [row[0] for row in c.execute("SELECT name FROM clients")]
            conn.close()
            client_combo['values'] = clients

        def load_ministry_services(ministry_id):
            # مسح الخدمات السابقة
            for item in services_tree.get_children():
                services_tree.delete(item)
            
            # تحميل الخدمات الخاصة بالوزارة المحددة
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT service_name, government_fee, office_fee 
                FROM services 
                WHERE entity_id = ?
            """, (ministry_id,))
            
            for row in c.fetchall():
                services_tree.insert("", "end", values=row)
            conn.close()

        def create_ministry_buttons():
            # مسح الأزرار السابقة
            for widget in ministries_buttons_frame.winfo_children():
                widget.destroy()
            
            # إنشاء أزرار للوزارات
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("SELECT id, name FROM government_entities")
            
            for ministry_id, ministry_name in c.fetchall():
                btn = ttk.Button(
                    ministries_buttons_frame, 
                    text=ministry_name,
                    command=lambda id=ministry_id: load_ministry_services(id)
                )
                btn.pack(side=tk.LEFT, padx=2, pady=2)
            
            conn.close()

        def add_service_to_selected(event):
            selected_item = services_tree.selection()
            if not selected_item:
                return
            
            values = services_tree.item(selected_item[0])['values']
            gov_fee = float(values[1])
            office_fee = float(values[2])
            total = gov_fee + office_fee
            
            selected_tree.insert("", "end", values=(values[0], gov_fee, office_fee, total))
            update_total()

        def remove_selected_service():
            selected_item = selected_tree.selection()
            if selected_item:
                selected_tree.delete(selected_item)
                update_total()

        def save_task():
            if not client_combo.get():
                messagebox.showerror("خطأ", "يرجى اختيار العميل")
                return
            
            if not selected_tree.get_children():
                messagebox.showerror("خطأ", "يرجى إضافة خدمة واحدة على الأقل")
                return
            
            description = task_description.get("1.0", tk.END).strip()
            if not description:
                messagebox.showerror("خطأ", "يرجى إدخال وصف المهمة")
                return
            
            total_cost = sum(float(selected_tree.item(item)['values'][3]) for item in selected_tree.get_children())
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            
            try:
                # الحصول على معرف العميل
                c.execute("SELECT id FROM clients WHERE name = ?", (client_combo.get(),))
                client_id = c.fetchone()[0]
                
                # إنشاء المهمة
                c.execute("""
                    INSERT INTO tasks (client_id, description, cost, status, creation_date)
                    VALUES (?, ?, ?, 'غير منجزة', ?)
                """, (client_id, description, total_cost, datetime.now().strftime("%Y-%m-%d")))
                
                task_id = c.lastrowid
                
                # إضافة الخدمات المختارة
                for item in selected_tree.get_children():
                    service_name = selected_tree.item(item)['values'][0]
                    c.execute("SELECT id FROM services WHERE service_name = ?", (service_name,))
                    service_id = c.fetchone()[0]
                    
                    c.execute("""
                        INSERT INTO task_services (task_id, service_id)
                        VALUES (?, ?)
                    """, (task_id, service_id))
                
                conn.commit()
                messagebox.showinfo("نجاح", "تم حفظ المهمة بنجاح")
                
                # مسح البيانات
                client_combo.set('')
                task_description.delete("1.0", tk.END)
                for item in selected_tree.get_children():
                    selected_tree.delete(item)
                update_total()
                
            except Exception as e:
                messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ المهمة: {str(e)}")
                conn.rollback()
            
            finally:
                conn.close()
        
        # ربط الأحداث
        services_tree.bind('<Double-1>', add_service_to_selected)
        save_btn.configure(command=save_task)

        # إضافة زر لإزالة الخدمات المحددة
        remove_btn = ttk.Button(right_frame, text="إزالة الخدمة المحددة", command=remove_selected_service)
        remove_btn.pack(fill=tk.X, pady=(5, 0))

        # تحميل البيانات الأولية
        update_clients()
        create_ministry_buttons()

    def show_incomplete_tasks(self):
        self.clear_window()
        self.create_back_button()
        
        #إطار العمليات
        operations_frame = ttk.Frame(self.content_frame, padding="10")
        operations_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # جدول المهام غير المنجزة
        tree = ttk.Treeview(self.content_frame, columns=("client", "service", "description", "cost", "date"), show="headings")
        tree.heading("client", text="العميل")
        tree.heading("service", text="الخدمة")
        tree.heading("description", text="الوصف")
        tree.heading("cost", text="التكلفة")
        tree.heading("date", text="تاريخ الإنشاء")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def mark_as_completed():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("تنبيه", "يرجى اختيار مهمة")
                return
            
            task_values = tree.item(selected_item[0])['values']
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            
            try:
                # الحصول على معرف المهمة أولاً
                c.execute("""
                    SELECT tasks.id 
                    FROM tasks
                    JOIN clients ON tasks.client_id = clients.id
                    JOIN task_services ON tasks.id = task_services.task_id
                    JOIN services ON task_services.service_id = services.id
                    WHERE clients.name = ? 
                    AND services.service_name = ?
                    AND tasks.description = ?
                    AND tasks.status = 'غير منجزة'
                """, (task_values[0], task_values[1], task_values[2]))
                
                task_id = c.fetchone()
                
                if task_id:
                    # تحديث حالة المهمة وتاريخ الإنجاز
                    c.execute("""
                        UPDATE tasks 
                        SET status = 'منجزة', 
                            completion_date = ?
                        WHERE id = ?
                    """, (datetime.now().strftime("%Y-%m-%d"), task_id[0]))
                    
                    conn.commit()
                    messagebox.showinfo("نجاح", "تم تحديث حالة المهمة بنجاح")
                    update_table()
                else:
                    messagebox.showerror("خطأ", "لم يتم العثور على المهمة")
                    
            except Exception as e:
                conn.rollback()
                messagebox.showerror("خطأ", f"حدث خطأ أثناء تحديث المهمة: {str(e)}")
            finally:
                conn.close()
        
        ttk.Button(operations_frame, text="تحديد كمنجزة", command=mark_as_completed).pack(side=tk.LEFT, padx=5)
        
        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT clients.name, services.service_name, tasks.description, tasks.cost, tasks.creation_date
                FROM tasks
                JOIN clients ON tasks.client_id = clients.id
                JOIN task_services ON tasks.id = task_services.task_id
                JOIN services ON task_services.service_id = services.id
                WHERE tasks.status = 'غير منجزة'
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_table()

    def show_completed_tasks(self):
        self.clear_window()
        self.create_back_button()
        
        # جدول المهام المنجزة
        tree = ttk.Treeview(self.content_frame, 
                           columns=("client", "service", "description", "office_fee", 
                                   "government_fee", "total_cost", "completion_date"),
                           show="headings")
        tree.heading("client", text="العميل")
        tree.heading("service", text="الخدمة")
        tree.heading("description", text="الوصف")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.heading("government_fee", text="الرسوم الحكومية")
        tree.heading("total_cost", text="إجمالي التكلفة")
        tree.heading("completion_date", text="تاريخ الإنجاز")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT clients.name, services.service_name, tasks.description,
                       services.office_fee, services.government_fee,
                       (services.office_fee + services.government_fee) as total_cost,
                       tasks.completion_date
                FROM tasks
                JOIN clients ON tasks.client_id = clients.id
                JOIN task_services ON tasks.id = task_services.task_id
                JOIN services ON task_services.service_id = services.id
                WHERE tasks.status = 'منجزة'
                ORDER BY tasks.completion_date DESC
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_table()

    def show_profits(self):
        self.clear_window()
        self.create_back_button()
        
        #إطار التقرير
        report_frame = ttk.LabelFrame(self.content_frame, text="تقرير الأرباح", padding="20")
        report_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        #إطار الفلترة
        filter_frame = ttk.Frame(report_frame)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="من تاريخ:").pack(side=tk.LEFT, padx=5)
        from_date = ttk.Entry(filter_frame, width=15)
        from_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="إلى تاريخ:").pack(side=tk.LEFT, padx=5)
        to_date = ttk.Entry(filter_frame, width=15)
        to_date.pack(side=tk.LEFT, padx=5)
        
        #إطار الإحصائيات
        stats_frame = ttk.Frame(report_frame)
        stats_frame.pack(fill=tk.X, pady=20)
        
        total_tasks_label = ttk.Label(stats_frame, text="")
        total_tasks_label.pack()
        
        total_revenue_label = ttk.Label(stats_frame, text="")
        total_revenue_label.pack()
        
        # جدول المهام المنجزة مع الأعمدة الجديدة
        tree = ttk.Treeview(report_frame,
                           columns=("completion_date", "client", "service", "description", 
                                   "office_fee", "government_fee", "total_cost"),
                           show="headings")
        tree.heading("completion_date", text="تاريخ الإنجاز")
        tree.heading("client", text="العميل")
        tree.heading("service", text="الخدمة")
        tree.heading("description", text="الوصف")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.heading("government_fee", text="الرسوم الحكومية")
        tree.heading("total_cost", text="إجمالي التكلفة")
        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def update_report():
            start_date = from_date.get() or "2000-01-01"
            end_date = to_date.get() or datetime.now().strftime("%Y-%m-%d")
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            
            # تحديث الجدول
            for item in tree.get_children():
                tree.delete(item)
            
            c.execute("""
                SELECT tasks.completion_date, clients.name, services.service_name,
                       tasks.description, services.office_fee, services.government_fee,
                       (services.office_fee + services.government_fee) as total_cost
                FROM tasks
                JOIN clients ON tasks.client_id = clients.id
                JOIN task_services ON tasks.id = task_services.task_id
                JOIN services ON task_services.service_id = services.id
                WHERE tasks.status = 'منجزة'
                AND tasks.completion_date BETWEEN ? AND ?
                ORDER BY tasks.completion_date DESC
            """, (start_date, end_date))
            
            total_revenue = 0
            total_tasks = 0
            
            for row in c.fetchall():
                tree.insert("", "end", values=row)
                total_revenue += row[6]  # total_cost column
                total_tasks += 1
            
            # تحديث الإحصائيات
            total_tasks_label.config(text=f"إجمالي عدد المهام: {total_tasks}")
            total_revenue_label.config(text=f"إجمالي الإيرادات: {total_revenue:.2f} ريال")
            
            conn.close()
        
        ttk.Button(filter_frame, text="تحديث التقرير", command=update_report).pack(side=tk.LEFT, padx=20)
        
        # عرض التقرير الأولي
        update_report()

    def create_database(self):
        conn = sqlite3.connect('management.db')
        c = conn.cursor()
        
        # إنشاء جدول العملاء
        c.execute('''CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            phone TEXT,
            email TEXT
        )''')
        
        # إنشاء جدول الجهات الحكومية
        c.execute('''CREATE TABLE IF NOT EXISTS government_entities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )''')
        
        # إنشاء جدول الخدمات
        c.execute('''CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_id INTEGER,
            service_name TEXT NOT NULL,
            government_fee REAL,
            office_fee REAL,
            FOREIGN KEY (entity_id) REFERENCES government_entities (id),
            UNIQUE(entity_id, service_name)
        )''')
        
        # إنشاء جدول المهام
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            description TEXT,
            cost REAL,           -- تم تغيير الاسم من total_cost إلى cost
            status TEXT,
            creation_date TEXT,
            completion_date TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )''')
        
        # إنشاء جدول الخدمات المرتبطة بالمهام
        c.execute('''CREATE TABLE IF NOT EXISTS task_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            service_id INTEGER,
            FOREIGN KEY (task_id) REFERENCES tasks (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )''')
        
        conn.commit()
        conn.close()

    def register_clients(self):
        window = tk.Toplevel(self.root)
        window.title("تسجيل العملاء")
        window.geometry("600x400")
        
        # النموذج
        form_frame = ttk.Frame(window, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # حقول الإدخال
        ttk.Label(form_frame, text="اسم العميل:").grid(row=0, column=0, pady=5)
        name_entry = ttk.Entry(form_frame)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(form_frame, text="رقم الهاتف:").grid(row=1, column=0, pady=5)
        phone_entry = ttk.Entry(form_frame)
        phone_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(form_frame, text="البريد الإلكتروني:").grid(row=2, column=0, pady=5)
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=2, column=1, pady=5)
        
        def save_client():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
                return
                
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)",
                     (name, phone, email))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجاح", "تم تسجيل العميل بنجاح")
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
        
        # زر الحفظ
        ttk.Button(form_frame, text="حفظ", command=save_client).grid(row=3, column=0, columnspan=2, pady=20)
        
        # جدول العملاء
        tree = ttk.Treeview(form_frame, columns=("name", "phone", "email"), show="headings")
        tree.heading("name", text="اسم العميل")
        tree.heading("phone", text="رقم الهاتف")
        tree.heading("email", text="البريد الإلكتروني")
        tree.grid(row=4, column=0, columnspan=2, pady=10)
        
        # تحديث الجدول
        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            for row in c.execute("SELECT name, phone, email FROM clients"):
                tree.insert("", "end", values=row)
            conn.close()
        
        update_table()

    def register_government(self):
        window = tk.Toplevel(self.root)
        window.title("تسجيل الوزارات والجهات الحكومية")
        window.geometry("800x600")
        
        # إنشاء الإطار الرئيسي
        main_frame = ttk.Frame(window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء الإطارات الفرعية
        entity_frame = ttk.LabelFrame(main_frame, text="تسجيل جهة حكومية", padding="20")
        entity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        service_frame = ttk.LabelFrame(main_frame, text="تسجيل خدمة", padding="20")
        service_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل جهة حكومية"
        ttk.Label(entity_frame, text="اسم الجهة:").grid(row=0, column=0, pady=5)
        entity_name = ttk.Entry(entity_frame)
        entity_name.grid(row=0, column=1, pady=5)
        
        def save_entity():
            name = entity_name.get()
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم الجهة")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO government_entities (name) VALUES (?)", (name,))
                conn.commit()
                messagebox.showinfo("نجاح", "تم تسجيل الجهة بنجاح")
                entity_name.delete(0, tk.END)
                update_entities()
                update_services()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "هذه الجهة موجودة مسبق<|im_start|>")
            conn.close()
        
        ttk.Button(entity_frame, text="حفظ الجهة", command=save_entity).grid(row=0, column=2, padx=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل خدمة"
        ttk.Label(service_frame, text="اختر الجهة:").grid(row=0, column=0, pady=5)
        entity_var = tk.StringVar()
        entity_combo = ttk.Combobox(service_frame, textvariable=entity_var)
        entity_combo.grid(row=0, column=1, pady=5)
        
        ttk.Label(service_frame, text="اسم الخدمة:").grid(row=1, column=0, pady=5)
        service_name = ttk.Entry(service_frame)
        service_name.grid(row=1, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم الخدمة الحكومية:").grid(row=2, column=0, pady=5)
        government_fee = ttk.Entry(service_frame)
        government_fee.grid(row=2, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم المكتب:").grid(row=3, column=0, pady=5)
        office_fee = ttk.Entry(service_frame)
        office_fee.grid(row=3, column=1, pady=5)
        
        def save_service():
            entity = entity_var.get()
            service = service_name.get()
            gov_fee = government_fee.get()
            off_fee = office_fee.get()
            
            if not all([entity, service, gov_fee, off_fee]):
                messagebox.showerror("خطأ", "يرجى إكمال جميع الحقول")
                return
            
            try:
                gov_fee = float(gov_fee)
                off_fee = float(off_fee)
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للرسوم")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("SELECT id FROM government_entities WHERE name=?", (entity,))
            entity_id = c.fetchone()[0]
            
            c.execute("""
                INSERT INTO services (entity_id, service_name, government_fee, office_fee) 
                VALUES (?, ?, ?, ?)
            """, (entity_id, service, gov_fee, off_fee))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجاح", "تم تسجيل الخدمة بنجاح")
            service_name.delete(0, tk.END)
            government_fee.delete(0, tk.END)
            office_fee.delete(0, tk.END)
            update_services()
        
        ttk.Button(service_frame, text="حفظ الخدمة", command=save_service).grid(row=3, column=2, padx=10)
        
        # إنشاء جدول الخدمات
        tree = ttk.Treeview(main_frame, columns=("entity", "service", "gov_fee", "office_fee"), show="headings")
        tree.heading("entity", text="الجهة الحكومية")
        tree.heading("service", text="الخدمة")
        tree.heading("gov_fee", text="رسوم الخدمة الحكومية")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def update_entities():
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            entities = [row[0] for row in c.execute("SELECT name FROM government_entities")]
            conn.close()
            entity_combo['values'] = entities
        
        def update_services():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT government_entities.name, services.service_name, 
                       services.government_fee, services.office_fee 
                FROM services 
                JOIN government_entities ON services.entity_id = government_entities.id
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_entities()
        update_services()

    def register_tasks(self):
        window = tk.Toplevel(self.root)
        window.title("تسجيل المهام")
        window.geometry("800x600")
        
        # إنشاء الإطار الرئيسي
        main_frame = ttk.Frame(window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء الإطارات الفرعية
        entity_frame = ttk.LabelFrame(main_frame, text="تسجيل جهة حكومية", padding="20")
        entity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        service_frame = ttk.LabelFrame(main_frame, text="تسجيل خدمة", padding="20")
        service_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل جهة حكومية"
        ttk.Label(entity_frame, text="اسم الجهة:").grid(row=0, column=0, pady=5)
        entity_name = ttk.Entry(entity_frame)
        entity_name.grid(row=0, column=1, pady=5)
        
        def save_entity():
            name = entity_name.get()
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم الجهة")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO government_entities (name) VALUES (?)", (name,))
                conn.commit()
                messagebox.showinfo("نجاح", "تم تسجيل الجهة بنجاح")
                entity_name.delete(0, tk.END)
                update_entities()
                update_services()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "هذه الجهة موجودة مسبق<|im_start|>")
            conn.close()
        
        ttk.Button(entity_frame, text="حفظ الجهة", command=save_entity).grid(row=0, column=2, padx=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل خدمة"
        ttk.Label(service_frame, text="اختر الجهة:").grid(row=0, column=0, pady=5)
        entity_var = tk.StringVar()
        entity_combo = ttk.Combobox(service_frame, textvariable=entity_var)
        entity_combo.grid(row=0, column=1, pady=5)
        
        ttk.Label(service_frame, text="اسم الخدمة:").grid(row=1, column=0, pady=5)
        service_name = ttk.Entry(service_frame)
        service_name.grid(row=1, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم الخدمة الحكومية:").grid(row=2, column=0, pady=5)
        government_fee = ttk.Entry(service_frame)
        government_fee.grid(row=2, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم المكتب:").grid(row=3, column=0, pady=5)
        office_fee = ttk.Entry(service_frame)
        office_fee.grid(row=3, column=1, pady=5)
        
        def save_service():
            entity = entity_var.get()
            service = service_name.get()
            gov_fee = government_fee.get()
            off_fee = office_fee.get()
            
            if not all([entity, service, gov_fee, off_fee]):
                messagebox.showerror("خطأ", "يرجى إكمال جميع الحقول")
                return
            
            try:
                gov_fee = float(gov_fee)
                off_fee = float(off_fee)
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للرسوم")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("SELECT id FROM government_entities WHERE name=?", (entity,))
            entity_id = c.fetchone()[0]
            
            c.execute("""
                INSERT INTO services (entity_id, service_name, government_fee, office_fee) 
                VALUES (?, ?, ?, ?)
            """, (entity_id, service, gov_fee, off_fee))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجاح", "تم تسجيل الخدمة بنجاح")
            service_name.delete(0, tk.END)
            government_fee.delete(0, tk.END)
            office_fee.delete(0, tk.END)
            update_services()
        
        ttk.Button(service_frame, text="حفظ الخدمة", command=save_service).grid(row=3, column=2, padx=10)
        
        # إنشاء جدول الخدمات
        tree = ttk.Treeview(main_frame, columns=("entity", "service", "gov_fee", "office_fee"), show="headings")
        tree.heading("entity", text="الجهة الحكومية")
        tree.heading("service", text="الخدمة")
        tree.heading("gov_fee", text="رسوم الخدمة الحكومية")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def update_entities():
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            entities = [row[0] for row in c.execute("SELECT name FROM government_entities")]
            conn.close()
            entity_combo['values'] = entities
        
        def update_services():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT government_entities.name, services.service_name, 
                       services.government_fee, services.office_fee 
                FROM services 
                JOIN government_entities ON services.entity_id = government_entities.id
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_entities()
        update_services()

    def incomplete_tasks(self):
        window = tk.Toplevel(self.root)
        window.title("المهام الغير منجزة")
        window.geometry("800x600")
        
        # جدول المهام غير المنجزة
        tree = ttk.Treeview(window, columns=("client", "service", "description", "cost", "date"), show="headings")
        tree.heading("client", text="العميل")
        tree.heading("service", text="الخدمة")
        tree.heading("description", text="الوصف")
        tree.heading("cost", text="التكلفة")
        tree.heading("date", text="تاريخ الإنشاء")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        def mark_as_completed():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("تنبيه", "يرجى اختيار مهمة")
                return
            
            task_values = tree.item(selected_item[0])['values']
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            
            try:
                # الحصول على معرف المهمة أولاً
                c.execute("""
                    SELECT tasks.id 
                    FROM tasks
                    JOIN clients ON tasks.client_id = clients.id
                    JOIN task_services ON tasks.id = task_services.task_id
                    JOIN services ON task_services.service_id = services.id
                    WHERE clients.name = ? 
                    AND services.service_name = ?
                    AND tasks.description = ?
                    AND tasks.status = 'غير منجزة'
                """, (task_values[0], task_values[1], task_values[2]))
                
                task_id = c.fetchone()
                
                if task_id:
                    # تحديث حالة المهمة وتاريخ الإنجاز
                    c.execute("""
                        UPDATE tasks 
                        SET status = 'منجزة', 
                            completion_date = ?
                        WHERE id = ?
                    """, (datetime.now().strftime("%Y-%m-%d"), task_id[0]))
                    
                    conn.commit()
                    messagebox.showinfo("نجاح", "تم تحديث حالة المهمة بنجاح")
                    update_table()
                else:
                    messagebox.showerror("خطأ", "لم يتم العثور على المهمة")
                    
            except Exception as e:
                conn.rollback()
                messagebox.showerror("خطأ", f"حدث خطأ أثناء تحديث المهمة: {str(e)}")
            finally:
                conn.close()
        
        ttk.Button(window, text="تحديد كمنجزة", command=mark_as_completed).pack(pady=10)
        
        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT clients.name, services.service_name, tasks.description, tasks.cost, tasks.creation_date
                FROM tasks
                JOIN clients ON tasks.client_id = clients.id
                JOIN task_services ON tasks.id = task_services.task_id
                JOIN services ON task_services.service_id = services.id
                WHERE tasks.status = 'غير منجزة'
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_table()

    def completed_tasks(self):
        window = tk.Toplevel(self.root)
        window.title("المهام المنجزة")
        window.geometry("800x600")
        
        # جدول المهام المنجزة
        tree = ttk.Treeview(window, 
                           columns=("client", "service", "description", "office_fee", 
                                   "government_fee", "total_cost", "completion_date"),
                           show="headings")
        tree.heading("client", text="العميل")
        tree.heading("service", text="الخدمة")
        tree.heading("description", text="الوصف")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.heading("government_fee", text="الرسوم الحكومية")
        tree.heading("total_cost", text="إجمالي التكلفة")
        tree.heading("completion_date", text="تاريخ الإنجاز")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT clients.name, services.service_name, tasks.description,
                       services.office_fee, services.government_fee,
                       (services.office_fee + services.government_fee) as total_cost,
                       tasks.completion_date
                FROM tasks
                JOIN clients ON tasks.client_id = clients.id
                JOIN task_services ON tasks.id = task_services.task_id
                JOIN services ON task_services.service_id = services.id
                WHERE tasks.status = 'منجزة'
                ORDER BY tasks.completion_date DESC
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_table()

    def profits(self):
        window = tk.Toplevel(self.root)
        window.title("الأرباح")
        window.geometry("800x600")
        
        # إنشاء الإطار الرئيسي
        main_frame = ttk.Frame(window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # إنشاء الإطارات الفرعية
        entity_frame = ttk.LabelFrame(main_frame, text="تسجيل جهة حكومية", padding="20")
        entity_frame.pack(fill=tk.X, padx=20, pady=10)
        
        service_frame = ttk.LabelFrame(main_frame, text="تسجيل خدمة", padding="20")
        service_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل جهة حكومية"
        ttk.Label(entity_frame, text="اسم الجهة:").grid(row=0, column=0, pady=5)
        entity_name = ttk.Entry(entity_frame)
        entity_name.grid(row=0, column=1, pady=5)
        
        def save_entity():
            name = entity_name.get()
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم الجهة")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO government_entities (name) VALUES (?)", (name,))
                conn.commit()
                messagebox.showinfo("نجاح", "تم تسجيل الجهة بنجاح")
                entity_name.delete(0, tk.END)
                update_entities()
                update_services()
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "هذه الجهة موجودة مسبق<|im_start|>")
            conn.close()
        
        ttk.Button(entity_frame, text="حفظ الجهة", command=save_entity).grid(row=0, column=2, padx=10)
        
        # إنشاء حقول الإدخال في الإطار "تسجيل خدمة"
        ttk.Label(service_frame, text="اختر الجهة:").grid(row=0, column=0, pady=5)
        entity_var = tk.StringVar()
        entity_combo = ttk.Combobox(service_frame, textvariable=entity_var)
        entity_combo.grid(row=0, column=1, pady=5)
        
        ttk.Label(service_frame, text="اسم الخدمة:").grid(row=1, column=0, pady=5)
        service_name = ttk.Entry(service_frame)
        service_name.grid(row=1, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم الخدمة الحكومية:").grid(row=2, column=0, pady=5)
        government_fee = ttk.Entry(service_frame)
        government_fee.grid(row=2, column=1, pady=5)
        
        ttk.Label(service_frame, text="رسوم المكتب:").grid(row=3, column=0, pady=5)
        office_fee = ttk.Entry(service_frame)
        office_fee.grid(row=3, column=1, pady=5)
        
        def save_service():
            entity = entity_var.get()
            service = service_name.get()
            gov_fee = government_fee.get()
            off_fee = office_fee.get()
            
            if not all([entity, service, gov_fee, off_fee]):
                messagebox.showerror("خطأ", "يرجى إكمال جميع الحقول")
                return
            
            try:
                gov_fee = float(gov_fee)
                off_fee = float(off_fee)
            except ValueError:
                messagebox.showerror("خطأ", "يرجى إدخال أرقام صحيحة للرسوم")
                return
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("SELECT id FROM government_entities WHERE name=?", (entity,))
            entity_id = c.fetchone()[0]
            
            c.execute("""
                INSERT INTO services (entity_id, service_name, government_fee, office_fee) 
                VALUES (?, ?, ?, ?)
            """, (entity_id, service, gov_fee, off_fee))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("نجاح", "تم تسجيل الخدمة بنجاح")
            service_name.delete(0, tk.END)
            government_fee.delete(0, tk.END)
            office_fee.delete(0, tk.END)
            update_services()
        
        ttk.Button(service_frame, text="حفظ الخدمة", command=save_service).grid(row=3, column=2, padx=10)
        
        # إنشاء جدول الخدمات
        tree = ttk.Treeview(main_frame, columns=("entity", "service", "gov_fee", "office_fee"), show="headings")
        tree.heading("entity", text="الجهة الحكومية")
        tree.heading("service", text="الخدمة")
        tree.heading("gov_fee", text="رسوم الخدمة الحكومية")
        tree.heading("office_fee", text="رسوم المكتب")
        tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def update_entities():
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            entities = [row[0] for row in c.execute("SELECT name FROM government_entities")]
            conn.close()
            entity_combo['values'] = entities
        
        def update_services():
            for item in tree.get_children():
                tree.delete(item)
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT government_entities.name, services.service_name, 
                       services.government_fee, services.office_fee 
                FROM services 
                JOIN government_entities ON services.entity_id = government_entities.id
            """)
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            conn.close()
        
        update_entities()
        update_services()

    def show_new_requests(self):
        self.clear_window()
        self.create_back_button()
        
        #إطار رئيسي
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # عنوان الصفحة
        title_label = ttk.Label(main_frame, text="الطلبات الجديدة", font=('Arial', '16', 'bold'))
        title_label.pack(pady=(0, 20))
        
        #إطار العمليات
        operations_frame = ttk.Frame(main_frame)
        operations_frame.pack(fill=tk.X, pady=(0, 10))
        
        # جدول الطلبات
        tree = ttk.Treeview(main_frame, columns=("client", "phone", "service", "date", "receipt"), show="headings")
        tree.heading("client", text="اسم العميل")
        tree.heading("phone", text="رقم الهاتف")
        tree.heading("service", text="الخدمة المطلوبة")
        tree.heading("date", text="تاريخ الطلب")
        tree.heading("receipt", text="الإيصال")
        
        # ضبط عرض الأعمدة
        tree.column("client", width=150)
        tree.column("phone", width=120)
        tree.column("service", width=200)
        tree.column("date", width=100)
        tree.column("receipt", width=100)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # إضافة شريط التمرير
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        def update_table():
            for item in tree.get_children():
                tree.delete(item)
            
            conn = sqlite3.connect('management.db')
            c = conn.cursor()
            c.execute("""
                SELECT clients.name, clients.phone, services.service_name, 
                       tasks.creation_date, tasks.receipt_path
                FROM tasks
                JOIN clients ON tasks.client_id = clients.id
                JOIN task_services ON tasks.id = task_services.task_id
                JOIN services ON task_services.service_id = services.id
                WHERE tasks.status = 'pending'
                ORDER BY tasks.creation_date DESC
            """)
            
            for row in c.fetchall():
                tree.insert("", "end", values=row)
            
            conn.close()

        def mark_as_task():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("تنبيه", "الرجاء اختيار طلب للتحويل")
                return
            
            if messagebox.askyesno("تأكيد", "هل تريد تحويل هذا الطلب إلى قائمة الطلبات الغير منجزة؟"):
                item_data = tree.item(selected_item)['values']
                
                conn = sqlite3.connect('management.db')
                c = conn.cursor()
                try:
                    # تحديث حالة الطلب إلى "غير منجزة"
                    c.execute("""
                        UPDATE tasks 
                        SET status = 'غير منجزة'
                        WHERE client_id = (SELECT id FROM clients WHERE name = ?)
                        AND id IN (
                            SELECT task_id FROM task_services 
                            JOIN services ON task_services.service_id = services.id 
                            WHERE services.service_name = ?
                        )
                        AND status = 'pending'
                    """, (item_data[0], item_data[2]))
                    
                    conn.commit()
                    messagebox.showinfo("نجاح", "تم تحويل الطلب إلى قائمة الطلبات الغير منجزة بنجاح")
                    update_table()
                    
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("خطأ", f"حدث خطأ أثناء تحويل الطلب: {str(e)}")
                finally:
                    conn.close()

        def view_request_details():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("تنبيه", "الرجاء اختيار طلب للعرض")
                return
            
            item_data = tree.item(selected_item)['values']
            
            details_window = tk.Toplevel(self.root)
            details_window.title("تفاصيل الطلب")
            details_window.geometry("600x400")
            
            #إطار التفاصيل
            details_frame = ttk.Frame(details_window, padding="20")
            details_frame.pack(fill=tk.BOTH, expand=True)
            
            # عرض المعلومات
            ttk.Label(details_frame, text=f"اسم العميل: {item_data[0]}", font=('Arial', '12')).pack(anchor=tk.W, pady=5)
            ttk.Label(details_frame, text=f"رقم الهاتف: {item_data[1]}", font=('Arial', '12')).pack(anchor=tk.W, pady=5)
            ttk.Label(details_frame, text=f"الخدمة المطلوبة: {item_data[2]}", font=('Arial', '12')).pack(anchor=tk.W, pady=5)
            ttk.Label(details_frame, text=f"تاريخ الطلب: {item_data[3]}", font=('Arial', '12')).pack(anchor=tk.W, pady=5)
            
            # عرض الإيصال
            if item_data[4]:
                receipt_path = os.path.join('static/uploads', item_data[4])
                if os.path.exists(receipt_path):
                    try:
                        from PIL import Image, ImageTk
                        image = Image.open(receipt_path)
                        image.thumbnail((300, 300))
                        photo = ImageTk.PhotoImage(image)
                        label = ttk.Label(details_frame, image=photo)
                        label.image = photo
                        label.pack(pady=10)
                    except Exception as e:
                        ttk.Label(details_frame, text="لا يمكن عرض الإيصال").pack(pady=10)

        # إضافة الأزرار
        ttk.Button(operations_frame, text="عرض التفاصيل", command=view_request_details).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="تحويل إلى الطلبات الغير منجزة", command=mark_as_task).pack(side=tk.LEFT, padx=5)
        
        update_table()

def main():
    root = tk.Tk()
    app = ManagementSystem(root)
    # تعيين اتجاه النص من اليمين إلى اليسار
    root.tk_setPalette(background='#f0f0f0')
    root.mainloop()

if __name__ == "__main__":
    main()