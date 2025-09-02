import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from auth import AuthSystem
from inventory import InventorySystem
from utils import hash_password, send_email_notification, export_to_csv
import re
import os
from datetime import datetime

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Inventory - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Center window
        self.root.eval('tk::PlaceWindow . center')
        
        self.auth = AuthSystem()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame with styling
        main_frame = ttk.Frame(self.root, padding=20, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Sistem Inventory", 
                               font=("Arial", 16, "bold"), foreground="#2c3e50")
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = ttk.Frame(main_frame, style="Form.TFrame")
        form_frame.pack(pady=20, fill=tk.X)
        
        # Username
        ttk.Label(form_frame, text="Username:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.username_entry = ttk.Entry(form_frame, width=25, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=8, padx=5)
        self.username_entry.focus()
        
        # Password
        ttk.Label(form_frame, text="Password:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.password_entry = ttk.Entry(form_frame, width=25, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, pady=8, padx=5)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda event: self.login())
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Login button
        login_btn = ttk.Button(button_frame, text="Login", command=self.login, width=12)
        login_btn.pack(side=tk.LEFT, padx=5)
        
        # Register button
        register_btn = ttk.Button(button_frame, text="Register", command=self.open_register, width=12)
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset password button
        reset_btn = ttk.Button(button_frame, text="Reset Password", command=self.open_reset_password, width=15)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Form.TFrame", background="#f0f0f0")
        style.configure("TButton", padding=6, font=("Arial", 9))
        style.map("TButton", background=[('active', '#e1e1e1')])
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi")
            return
            
        user = self.auth.login(username, password)
        if user:
            messagebox.showinfo("Success", f"Login berhasil! Selamat datang {username}")
            self.root.destroy()
            app_root = tk.Tk()
            InventoryApp(app_root, user)
            app_root.mainloop()
        else:
            messagebox.showerror("Error", "Username atau password salah")
            
    def open_register(self):
        RegisterWindow(self.root)
        
    def open_reset_password(self):
        ResetPasswordWindow(self.root)


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrasi Pengguna")
        self.geometry("450x450")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        
        # Center window
        self.transient(parent)
        self.grab_set()
        self.eval(f'tk::PlaceWindow {str(self)} center')
        
        self.auth = AuthSystem()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=20, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Registrasi Pengguna Baru", 
                               font=("Arial", 14, "bold"), foreground="#2c3e50")
        title_label.pack(pady=10)
        
        form_frame = ttk.Frame(main_frame, style="Form.TFrame")
        form_frame.pack(pady=20, fill=tk.X)
        
        # Form fields
        ttk.Label(form_frame, text="Username:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.username_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.username_entry.grid(row=0, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Password:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*", font=("Arial", 10))
        self.password_entry.grid(row=1, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Konfirmasi Password:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=5)
        self.confirm_password_entry = ttk.Entry(form_frame, width=30, show="*", font=("Arial", 10))
        self.confirm_password_entry.grid(row=2, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Email:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=5)
        self.email_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.email_entry.grid(row=3, column=1, pady=8, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Register", command=self.register, width=12).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Batal", command=self.destroy, width=12).pack(side=tk.LEFT, padx=10)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Form.TFrame", background="#f0f0f0")
        
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get().strip()
        
        if not username or not password or not confirm_password or not email:
            messagebox.showerror("Error", "Semua field harus diisi")
            return
            
        if len(username) < 3:
            messagebox.showerror("Error", "Username harus minimal 3 karakter")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password harus minimal 6 karakter")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Password dan konfirmasi password tidak sama")
            return
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Format email tidak valid")
            return
            
        if self.auth.register(username, password, email):
            messagebox.showinfo("Success", "Registrasi berhasil! Silakan login.")
            self.destroy()
        else:
            messagebox.showerror("Error", "Username sudah digunakan")


class ResetPasswordWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reset Password")
        self.geometry("400x200")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        
        # Center window
        self.transient(parent)
        self.grab_set()
        self.eval(f'tk::PlaceWindow {str(self)} center')
        
        self.auth = AuthSystem()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=20, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Reset Password", 
                               font=("Arial", 14, "bold"), foreground="#2c3e50")
        title_label.pack(pady=10)
        
        form_frame = ttk.Frame(main_frame, style="Form.TFrame")
        form_frame.pack(pady=20, fill=tk.X)
        
        ttk.Label(form_frame, text="Email:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=10, padx=5)
        self.email_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.email_entry.grid(row=0, column=1, pady=10, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Reset Password", command=self.reset_password, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Batal", command=self.destroy, width=15).pack(side=tk.LEFT, padx=10)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Form.TFrame", background="#f0f0f0")
        
    def reset_password(self):
        email = self.email_entry.get().strip()
        
        if not email:
            messagebox.showerror("Error", "Email harus diisi")
            return
            
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Format email tidak valid")
            return
            
        if self.auth.reset_password(email):
            messagebox.showinfo("Success", "Password telah direset. Silakan cek email Anda.")
            self.destroy()
        else:
            messagebox.showerror("Error", "Email tidak ditemukan")


class InventoryApp:
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"Sistem Inventory - {user['username']}")
        self.root.geometry("1200x700")
        self.root.state('zoomed')  # Maximize window
        
        self.user = user
        self.inventory = InventorySystem()
        
        # Configure styles
        self.configure_styles()
        
        self.setup_ui()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[10, 5])
        style.configure("Title.TLabel", font=("Arial", 12, "bold"), foreground="#2c3e50")
        style.configure("Card.TFrame", background="white", relief=tk.RAISED, borderwidth=1)
        
    def setup_ui(self):
        # Main notebook (Tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.items_frame = ttk.Frame(self.notebook, padding=10)
        self.stock_in_frame = ttk.Frame(self.notebook, padding=10)
        self.stock_out_frame = ttk.Frame(self.notebook, padding=10)
        self.report_frame = ttk.Frame(self.notebook, padding=10)
        self.dashboard_frame = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.items_frame, text="📦 Daftar Barang")
        self.notebook.add(self.stock_in_frame, text="⬇️ Stok Masuk")
        self.notebook.add(self.stock_out_frame, text="⬆️ Stok Keluar")
        self.notebook.add(self.report_frame, text="📊 Laporan")
        self.notebook.add(self.dashboard_frame, text="🏠 Dashboard")
        
        self.setup_items_tab()
        self.setup_stock_in_tab()
        self.setup_stock_out_tab()
        self.setup_report_tab()
        self.setup_dashboard_tab()
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
    def on_tab_changed(self, event):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  # Items tab
            self.refresh_items()
        elif current_tab == 1:  # Stock in tab
            self.refresh_stock_in()
        elif current_tab == 2:  # Stock out tab
            self.refresh_stock_out()
        elif current_tab == 3:  # Report tab
            pass
        elif current_tab == 4:  # Dashboard tab
            self.update_dashboard()
        
    def setup_items_tab(self):
        # Toolbar frame
        toolbar = ttk.Frame(self.items_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(toolbar, text="➕ Tambah Barang", command=self.open_add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="✏️ Edit Barang", command=self.open_edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🗑️ Hapus Barang", command=self.delete_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_items).pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.items_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Cari:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_items)
        
        # Treeview frame
        tree_frame = ttk.Frame(self.items_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview untuk menampilkan barang
        columns = ("id", "name", "category", "stock", "unit", "min_stock", "created_date", "expiry_date")
        self.items_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define headings
        self.items_tree.heading("id", text="ID", command=lambda: self.sort_treeview(self.items_tree, "id", False))
        self.items_tree.heading("name", text="Nama Barang", command=lambda: self.sort_treeview(self.items_tree, "name", False))
        self.items_tree.heading("category", text="Kategori", command=lambda: self.sort_treeview(self.items_tree, "category", False))
        self.items_tree.heading("stock", text="Stok", command=lambda: self.sort_treeview(self.items_tree, "stock", False))
        self.items_tree.heading("unit", text="Satuan", command=lambda: self.sort_treeview(self.items_tree, "unit", False))
        self.items_tree.heading("min_stock", text="Min Stok", command=lambda: self.sort_treeview(self.items_tree, "min_stock", False))
        self.items_tree.heading("created_date", text="Tanggal Dibuat", command=lambda: self.sort_treeview(self.items_tree, "created_date", False))
        self.items_tree.heading("expiry_date", text="Tanggal Kadaluarsa", command=lambda: self.sort_treeview(self.items_tree, "expiry_date", False))
        
        # Define columns
        self.items_tree.column("id", width=50, anchor=tk.CENTER)
        self.items_tree.column("name", width=180)
        self.items_tree.column("category", width=120)
        self.items_tree.column("stock", width=80, anchor=tk.CENTER)
        self.items_tree.column("unit", width=80, anchor=tk.CENTER)
        self.items_tree.column("min_stock", width=80, anchor=tk.CENTER)
        self.items_tree.column("created_date", width=120, anchor=tk.CENTER)
        self.items_tree.column("expiry_date", width=120, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.items_tree.yview)
        self.items_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.items_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double click to edit
        self.items_tree.bind("<Double-1>", self.on_item_double_click)
        
        # Load data
        self.refresh_items()
        
    def setup_stock_in_tab(self):
        # Form frame
        form_frame = ttk.LabelFrame(self.stock_in_frame, text="Form Stok Masuk", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Item selection
        ttk.Label(form_frame, text="Pilih Barang:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_in_item = ttk.Combobox(form_frame, state="readonly", width=30, font=("Arial", 10))
        self.stock_in_item.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Quantity
        ttk.Label(form_frame, text="Jumlah:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_in_qty = ttk.Spinbox(form_frame, from_=1, to=10000, width=15, font=("Arial", 10))
        self.stock_in_qty.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.stock_in_qty.set(1)
        
        # Date
        ttk.Label(form_frame, text="Tanggal:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_in_date = DateEntry(form_frame, width=15, background='darkblue', 
                                      foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                      font=("Arial", 10))
        self.stock_in_date.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Supplier
        ttk.Label(form_frame, text="Supplier:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_in_supplier = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.stock_in_supplier.grid(row=3, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Notes
        ttk.Label(form_frame, text="Catatan:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_in_notes = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.stock_in_notes.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Button
        ttk.Button(form_frame, text="💾 Simpan Stok Masuk", command=self.save_stock_in).grid(row=5, column=1, sticky=tk.E, pady=10, padx=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Treeview frame
        tree_frame = ttk.LabelFrame(self.stock_in_frame, text="Riwayat Stok Masuk", padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview untuk riwayat stok masuk
        columns = ("id", "item_name", "quantity", "date", "supplier", "notes")
        self.stock_in_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.stock_in_tree.heading("id", text="ID")
        self.stock_in_tree.heading("item_name", text="Nama Barang")
        self.stock_in_tree.heading("quantity", text="Jumlah")
        self.stock_in_tree.heading("date", text="Tanggal")
        self.stock_in_tree.heading("supplier", text="Supplier")
        self.stock_in_tree.heading("notes", text="Catatan")
        
        self.stock_in_tree.column("id", width=50, anchor=tk.CENTER)
        self.stock_in_tree.column("item_name", width=180)
        self.stock_in_tree.column("quantity", width=80, anchor=tk.CENTER)
        self.stock_in_tree.column("date", width=100, anchor=tk.CENTER)
        self.stock_in_tree.column("supplier", width=150)
        self.stock_in_tree.column("notes", width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.stock_in_tree.yview)
        self.stock_in_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stock_in_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load data
        self.refresh_stock_in()
        
    def setup_stock_out_tab(self):
        # Form frame
        form_frame = ttk.LabelFrame(self.stock_out_frame, text="Form Stok Keluar", padding=10)
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Item selection
        ttk.Label(form_frame, text="Pilih Barang:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_out_item = ttk.Combobox(form_frame, state="readonly", width=30, font=("Arial", 10))
        self.stock_out_item.grid(row=0, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Quantity
        ttk.Label(form_frame, text="Jumlah:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_out_qty = ttk.Spinbox(form_frame, from_=1, to=10000, width=15, font=("Arial", 10))
        self.stock_out_qty.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.stock_out_qty.set(1)
        
        # Method
        ttk.Label(form_frame, text="Metode:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_out_method = ttk.Combobox(form_frame, values=["FIFO", "LIFO"], state="readonly", width=15, font=("Arial", 10))
        self.stock_out_method.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        self.stock_out_method.set("FIFO")
        
        # Date
        ttk.Label(form_frame, text="Tanggal:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_out_date = DateEntry(form_frame, width=15, background='darkblue', 
                                       foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                       font=("Arial", 10))
        self.stock_out_date.grid(row=3, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Customer
        ttk.Label(form_frame, text="Customer:").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_out_customer = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.stock_out_customer.grid(row=4, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Notes
        ttk.Label(form_frame, text="Catatan:").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.stock_out_notes = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.stock_out_notes.grid(row=5, column=1, pady=5, padx=5, sticky=tk.EW)
        
        # Button
        ttk.Button(form_frame, text="💾 Simpan Stok Keluar", command=self.save_stock_out).grid(row=6, column=1, sticky=tk.E, pady=10, padx=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        # Treeview frame
        tree_frame = ttk.LabelFrame(self.stock_out_frame, text="Riwayat Stok Keluar", padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview untuk riwayat stok keluar
        columns = ("id", "item_name", "quantity", "method", "date", "customer", "notes")
        self.stock_out_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        self.stock_out_tree.heading("id", text="ID")
        self.stock_out_tree.heading("item_name", text="Nama Barang")
        self.stock_out_tree.heading("quantity", text="Jumlah")
        self.stock_out_tree.heading("method", text="Metode")
        self.stock_out_tree.heading("date", text="Tanggal")
        self.stock_out_tree.heading("customer", text="Customer")
        self.stock_out_tree.heading("notes", text="Catatan")
        
        self.stock_out_tree.column("id", width=50, anchor=tk.CENTER)
        self.stock_out_tree.column("item_name", width=180)
        self.stock_out_tree.column("quantity", width=80, anchor=tk.CENTER)
        self.stock_out_tree.column("method", width=80, anchor=tk.CENTER)
        self.stock_out_tree.column("date", width=100, anchor=tk.CENTER)
        self.stock_out_tree.column("customer", width=150)
        self.stock_out_tree.column("notes", width=200)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.stock_out_tree.yview)
        self.stock_out_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stock_out_tree.pack(fill=tk.BOTH, expand=True)
        
        # Load data
        self.refresh_stock_out()
        
    def setup_report_tab(self):
        # Notebook untuk berbagai jenis laporan
        report_notebook = ttk.Notebook(self.report_frame)
        report_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Laporan Penjualan
        sales_frame = ttk.Frame(report_notebook, padding=10)
        report_notebook.add(sales_frame, text="📈 Laporan Penjualan")
        
        # Laporan Stok
        stock_frame = ttk.Frame(report_notebook, padding=10)
        report_notebook.add(stock_frame, text="📦 Laporan Stok")
        
        # Laporan Kadaluarsa
        expiry_frame = ttk.Frame(report_notebook, padding=10)
        report_notebook.add(expiry_frame, text="⚠️ Barang Kadaluarsa")
        
        self.setup_sales_report(sales_frame)
        self.setup_stock_report(stock_frame)
        self.setup_expiry_report(expiry_frame)
    
    def setup_sales_report(self, parent):
        # Filter frame
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Dari Tanggal:").grid(row=0, column=0, padx=5)
        self.sales_start_date = DateEntry(filter_frame, width=12, background='darkblue', 
                                         foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.sales_start_date.grid(row=0, column=1, padx=5)
        
        ttk.Label(filter_frame, text="Sampai Tanggal:").grid(row=0, column=2, padx=5)
        self.sales_end_date = DateEntry(filter_frame, width=12, background='darkblue', 
                                       foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.sales_end_date.grid(row=0, column=3, padx=5)
        
        ttk.Button(filter_frame, text="🔄 Generate Laporan", 
                  command=self.generate_sales_report).grid(row=0, column=4, padx=5)
        
        ttk.Button(filter_frame, text="📊 Export ke CSV", 
                  command=self.export_sales_report).grid(row=0, column=5, padx=5)
        
        # Treeview untuk laporan penjualan
        columns = ("item_name", "total_sold", "transaction_count", "average_per_day", "days_count")
        self.sales_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        self.sales_tree.heading("item_name", text="Nama Barang")
        self.sales_tree.heading("total_sold", text="Total Terjual")
        self.sales_tree.heading("transaction_count", text="Jumlah Transaksi")
        self.sales_tree.heading("average_per_day", text="Rata-rata per Hari")
        self.sales_tree.heading("days_count", text="Jumlah Hari")
        
        self.sales_tree.column("item_name", width=200)
        self.sales_tree.column("total_sold", width=100, anchor=tk.CENTER)
        self.sales_tree.column("transaction_count", width=120, anchor=tk.CENTER)
        self.sales_tree.column("average_per_day", width=120, anchor=tk.CENTER)
        self.sales_tree.column("days_count", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_tree.pack(fill=tk.BOTH, expand=True)
    
    def setup_stock_report(self, parent):
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="🔄 Generate Laporan Stok", 
                  command=self.generate_stock_report).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📊 Export ke CSV", 
                  command=self.export_stock_report).pack(side=tk.LEFT, padx=5)
        
        # Treeview untuk laporan stok
        columns = ("name", "category", "stock", "unit", "min_stock", "status")
        self.stock_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        self.stock_tree.heading("name", text="Nama Barang")
        self.stock_tree.heading("category", text="Kategori")
        self.stock_tree.heading("stock", text="Stok")
        self.stock_tree.heading("unit", text="Satuan")
        self.stock_tree.heading("min_stock", text="Stok Minimum")
        self.stock_tree.heading("status", text="Status")
        
        self.stock_tree.column("name", width=200)
        self.stock_tree.column("category", width=150)
        self.stock_tree.column("stock", width=80, anchor=tk.CENTER)
        self.stock_tree.column("unit", width=80, anchor=tk.CENTER)
        self.stock_tree.column("min_stock", width=100, anchor=tk.CENTER)
        self.stock_tree.column("status", width=100, anchor=tk.CENTER)
        
        # Configure tags for coloring
        self.stock_tree.tag_configure("low", background="#fff0cc")
        self.stock_tree.tag_configure("out", background="#ffcccc")
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.stock_tree.yview)
        self.stock_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stock_tree.pack(fill=tk.BOTH, expand=True)
    
    def setup_expiry_report(self, parent):
        # Filter frame
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(filter_frame, text="Threshold (hari):").pack(side=tk.LEFT, padx=5)
        self.expiry_threshold = ttk.Spinbox(filter_frame, from_=1, to=365, width=5)
        self.expiry_threshold.pack(side=tk.LEFT, padx=5)
        self.expiry_threshold.set(30)
        
        ttk.Button(filter_frame, text="🔄 Generate Laporan Kadaluarsa", 
                  command=self.generate_expiry_report).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="📊 Export ke CSV", 
                  command=self.export_expiry_report).pack(side=tk.LEFT, padx=5)
        
        # Treeview untuk laporan kadaluarsa
        columns = ("name", "category", "stock", "expiry_date", "days_until", "status")
        self.expiry_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        self.expiry_tree.heading("name", text="Nama Barang")
        self.expiry_tree.heading("category", text="Kategori")
        self.expiry_tree.heading("stock", text="Stok")
        self.expiry_tree.heading("expiry_date", text="Tanggal Kadaluarsa")
        self.expiry_tree.heading("days_until", text="Hari hingga Kadaluarsa")
        self.expiry_tree.heading("status", text="Status")
        
        self.expiry_tree.column("name", width=200)
        self.expiry_tree.column("category", width=150)
        self.expiry_tree.column("stock", width=80, anchor=tk.CENTER)
        self.expiry_tree.column("expiry_date", width=120, anchor=tk.CENTER)
        self.expiry_tree.column("days_until", width=120, anchor=tk.CENTER)
        self.expiry_tree.column("status", width=100, anchor=tk.CENTER)
        
        # Configure tags for coloring
        self.expiry_tree.tag_configure("expired", background="#ffcccc")
        self.expiry_tree.tag_configure("expiring", background="#fff0cc")
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.expiry_tree.yview)
        self.expiry_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expiry_tree.pack(fill=tk.BOTH, expand=True)
    
    def setup_dashboard_tab(self):
        # Dashboard dengan summary dan grafik
        summary_frame = ttk.Frame(self.dashboard_frame)
        summary_frame.pack(fill=tk.X, pady=10)
        
        # Summary cards
        self.total_items_var = tk.StringVar(value="0")
        self.total_stock_var = tk.StringVar(value="0")
        self.low_stock_var = tk.StringVar(value="0")
        self.expired_var = tk.StringVar(value="0")
        
        # Card 1: Total Items
        card1 = ttk.Frame(summary_frame, style="Card.TFrame")
        card1.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        ttk.Label(card1, text="Total Barang", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        ttk.Label(card1, textvariable=self.total_items_var, font=("Arial", 16, "bold"), foreground="#2c3e50").pack(pady=(0, 10))
        
        # Card 2: Total Stock
        card2 = ttk.Frame(summary_frame, style="Card.TFrame")
        card2.grid(row=0, column=1, padx=10, sticky=tk.NSEW)
        ttk.Label(card2, text="Total Stok", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        ttk.Label(card2, textvariable=self.total_stock_var, font=("Arial", 16, "bold"), foreground="#2c3e50").pack(pady=(0, 10))
        
        # Card 3: Low Stock
        card3 = ttk.Frame(summary_frame, style="Card.TFrame")
        card3.grid(row=0, column=2, padx=10, sticky=tk.NSEW)
        ttk.Label(card3, text="Stok Rendah", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        ttk.Label(card3, textvariable=self.low_stock_var, font=("Arial", 16, "bold"), foreground="#e74c3c").pack(pady=(0, 10))
        
        # Card 4: Expired
        card4 = ttk.Frame(summary_frame, style="Card.TFrame")
        card4.grid(row=0, column=3, padx=10, sticky=tk.NSEW)
        ttk.Label(card4, text="Kadaluarsa", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        ttk.Label(card4, textvariable=self.expired_var, font=("Arial", 16, "bold"), foreground="#e74c3c").pack(pady=(0, 10))
        
        # Refresh button
        ttk.Button(summary_frame, text="🔄 Refresh", command=self.update_dashboard).grid(row=0, column=4, padx=10)
        
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.columnconfigure(1, weight=1)
        summary_frame.columnconfigure(2, weight=1)
        summary_frame.columnconfigure(3, weight=1)
        summary_frame.columnconfigure(4, weight=0)
        
        # Info frame
        info_frame = ttk.Frame(self.dashboard_frame)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Low stock warning
        low_stock_frame = ttk.LabelFrame(info_frame, text="⚠️ Peringatan Stok Rendah", padding=10)
        low_stock_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("name", "category", "stock", "min_stock")
        self.low_stock_tree = ttk.Treeview(low_stock_frame, columns=columns, show="headings", height=5)
        
        self.low_stock_tree.heading("name", text="Nama Barang")
        self.low_stock_tree.heading("category", text="Kategori")
        self.low_stock_tree.heading("stock", text="Stok")
        self.low_stock_tree.heading("min_stock", text="Stok Minimum")
        
        self.low_stock_tree.column("name", width=200)
        self.low_stock_tree.column("category", width=150)
        self.low_stock_tree.column("stock", width=80, anchor=tk.CENTER)
        self.low_stock_tree.column("min_stock", width=100, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(low_stock_frame, orient=tk.VERTICAL, command=self.low_stock_tree.yview)
        self.low_stock_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.low_stock_tree.pack(fill=tk.BOTH, expand=True)
        
        # Expired items warning
        expired_frame = ttk.LabelFrame(info_frame, text="⏰ Barang Kadaluarsa", padding=10)
        expired_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("name", "category", "expiry_date", "days_until")
        self.expired_tree = ttk.Treeview(expired_frame, columns=columns, show="headings", height=5)
        
        self.expired_tree.heading("name", text="Nama Barang")
        self.expired_tree.heading("category", text="Kategori")
        self.expired_tree.heading("expiry_date", text="Tanggal Kadaluarsa")
        self.expired_tree.heading("days_until", text="Hari Hingga Kadaluarsa")
        
        self.expired_tree.column("name", width=200)
        self.expired_tree.column("category", width=150)
        self.expired_tree.column("expiry_date", width=120, anchor=tk.CENTER)
        self.expired_tree.column("days_until", width=150, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(expired_frame, orient=tk.VERTICAL, command=self.expired_tree.yview)
        self.expired_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expired_tree.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags
        self.expired_tree.tag_configure("expired", background="#ffcccc")
        self.expired_tree.tag_configure("expiring", background="#fff0cc")
        
        self.update_dashboard()
        
    def refresh_items(self):
        # Clear existing data
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
            
        # Load items
        items = self.inventory.get_all_items()
        for item in items:
            self.items_tree.insert("", tk.END, values=(
                item["id"], item["name"], item["category"], 
                item["stock"], item["unit"], item.get("min_stock", 10),
                item["created_date"], item["expiry_date"]
            ))
            
        # Update comboboxes
        item_names = [f"{item['id']} - {item['name']}" for item in items]
        self.stock_in_item["values"] = item_names
        self.stock_out_item["values"] = item_names
        
        if item_names:
            self.stock_in_item.current(0)
            self.stock_out_item.current(0)
            
    def refresh_stock_in(self):
        for item in self.stock_in_tree.get_children():
            self.stock_in_tree.delete(item)
            
        transactions = self.inventory.get_stock_in_transactions()
        for trans in transactions:
            self.stock_in_tree.insert("", tk.END, values=(
                trans["id"], trans["item_name"], trans["quantity"], 
                trans["date"], trans.get("supplier", ""), trans.get("notes", "")
            ))
            
    def refresh_stock_out(self):
        for item in self.stock_out_tree.get_children():
            self.stock_out_tree.delete(item)
            
        transactions = self.inventory.get_stock_out_transactions()
        for trans in transactions:
            self.stock_out_tree.insert("", tk.END, values=(
                trans["id"], trans["item_name"], trans["quantity"], 
                trans["method"], trans["date"], trans.get("customer", ""), trans.get("notes", "")
            ))
            
    def search_items(self, event):
        search_term = self.search_entry.get().lower()
        
        # Clear existing data
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
            
        # Filter items
        items = self.inventory.get_all_items()
        for item in items:
            if (search_term in item["name"].lower() or 
                search_term in item["category"].lower() or 
                search_term in str(item["id"]) or
                search_term in item["unit"].lower()):
                self.items_tree.insert("", tk.END, values=(
                    item["id"], item["name"], item["category"], 
                    item["stock"], item["unit"], item.get("min_stock", 10),
                    item["created_date"], item["expiry_date"]
                ))
                
    def sort_treeview(self, tree, col, reverse):
        try:
            data = [(tree.set(item, col), item) for item in tree.get_children('')]
            
            # Try to convert to numbers for proper sorting
            try:
                data.sort(key=lambda x: float(x[0]), reverse=reverse)
            except ValueError:
                data.sort(reverse=reverse)
                
            for index, (val, item) in enumerate(data):
                tree.move(item, '', index)
                
            tree.heading(col, command=lambda: self.sort_treeview(tree, col, not reverse))
        except Exception as e:
            print(f"Error sorting: {e}")
            
    def on_item_double_click(self, event):
        self.open_edit_item()
            
    def open_add_item(self):
        AddItemWindow(self.root, self.inventory, self.refresh_items)
        
    def open_edit_item(self):
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Pilih barang yang akan diedit")
            return
            
        item_id = self.items_tree.item(selection[0])["values"][0]
        EditItemWindow(self.root, self.inventory, item_id, self.refresh_items)
        
    def delete_item(self):
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showerror("Error", "Pilih barang yang akan dihapus")
            return
            
        item_id = self.items_tree.item(selection[0])["values"][0]
        item_name = self.items_tree.item(selection[0])["values"][1]
        
        if messagebox.askyesno("Konfirmasi", f"Apakah Anda yakin ingin menghapus barang '{item_name}'?"):
            if self.inventory.delete_item(item_id):
                messagebox.showinfo("Success", "Barang berhasil dihapus")
                self.refresh_items()
            else:
                messagebox.showerror("Error", "Gagal menghapus barang")
                
    def save_stock_in(self):
        selection = self.stock_in_item.get()
        if not selection:
            messagebox.showerror("Error", "Pilih barang terlebih dahulu")
            return
            
        try:
            item_id = int(selection.split(" - ")[0])
            quantity = int(self.stock_in_qty.get())
            date = self.stock_in_date.get_date().strftime("%Y-%m-%d")
            supplier = self.stock_in_supplier.get().strip()
            notes = self.stock_in_notes.get().strip()
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka")
            return
            
        if quantity <= 0:
            messagebox.showerror("Error", "Jumlah harus lebih dari 0")
            return
            
        if self.inventory.stock_in(item_id, quantity, date, supplier, notes):
            messagebox.showinfo("Success", "Stok masuk berhasil disimpan")
            self.refresh_items()
            self.refresh_stock_in()
            self.stock_in_qty.delete(0, tk.END)
            self.stock_in_qty.insert(0, "1")
            self.stock_in_supplier.delete(0, tk.END)
            self.stock_in_notes.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Gagal menyimpan stok masuk")
            
    def save_stock_out(self):
        selection = self.stock_out_item.get()
        if not selection:
            messagebox.showerror("Error", "Pilih barang terlebih dahulu")
            return
            
        try:
            item_id = int(selection.split(" - ")[0])
            quantity = int(self.stock_out_qty.get())
            method = self.stock_out_method.get()
            date = self.stock_out_date.get_date().strftime("%Y-%m-%d")
            customer = self.stock_out_customer.get().strip()
            notes = self.stock_out_notes.get().strip()
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka")
            return
            
        if quantity <= 0:
            messagebox.showerror("Error", "Jumlah harus lebih dari 0")
            return
            
        success, message = self.inventory.stock_out(item_id, quantity, method, date, customer, notes)
        if success:
            messagebox.showinfo("Success", message)
            self.refresh_items()
            self.refresh_stock_out()
            self.stock_out_qty.delete(0, tk.END)
            self.stock_out_qty.insert(0, "1")
            self.stock_out_customer.delete(0, tk.END)
            self.stock_out_notes.delete(0, tk.END)
        else:
            messagebox.showerror("Error", message)
            
    def generate_sales_report(self):
        start_date = self.sales_start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.sales_end_date.get_date().strftime("%Y-%m-%d")
        
        if start_date > end_date:
            messagebox.showerror("Error", "Tanggal mulai tidak boleh lebih besar dari tanggal akhir")
            return
        
        # Clear existing data
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
            
        # Generate report
        report = self.inventory.generate_sales_report(start_date, end_date)
        for item in report:
            self.sales_tree.insert("", tk.END, values=(
                item["item_name"], item["total_sold"], item["transaction_count"],
                item["average_per_day"], item["days_count"]
            ))
    
    def generate_stock_report(self):
        # Clear existing data
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
            
        # Add items to treeview
        for item in self.inventory.get_all_items():
            status = "Normal"
            tags = ()
            if item["stock"] == 0:
                status = "Habis"
                tags = ("out",)
            elif item["stock"] <= item.get("min_stock", 10):
                status = "Rendah"
                tags = ("low",)
                
            self.stock_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["stock"],
                item["unit"], item.get("min_stock", 10), status
            ), tags=tags)
    
    def generate_expiry_report(self):
        try:
            threshold = int(self.expiry_threshold.get())
        except ValueError:
            messagebox.showerror("Error", "Threshold harus berupa angka")
            return
            
        # Clear existing data
        for item in self.expiry_tree.get_children():
            self.expiry_tree.delete(item)
            
        # Generate report
        report = self.inventory.generate_expiry_report(threshold)
        
        # Add expired items
        for item in report["expired"]:
            self.expiry_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["stock"],
                item["expiry_date"], item["days_until_expiry"], "KADALUARSA"
            ), tags=("expired",))
        
        # Add expiring soon items
        for item in report["expiring_soon"]:
            self.expiry_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["stock"],
                item["expiry_date"], item["days_until_expiry"], "Akan Kadaluarsa"
            ), tags=("expiring",))
    
    def update_dashboard(self):
        # Update summary cards
        items = self.inventory.get_all_items()
        self.total_items_var.set(str(len(items)))
        
        total_stock = sum(item["stock"] for item in items)
        self.total_stock_var.set(str(total_stock))
        
        # Update low stock count
        stock_report = self.inventory.generate_stock_report()
        self.low_stock_var.set(str(len(stock_report["low_stock_items"]) + len(stock_report["out_of_stock_items"])))
        
        # Update expired count
        expiry_report = self.inventory.generate_expiry_report()
        self.expired_var.set(str(len(expiry_report["expired"])))
        
        # Update low stock items
        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)
            
        for item in stock_report["low_stock_items"]:
            self.low_stock_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["stock"], item.get("min_stock", 10)
            ))
            
        for item in stock_report["out_of_stock_items"]:
            self.low_stock_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["stock"], item.get("min_stock", 10)
            ))
        
        # Update expired items
        for item in self.expired_tree.get_children():
            self.expired_tree.delete(item)
            
        for item in expiry_report["expired"]:
            self.expired_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["expiry_date"], item["days_until_expiry"]
            ), tags=("expired",))
            
        for item in expiry_report["expiring_soon"]:
            self.expired_tree.insert("", tk.END, values=(
                item["name"], item["category"], item["expiry_date"], item["days_until_expiry"]
            ), tags=("expiring",))
    
    def export_sales_report(self):
        start_date = self.sales_start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.sales_end_date.get_date().strftime("%Y-%m-%d")
        
        if start_date > end_date:
            messagebox.showerror("Error", "Tanggal mulai tidak boleh lebih besar dari tanggal akhir")
            return
            
        report = self.inventory.generate_sales_report(start_date, end_date)
        if not report:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk diexport")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Simpan Laporan Penjualan"
        )
        
        if filename:
            fieldnames = ["item_name", "total_sold", "transaction_count", "average_per_day", "days_count"]
            if export_to_csv(report, filename, fieldnames):
                messagebox.showinfo("Success", f"Laporan berhasil diexport ke {filename}")
            else:
                messagebox.showerror("Error", "Gagal mengexport laporan")
    
    def export_stock_report(self):
        items = self.inventory.get_all_items()
        if not items:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk diexport")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Simpan Laporan Stok"
        )
        
        if filename:
            # Prepare data for export
            export_data = []
            for item in items:
                status = "Normal"
                if item["stock"] == 0:
                    status = "Habis"
                elif item["stock"] <= item.get("min_stock", 10):
                    status = "Rendah"
                    
                export_data.append({
                    "name": item["name"],
                    "category": item["category"],
                    "stock": item["stock"],
                    "unit": item["unit"],
                    "min_stock": item.get("min_stock", 10),
                    "status": status,
                    "created_date": item["created_date"],
                    "expiry_date": item["expiry_date"]
                })
            
            fieldnames = ["name", "category", "stock", "unit", "min_stock", "status", "created_date", "expiry_date"]
            if export_to_csv(export_data, filename, fieldnames):
                messagebox.showinfo("Success", f"Laporan berhasil diexport ke {filename}")
            else:
                messagebox.showerror("Error", "Gagal mengexport laporan")
    
    def export_expiry_report(self):
        try:
            threshold = int(self.expiry_threshold.get())
        except ValueError:
            messagebox.showerror("Error", "Threshold harus berupa angka")
            return
            
        report = self.inventory.generate_expiry_report(threshold)
        if not report["expired"] and not report["expiring_soon"]:
            messagebox.showwarning("Peringatan", "Tidak ada data untuk diexport")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Simpan Laporan Kadaluarsa"
        )
        
        if filename:
            # Combine expired and expiring items
            export_data = []
            for item in report["expired"]:
                export_data.append({
                    "name": item["name"],
                    "category": item["category"],
                    "stock": item["stock"],
                    "expiry_date": item["expiry_date"],
                    "days_until_expiry": item["days_until_expiry"],
                    "status": "KADALUARSA"
                })
                
            for item in report["expiring_soon"]:
                export_data.append({
                    "name": item["name"],
                    "category": item["category"],
                    "stock": item["stock"],
                    "expiry_date": item["expiry_date"],
                    "days_until_expiry": item["days_until_expiry"],
                    "status": "Akan Kadaluarsa"
                })
            
            fieldnames = ["name", "category", "stock", "expiry_date", "days_until_expiry", "status"]
            if export_to_csv(export_data, filename, fieldnames):
                messagebox.showinfo("Success", f"Laporan berhasil diexport ke {filename}")
            else:
                messagebox.showerror("Error", "Gagal mengexport laporan")


class AddItemWindow(tk.Toplevel):
    def __init__(self, parent, inventory, callback):
        super().__init__(parent)
        self.title("Tambah Barang Baru")
        self.geometry("450x500")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        
        # Center window
        self.transient(parent)
        self.grab_set()
        self.eval(f'tk::PlaceWindow {str(self)} center')
        
        self.inventory = inventory
        self.callback = callback
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=20, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        form_frame = ttk.Frame(main_frame, style="Form.TFrame")
        form_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(form_frame, text="Nama Barang:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.name_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Kategori:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.category_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.category_entry.grid(row=1, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Stok Awal:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=5)
        self.stock_entry = ttk.Spinbox(form_frame, from_=0, to=10000, width=15, font=("Arial", 10))
        self.stock_entry.grid(row=2, column=1, sticky=tk.W, pady=8, padx=5)
        self.stock_entry.set(0)
        
        ttk.Label(form_frame, text="Satuan:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=5)
        self.unit_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.unit_entry.grid(row=3, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Stok Minimum:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=8, padx=5)
        self.min_stock_entry = ttk.Spinbox(form_frame, from_=0, to=1000, width=15, font=("Arial", 10))
        self.min_stock_entry.grid(row=4, column=1, sticky=tk.W, pady=8, padx=5)
        self.min_stock_entry.set(10)
        
        ttk.Label(form_frame, text="Tanggal Dibuat:", font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=8, padx=5)
        self.created_date_entry = DateEntry(form_frame, width=15, background='darkblue', 
                                          foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                          font=("Arial", 10))
        self.created_date_entry.grid(row=5, column=1, sticky=tk.W, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Tanggal Kadaluarsa:", font=("Arial", 10)).grid(row=6, column=0, sticky=tk.W, pady=8, padx=5)
        self.expiry_date_entry = DateEntry(form_frame, width=15, background='darkblue', 
                                         foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                         font=("Arial", 10))
        self.expiry_date_entry.grid(row=6, column=1, sticky=tk.W, pady=8, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="💾 Simpan", command=self.save_item, width=12).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ Batal", command=self.destroy, width=12).pack(side=tk.LEFT, padx=10)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Form.TFrame", background="#f0f0f0")
        
    def save_item(self):
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        
        try:
            stock = int(self.stock_entry.get())
            min_stock = int(self.min_stock_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka")
            return
            
        unit = self.unit_entry.get().strip()
        created_date = self.created_date_entry.get_date().strftime("%Y-%m-%d")
        expiry_date = self.expiry_date_entry.get_date().strftime("%Y-%m-%d")
        
        if not name or not category or not unit:
            messagebox.showerror("Error", "Nama, kategori, dan satuan harus diisi")
            return
            
        if created_date > expiry_date:
            messagebox.showerror("Error", "Tanggal kadaluarsa tidak boleh sebelum tanggal dibuat")
            return
            
        if self.inventory.add_item(name, category, stock, unit, created_date, expiry_date, min_stock):
            messagebox.showinfo("Success", "Barang berhasil ditambahkan")
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Gagal menambahkan barang")


class EditItemWindow(tk.Toplevel):
    def __init__(self, parent, inventory, item_id, callback):
        super().__init__(parent)
        self.title("Edit Barang")
        self.geometry("450x500")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        
        # Center window
        self.transient(parent)
        self.grab_set()
        self.eval(f'tk::PlaceWindow {str(self)} center')
        
        self.inventory = inventory
        self.item_id = item_id
        self.callback = callback
        
        self.setup_ui()
        self.load_item_data()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self, padding=20, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        form_frame = ttk.Frame(main_frame, style="Form.TFrame")
        form_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(form_frame, text="Nama Barang:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=5)
        self.name_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Kategori:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=5)
        self.category_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.category_entry.grid(row=1, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Stok:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=5)
        self.stock_entry = ttk.Spinbox(form_frame, from_=0, to=10000, width=15, font=("Arial", 10))
        self.stock_entry.grid(row=2, column=1, sticky=tk.W, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Satuan:", font=("Arial", 10)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=5)
        self.unit_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        self.unit_entry.grid(row=3, column=1, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Stok Minimum:", font=("Arial", 10)).grid(row=4, column=0, sticky=tk.W, pady=8, padx=5)
        self.min_stock_entry = ttk.Spinbox(form_frame, from_=0, to=1000, width=15, font=("Arial", 10))
        self.min_stock_entry.grid(row=4, column=1, sticky=tk.W, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Tanggal Dibuat:", font=("Arial", 10)).grid(row=5, column=0, sticky=tk.W, pady=8, padx=5)
        self.created_date_entry = DateEntry(form_frame, width=15, background='darkblue', 
                                          foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                          font=("Arial", 10))
        self.created_date_entry.grid(row=5, column=1, sticky=tk.W, pady=8, padx=5)
        
        ttk.Label(form_frame, text="Tanggal Kadaluarsa:", font=("Arial", 10)).grid(row=6, column=0, sticky=tk.W, pady=8, padx=5)
        self.expiry_date_entry = DateEntry(form_frame, width=15, background='darkblue', 
                                         foreground='white', borderwidth=2, date_pattern='y-mm-dd',
                                         font=("Arial", 10))
        self.expiry_date_entry.grid(row=6, column=1, sticky=tk.W, pady=8, padx=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="💾 Simpan", command=self.save_item, width=12).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ Batal", command=self.destroy, width=12).pack(side=tk.LEFT, padx=10)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Main.TFrame", background="#f0f0f0")
        style.configure("Form.TFrame", background="#f0f0f0")
        
    def load_item_data(self):
        item = self.inventory.get_item(self.item_id)
        if item:
            self.name_entry.insert(0, item["name"])
            self.category_entry.insert(0, item["category"])
            self.stock_entry.delete(0, tk.END)
            self.stock_entry.insert(0, str(item["stock"]))
            self.unit_entry.insert(0, item["unit"])
            self.min_stock_entry.delete(0, tk.END)
            self.min_stock_entry.insert(0, str(item.get("min_stock", 10)))
            
            # Set dates
            try:
                created_date = datetime.strptime(item["created_date"], "%Y-%m-%d")
                self.created_date_entry.set_date(created_date)
            except:
                pass
                
            try:
                expiry_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d")
                self.expiry_date_entry.set_date(expiry_date)
            except:
                pass
            
    def save_item(self):
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        
        try:
            stock = int(self.stock_entry.get())
            min_stock = int(self.min_stock_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka")
            return
            
        unit = self.unit_entry.get().strip()
        created_date = self.created_date_entry.get_date().strftime("%Y-%m-%d")
        expiry_date = self.expiry_date_entry.get_date().strftime("%Y-%m-%d")
        
        if not name or not category or not unit:
            messagebox.showerror("Error", "Nama, kategori, dan satuan harus diisi")
            return
            
        if created_date > expiry_date:
            messagebox.showerror("Error", "Tanggal kadaluarsa tidak boleh sebelum tanggal dibuat")
            return
            
        if self.inventory.update_item(self.item_id, name, category, stock, unit, created_date, expiry_date, min_stock):
            messagebox.showinfo("Success", "Barang berhasil diupdate")
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Gagal mengupdate barang")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()