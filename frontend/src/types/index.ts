/**
 * Type definitions for the application
 */

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  detail?: string;
}

// Database Connection
export interface DatabaseConnection {
  host: string;
  port: number;
  database: string;
  user: string;
  password: string;
}

// Schema Types
export interface ColumnInfo {
  name: string;
  data_type: string;
  is_nullable: boolean;
  default?: string;
  position: number;
}

export interface TableInfo {
  name: string;
  schema: string;
  column_count: number;
  type: string;
}

export interface ForeignKey {
  table: string;
  column: string;
  referenced_table: string;
  referenced_column: string;
  constraint_name: string;
}

export interface Constraint {
  name: string;
  type: string;
}

export interface Index {
  name: string;
  type: string;
  is_unique: boolean;
  is_primary: boolean;
}

export interface SchemaMetadata {
  schema: string;
  tables: TableInfo[];
  columns: Record<string, ColumnInfo[]>;
  foreign_keys: ForeignKey[];
  constraints: Record<string, Constraint[]>;
  indexes: Record<string, Index[]>;
}

// SQL Generation Types
export type QueryType = 'SELECT' | 'INSERT' | 'UPDATE' | 'DELETE' | 'ALTER';

export interface GeneratedSQL {
  sql: string;
  type: QueryType;
  confidence: number;
  explanation: string;
}

export interface GenerateSQLResponse extends ApiResponse<GeneratedSQL> {
  data?: GeneratedSQL;
}

// Query Preview Types
export interface PreviewResponse extends ApiResponse<any> {
  query_type?: QueryType;
  preview_rows: any[];
  affected_rows: number;
  error?: string;
}

// Query Execution Types
export interface ExecutionResponse extends ApiResponse<any> {
  query_type?: QueryType;
  data?: any[];
  rows_returned?: number;
  affected_rows?: number;
  error?: string;
}

// Query History
export interface QueryHistoryEntry {
  id: string;
  query: string;
  query_type: QueryType;
  timestamp: string;
  execution_time_ms: number;
  success: boolean;
  rows_affected: number;
}

export interface HistoryResponse extends ApiResponse<any> {
  total: number;
  history: QueryHistoryEntry[];
}

// Chart Types
export type ChartType = 'table' | 'bar' | 'line' | 'pie' | 'histogram' | 'scatter';

export interface ChartData {
  type: ChartType;
  labels: string[];
  datasets: Array<{
    label: string;
    data: any[];
    backgroundColor?: string | string[];
    borderColor?: string;
    fill?: boolean;
  }>;
}

export interface ChartSuggestion {
  type: ChartType;
  columns: string[];
  description: string;
}

// UI State Types
export interface DialogState {
  isOpen: boolean;
  title?: string;
  message?: string;
  type?: 'confirm' | 'error' | 'success' | 'info';
  onConfirm?: () => void;
  onCancel?: () => void;
}

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  message?: string;
  code?: string;
}

// Application State
export interface AppState {
  connected: boolean;
  schema?: SchemaMetadata;
  currentQuery?: string;
  queryHistory: QueryHistoryEntry[];
  mode: 'safe' | 'edit';
  loading: LoadingState;
  error: ErrorState;
  dialog: DialogState;
}

// Context Types
export interface DatabaseContextType {
  state: AppState;
  connectDatabase: (connection: DatabaseConnection) => Promise<void>;
  disconnect: () => void;
  fetchSchema: () => Promise<void>;
  generateSQL: (query: string, schema: string) => Promise<GeneratedSQL | null>;
  previewQuery: (sql: string) => Promise<PreviewResponse | null>;
  executeQuery: (sql: string) => Promise<ExecutionResponse | null>;
  getQueryHistory: () => Promise<void>;
  clearHistory: () => Promise<void>;
  addToHistory: (entry: QueryHistoryEntry) => void;
  setMode: (mode: 'safe' | 'edit') => void;
  showDialog: (dialog: DialogState) => void;
  hideDialog: () => void;
}
