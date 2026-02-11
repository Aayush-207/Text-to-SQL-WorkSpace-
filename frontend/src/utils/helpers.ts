/**
 * Utility functions for data processing
 */

import { QueryType, ChartType, ChartSuggestion } from '../types';

/**
 * Detect if a value is numeric
 */
export const isNumeric = (value: any): boolean => {
  if (value === null || value === undefined) return false;
  if (typeof value === 'number') return true;
  if (typeof value === 'string') {
    const num = parseFloat(value);
    return !isNaN(num) && isFinite(num);
  }
  return false;
};

/**
 * Detect if a value is a date
 */
export const isDate = (value: any): boolean => {
  if (!value) return false;
  if (value instanceof Date) return true;
  if (typeof value === 'string') {
    const date = new Date(value);
    return !isNaN(date.getTime());
  }
  return false;
};

/**
 * Get numeric columns from data
 */
export const getNumericColumns = (data: any[]): string[] => {
  if (!Array.isArray(data) || data.length === 0) return [];

  const columns = Object.keys(data[0]);
  return columns.filter((col) => {
    // Check first non-null value
    for (let row of data) {
      if (row[col] !== null && row[col] !== undefined) {
        return isNumeric(row[col]);
      }
    }
    return false;
  });
};

/**
 * Get date columns from data
 */
export const getDateColumns = (data: any[]): string[] => {
  if (!Array.isArray(data) || data.length === 0) return [];

  const columns = Object.keys(data[0]);
  return columns.filter((col) => {
    // Check first non-null value
    for (let row of data) {
      if (row[col] !== null && row[col] !== undefined) {
        return isDate(row[col]);
      }
    }
    return false;
  });
};

/**
 * Suggest chart types based on data
 */
export const suggestCharts = (data: any[]): ChartSuggestion[] => {
  if (!Array.isArray(data) || data.length === 0) return [];

  const numericCols = getNumericColumns(data);
  const dateCols = getDateColumns(data);
  const allCols = Object.keys(data[0]);
  const categoricalCols = allCols.filter(
    (col) => !numericCols.includes(col) && !dateCols.includes(col)
  );

  const suggestions: ChartSuggestion[] = [];

  // Suggest bar chart for categorical + numeric
  if (categoricalCols.length > 0 && numericCols.length > 0) {
    suggestions.push({
      type: 'bar',
      columns: [categoricalCols[0], numericCols[0]],
      description: `Bar chart: ${categoricalCols[0]} vs ${numericCols[0]}`,
    });
  }

  // Suggest line chart for date + numeric
  if (dateCols.length > 0 && numericCols.length > 0) {
    suggestions.push({
      type: 'line',
      columns: [dateCols[0], numericCols[0]],
      description: `Line chart: ${dateCols[0]} vs ${numericCols[0]}`,
    });
  }

  // Suggest pie chart for categorical + numeric
  if (categoricalCols.length > 0 && numericCols.length > 0) {
    suggestions.push({
      type: 'pie',
      columns: [categoricalCols[0], numericCols[0]],
      description: `Pie chart: ${categoricalCols[0]} distribution`,
    });
  }

  // Suggest histogram for single numeric
  if (numericCols.length > 0) {
    suggestions.push({
      type: 'histogram',
      columns: [numericCols[0]],
      description: `Histogram: ${numericCols[0]} distribution`,
    });
  }

  return suggestions;
};

/**
 * Format large numbers for display
 */
export const formatNumber = (num: number): string => {
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
  if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
  return num.toString();
};

/**
 * Format date for display
 */
export const formatDate = (date: string): string => {
  try {
    return new Date(date).toLocaleString();
  } catch {
    return date;
  }
};

/**
 * Truncate long strings
 */
export const truncate = (text: string, length: number = 50): string => {
  return text.length > length ? text.substring(0, length) + '...' : text;
};

/**
 * Get query type badge color
 */
export const getQueryTypeColor = (type: QueryType): string => {
  const colors: Record<QueryType, string> = {
    SELECT: 'bg-blue-100 text-blue-800',
    INSERT: 'bg-green-100 text-green-800',
    UPDATE: 'bg-yellow-100 text-yellow-800',
    DELETE: 'bg-red-100 text-red-800',
    ALTER: 'bg-purple-100 text-purple-800',
  };
  return colors[type] || 'bg-gray-100 text-gray-800';
};

/**
 * Check if query is safe (SELECT only)
 */
export const isSafeQuery = (type: QueryType): boolean => {
  return type === 'SELECT';
};

/**
 * Compare two objects for changes
 */
export const findChanges = (before: any, after: any): Record<string, any> => {
  const changes: Record<string, any> = {};

  const allKeys = new Set([...Object.keys(before), ...Object.keys(after)]);
  allKeys.forEach((key) => {
    if (JSON.stringify(before[key]) !== JSON.stringify(after[key])) {
      changes[key] = {
        before: before[key],
        after: after[key],
      };
    }
  });

  return changes;
};
