/**
 * Database Context for state management
 */

import React, { createContext, useReducer, ReactNode, useCallback } from 'react';
import {
  AppState,
  DatabaseContextType,
  DatabaseConnection,
  DialogState,
  QueryHistoryEntry,
} from '../types';
import {
  connectionAPI,
  schemaAPI,
  generationAPI,
  previewAPI,
  executionAPI,
  historyAPI,
} from '../api/endpoints';

// Initial state
const initialState: AppState = {
  connected: false,
  schema: undefined,
  currentQuery: '',
  queryHistory: [],
  mode: 'safe',
  loading: { isLoading: false },
  error: { hasError: false },
  dialog: { isOpen: false },
};

// Action types
type Action =
  | { type: 'SET_CONNECTED'; payload: boolean }
  | { type: 'SET_SCHEMA'; payload: any }
  | { type: 'SET_LOADING'; payload: { isLoading: boolean; message?: string } }
  | { type: 'SET_ERROR'; payload: { hasError: boolean; message?: string; code?: string } }
  | { type: 'SET_DIALOG'; payload: DialogState }
  | { type: 'HIDE_DIALOG' }
  | { type: 'SET_QUERY'; payload: string }
  | { type: 'SET_HISTORY'; payload: QueryHistoryEntry[] }
  | { type: 'ADD_HISTORY'; payload: QueryHistoryEntry }
  | { type: 'SET_MODE'; payload: 'safe' | 'edit' };

// Reducer
function appReducer(state: AppState, action: Action): AppState {
  switch (action.type) {
    case 'SET_CONNECTED':
      return { ...state, connected: action.payload };
    case 'SET_SCHEMA':
      return { ...state, schema: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_DIALOG':
      return { ...state, dialog: action.payload };
    case 'HIDE_DIALOG':
      return { ...state, dialog: { isOpen: false } };
    case 'SET_QUERY':
      return { ...state, currentQuery: action.payload };
    case 'SET_HISTORY':
      return { ...state, queryHistory: action.payload };
    case 'ADD_HISTORY':
      return {
        ...state,
        queryHistory: [action.payload, ...state.queryHistory].slice(0, 100),
      };
    case 'SET_MODE':
      return { ...state, mode: action.payload };
    default:
      return state;
  }
}

export const DatabaseContext = createContext<DatabaseContextType | undefined>(undefined);

interface DatabaseProviderProps {
  children: ReactNode;
}

export const DatabaseProvider: React.FC<DatabaseProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  const setLoading = useCallback((isLoading: boolean, message?: string) => {
    dispatch({ type: 'SET_LOADING', payload: { isLoading, message } });
  }, []);

  const setError = useCallback((hasError: boolean, message?: string, code?: string) => {
    dispatch({ type: 'SET_ERROR', payload: { hasError, message, code } });
  }, []);

  const connectDatabase = useCallback(
    async (connection: DatabaseConnection) => {
      try {
        setLoading(true, 'Connecting to database...');
        const response = await connectionAPI.test(connection);
        if (response.success) {
          dispatch({ type: 'SET_CONNECTED', payload: true });
          setError(false);
          await fetchSchema();
        } else {
          throw new Error(response.error || 'Connection failed');
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Connection failed';
        setError(true, message);
        dispatch({ type: 'SET_CONNECTED', payload: false });
        throw error;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setError]
  );

  const fetchSchema = useCallback(async () => {
    try {
      setLoading(true, 'Fetching schema...');
      const response = await schemaAPI.getMetadata('public');
      if (response.success && response.data) {
        dispatch({ type: 'SET_SCHEMA', payload: response.data });
        setError(false);
      } else {
        throw new Error(response.error || 'Failed to fetch schema');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to fetch schema';
      setError(true, message);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  const disconnect = useCallback(() => {
    dispatch({ type: 'SET_CONNECTED', payload: false });
    dispatch({ type: 'SET_SCHEMA', payload: undefined });
    setError(false);
  }, [setError]);

  const generateSQL = useCallback(
    async (query: string, schema: string = 'public') => {
      try {
        setLoading(true, 'Generating SQL...');
        const response = await generationAPI.generateSQL(query, schema);
        if (response.success && response.data) {
          setError(false);
          return response.data;
        } else {
          throw new Error(response.error || 'Failed to generate SQL');
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Failed to generate SQL';
        setError(true, message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setError]
  );

  const previewQuery = useCallback(
    async (sql: string) => {
      try {
        setLoading(true, 'Previewing query...');
        const response = await previewAPI.execute(sql);
        if (response.success) {
          setError(false);
          return response;
        } else {
          throw new Error(response.error || 'Failed to preview query');
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Failed to preview query';
        setError(true, message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setError]
  );

  const executeQuery = useCallback(
    async (sql: string) => {
      try {
        setLoading(true, 'Executing query...');
        const response = await executionAPI.executeQuery(sql);
        if (response.success) {
          setError(false);
          return response;
        } else {
          throw new Error(response.error || 'Failed to execute query');
        }
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Failed to execute query';
        setError(true, message);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [setLoading, setError]
  );

  const getQueryHistory = useCallback(async () => {
    try {
      setLoading(true, 'Fetching history...');
      const response = await historyAPI.getQueries();
      if (response.success) {
        dispatch({ type: 'SET_HISTORY', payload: response.history || [] });
        setError(false);
      } else {
        throw new Error(response.error || 'Failed to fetch history');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to fetch history';
      setError(true, message);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  const clearHistory = useCallback(async () => {
    try {
      setLoading(true, 'Clearing history...');
      const response = await historyAPI.clear();
      if (response.success) {
        dispatch({ type: 'SET_HISTORY', payload: [] });
        setError(false);
      } else {
        throw new Error(response.error || 'Failed to clear history');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to clear history';
      setError(true, message);
    } finally {
      setLoading(false);
    }
  }, [setLoading, setError]);

  const addToHistory = useCallback((entry: QueryHistoryEntry) => {
    dispatch({ type: 'ADD_HISTORY', payload: entry });
  }, []);

  const setMode = useCallback((mode: 'safe' | 'edit') => {
    dispatch({ type: 'SET_MODE', payload: mode });
  }, []);

  const showDialog = useCallback((dialog: DialogState) => {
    dispatch({ type: 'SET_DIALOG', payload: dialog });
  }, []);

  const hideDialog = useCallback(() => {
    dispatch({ type: 'HIDE_DIALOG' });
  }, []);

  const value: DatabaseContextType = {
    state,
    connectDatabase,
    disconnect,
    fetchSchema,
    generateSQL,
    previewQuery,
    executeQuery,
    getQueryHistory,
    clearHistory,
    addToHistory,
    setMode,
    showDialog,
    hideDialog,
  };

  return <DatabaseContext.Provider value={value}>{children}</DatabaseContext.Provider>;
};
