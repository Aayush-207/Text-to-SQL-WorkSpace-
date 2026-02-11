/**
 * ChartViewer Component - Dynamic chart visualization
 */

import React, { useMemo } from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChartSuggestion } from '../types';
import { suggestCharts, getNumericColumns, getDateColumns } from '../utils/helpers';

const COLORS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#06b6d4',
];

interface Props {
  data?: any[];
  isLoading?: boolean;
  selectedChart?: ChartSuggestion;
  onChartSelect?: (chart: ChartSuggestion) => void;
}

export const ChartViewer: React.FC<Props> = ({
  data = [],
  isLoading = false,
  selectedChart,
  onChartSelect,
}) => {
  const suggestions = useMemo(() => suggestCharts(data), [data]);

  const chartData = useMemo(() => {
    if (!selectedChart || !data.length) return [];

    const [xCol, yCol] = selectedChart.columns;

    if (selectedChart.type === 'pie') {
      return data.map((row, idx) => ({
        name: String(row[xCol] ?? `Item ${idx}`),
        value: Number(row[yCol] ?? 0),
      }));
    }

    if (selectedChart.type === 'histogram') {
      // Group numeric data into buckets
      const values = data.map((row) => Number(row[xCol] ?? 0));
      const min = Math.min(...values);
      const max = Math.max(...values);
      const bucketCount = 10;
      const bucketSize = (max - min) / bucketCount;

      const buckets: Record<string, number> = {};
      values.forEach((val) => {
        const bucketIdx = Math.floor((val - min) / bucketSize);
        const key = `${(min + bucketIdx * bucketSize).toFixed(0)}-${(
          min +
          (bucketIdx + 1) * bucketSize
        ).toFixed(0)}`;
        buckets[key] = (buckets[key] || 0) + 1;
      });

      return Object.entries(buckets).map(([key, value]) => ({
        name: key,
        value,
      }));
    }

    return data.map((row) => ({
      name: String(row[xCol] ?? ''),
      value: Number(row[yCol] ?? 0),
    }));
  }, [selectedChart, data]);

  if (isLoading) {
    return (
      <div className="h-full flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="text-gray-600 text-sm mt-2">Loading chart...</p>
      </div>
    );
  }

  if (!data.length || !suggestions.length) {
    return (
      <div className="h-full flex flex-col items-center justify-center">
        <p className="text-gray-500 text-sm">No numeric data for visualization</p>
      </div>
    );
  }

  if (!selectedChart) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h3 className="text-lg font-bold text-gray-800">Visualizations</h3>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {suggestions.map((chart, idx) => (
            <button
              key={idx}
              onClick={() => onChartSelect?.(chart)}
              className="w-full text-left px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-md border border-gray-200 transition"
            >
              <p className="font-medium text-gray-800 text-sm capitalize">{chart.type}</p>
              <p className="text-xs text-gray-600 mt-1">{chart.description}</p>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-gray-800 capitalize">{selectedChart.type}</h3>
          <p className="text-xs text-gray-600 mt-1">{selectedChart.description}</p>
        </div>
        <button
          onClick={() => onChartSelect?.(undefined as any)}
          className="text-sm px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Change
        </button>
      </div>

      <div className="flex-1 overflow-hidden">
        <ResponsiveContainer width="100%" height="100%">
          {selectedChart.type === 'bar' && (
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          )}

          {selectedChart.type === 'line' && (
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" dot={false} />
            </LineChart>
          )}

          {selectedChart.type === 'pie' && (
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={true}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          )}

          {selectedChart.type === 'histogram' && (
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#10b981" />
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    </div>
  );
};
