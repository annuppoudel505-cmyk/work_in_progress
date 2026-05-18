import sqlite3

###database setup

def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT,
        role TEXT DEFAULT 'user',
        admin_request INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (username, email)
    )
    """)

    # Create default super admin
    cursor.execute("""
    INSERT OR IGNORE INTO users
    (username, email, password, role, admin_request)
    VALUES (?, ?, ?, ?, ?)
    """, ("superadmin", "superadmin@example.com", "super_admin", "super_admin", 0))

    # Create national park table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS national_park (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        location TEXT,
        province TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (name, location, province)
    )
    """)
    # Create default national park
    cursor.execute("""
    INSERT OR IGNORE INTO national_park (name, location, province)
    VALUES (?, ?, ?)
    """, ("Chitwan National Park", "Chitwan", "Chitwan"))

    # Create park admin table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS park_admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        park_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (park_id) REFERENCES national_park(id) ON DELETE CASCADE,
        UNIQUE (user_id, park_id)
    )
    """)

    # Create default park admin
    cursor.execute("""
    INSERT OR IGNORE INTO park_admin (user_id, park_id)
    VALUES (?, ?)
    """, (1, 1))

    # Create ticket type table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        park_id INTEGER NOT NULL,
        type_name TEXT NOT NULL,
        price REAL NOT NULL,
        is_group INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (park_id) REFERENCES national_park(id) ON DELETE CASCADE,
        UNIQUE (park_id)
    )
    """)

    # Create default ticket type
    cursor.execute("""
    INSERT OR IGNORE INTO ticket_type (park_id, type_name, price)
    VALUES (?, ?, ?)
    """, (1, "Adult", 20.0))

    # Create ticket table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER Nullable,
        park_id INTEGER NOT NULL,
        ticket_type_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        ticket_category TEXT NOT NULL,
        qr_code TEXT,
        total_visitors INTEGER,
        total_amount REAL,
        payment_status TEXT DEFAULT 'pending',
        status TEXT DEFAULT 'valid',
        issued_by TEXT,
        issued_from TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (park_id) REFERENCES national_park(id) ON DELETE CASCADE,
        FOREIGN KEY (ticket_type_id) REFERENCES ticket_type(id) ON DELETE CASCADE
    )
    """)

    # Create default ticket
    cursor.execute("""
    INSERT OR IGNORE INTO ticket (user_id, park_id, ticket_type_id, quantity, ticket_category, total_visitors, total_amount, payment_status, status, issued_by, issued_from)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (1, 1, 1, 2, "Adult", 2, 40.0, "paid", "valid", "superadmin", "online"))  

    # Create individual ticket table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS individual_ticket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        visitor_name TEXT NOT NULL,
        visitor_age INTEGER NOT NULL,
        visitor_phone TEXT NOT NULL,
        nationality TEXT NOT NULL,
        id_type TEXT DEFAULT 'citizenship',
        id_number TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES ticket(id) ON DELETE CASCADE,
        UNIQUE (ticket_id)
    )
    """)

    # Create default individual ticket
    cursor.execute(""" 
    INSERT OR IGNORE INTO individual_ticket (ticket_id, visitor_name, visitor_age, visitor_phone, nationality, id_type, id_number)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (1, "John Doe", 30, "1234567890", "American", "citizenship", "123456789"))

    # Create group ticket table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_ticket (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        contact_person TEXT NOT NULL,
        contact_phone TEXT NOT NULL,
        nationality TEXT NOT NULL,
        male_count INTEGER NOT NULL,
        female_count INTEGER NOT NULL,
        group_size INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES ticket(id) ON DELETE CASCADE,
        UNIQUE (ticket_id)
    )
    """)

    # Create default group ticket    
    cursor.execute("""
    INSERT OR IGNORE INTO group_ticket (ticket_id, contact_person, contact_phone, nationality, male_count, female_count, group_size)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (1, "Jane Smith", "0987654321", "British", 5, 5, 10))  

    # Create payment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,   
        payment_status TEXT DEFAULT 'pending',
        transaction_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES ticket(id) ON DELETE CASCADE,
        UNIQUE (ticket_id)
    )
    """)

    # Create default payment
    cursor.execute("""
    INSERT OR IGNORE INTO payment (ticket_id, amount, payment_method, payment_status, transaction_id)
    VALUES (?, ?, ?, ?, ?)
    """, (1, 40.0, "credit_card", "paid", "TXN123456"))

    # Create Counter table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS counter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        park_id INTEGER NOT NULL,
        counter_name TEXT NOT NULL,
        location TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (park_id) REFERENCES national_park(id) ON DELETE CASCADE,
        UNIQUE (park_id)
    )
    """)

    # Create default counter
    cursor.execute("""
    INSERT OR IGNORE INTO counter (park_id, counter_name, location)
    VALUES (?, ?, ?)
    """, (1, "Main Counter", "Entrance"))

    # Create Ranger table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ranger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        park_id INTEGER NOT NULL,
        ranger_name TEXT NOT NULL,
        contact_info TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (park_id) REFERENCES national_park(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE (user_id, park_id)
    )
    """) 

    # Create default ranger
    cursor.execute("""
    INSERT OR IGNORE INTO ranger (user_id, park_id, ranger_name, contact_info)
    VALUES (?, ?, ?, ?)
    """, (1, 1, "Ranger Rick", "ranger.rick"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
