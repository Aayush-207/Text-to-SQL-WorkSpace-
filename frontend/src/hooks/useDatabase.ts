/**
 * Custom hook to use Database Context
 */

import { useContext } from 'react';
import { DatabaseContext } from '../store/DatabaseContext';
import { DatabaseContextType } from '../types';

export const useDatabase = (): DatabaseContextType => {
  const context = useContext(DatabaseContext);
  if (!context) {
    throw new Error('useDatabase must be used within DatabaseProvider');
  }
  return context;
};
