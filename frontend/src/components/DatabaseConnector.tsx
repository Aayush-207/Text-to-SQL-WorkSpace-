/**
 * DatabaseConnector Component - Database connection form
 */

import React, { useState } from 'react';
import { DatabaseConnection } from '../types';
import { useDatabase } from '../hooks/useDatabase';

interface Props {
  onConnected?: () => void;
}

export const DatabaseConnector: React.FC<Props> = ({ onConnected }) => {
  const { connectDatabase, state } = useDatabase();
  const [connection, setConnection] = useState<DatabaseConnection>({
    host: 'localhost',
    port: 5432,
    database: 'postgres',
    user: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setConnection((prev) => ({
      ...prev,
      [name]: name === 'port' ? parseInt(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await connectDatabase(connection);
      onConnected?.();
    } catch (error) {
      // Error handled by context
    }
  };

  return (
    <div className="w-full max-w-md">
      <form onSubmit={handleSubmit} className="space-y-4">
        <h2 className="text-xl font-bold text-gray-800">Connect to Database</h2>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Host</label>
          <input
            type="text"
            name="host"
            value={connection.host}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="localhost"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Port</label>
            <input
              type="number"
              name="port"
              value={connection.port}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="5432"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Database</label>
            <input
              type="text"
              name="database"
              value={connection.database}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="postgres"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Username</label>
          <input
            type="text"
            name="user"
            value={connection.user}
            onChange={handleChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="postgres"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
          <div className="relative">
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              value={connection.password}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter password"
              required
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-2.5 text-gray-500 text-sm"
            >
              {showPassword ? 'Hide' : 'Show'}
            </button>
          </div>
        </div>

        {state.error.hasError && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-700 text-sm">{state.error.message}</p>
          </div>
        )}

        {state.loading.isLoading && (
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-md">
            <p className="text-blue-700 text-sm">{state.loading.message}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={state.loading.isLoading}
          className="w-full px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {state.loading.isLoading ? 'Connecting...' : 'Connect'}
        </button>
      </form>
    </div>
  );
};
