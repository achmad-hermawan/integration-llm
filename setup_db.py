import sqlite3
import os

def init_db():
    db_name = 'sales_data.db'
    
    # Hapus file database lama jika ada (biar bersih)
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"🗑️ Database lama '{db_name}' dihapus.")

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    print("⚙️ Sedang membuat tabel...")

    # 1. Buat Tabel PRODUCTS
    c.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')

    # 2. Buat Tabel CUSTOMERS
    c.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            city TEXT NOT NULL
        )
    ''')

    # 3. Buat Tabel SALES (Transaksi)
    c.execute('''
        CREATE TABLE sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            date TEXT,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')

    # --- ISI DATA DUMMY (SAMPLE DATA) ---
    print("📥 Sedang mengisi data dummy...")

    # Data Produk (Electronics)
    products = [
        ('Laptop Gaming ROG', 15000000, 10),
        ('MacBook Air M2', 18000000, 15),
        ('Mouse Logitech Wireless', 250000, 50),
        ('Mechanical Keyboard Keychron', 1200000, 30),
        ('Monitor Samsung 24 inch', 2100000, 20),
        ('Headset HyperX Cloud', 1500000, 25),
        ('SSD Samsung 1TB', 1800000, 40),
        ('RAM Corsair 16GB', 900000, 35)
    ]
    c.executemany('INSERT INTO products (name, price, stock) VALUES (?,?,?)', products)

    # Data Pelanggan (Indonesia)
    customers = [
        ('Budi Santoso', 'budi@gmail.com', 'Jakarta'),
        ('Siti Aminah', 'siti@yahoo.com', 'Surabaya'),
        ('Andi Wijaya', 'andi@outlook.com', 'Bandung'),
        ('Dewi Lestari', 'dewi@gmail.com', 'Jakarta'),
        ('Rizky Febian', 'rizky@music.com', 'Jakarta'),
        ('Eka Gusti', 'eka@mail.com', 'Yogyakarta')
    ]
    c.executemany('INSERT INTO customers (name, email, city) VALUES (?,?,?)', customers)

    # Data Penjualan (Sales)
    # Format: (customer_id, product_id, quantity, date)
    sales = [
        (1, 1, 1, '2023-11-01'), # Budi beli Laptop
        (1, 3, 1, '2023-11-01'), # Budi beli Mouse juga
        (2, 2, 1, '2023-11-02'), # Siti beli MacBook
        (3, 4, 1, '2023-11-03'), # Andi beli Keyboard
        (4, 5, 2, '2023-11-05'), # Dewi beli 2 Monitor
        (5, 6, 1, '2023-11-06'), # Rizky beli Headset
        (6, 3, 5, '2023-11-07'), # Eka borong Mouse
        (2, 7, 1, '2023-11-08'), # Siti beli SSD
    ]
    c.executemany('INSERT INTO sales (customer_id, product_id, quantity, date) VALUES (?,?,?,?)', sales)

    conn.commit()
    conn.close()
    print("✅ SUKSES! Database 'sales_data.db' berhasil dibuat.")

if __name__ == "__main__":
    init_db()