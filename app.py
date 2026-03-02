"""
GridPulse — Автоматизирана крипто търговска платформа
Версия: 1.0
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from datetime import datetime
import secrets

# Инициализация на Flask приложението
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Случаен секретен ключ

# Път към базата данни
DB_PATH = 'gridpulse.db'

# ============================================================
# БАЗА ДАННИ — Създаване на таблиците при първо стартиране
# ============================================================

def init_db():
    """Създава базата данни и таблиците ако не съществуват"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица за потребители
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            referral_code TEXT UNIQUE NOT NULL,
            referred_by TEXT,
            balance_demo REAL DEFAULT 10000.0,
            balance_real REAL DEFAULT 0.0,
            subscription_active BOOLEAN DEFAULT 0,
            subscription_expiry TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Таблица за плащания
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            tx_hash TEXT UNIQUE NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Таблица за сделки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            exchange TEXT NOT NULL,
            pair TEXT NOT NULL,
            side TEXT NOT NULL,
            amount REAL NOT NULL,
            price REAL NOT NULL,
            is_demo BOOLEAN DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ============================================================
# СТРАНИЦИ НА САЙТА
# ============================================================

@app.route('/')
def index():
    """Лендинг страница"""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация на нов потребител"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        referral = request.form.get('referral', '')
        
        # Генериране на уникален реферален код
        ref_code = secrets.token_hex(8)
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Добавяне на потребител
            cursor.execute('''
                INSERT INTO users (email, password, referral_code, referred_by, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, password, ref_code, referral, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            
            flash('Регистрацията е успешна! Можете да влезете.')
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError:
            flash('Имейлът вече съществува!')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Вход на потребител"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, email FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['email'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Грешен имейл или парола!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Потребителски панел"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Тук ще показваме баланса, сделки, настройки и т.н.
    return render_template('dashboard.html', email=session['email'])

@app.route('/logout')
def logout():
    """Изход от акаунта"""
    session.clear()
    return redirect(url_for('index'))

# ============================================================
# СТАРТИРАНЕ НА СЪРВЕРА
# ============================================================

if __name__ == '__main__':
    # Създаване на базата данни при първо стартиране
    if not os.path.exists(DB_PATH):
        init_db()
        print("✅ Базата данни е създадена!")
    
    print("🚀 GridPulse стартира на http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
