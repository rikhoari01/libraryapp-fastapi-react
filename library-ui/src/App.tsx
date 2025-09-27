import React, { useState, useEffect } from 'react';
import {BookOpen, Users, Calendar, AlertCircle, Clock, Plus, RefreshCw, PencilIcon, TrashIcon} from 'lucide-react';

interface Book {
    id: number;
    title: string;
    isbn: string;
    stock: number;
}

interface Member {
    id: number;
    id_card_number: string;
    name: string;
    email: string;
}

interface Loan {
    id: number;
    member_name: string;
    member_email: string;
    member_id_card: string;
    book_title: string;
    book_isbn: string;
    loan_date: string;
    return_deadline: string;
    actual_return_date: string|null
    status: string;
    return_status: string|null;
    days_difference: number|null;
}

interface ApiConfig {
    baseUrl: string;
    username: string;
    password: string;
}

interface BookForm {
    id: number|null;
    title: string;
    isbn: string;
    stock: number;
}

interface MemberForm {
    id: number|null;
    idCardNumber: string;
    name: string;
    email: string;
}

interface LoanForm {
    memberId: number|null;
    bookId: number|null;
    returnDeadline: string;
}

const LibraryManagementUI: React.FC = () => {
    const [books, setBooks] = useState<Book[]>([]);
    const [members, setMembers] = useState<Member[]>([]);
    const [loans, setLoans] = useState<Loan[]>([]);
    const [activeTab, setActiveTab] = useState<'books' | 'members' | 'loans' | 'admin'>('books');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [isEditBook, setIsEditBook] = useState<boolean>(false);
    const [isEditMember, setIsEditMember] = useState<boolean>(false);

    // API Configuration from environment variables
    const apiConfig: ApiConfig = {
        baseUrl: import.meta.env.VITE_APP_API_BASE_URL || 'http://localhost:3001/api',
        username: import.meta.env.VITE_APP_API_USERNAME || 'admin',
        password: import.meta.env.VITE_APP_API_PASSWORD || 'password'
    };

    // Book form state
    const [bookForm, setBookForm] = useState<BookForm>({ id: null, title: '', isbn: '', stock: 0 });

    // Member form state
    const [memberForm, setMemberForm] = useState<MemberForm>({ id: null, idCardNumber: '', name: '', email: '' });

    // Loan form state
    const [loanForm, setLoanForm] = useState<LoanForm>({ memberId: null, bookId: null, returnDeadline: '' });

    // Create authorization header for basic auth
    const getAuthHeaders = () => {
        const credentials = btoa(`${apiConfig.username}:${apiConfig.password}`);
        return {
            'Authorization': `Basic ${credentials}`,
            'Content-Type': 'application/json'
        };
    };

    // Generic API call function
    const apiCall = async (endpoint: string, method: string = 'GET', data?: any) => {
        setError(null);
        try {
            const response = await fetch(`${apiConfig.baseUrl}${endpoint}`, {
                method,
                headers: getAuthHeaders(),
                body: data ? JSON.stringify(data) : undefined
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status} ${response.statusText}`);
            }

            return await response.json();
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
            setError(errorMessage);
            throw err;
        }
    };

    // Fetch all data
    const fetchAllData = async () => {
        setLoading(true);
        try {
            const [booksData, membersData, loansData] = await Promise.all([
                apiCall('/books'),
                apiCall('/members'),
                apiCall('/loans')
            ]);

            setBooks(booksData.data ? booksData.data : []);
            setMembers(membersData.data ? membersData.data : []);
            setLoans(loansData.data ? loansData.data : []);
        } catch (err) {
            console.error('Error fetching data:', err);
        } finally {
            setLoading(false);
        }
    };

    // Initialize data on component mount
    useEffect(() => {
        fetchAllData();
    }, []);

    const addBook = async () => {
        if (!bookForm.title || !bookForm.isbn) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            setLoading(true);
            const newBook = await apiCall('/books', 'POST', bookForm);
            setBooks([...books, newBook.data]);
            setBookForm({ id: null, title: '', isbn: '', stock: 0 });
        } catch (err) {
            console.error('Error adding book:', err);
        } finally {
            setLoading(false);
        }
    };

    const setEditBook = async (book: Book) => {
        const checkBook = books.find(book => book.id === book.id);
        if (!checkBook) {
            alert('Book does not exist');
            return;
        }

        setBookForm({ id: book.id, isbn: book.isbn, title: book.title, stock: book.stock });
        setIsEditBook(true);
    }

    const editBook = async () => {
        if (!bookForm.title || !bookForm.isbn) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            setLoading(true);
            await apiCall(`/books/${bookForm.id}`, 'PUT', bookForm);

            // Refresh data to get updated status
            await fetchAllData();

            setBookForm({ id: null, title: '', isbn: '', stock: 0 });
        } catch (err) {
            console.error('Error editing book:', err);
        } finally {
            setLoading(false);
            setIsEditBook(false);
        }
    }

    const deleteBook = async (book: Book) => {
        const isBorrowed = loans.find(loan => loan.book_isbn === book.isbn);
        if (isBorrowed) {
            alert('Book is being borrowed, cannot delete book');
            return;
        }

        const confirmed = confirm('Are you sure you want to delete this book?');
        if (!confirmed) return;

        try {
            setLoading(true);
            await apiCall(`/books/${book.id}`, 'DELETE');

            // Refresh data to get updated status
            await fetchAllData();
        } catch (err) {
            console.error('Error deleting book:', err);
        } finally {
            setLoading(false);
        }
    }

    const addMember = async () => {
        if (!memberForm.idCardNumber || !memberForm.name || !memberForm.email) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            setLoading(true);
            const newMember = await apiCall('/members', 'POST', memberForm);
            setMembers([...members, newMember.data]);
            setMemberForm({ id: null, idCardNumber: '', name: '', email: '' });
        } catch (err) {
            console.error('Error adding member:', err);
        } finally {
            setLoading(false);
        }
    };

    const setEditMember = async (member: Member) => {
        const checkMember = members.find(member => member.id === member.id);
        if (!checkMember) {
            alert('Book does not exist');
            return;
        }

        setMemberForm({ id: member.id, idCardNumber: member.id_card_number, name: member.name, email: member.email });
        setIsEditMember(true);
    }

    const editMember = async () => {
        if (!memberForm.idCardNumber || !memberForm.name || !memberForm.email) {
            alert('Please fill in all required fields');
            return;
        }

        try {
            setLoading(true);
            await apiCall(`/members/${memberForm.id}`, 'PUT', memberForm);

            // Refresh data to get updated status
            await fetchAllData();

            setMemberForm({ id: null, idCardNumber: '', name: '', email: '' });
        } catch (err) {
            console.error('Error editing book:', err);
        } finally {
            setLoading(false);
            setIsEditMember(false)
        }
    }

    const deleteMember = async (member: Member) => {
        const hasActiveLoan = loans.some(l => l.member_id_card == member.id_card_number && l.status === 'ACTIVE');
        if (hasActiveLoan) {
            alert('Member has active loan, cannot delete member')
            return
        }

        const confirmed = confirm('Are you sure you want to delete this member?');
        if (!confirmed) return;

        try {
            setLoading(true);
            await apiCall(`/members/${member.id}`, 'DELETE');

            // Refresh data to get updated status
            await fetchAllData();
        } catch (err) {
            console.error('Error deleting book:', err);
        } finally {
            setLoading(false);
            setIsEditMember(false);
        }
    }

    const borrowBook = async () => {
        const member = members.find(b => b.id == loanForm.memberId);
        const book = books.find(b => b.id == loanForm.bookId);
        if (!member || !book) {
            alert('Invalid member or book selection');
            return;
        }

        const hasActiveLoan = loans.some(l => l.member_id_card == member.id_card_number && l.status === 'ACTIVE');
        if (hasActiveLoan) {
            alert('Member already has an active loan');
            return;
        }

        if (book && book.stock <= 0) {
            alert('Book is not available (no stock)');
            return;
        }

        const today = new Date();
        const deadline = new Date(loanForm.returnDeadline);
        const daysDiff = Math.ceil((deadline.getTime() - today.getTime()) / (1000 * 3600 * 24));

        if (daysDiff > 30) {
            alert('Loan duration cannot exceed 30 days');
            return;
        }

        if (daysDiff <= 0) {
            alert('Return deadline must be in the future');
            return;
        }

        try {
            setLoading(true);
            const loanData = {
                member_id: loanForm.memberId,
                book_id: loanForm.bookId,
                return_deadline: loanForm.returnDeadline
            };

            await apiCall('/loans', 'POST', loanData);

            // Refresh data to get updated stock and loans
            await fetchAllData();

            setLoanForm({ memberId: null, bookId: null, returnDeadline: '' });
            alert('Book borrowed successfully!');
        } catch (err) {
            console.error('Error borrowing book:', err);
        } finally {
            setLoading(false);
        }
    };

    const returnBook = async (loanId: string) => {
        try {
            setLoading(true);
            await apiCall(`/loans/${loanId}/return`, 'PUT');

            // Refresh data to get updated status
            await fetchAllData();

            alert('Book returned successfully!');
        } catch (err) {
            console.error('Error returning book:', err);
        } finally {
            setLoading(false);
        }
    };

    const isOverdue = (loan: Loan) => {
        if (loan.status !== 'ACTIVE') return false;
        return new Date() > new Date(loan.return_deadline);
    };

    return (
        <div className="min-h-screen bg-gray-50 p-4">
            <div className="max-w-6xl mx-auto">
                <div className="flex items-center justify-between mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">Library Management System</h1>
                    <div className="flex items-center space-x-4">
                        {error && (
                            <div className="bg-red-100 text-red-700 px-4 py-2 rounded-md text-sm">
                                {error}
                            </div>
                        )}
                        <button
                            onClick={fetchAllData}
                            disabled={loading}
                            className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
                        >
                            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                            <span>Refresh</span>
                        </button>
                    </div>
                </div>

                {/* Tab Navigation */}
                <div className="flex space-x-1 mb-8 bg-gray-200 p-1 rounded-lg">
                    {[
                        { key: 'books', label: 'Books', icon: BookOpen },
                        { key: 'members', label: 'Members', icon: Users },
                        { key: 'loans', label: 'Borrow/Return', icon: Calendar },
                        { key: 'admin', label: 'Admin Dashboard', icon: AlertCircle }
                    ].map(({ key, label, icon: Icon }) => (
                        <button
                            key={key}
                            onClick={() => setActiveTab(key as any)}
                            className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                                activeTab === key
                                    ? 'bg-white text-blue-600 shadow'
                                    : 'text-gray-600 hover:text-gray-900'
                            }`}
                        >
                            <Icon size={16} />
                            <span>{label}</span>
                        </button>
                    ))}
                </div>

                {/* Books Tab */}
                {activeTab === 'books' && (
                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h2 className="text-xl font-semibold mb-4">Add New Book</h2>
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                                <input
                                    type="text"
                                    placeholder="Book Title"
                                    value={bookForm.title}
                                    onChange={(e) => setBookForm({...bookForm, title: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                />
                                <input
                                    type="text"
                                    placeholder="ISBN"
                                    value={bookForm.isbn}
                                    onChange={(e) => setBookForm({...bookForm, isbn: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                />
                                <input
                                    type="number"
                                    placeholder="Stock"
                                    value={bookForm.stock}
                                    onChange={(e) => setBookForm({...bookForm, stock: parseInt(e.target.value) || 0})}
                                    className="border rounded-md px-3 py-2"
                                />
                                {!isEditBook ?
                                    <button
                                        onClick={addBook}
                                        disabled={loading}
                                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center space-x-2"
                                    >
                                        <Plus size={16} />
                                        <span>Add Book</span>
                                    </button>
                                    :
                                    <button
                                        onClick={editBook}
                                        disabled={loading}
                                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center space-x-2"
                                    >
                                        <Plus size={16} />
                                        <span>Edit Book</span>
                                    </button>
                                }
                            </div>
                        </div>

                        <div className="bg-white rounded-lg shadow">
                            <div className="p-6 border-b">
                                <h2 className="text-xl font-semibold">Book Inventory</h2>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ISBN</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Stock</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                                    </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-200">
                                    {books?.map(book => (
                                        <tr key={book.isbn}>
                                            <td className="px-6 py-4 whitespace-nowrap font-medium">{book.title}</td>
                                            <td className="px-6 py-4 whitespace-nowrap text-gray-600">{book.isbn}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{book.stock}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                              <span className={`px-2 py-1 rounded-full text-xs ${
                                                  book.stock > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                              }`}>
                                                {book.stock > 0 ? 'Available' : 'Out of Stock'}
                                              </span>
                                            </td>
                                            <td className="px-6 py-4 flex gap-2">
                                                <button
                                                    onClick={() => setEditBook(book)}
                                                    className="flex items-center space-x-2 p-3 rounded-md bg-amber-300 "
                                                >
                                                    <PencilIcon className="w-5" />
                                                </button>
                                                <button
                                                    onClick={() => deleteBook(book)}
                                                    className="flex items-center space-x-2 p-3 rounded-md bg-red-500 text-white"
                                                >
                                                    <TrashIcon className="w-5" />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {/* Members Tab */}
                {activeTab === 'members' && (
                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h2 className="text-xl font-semibold mb-4">Add New Member</h2>
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                                <input
                                    type="text"
                                    placeholder="ID Card Number"
                                    value={memberForm.idCardNumber}
                                    onChange={(e) => setMemberForm({...memberForm, idCardNumber: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                />
                                <input
                                    type="text"
                                    placeholder="Full Name"
                                    value={memberForm.name}
                                    onChange={(e) => setMemberForm({...memberForm, name: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                />
                                <input
                                    type="email"
                                    placeholder="Email"
                                    value={memberForm.email}
                                    onChange={(e) => setMemberForm({...memberForm, email: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                />
                                {!isEditMember ?
                                    <button
                                        onClick={addMember}
                                        disabled={loading}
                                        className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center justify-center space-x-2"
                                    >
                                        <Plus size={16} />
                                        <span>Add Member</span>
                                    </button>
                                    :
                                    <button
                                        onClick={editMember}
                                        disabled={loading}
                                        className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center justify-center space-x-2"
                                    >
                                        <Plus size={16} />
                                        <span>Edit Member</span>
                                    </button>
                                }
                            </div>
                        </div>

                        <div className="bg-white rounded-lg shadow">
                            <div className="p-6 border-b">
                                <h2 className="text-xl font-semibold">Registered Members</h2>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID Card</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                                    </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-200">
                                    {members?.map(member => {
                                        const hasActiveLoan = loans.some(l => l.member_id_card === member.id_card_number && l.status === 'ACTIVE');
                                        return (
                                            <tr key={member.id}>
                                                <td className="px-6 py-4 whitespace-nowrap font-medium">{member.id_card_number}</td>
                                                <td className="px-6 py-4 whitespace-nowrap">{member.name}</td>
                                                <td className="px-6 py-4 whitespace-nowrap text-gray-600">{member.email}</td>
                                                <td className="px-6 py-4 whitespace-nowrap">
                                                    <span className={`px-2 py-1 rounded-full text-xs ${
                                                        hasActiveLoan ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
                                                    }`}>
                                                      {hasActiveLoan ? 'Has Active Loan' : 'Available'}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 flex gap-2">
                                                    <button
                                                        onClick={() => setEditMember(member)}
                                                        className="flex items-center space-x-2 p-3 rounded-md bg-amber-300 "
                                                    >
                                                        <PencilIcon className="w-5" />
                                                    </button>
                                                    <button
                                                        onClick={() => deleteMember(member)}
                                                        className="flex items-center space-x-2 p-3 rounded-md bg-red-500 text-white"
                                                    >
                                                        <TrashIcon className="w-5" />
                                                    </button>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {/* Loans Tab */}
                {activeTab === 'loans' && (
                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-lg shadow">
                            <h2 className="text-xl font-semibold mb-4">Borrow Book</h2>
                            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                                <select
                                    value={loanForm.memberId}
                                    onChange={(e) => setLoanForm({...loanForm, memberId: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                >
                                    <option value="">Select Member</option>
                                    {members?.map(member => (
                                        <option key={member.id} value={member.id}>
                                            {member.name} ({member.id_card_number})
                                        </option>
                                    ))}
                                </select>
                                <select
                                    value={loanForm.bookId}
                                    onChange={(e) => setLoanForm({...loanForm, bookId: e.target.value})}
                                    className="border rounded-md px-3 py-2"
                                >
                                    <option value="">Select Book</option>
                                    {books?.filter(book => book.stock > 0).map(book => (
                                        <option key={book.id} value={book.id}>
                                            {book.title} (Stock: {book.stock})
                                        </option>
                                    ))}
                                </select>
                                <input
                                    type="date"
                                    value={loanForm.returnDeadline}
                                    onChange={(e) => setLoanForm({...loanForm, returnDeadline: e.target.value})}
                                    min={new Date().toISOString().split('T')[0]}
                                    max={new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]}
                                    className="border rounded-md px-3 py-2"
                                />
                                <button
                                    onClick={borrowBook}
                                    disabled={loading}
                                    className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50"
                                >
                                    Borrow Book
                                </button>
                            </div>
                            <div className="mt-2 text-sm text-gray-600">
                                <p>• Maximum loan duration: 30 days</p>
                                <p>• One book per loan</p>
                                <p>• No concurrent loans allowed</p>
                            </div>
                        </div>

                        <div className="bg-white rounded-lg shadow">
                            <div className="p-6 border-b">
                                <h2 className="text-xl font-semibold">Active Loans</h2>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Member ID</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Member Name</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Book ISBN</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Book Title</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Borrow Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                                    </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-200">
                                    {loans.filter(loan => loan.status === 'ACTIVE').map(loan => (
                                        <tr key={loan.id}>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.member_id_card}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.member_name}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.book_isbn}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.book_title}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.loan_date}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.return_deadline}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                              <span className={`px-2 py-1 rounded-full text-xs ${
                                                  isOverdue(loan) ? 'bg-red-100 text-red-800' : 'bg-blue-100 text-blue-800'
                                              }`}>
                                                {isOverdue(loan) ? 'Overdue' : 'Active'}
                                              </span>
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                <button
                                                    onClick={() => returnBook(loan.id)}
                                                    disabled={loading}
                                                    className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 disabled:opacity-50"
                                                >
                                                    Return Book
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}

                {/* Admin Dashboard Tab */}
                {activeTab === 'admin' && (
                    <div className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            <div className="bg-white p-6 rounded-lg shadow">
                                <div className="flex items-center">
                                    <BookOpen className="h-8 w-8 text-blue-600" />
                                    <div className="ml-4">
                                        <p className="text-sm font-medium text-gray-500">Total Books</p>
                                        <p className="text-2xl font-semibold text-gray-900">{books.length}</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-white p-6 rounded-lg shadow">
                                <div className="flex items-center">
                                    <Users className="h-8 w-8 text-green-600" />
                                    <div className="ml-4">
                                        <p className="text-sm font-medium text-gray-500">Active Members</p>
                                        <p className="text-2xl font-semibold text-gray-900">{members.length}</p>
                                    </div>
                                </div>
                            </div>
                            <div className="bg-white p-6 rounded-lg shadow">
                                <div className="flex items-center">
                                    <Clock className="h-8 w-8 text-yellow-600" />
                                    <div className="ml-4">
                                        <p className="text-sm font-medium text-gray-500">Active Loans</p>
                                        <p className="text-2xl font-semibold text-gray-900">
                                            {loans.filter(l => l.status === 'ACTIVE').length}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="bg-white rounded-lg shadow">
                            <div className="p-6 border-b">
                                <h2 className="text-xl font-semibold">Loan History & Tracking</h2>
                            </div>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Member ID</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Member</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ISBN</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Book</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Borrow Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Due Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Return Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                    </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-200">
                                    {loans.map(loan => (
                                        <tr key={loan.id}>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.member_id_card}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.member_name}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.book_isbn}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.book_title}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.loan_date}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.return_deadline}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{loan.actual_return_date || '-'}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                              <span className={`px-2 py-1 rounded-full text-xs ${
                                                  loan.status === 'RETURNED'
                                                      ? (loan.actual_return_date && new Date(loan.actual_return_date) > new Date(loan.return_deadline)
                                                          ? 'bg-orange-100 text-orange-800'
                                                          : 'bg-green-100 text-green-800')
                                                      : isOverdue(loan)
                                                          ? 'bg-red-100 text-red-800'
                                                          : 'bg-blue-100 text-blue-800'
                                              }`}>
                                                {loan.status === 'RETURNED'
                                                    ? loan.return_status
                                                    : isOverdue(loan)
                                                        ? 'Overdue'
                                                        : 'Active'
                                                }
                                              </span>
                                            </td>
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default LibraryManagementUI;