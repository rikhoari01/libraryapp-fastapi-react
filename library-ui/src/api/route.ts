const API_URL = "http://localhost:3001/api/v1"; // adjust if needed

// BOOKS
export const addBook = async (book: { title: string; isbn: string; stock: number }) =>
    fetch(`${API_URL}/books`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(book) }).then(r => r.json());

export const getAllBooks = async () =>
    fetch(`${API_URL}/books`).then(r => r.json());

export const getBookById = async (id: number) =>
    fetch(`${API_URL}/books/${id}`).then(r => r.json());

export const getBookByIsbn = async (isbn: string) =>
    fetch(`${API_URL}/books/isbn/${isbn}`).then(r => r.json());

export const deleteBook = async (id: number) =>
    fetch(`${API_URL}/books/${id}`, { method: "DELETE" }).then(r => r.json());

// MEMBERS
export const addMember = async (member: { name: string; id_card: string; email: string }) =>
    fetch(`${API_URL}/members`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(member) }).then(r => r.json());

export const getAllMembers = async () =>
    fetch(`${API_URL}/members`).then(r => r.json());

export const getMemberById = async (id: number) =>
    fetch(`${API_URL}/members/${id}`).then(r => r.json());

export const getMemberByCard = async (id_card: string) =>
    fetch(`${API_URL}/members/idcard/${id_card}`).then(r => r.json());

// LOANS
export const addLoan = async (data: { member_id: number; book_id: number }) =>
    fetch(`${API_URL}/loans`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) }).then(r => r.json());

export const returnLoan = async (loanId: number) =>
    fetch(`${API_URL}/loans/${loanId}/return`, { method: "PUT" }).then(r => r.json());

export const trackLoan = async (loanId: number) =>
    fetch(`${API_URL}/loans/${loanId}`).then(r => r.json());
