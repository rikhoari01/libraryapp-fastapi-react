from config.database import get_db_connection
from typing import List, Optional, Dict, Any
import sqlite3

class MemberModel:

    @staticmethod
    def create(id_card_number: str, name: str, email: str) -> Optional[Dict[str, Any]]:
        """Create a new member"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO members (id_card_number, name, email) VALUES (?, ?, ?)",
                    (id_card_number, name, email)
                )
                member_id = cursor.lastrowid
                conn.commit()

                # Return the created member
                return MemberModel.get_by_id(member_id)
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all members with pagination"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members LIMIT ? OFFSET ?", (limit, skip))
            members = cursor.fetchall()
            return [dict(member) for member in members]

    @staticmethod
    def get_by_id(member_id: int) -> Optional[Dict[str, Any]]:
        """Get member by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
            member = cursor.fetchone()
            return dict(member) if member else None

    @staticmethod
    def get_by_id_card(id_card_number: str) -> Optional[Dict[str, Any]]:
        """Get member by ID card number"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE id_card_number = ?", (id_card_number,))
            member = cursor.fetchone()
            return dict(member) if member else None

    @staticmethod
    def get_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Get member by email"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE email = ?", (email,))
            member = cursor.fetchone()
            return dict(member) if member else None

    @staticmethod
    def update(member_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update member information"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # Check if member exists
                if not MemberModel.get_by_id(member_id):
                    return None

                # Build update query
                update_fields = []
                values = []

                for field in ['id_card_number', 'name', 'email']:
                    if field in kwargs and kwargs[field] is not None:
                        update_fields.append(f"{field} = ?")
                        values.append(kwargs[field])

                if not update_fields:
                    return MemberModel.get_by_id(member_id)

                update_fields.append("updated_at = datetime('now')")
                values.append(member_id)

                query = f"UPDATE members SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()

                return MemberModel.get_by_id(member_id)
        except sqlite3.IntegrityError:
            return None

    @staticmethod
    def delete(member_id: int) -> bool:
        """Delete a member"""
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if member exists
            if not MemberModel.get_by_id(member_id):
                return False

            cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def has_active_loan(member_id: int) -> bool:
        """Check if member has an active loan"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM loans WHERE member_id = ? AND status = 'ACTIVE'",
                (member_id,)
            )
            return cursor.fetchone()[0] > 0

    @staticmethod
    def get_loan_history(member_id: int) -> List[Dict[str, Any]]:
        """Get member's loan history"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.*, b.title as book_title, b.isbn as book_isbn
                FROM loans l
                JOIN books b ON l.book_id = b.id
                WHERE l.member_id = ?
                ORDER BY l.created_at DESC
            """, (member_id,))
            loans = cursor.fetchall()
            return [dict(loan) for loan in loans]