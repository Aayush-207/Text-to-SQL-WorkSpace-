/**
 * SchemaViewer Component - Tree view of database schema
 */

import React, { useState } from 'react';
import { SchemaMetadata } from '../types';

interface Props {
  schema?: SchemaMetadata;
  onTableSelect?: (table: string) => void;
}

export const SchemaViewer: React.FC<Props> = ({ schema, onTableSelect }) => {
  const [expandedTables, setExpandedTables] = useState<Set<string>>(new Set());
  const [searchTerm, setSearchTerm] = useState('');

  const toggleTableExpand = (tableName: string) => {
    const newExpanded = new Set(expandedTables);
    if (newExpanded.has(tableName)) {
      newExpanded.delete(tableName);
    } else {
      newExpanded.add(tableName);
    }
    setExpandedTables(newExpanded);
  };

  if (!schema) {
    return (
      <div className="p-4 text-gray-500">
        <p>Connect to a database to view schema</p>
      </div>
    );
  }

  const filteredTables = schema.tables.filter((table) =>
    table.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-bold text-gray-800 mb-3">Schema</h3>
        <input
          type="text"
          placeholder="Search tables..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </div>

      <div className="flex-1 overflow-y-auto">
        {filteredTables.length === 0 ? (
          <div className="p-4 text-gray-500 text-sm">No tables found</div>
        ) : (
          <div className="divide-y divide-gray-200">
            {filteredTables.map((table) => (
              <div key={table.name} className="border-b border-gray-100">
                <button
                  onClick={() => {
                    toggleTableExpand(table.name);
                    onTableSelect?.(table.name);
                  }}
                  className="w-full px-4 py-3 text-left hover:bg-gray-50 flex items-center gap-2 transition"
                >
                  <span
                    className={`transform transition ${
                      expandedTables.has(table.name) ? 'rotate-90' : ''
                    }`}
                  >
                    ▶
                  </span>
                  <span className="font-medium text-gray-700">{table.name}</span>
                  <span className="text-xs bg-gray-200 text-gray-600 px-2 py-1 rounded">
                    {table.column_count} cols
                  </span>
                </button>

                {expandedTables.has(table.name) && (
                  <div className="bg-gray-50 px-4 py-2 space-y-1">
                    {schema.columns[table.name]?.map((column) => (
                      <div key={column.name} className="text-sm text-gray-600 pl-6 py-1">
                        <span className="font-mono text-gray-700">{column.name}</span>
                        <span className="text-gray-500 ml-2">: {column.data_type}</span>
                        {!column.is_nullable && (
                          <span className="text-red-500 ml-2 text-xs">NOT NULL</span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {schema.foreign_keys.length > 0 && (
        <div className="p-4 border-t border-gray-200 bg-gray-50">
          <h4 className="text-xs font-bold text-gray-600 uppercase mb-2">Relationships</h4>
          <div className="space-y-1">
            {schema.foreign_keys.slice(0, 5).map((fk) => (
              <div key={fk.constraint_name} className="text-xs text-gray-600">
                <span className="font-mono">{fk.table}</span>
                <span className="text-gray-500"> → </span>
                <span className="font-mono">{fk.referenced_table}</span>
              </div>
            ))}
            {schema.foreign_keys.length > 5 && (
              <p className="text-xs text-gray-500 italic">
                +{schema.foreign_keys.length - 5} more relationships
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
