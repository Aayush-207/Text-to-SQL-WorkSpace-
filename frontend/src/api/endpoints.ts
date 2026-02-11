/**
 * API Endpoints - All API calls defined here
 */

import { apiClient } from './client';
import {
  ApiResponse,
  DatabaseConnection,
  SchemaMetadata,
  GeneratedSQL,
  PreviewResponse,
  ExecutionResponse,
  HistoryResponse,
  QueryHistoryEntry,
} from '../types';

const API_V1 = '/api/v1';

// ============================================================================
// CONNECTION ENDPOINTS
// ============================================================================

export const connectionAPI = {
  test: async (connection: DatabaseConnection): Promise<ApiResponse<any>> => {
    return apiClient.post(`${API_V1}/connect/test`, connection);
  },

  status: async (): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/connect/status`);
  },
};

// ============================================================================
// SCHEMA ENDPOINTS
// ============================================================================

export const schemaAPI = {
  getMetadata: async (schema: string = 'public'): Promise<ApiResponse<SchemaMetadata>> => {
    return apiClient.get(`${API_V1}/schema/metadata`, {
      params: { schema },
    });
  },

  getTables: async (schema: string = 'public'): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/schema/tables`, {
      params: { schema },
    });
  },

  getColumns: async (schema: string = 'public'): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/schema/columns`, {
      params: { schema },
    });
  },

  getForeignKeys: async (schema: string = 'public'): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/schema/foreign-keys`, {
      params: { schema },
    });
  },

  getIndexes: async (schema: string = 'public'): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/schema/indexes`, {
      params: { schema },
    });
  },

  getSampleData: async (
    table: string,
    schema: string = 'public',
    limit: number = 5
  ): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/schema/sample-data`, {
      params: { table, schema, limit },
    });
  },
};

// ============================================================================
// SQL GENERATION ENDPOINTS
// ============================================================================

export const generationAPI = {
  generateSQL: async (
    naturalLanguageQuery: string,
    schema: string = 'public'
  ): Promise<GenerateSQLResponse> => {
    return apiClient.post(`${API_V1}/generate/sql`, {
      natural_language_query: naturalLanguageQuery,
      schema,
    });
  },

  getAvailableModels: async (): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/generate/available-models`);
  },
};

export interface GenerateSQLResponse extends ApiResponse<GeneratedSQL> {
  data?: GeneratedSQL;
}

// ============================================================================
// PREVIEW ENDPOINTS
// ============================================================================

export const previewAPI = {
  execute: async (sql: string, limit: number = 100): Promise<PreviewResponse> => {
    return apiClient.post(`${API_V1}/preview/execute`, {
      sql,
      limit,
    });
  },

  simulate: async (sql: string, limit: number = 100): Promise<PreviewResponse> => {
    return apiClient.post(`${API_V1}/preview/simulate`, {
      sql,
      limit,
    });
  },
};

// ============================================================================
// EXECUTION ENDPOINTS
// ============================================================================

export const executionAPI = {
  executeQuery: async (sql: string): Promise<ExecutionResponse> => {
    return apiClient.post(`${API_V1}/execute/query`, { sql });
  },

  executeBatch: async (queries: Array<{ sql: string }>): Promise<ApiResponse<any>> => {
    return apiClient.post(`${API_V1}/execute/batch`, queries);
  },

  explain: async (sql: string): Promise<ApiResponse<any>> => {
    return apiClient.post(`${API_V1}/execute/explain`, { sql });
  },
};

// ============================================================================
// HISTORY ENDPOINTS
// ============================================================================

export const historyAPI = {
  getQueries: async (
    limit: number = 50,
    queryType?: string,
    successOnly?: boolean
  ): Promise<HistoryResponse> => {
    return apiClient.get(`${API_V1}/history/queries`, {
      params: { limit, query_type: queryType, success_only: successOnly },
    });
  },

  getStatistics: async (): Promise<ApiResponse<any>> => {
    return apiClient.get(`${API_V1}/history/statistics`);
  },

  clear: async (): Promise<ApiResponse<any>> => {
    return apiClient.delete(`${API_V1}/history/clear`);
  },

  add: async (entry: QueryHistoryEntry): Promise<ApiResponse<any>> => {
    return apiClient.post(`${API_V1}/history/add`, entry);
  },
};

// ============================================================================
// HEALTH CHECK
// ============================================================================

export const healthAPI = {
  check: async (): Promise<ApiResponse<any>> => {
    return apiClient.get('/health');
  },
};
