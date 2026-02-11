/**
 * QueryHistory Component - Sidebar with query history
 */

import React, { useState, useEffect } from 'react';
import { QueryHistoryEntry } from '../types';
import { useDatabase } from '../hooks/useDatabase';
import { getQueryTypeColor, truncate } from '../utils/helpers';

interface Props {
  onQuerySelect?: (query: string) => void;
}

export const QueryHistory: React.FC<Props> = ({ onQuerySelect }) => {
  const { state, getQueryHistory, clearHistory } = useDatabase();
  const [isOpen, setIsOpen] = useState(true);

  useEffect(() => {
    getQueryHistory();
  }, [getQueryHistory]);

  const handleClear = async () => {
    if (window.confirm('Are you sure you want to clear all query history?')) {
      await clearHistory();
    }
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="w-64 bg-white border-l border-gray-200 flex flex-col">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <h3 className="font-bold text-gray-800">Query History</h3>
        <button
          onClick={() => setIsOpen(false)}
          className="text-gray-500 hover:text-gray-700 text-lg"
        >
          ×
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {state.queryHistory.length === 0 ? (
          <div className="p-4 text-gray-500 text-sm text-center">No queries yet</div>
        ) : (
          <div className="divide-y divide-gray-200">
            {state.queryHistory.map((entry, idx) => (
              <button
                key={idx}
                onClick={() => onQuerySelect?.(entry.query)}
                className="w-full text-left p-3 hover:bg-gray-50 transition"
              >
                <div className="flex items-center gap-2 mb-2">
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${getQueryTypeColor(
                      entry.query_type
                    )}`}
                  >
                    {entry.query_type}
                  </span>
                  {entry.success ? (
                    <span className="text-xs text-green-600">✓</span>
                  ) : (
                    <span className="text-xs text-red-600">✗</span>
                  )}
                </div>
                <p className="text-xs text-gray-600 font-mono mb-1">
                  {truncate(entry.query, 40)}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{entry.execution_time_ms}ms</span>
                  <span>{new Date(entry.timestamp).toLocaleTimeString()}</span>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-200 space-y-2">
        <button
          onClick={handleClear}
          disabled={state.queryHistory.length === 0}
          className="w-full px-3 py-2 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md border border-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Clear History
        </button>
      </div>
    </div>
  );
};
