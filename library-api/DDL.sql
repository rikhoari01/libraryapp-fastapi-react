DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS books;

-- Create Books table
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    isbn TEXT NOT NULL UNIQUE,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    CHECK (stock >= 0),
    CHECK (length(isbn) >= 10)
);

    -- Create Member table
CREATE TABLE members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_card_number TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    CHECK (email LIKE '%_@_%.__%'),
    CHECK (length(trim(name)) > 0),
    CHECK (length(trim(id_card_number)) > 0)
);

-- Create Loans table
CREATE TABLE loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL DEFAULT (date('now')),
    return_deadline TEXT NOT NULL,
    actual_return_date TEXT NULL,
    status TEXT NOT NULL DEFAULT 'ACTIVE',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,

    CHECK (status IN ('ACTIVE', 'RETURNED', 'OVERDUE')),
    CHECK (return_deadline >= loan_date),
    CHECK (julianday(return_deadline) <= julianday(loan_date) + 30),
    CHECK (actual_return_date IS NULL OR actual_return_date >= loan_date),
    CHECK (
        (status = 'RETURNED' AND actual_return_date IS NOT NULL) OR
        (status != 'RETURNED' AND actual_return_date IS NULL)
    )
);

-- Create indexes
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_members_id_card ON members(id_card_number);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_loans_member_id ON loans(member_id);
CREATE INDEX idx_loans_book_id ON loans(book_id);
CREATE INDEX idx_loans_status ON loans(status);
CREATE INDEX idx_loans_return_deadline ON loans(return_deadline);

-- Unique constraint for one active loan per member
CREATE UNIQUE INDEX idx_one_active_loan_per_member ON loans(member_id) WHERE status = 'ACTIVE';