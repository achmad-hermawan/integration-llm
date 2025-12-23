import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_NAME = "sales_data.db"

# --- DATA DUMMY REALISTIS ---
CATEGORIES_LIST = [
    "Laptop", "Smartphone", "Tablet", "Aksesoris", "Monitor", 
    "Networking", "Printer", "Storage"
]

PRODUCT_NAMES = {
    "Laptop": ["MacBook Air M2", "MacBook Pro M3", "Lenovo ThinkPad X1", "Dell XPS 13", "Asus ROG Zephyrus", "HP Spectre x360", "Acer Swift 5"],
    "Smartphone": ["iPhone 15 Pro", "Samsung Galaxy S24", "Google Pixel 8", "Xiaomi 14", "iPhone 14", "Samsung Z Flip 5"],
    "Tablet": ["iPad Pro M4", "iPad Air 5", "Samsung Tab S9", "Xiaomi Pad 6"],
    "Aksesoris": ["Logitech MX Master 3", "Apple Magic Mouse", "Keychron K2 Keyboard", "Sony WH-1000XM5 Headphone", "Anker Charger 65W"],
    "Monitor": ["Dell UltraSharp 27", "LG UltraGear 24", "Samsung Odyssey G9", "BenQ Designer Monitor"],
    "Networking": ["TP-Link Archer AX73", "Ubiquiti Unifi AP", "Asus RT-AX86U Router"],
    "Printer": ["Epson EcoTank L3210", "HP LaserJet Pro", "Canon Pixma"],
    "Storage": ["Samsung T7 SSD 1TB", "WD MyPassport 2TB", "SanDisk Extreme Pro 128GB"]
}

CITIES = [
    "Jakarta Selatan", "Jakarta Pusat", "Jakarta Barat", "Bandung", "Surabaya", 
    "Medan", "Yogyakarta", "Semarang", "Makassar", "Denpasar", "Balikpapan", 
    "Tangerang Selatan", "Bekasi", "Depok", "Bogor", "Malang"
]

COURIERS = ["JNE", "J&T", "SiCepat", "AnterAja", "GoSend Instant"]

