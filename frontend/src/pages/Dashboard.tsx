/**
 * Dashboard Page - Main application layout
 */

import React, { useState, useEffect } from 'react';
import { DatabaseConnector } from '../components/DatabaseConnector';
import { SchemaViewer } from '../components/SchemaViewer';
import { ChatPanel } from '../components/ChatPanel';
import { QueryEditor } from '../components/QueryEditor';
import { ResultTable } from '../components/ResultTable';
import { ChartViewer } from '../components/ChartViewer';
import { ConfirmationModal } from '../components/ConfirmationModal';
import { QueryHistory } from '../components/QueryHistory';
import { useDatabase } from '../hooks/useDatabase';
import { GeneratedSQL, ChartSuggestion, PreviewResponse, ExecutionResponse } from '../types';
import { isSafeQuery } from '../utils/helpers';

type ViewMode = 'table' | 'chart';

export const Dashboard: React.FC = () => {
  const { state, previewQuery, executeQuery, addToHistory, setMode } = useDatabase();

  // UI State
  const [generatedSQL, setGeneratedSQL] = useState<GeneratedSQL | null>(null);
  const [currentSQL, setCurrentSQL] = useState('');
  const [previewData, setPreviewData] = useState<PreviewResponse | null>(null);
  const [executionResult, setExecutionResult] = useState<ExecutionResponse | null>(null);
  const [isPreviewMode, setIsPreviewMode] = useState(false);
  const [selectedChart, setSelectedChart] = useState<ChartSuggestion | undefined>();
  const [viewMode, setViewMode] = useState<ViewMode>('table');
  const [showHistory, setShowHistory] = useState(true);

  // Handle SQL generation from chat
  const handleSQLGenerated = (sql: GeneratedSQL) => {
    setGeneratedSQL(sql);
    setCurrentSQL(sql.sql);
    setPreviewData(null);
    setExecutionResult(null);

    if (isSafeQuery(sql.type)) {
      handleExecute(sql.sql);
    } else {
      setMode('edit');
    }
  };

  // Preview query
  const handlePreview = async (sql: string) => {
    setIsPreviewMode(true);
    const result = await previewQuery(sql);
    if (result) {
      setPreviewData(result);
    }
    setIsPreviewMode(false);
  };

  // Execute query
  const handleExecute = async (sql: string) => {
    setIsPreviewMode(true);

    // If it's a write operation, show confirmation first
    if (
      generatedSQL &&
      !isSafeQuery(generatedSQL.type) &&
      state.mode === 'safe'
    ) {
      state.dialog.onConfirm = async () => {
        await performExecution(sql);
      };
      return;
    }

    await performExecution(sql);
    setIsPreviewMode(false);
  };

  const performExecution = async (sql: string) => {
    const result = await executeQuery(sql);
    if (result) {
      setExecutionResult(result);
      setViewMode('table');

      // Add to history
      addToHistory({
        id: Date.now().toString(),
        query: sql,
        query_type: generatedSQL?.type || 'SELECT',
        timestamp: new Date().toISOString(),
        execution_time_ms: 0,
        success: !result.error,
        rows_affected: result.affected_rows || result.data?.length || 0,
      });
    }
    setIsPreviewMode(false);
  };

  // Not connected view
  if (!state.connected) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <DatabaseConnector onConnected={() => {}} />
      </div>
    );
  }

  // Main dashboard layout
  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Text to SQL</h1>
        <div className="flex items-center gap-4">
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
          >
            {showHistory ? 'Hide' : 'Show'} History
          </button>
          <div className="flex items-center gap-2 border-l border-gray-200 pl-4">
            <label className="text-sm font-medium text-gray-700">Mode:</label>
            <select
              value={state.mode}
              onChange={(e) => setMode(e.target.value as 'safe' | 'edit')}
              className="px-3 py-1 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="safe">Safe (SELECT only)</option>
              <option value="edit">Edit (All queries)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Schema */}
        <div className="w-1/5 border-r border-gray-200 bg-gray-50 flex flex-col">
          <SchemaViewer
            schema={state.schema}
            onTableSelect={(table) => {
              // Set focus to chat panel with table suggestion
            }}
          />
        </div>

        {/* Center Panel - Chat + Editor */}
        <div className="flex-1 flex flex-col">
          {!generatedSQL ? (
            <div className="flex-1">
              <ChatPanel onSQLGenerated={handleSQLGenerated} />
            </div>
          ) : (
            <div className="flex-1 flex flex-col">
              {/* SQL Info */}
              <div className="bg-blue-50 border-b border-blue-200 px-4 py-3">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-blue-800">{generatedSQL.explanation}</p>
                    <p className="text-xs text-blue-600 mt-1">
                      Confidence: {(generatedSQL.confidence * 100).toFixed(0)}%
                    </p>
                  </div>
                  <button
                    onClick={() => {
                      setGeneratedSQL(null);
                      setCurrentSQL('');
                    }}
                    className="text-sm px-3 py-1 border border-blue-300 rounded-md hover:bg-blue-100"
                  >
                    New Query
                  </button>
                </div>
              </div>

              {/* Editor */}
              <div className="flex-1">
                <QueryEditor
                  sql={currentSQL}
                  onChange={setCurrentSQL}
                  queryType={generatedSQL.type}
                  onExecute={handleExecute}
                  onPreview={handlePreview}
                  isLoading={isPreviewMode || state.loading.isLoading}
                />
              </div>

              {/* Preview Info */}
              {previewData && !executionResult && (
                <div className="bg-yellow-50 border-t border-yellow-200 px-4 py-3">
                  <p className="text-sm font-medium text-yellow-800">
                    Preview: {previewData.affected_rows} rows will be affected
                  </p>
                  <p className="text-xs text-yellow-600 mt-1">
                    Review the results and confirm before executing
                  </p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Panel - Results */}
        <div className="w-1/3 border-l border-gray-200 flex flex-col">
          {!executionResult ? (
            <div className="h-full flex items-center justify-center text-gray-500">
              <p>Results will appear here</p>
            </div>
          ) : (
            <>
              {/* View Mode Toggle */}
              <div className="px-4 py-2 border-b border-gray-200 flex gap-2">
                <button
                  onClick={() => setViewMode('table')}
                  className={`px-3 py-1 text-sm rounded-md ${
                    viewMode === 'table'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Table
                </button>
                <button
                  onClick={() => setViewMode('chart')}
                  className={`px-3 py-1 text-sm rounded-md ${
                    viewMode === 'chart'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Chart
                </button>
              </div>

              {/* Results */}
              <div className="flex-1 overflow-hidden">
                {viewMode === 'table' ? (
                  <ResultTable
                    data={executionResult.data || previewData?.preview_rows}
                    rowsAffected={executionResult.affected_rows}
                    error={executionResult.error}
                    isLoading={state.loading.isLoading}
                  />
                ) : (
                  <ChartViewer
                    data={executionResult.data || previewData?.preview_rows}
                    selectedChart={selectedChart}
                    onChartSelect={setSelectedChart}
                  />
                )}
              </div>
            </>
          )}
        </div>

        {/* Query History Sidebar */}
        {showHistory && <QueryHistory onQuerySelect={setCurrentSQL} />}
      </div>

      {/* Confirmation Modal */}
      <ConfirmationModal
        dialog={state.dialog}
        onConfirm={() => performExecution(currentSQL)}
        onCancel={() => {}}
        isLoading={state.loading.isLoading}
      />
    </div>
  );
};
