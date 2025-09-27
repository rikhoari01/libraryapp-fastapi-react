import type {JSX} from "react";

interface TableProps {
    headers: string[];
    rows: (string | number | JSX.Element)[][];
}

export default function Table({ headers, rows }: TableProps) {
    return (
        <table className="w-full border border-gray-300 rounded mt-3">
            <thead>
            <tr className="bg-gray-100">
                {headers.map((h, i) => (
                    <th key={i} className="p-2 border">{h}</th>
                ))}
            </tr>
            </thead>
            <tbody>
            {rows.map((row, i) => (
                <tr key={i} className="odd:bg-white even:bg-gray-50">
                    {row.map((cell, j) => (
                        <td key={j} className="p-2 border text-center">{cell}</td>
                    ))}
                </tr>
            ))}
            </tbody>
        </table>
    );
}
