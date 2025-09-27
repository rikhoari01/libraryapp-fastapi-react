from config.database import get_db_connection
from typing import List, Optional, Dict, Any
from datetime import date
import sqlite3

class LoanModel:

    @staticmethod
    def create(member_id: int, book_id: int, return_deadline: str) -> Optional[Dict[str, Any]]:
        """Create a new loan"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO loans (member_id, book_id, return_deadline) VALUES (?, ?, ?)",
                    (member_id, book_id, return_deadline)
                )
                loan_id = cursor.lastrowid
                conn.commit()

                return LoanModel.get_by_id(loan_id)
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all loans with pagination and optional status filter"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            if status:
                cursor.execute(
                    "SELECT * FROM loans WHERE status = ? LIMIT ? OFFSET ?",
                    (status.upper(), limit, skip)
                )
            else:
                cursor.execute("SELECT * FROM loans LIMIT ? OFFSET ?", (limit, skip))

            loans = cursor.fetchall()
            return [dict(loan) for loan in loans]

    @staticmethod
    def get_by_id(loan_id: int) -> Optional[Dict[str, Any]]:
        """Get loan by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
            loan = cursor.fetchone()
            return dict(loan) if loan else None

    @staticmethod
    def get_detailed_loans(skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get loans with detailed information including member and book details"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            base_query = """
            SELECT 
                l.id,
                m.id as member_id,
                m.name as member_name,
                m.id_card_number as member_id_card,
                bk.id as book_id,
                bk.title as book_title,
                bk.isbn as book_isbn,
                l.loan_date,
                l.return_deadline,
                l.actual_return_date,
                l.status,
                CASE 
                    WHEN l.status = 'RETURNED' AND l.actual_return_date <= l.return_deadline 
                    THEN 'ON_TIME'
                    WHEN l.status = 'RETURNED' AND l.actual_return_date > l.return_deadline 
                    THEN 'RETURNED_LATE'
                    WHEN l.status = 'ACTIVE' AND l.return_deadline >= date('now') 
                    THEN 'ACTIVE_ON_TIME'
                    WHEN l.status = 'ACTIVE' AND l.return_deadline < date('now') 
                    THEN 'OVERDUE'
                    ELSE 'UNKNOWN'
                END as return_status,
                CASE 
                    WHEN l.status = 'RETURNED' 
                    THEN CAST(julianday(l.actual_return_date) - julianday(l.return_deadline) AS INTEGER)
                    WHEN l.status = 'ACTIVE' 
                    THEN CAST(julianday(date('now')) - julianday(l.return_deadline) AS INTEGER)
                    ELSE NULL
                END as days_difference
            FROM loans l
            JOIN members m ON l.member_id = m.id
            JOIN books bk ON l.book_id = bk.id
            """

            if status:
                query = base_query + " WHERE l.status = ? ORDER BY l.created_at DESC LIMIT ? OFFSET ?"
                cursor.execute(query, (status.upper(), limit, skip))
            else:
                query = base_query + " ORDER BY l.created_at DESC LIMIT ? OFFSET ?"
                cursor.execute(query, (limit, skip))

            loans = cursor.fetchall()
            return [dict(loan) for loan in loans]

    @staticmethod
    def get_detailed_by_id(loan_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific loan"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                l.id,
                m.name as member_name,
                m.email as member_email,
                m.id_card_number as member_id_card,
                bk.title as book_title,
                bk.isbn as book_isbn,
                l.loan_date,
                l.return_deadline,
                l.actual_return_date,
                l.status,
                CASE 
                    WHEN l.status = 'RETURNED' AND l.actual_return_date <= l.return_deadline 
                    THEN 'ON_TIME'
                    WHEN l.status = 'RETURNED' AND l.actual_return_date > l.return_deadline 
                    THEN 'RETURNED_LATE'
                    WHEN l.status = 'ACTIVE' AND l.return_deadline >= date('now') 
                    THEN 'ACTIVE_ON_TIME'
                    WHEN l.status = 'ACTIVE' AND l.return_deadline < date('now') 
                    THEN 'OVERDUE'
                    ELSE 'UNKNOWN'
                END as return_status,
                CASE 
                    WHEN l.status = 'RETURNED' 
                    THEN CAST(julianday(l.actual_return_date) - julianday(l.return_deadline) AS INTEGER)
                    WHEN l.status = 'ACTIVE' 
                    THEN CAST(julianday(date('now')) - julianday(l.return_deadline) AS INTEGER)
                    ELSE NULL
                END as days_difference
            FROM loans l
            JOIN members m ON l.member_id = m.id
            JOIN books bk ON l.book_id = bk.id
            WHERE l.id = ?
            """, (loan_id,))

            loan = cursor.fetchone()
            return dict(loan) if loan else None

    @staticmethod
    def return_book(loan_id: int) -> Optional[Dict[str, Any]]:
        """Return a borrowed book"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if loan exists and is active
            loan = LoanModel.get_by_id(loan_id)
            if not loan or loan['status'] != 'ACTIVE':
                return None

            # Update loan status
            today = date.today().isoformat()
            cursor.execute(
                "UPDATE loans SET status = 'RETURNED', actual_return_date = ?, updated_at = datetime('now') WHERE id = ?",
                (today, loan_id)
            )
            conn.commit()

            return LoanModel.get_by_id(loan_id)

    @staticmethod
    def update_overdue_loans() -> int:
        """Update loan status to OVERDUE for loans past their deadline"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE loans SET status = 'OVERDUE', updated_at = datetime('now') WHERE status = 'ACTIVE' AND return_deadline < date('now')"
            )
            updated_count = cursor.rowcount
            conn.commit()
            return updated_count

    @staticmethod
    def get_active_loans() -> List[Dict[str, Any]]:
        """Get all active loans"""
        return LoanModel.get_all(status='ACTIVE', limit=1000)

    @staticmethod
    def get_overdue_loans() -> List[Dict[str, Any]]:
        """Get all overdue loans"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.*, m.name as member_name, bk.title as book_title
                FROM loans l
                JOIN members m ON l.member_id = m.id
                JOIN books bk ON l.book_id = bk.id
                WHERE l.status = 'ACTIVE' AND l.return_deadline < date('now')
            """)
            loans = cursor.fetchall()
            return [dict(loan) for loan in loans]

    @staticmethod
    def get_member_active_loan(member_id: int) -> Optional[Dict[str, Any]]:
        """Get member's active loan if any"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM loans WHERE member_id = ? AND status = 'ACTIVE'",
                (member_id,)
            )
            loan = cursor.fetchone()
            return dict(loan) if loan else None