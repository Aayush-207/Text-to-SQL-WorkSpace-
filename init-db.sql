"""Database initialization script for development."""
-- Create sample tables for testing

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    department VARCHAR(100),
    salary DECIMAL(10, 2),
    hire_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2),
    stock_quantity INTEGER,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items table (junction table)
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (username, email, first_name, last_name) VALUES
    ('john_doe', 'john@example.com', 'John', 'Doe'),
    ('jane_smith', 'jane@example.com', 'Jane', 'Smith'),
    ('bob_johnson', 'bob@example.com', 'Bob', 'Johnson'),
    ('alice_williams', 'alice@example.com', 'Alice', 'Williams'),
    ('charlie_brown', 'charlie@example.com', 'Charlie', 'Brown');

INSERT INTO employees (user_id, department, salary, hire_date, is_active) VALUES
    (1, 'Engineering', 80000.00, '2022-01-15', true),
    (2, 'Marketing', 70000.00, '2022-03-20', true),
    (3, 'Sales', 75000.00, '2021-06-10', true),
    (4, 'Engineering', 85000.00, '2023-02-01', true),
    (5, 'HR', 65000.00, '2020-11-30', true);

INSERT INTO products (name, description, price, stock_quantity, category) VALUES
    ('Laptop', 'High-performance laptop', 1299.99, 50, 'Electronics'),
    ('Mouse', 'Wireless mouse', 29.99, 200, 'Accessories'),
    ('Keyboard', 'Mechanical keyboard', 99.99, 150, 'Accessories'),
    ('Monitor', '4K Monitor', 399.99, 80, 'Electronics'),
    ('USB Cable', 'USB-C cable', 9.99, 500, 'Accessories');

INSERT INTO orders (user_id, order_date, total_amount, status) VALUES
    (1, '2024-01-10', 1329.98, 'completed'),
    (2, '2024-01-15', 99.99, 'completed'),
    (1, '2024-02-01', 2129.97, 'pending'),
    (3, '2024-02-05', 429.98, 'completed'),
    (4, '2024-02-10', 509.97, 'shipped');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 1299.99),
    (1, 2, 1, 29.99),
    (2, 3, 1, 99.99),
    (3, 1, 1, 1299.99),
    (3, 4, 1, 399.99),
    (3, 2, 1, 29.99),
    (4, 4, 1, 399.99),
    (4, 5, 3, 9.99),
    (5, 1, 1, 1299.99),
    (5, 3, 1, 99.99),
    (5, 5, 1, 9.99);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_employees_user_id ON employees(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
