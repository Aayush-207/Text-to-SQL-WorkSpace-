/**
 * Main App Component
 */

import React from 'react';
import { DatabaseProvider } from './store/DatabaseContext';
import { Dashboard } from './pages/Dashboard';
import './index.css';

export const App: React.FC = () => {
  return (
    <DatabaseProvider>
      <Dashboard />
    </DatabaseProvider>
  );
};

export default App;
