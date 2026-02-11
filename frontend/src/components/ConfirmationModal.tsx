/**
 * ConfirmationModal Component - Confirmation for write operations
 */

import React from 'react';
import { DialogState } from '../types';

interface Props {
  dialog?: DialogState;
  onConfirm?: () => void;
  onCancel?: () => void;
  isLoading?: boolean;
}

export const ConfirmationModal: React.FC<Props> = ({
  dialog,
  onConfirm,
  onCancel,
  isLoading = false,
}) => {
  if (!dialog?.isOpen) return null;

  const bgColor = {
    confirm: 'bg-blue-50 border-blue-200',
    error: 'bg-red-50 border-red-200',
    success: 'bg-green-50 border-green-200',
    info: 'bg-gray-50 border-gray-200',
  };

  const textColor = {
    confirm: 'text-blue-800',
    error: 'text-red-800',
    success: 'text-green-800',
    info: 'text-gray-800',
  };

  const buttonColor = {
    confirm: 'bg-blue-600 hover:bg-blue-700',
    error: 'bg-red-600 hover:bg-red-700',
    success: 'bg-green-600 hover:bg-green-700',
    info: 'bg-gray-600 hover:bg-gray-700',
  };

  const type = dialog.type || 'confirm';
  const bg = bgColor[type as keyof typeof bgColor];
  const textClass = textColor[type as keyof typeof textColor];
  const btn = buttonColor[type as keyof typeof buttonColor];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className={`bg-white rounded-lg shadow-xl max-w-md w-full mx-4 border ${bg}`}>
        <div className="p-6">
          {dialog.title && (
            <h2 className={`text-lg font-bold mb-2 ${textClass}`}>{dialog.title}</h2>
          )}
          {dialog.message && (
            <p className={`text-sm mb-6 ${textClass}`}>{dialog.message}</p>
          )}
        </div>

        <div className="px-6 pb-6 flex gap-3">
          <button
            onClick={() => {
              dialog.onCancel?.();
              onCancel?.();
            }}
            disabled={isLoading}
            className="flex-1 px-4 py-2 text-sm font-medium border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              dialog.onConfirm?.();
              onConfirm?.();
            }}
            disabled={isLoading}
            className={`flex-1 px-4 py-2 text-sm font-medium text-white rounded-md ${btn} disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            {isLoading ? 'Processing...' : 'Confirm'}
          </button>
        </div>
      </div>
    </div>
  );
};
