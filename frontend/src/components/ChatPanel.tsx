/**
 * ChatPanel Component - Natural language input for SQL generation
 */

import React, { useState } from 'react';
import { useDatabase } from '../hooks/useDatabase';
import { GeneratedSQL } from '../types';

interface Props {
  onSQLGenerated?: (sql: GeneratedSQL) => void;
}

export const ChatPanel: React.FC<Props> = ({ onSQLGenerated }) => {
  const { state, generateSQL } = useDatabase();
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([
    'Show me all users',
    'Count orders by customer',
    'Find products under $50',
    'List employees and their departments',
    'Get sales by region',
  ]);

  const handleSubmit = async (e: React.FormEvent, query: string = input) => {
    e.preventDefault();
    if (!query.trim()) return;

    const sql = await generateSQL(query, 'public');
    if (sql) {
      onSQLGenerated?.(sql);
      setInput('');
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-bold text-gray-800 mb-3">Natural Language Query</h3>
        <p className="text-sm text-gray-600 mb-4">
          Describe what data you want to see, and we'll generate the SQL for you.
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        <p className="text-xs font-semibold text-gray-600 uppercase mb-3">Try:</p>
        {suggestions.map((suggestion) => (
          <button
            key={suggestion}
            onClick={(e) => {
              setInput(suggestion);
              handleSubmit(e, suggestion);
            }}
            className="block w-full text-left px-3 py-2 text-sm text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-md border border-gray-200 transition"
          >
            {suggestion}
          </button>
        ))}
      </div>

      <form onSubmit={(e) => handleSubmit(e)} className="p-4 border-t border-gray-200 space-y-3">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="What data would you like to see? (e.g., 'Show me all orders from 2024')"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none h-20 text-sm"
        />

        {state.error.hasError && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700 text-sm">{state.error.message}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={state.loading.isLoading || !input.trim()}
          className="w-full px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {state.loading.isLoading ? 'Generating...' : 'Generate SQL'}
        </button>
      </form>
    </div>
  );
};