def init_db():
    print("⏳ Sedang menghapus database lama...")
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    print("🏗️  Membangun struktur database baru...")
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()

    # 1. USERS
    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('ADMIN','STAFF')),
            created_at TEXT NOT NULL
        )
    """)

    # 2. CUSTOMERS
    c.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # 3. ADDRESSES
    c.execute("""
        CREATE TABLE addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            address TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    # 4. CATEGORIES
    c.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # 5. PRODUCTS
    c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL CHECK(price > 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            is_active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
    """)

    # 6. ORDERS
    c.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('PENDING','PAID','SHIPPED','CANCELLED')),
            total REAL NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    # 7. ORDER ITEMS
    c.execute("""
        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # 8. PAYMENTS
    c.execute("""
        CREATE TABLE payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            method TEXT NOT NULL CHECK(method IN ('TRANSFER','EWALLET','CREDIT_CARD')),
            amount REAL NOT NULL,
            paid_at TEXT NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)

    # 9. SHIPMENTS
    c.execute("""
        CREATE TABLE shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            courier TEXT NOT NULL,
            tracking_number TEXT UNIQUE,
            shipped_at TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    """)

    # INDEXES
    c.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
    c.execute("CREATE INDEX idx_orders_date ON orders(order_date)")
    c.execute("CREATE INDEX idx_products_category ON products(category_id)")

    now = datetime.now().isoformat()

    # --- SEEDING DATA ---
    print("🌱 Mulai mengisi data dummy (Ini mungkin butuh beberapa detik)...")

    # A. USERS
    users = [("admin", "ADMIN", now), ("budi_staff", "STAFF", now), ("siti_staff", "STAFF", now)]
    c.executemany("INSERT INTO users VALUES (NULL,?,?,?)", users)

    # B. CATEGORIES
    for cat in CATEGORIES_LIST:
        c.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
    
    # Mapping Category ID
    c.execute("SELECT id, name FROM categories")
    cat_map = {name: id for id, name in c.fetchall()}

    # C. PRODUCTS
    products_data = []
    for cat_name, items in PRODUCT_NAMES.items():
        cat_id = cat_map[cat_name]
        for item_name in items:
            price = random.randint(5, 300) * 100_000  # 500rb - 30jt
            stock = random.randint(10, 200)
            products_data.append((cat_id, item_name, price, stock, 1, now))
    
    c.executemany("INSERT INTO products VALUES (NULL,?,?,?,?,?,?)", products_data)
    print(f"   - {len(products_data)} Produk berhasil dibuat.")

    # D. CUSTOMERS & ADDRESSES
    customers_data = []
    addresses_data = []
    num_customers = 100  # Bikin 100 Customer
    
    first_names = ["Adi", "Budi", "Citra", "Dewi", "Eko", "Fajar", "Gita", "Hendra", "Indah", "Joko"]
    last_names = ["Santoso", "Wijaya", "Putra", "Putri", "Kusuma", "Pratama", "Hidayat", "Saputra"]

    for i in range(1, num_customers + 1):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"customer{i}@gmail.com"
        phone = f"08{random.randint(1111111111, 9999999999)}"
        created_at = (datetime.now() - timedelta(days=random.randint(100, 365))).isoformat()
        
        c.execute("INSERT INTO customers VALUES (NULL,?,?,?,?)", (full_name, email, phone, created_at))
        cust_id = c.lastrowid
        
        city = random.choice(CITIES)
        address = f"Jl. {random.choice(['Merpati', 'Sudirman', 'Gatot Subroto', 'Ahmad Yani', 'Melati'])} No. {random.randint(1, 100)}"
        addresses_data.append((cust_id, city, address))

    c.executemany("INSERT INTO addresses VALUES (NULL,?,?,?)", addresses_data)
    print(f"   - {num_customers} Customer & Alamat berhasil dibuat.")

    # E. ORDERS (TRANSAKSI BESAR)
    num_orders = 1000  # Bikin 1.000 Transaksi
    print(f"   - Sedang generate {num_orders} transaksi...")

    # Ambil list product ID dan harga biar cepat
    c.execute("SELECT id, price FROM products")
    all_products = c.fetchall() # List of (id, price)

    for i in range(num_orders):
        customer_id = random.randint(1, num_customers)
        
        # Random date dalam 1 tahun terakhir
        days_ago = random.randint(0, 365)
        order_date = (datetime.now() - timedelta(days=days_ago)).date().isoformat()
        
        # Status logic
        if days_ago < 3:
            status = random.choice(['PENDING', 'PAID'])
        else:
            status = random.choices(['SHIPPED', 'CANCELLED', 'PAID'], weights=[80, 5, 15])[0]

        # Insert Order (Total 0 dulu)
        c.execute("INSERT INTO orders VALUES (NULL,?,?,?,0)", (customer_id, order_date, status))
        order_id = c.lastrowid

        # Generate Items
        num_items = random.randint(1, 4)
        total_order = 0
        
        # Pilih produk unik untuk order ini
        selected_products = random.sample(all_products, num_items)

        for prod_id, prod_price in selected_products:
            qty = random.randint(1, 3)
            total_price = prod_price * qty # Harga item saat itu (simplified)
            total_order += total_price

            # FIX: HANYA ADA 4 Value setelah NULL (order_id, product_id, qty, price)
            c.execute("INSERT INTO order_items VALUES (NULL,?,?,?,?)", 
                      (order_id, prod_id, qty, prod_price))

        # Update Total Order
        c.execute("UPDATE orders SET total=? WHERE id=?", (total_order, order_id))

        # Jika sudah bayar/dikirim, bikin data Payment
        if status in ['PAID', 'SHIPPED']:
            paid_at = (datetime.strptime(order_date, "%Y-%m-%d") + timedelta(hours=random.randint(1, 24))).isoformat()
            c.execute("INSERT INTO payments VALUES (NULL,?,?,?,?)", 
                      (order_id, random.choice(['TRANSFER', 'EWALLET', 'CREDIT_CARD']), total_order, paid_at))

        # Jika sudah dikirim, bikin data Shipment
        if status == 'SHIPPED':
            shipped_at = (datetime.strptime(order_date, "%Y-%m-%d") + timedelta(days=1)).isoformat()
            courier = random.choice(COURIERS)
            tracking = f"RES-{random.randint(10000,99999)}-{random.choice(['A','B','C'])}"
            c.execute("INSERT INTO shipments VALUES (NULL,?,?,?,?)",
                      (order_id, courier, tracking, shipped_at))

    conn.commit()
    conn.close()
    print("\n✅ SUKSES! Database Enterprise dengan 1000+ data siap digunakan.")
    print(f"📂 Lokasi: {os.path.abspath(DB_NAME)}")

if __name__ == "__main__":
    init_db()