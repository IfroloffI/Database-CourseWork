-- Создание таблицы клиентов
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    passport_number VARCHAR(20) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    email VARCHAR(100) UNIQUE,  -- Теперь email тоже уникален
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Создание таблицы авторизации
CREATE TABLE auth (
    id SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',  -- 'user' или 'admin'
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL
);

-- Индекс для ускорения поиска по логину
CREATE INDEX idx_auth_login ON auth(login);

-- Создание таблицы счетов
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    account_type VARCHAR(50) NOT NULL, -- 'checking', 'savings', 'credit'
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'RUB',
    opened_date DATE NOT NULL DEFAULT CURRENT_DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Создание таблицы транзакций
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    from_account_id INTEGER REFERENCES accounts(id),
    to_account_id INTEGER NOT NULL REFERENCES accounts(id),
    amount DECIMAL(15, 2) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- 'transfer', 'deposit', 'withdrawal'
    description TEXT,
    transaction_date TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'completed', -- 'pending', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы для улучшения производительности
CREATE INDEX idx_accounts_client_id ON accounts(client_id);
CREATE INDEX idx_transactions_from_account ON transactions(from_account_id);
CREATE INDEX idx_transactions_to_account ON transactions(to_account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);

-- Начальные данные: клиенты
INSERT INTO clients (first_name, last_name, passport_number, phone_number, email)
VALUES 
    ('Иван', 'Иванов', '1234567890', '+79161234567', 'ivan@example.com'),
    ('Петр', 'Петров', '0987654321', '+79169876543', 'petr@example.com'),
    ('Сергей', 'Сергеев', '1122334455', '+79161122334', 'sergey@example.com');

-- Аккаунт администратора
INSERT INTO auth (login, password_hash, role, client_id)
VALUES ('admin@example.com', '$2b$12$URVZhrVpkt0GKo.WYigMoePvaXUiIxkQZBqo2NLW44c6.dv0wlVz6', 'admin', NULL);

-- Аккаунты пользователей
INSERT INTO auth (login, password_hash, role, client_id)
SELECT c.email, '$2b$12$URVZhrVpkt0GKo.WYigMoePvaXUiIxkQZBqo2NLW44c6.dv0wlVz6', 'user', c.id
FROM clients c;

-- Начальные данные: счета
INSERT INTO accounts (client_id, account_number, account_type, balance, currency)
VALUES 
    (1, '40817810000000000001', 'checking', 150000.00, 'RUB'),
    (1, '40817810000000000002', 'savings', 500000.00, 'RUB'),
    (2, '40817810000000000003', 'checking', 75000.50, 'RUB'),
    (3, '40817810000000000004', 'credit', -30000.00, 'RUB');

-- Начальные данные: транзакции
INSERT INTO transactions (from_account_id, to_account_id, amount, transaction_type, description)
VALUES 
    (NULL, 1, 200000.00, 'deposit', 'Первоначальный взнос'),
    (1, 2, 50000.00, 'transfer', 'Перевод на сберегательный счет'),
    (1, 3, 10000.00, 'transfer', 'Оплата услуг'),
    (3, 4, 5000.00, 'transfer', 'Кредитный платеж');