/**
 * QueryEditor Component - SQL editor with syntax highlighting
 */

import React, { useState } from 'react';
import { QueryType } from '../types';

interface Props {
  sql: string;
  onChange?: (sql: string) => void;
  queryType?: QueryType;
  onExecute?: (sql: string) => void;
  onPreview?: (sql: string) => void;
  isLoading?: boolean;
}

export const QueryEditor: React.FC<Props> = ({
  sql,
  onChange,
  queryType,
  onExecute,
  onPreview,
  isLoading = false,
}) => {
  const [lineNumbers, setLineNumbers] = useState<number[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    onChange?.(value);

    // Update line numbers
    const lines = value.split('\n').length;
    setLineNumbers(Array.from({ length: lines }, (_, i) => i + 1));
  };

  const getQueryTypeColor = (type?: QueryType): string => {
    if (!type) return 'bg-gray-100 text-gray-800';
    const colors: Record<QueryType, string> = {
      SELECT: 'bg-blue-100 text-blue-800',
      INSERT: 'bg-green-100 text-green-800',
      UPDATE: 'bg-yellow-100 text-yellow-800',
      DELETE: 'bg-red-100 text-red-800',
      ALTER: 'bg-purple-100 text-purple-800',
    };
    return colors[type];
  };

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h3 className="text-lg font-bold text-gray-800">SQL Query</h3>
          {queryType && (
            <span className={`px-3 py-1 rounded text-sm font-medium ${getQueryTypeColor(queryType)}`}>
              {queryType}
            </span>
          )}
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Line numbers */}
        <div className="bg-gray-50 border-r border-gray-200 px-3 py-4 text-right text-xs text-gray-500 font-mono select-none">
          {lineNumbers.length === 0 ? (
            <div>1</div>
          ) : (
            lineNumbers.map((num) => <div key={num}>{num}</div>)
          )}
        </div>

        {/* Editor */}
        <textarea
          value={sql}
          onChange={handleChange}
          placeholder="Write SQL here or use natural language on the left..."
          className="flex-1 px-4 py-4 border-0 focus:outline-none focus:ring-0 font-mono text-sm resize-none"
          spellCheck="false"
        />
      </div>

      <div className="p-4 border-t border-gray-200 flex gap-2">
        <button
          onClick={() => onPreview?.(sql)}
          disabled={isLoading || !sql.trim()}
          className="flex-1 px-4 py-2 bg-gray-600 text-white font-medium rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Preview
        </button>
        <button
          onClick={() => onExecute?.(sql)}
          disabled={isLoading || !sql.trim()}
          className="flex-1 px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Execute
        </button>
      </div>
    </div>
  );
};
