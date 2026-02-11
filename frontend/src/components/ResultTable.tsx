/**
 * ResultTable Component - Paginated table display
 */

import React, { useState, useMemo } from 'react';

interface Props {
  data?: any[];
  isLoading?: boolean;
  error?: string;
  title?: string;
  rowsAffected?: number;
}

const ITEMS_PER_PAGE = 10;

export const ResultTable: React.FC<Props> = ({
  data = [],
  isLoading = false,
  error,
  title = 'Results',
  rowsAffected,
}) => {
  const [currentPage, setCurrentPage] = useState(1);

  const columns = useMemo(() => {
    if (!data || data.length === 0) return [];
    return Object.keys(data[0]);
  }, [data]);

  const paginatedData = useMemo(() => {
    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end = start + ITEMS_PER_PAGE;
    return data.slice(start, end);
  }, [data, currentPage]);

  const pageCount = Math.ceil(data.length / ITEMS_PER_PAGE);

  if (error) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">{title}</h3>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <div className="p-4 bg-red-50 border border-red-200 rounded-md max-w-md">
            <p className="text-red-700 text-sm font-medium">Error executing query</p>
            <p className="text-red-600 text-sm mt-1">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="h-full flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="text-gray-600 text-sm mt-2">Loading...</p>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">{title}</h3>
        </div>
        <div className="flex-1 flex items-center justify-center">
          <p className="text-gray-500">No results</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-bold text-gray-800">{title}</h3>
          <div className="text-sm text-gray-600">
            {rowsAffected !== undefined ? (
              <>
                <span className="font-medium">{rowsAffected}</span> rows affected
              </>
            ) : (
              <>
                <span className="font-medium">{data.length}</span> rows
              </>
            )}
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-x-auto">
        <table className="w-full border-collapse">
          <thead className="bg-gray-50 border-b border-gray-200 sticky top-0">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="px-4 py-3 text-left text-xs font-semibold text-gray-700"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {paginatedData.map((row, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                {columns.map((col) => (
                  <td key={`${idx}-${col}`} className="px-4 py-2 text-sm text-gray-700">
                    {row[col] === null ? (
                      <span className="text-gray-400 italic">NULL</span>
                    ) : typeof row[col] === 'object' ? (
                      <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                        {JSON.stringify(row[col])}
                      </code>
                    ) : (
                      String(row[col])
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {pageCount > 1 && (
        <div className="p-4 border-t border-gray-200 flex items-center justify-between">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <div className="text-sm text-gray-700">
            Page <span className="font-medium">{currentPage}</span> of{' '}
            <span className="font-medium">{pageCount}</span>
          </div>
          <button
            onClick={() => setCurrentPage((p) => Math.min(pageCount, p + 1))}
            disabled={currentPage === pageCount}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};
