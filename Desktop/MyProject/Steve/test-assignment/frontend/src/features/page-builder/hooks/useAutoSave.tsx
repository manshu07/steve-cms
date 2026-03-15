/**
 * Auto-save hook with debouncing.
 * Automatically saves builder state after changes stop.
 */

import { useEffect, useRef } from 'react';
import { useBuilderStore } from '../stores/useBuilderStore';
import { builderApi } from '../api/builderApi';

interface UseAutoSaveOptions {
  delay?: number; // Delay in milliseconds (default: 3000)
  enabled?: boolean;
  pageId: number;
  onSave?: (success: boolean, error?: string) => void;
}

export const useAutoSave = ({
  delay = 3000,
  enabled = true,
  pageId,
  onSave,
}: UseAutoSaveOptions) => {
  const { builderData, currentPageId } = useBuilderStore();
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const lastSavedDataRef = useRef<string>(JSON.stringify(builderData));

  useEffect(() => {
    if (!enabled || pageId !== currentPageId) {
      return;
    }

    const currentData = JSON.stringify(builderData);

    // Only save if data has actually changed
    if (currentData === lastSavedDataRef.current) {
      return;
    }

    // Clear existing timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    // Set new timeout for auto-save
    timeoutRef.current = setTimeout(async () => {
      try {
        await builderApi.updateBuilderPage(pageId, builderData);
        lastSavedDataRef.current = currentData;
        onSave?.(true, undefined);
      } catch (error) {
        console.error('Auto-save failed:', error);
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        onSave?.(false, errorMessage);
      }
    }, delay);

    // Cleanup timeout on unmount
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [builderData, pageId, currentPageId, delay, enabled, onSave]);

  // Manual save trigger
  const saveNow = async () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    try {
      await builderApi.updateBuilderPage(pageId, builderData);
      lastSavedDataRef.current = JSON.stringify(builderData);
      return { success: true };
    } catch (error) {
      console.error('Manual save failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      return { success: false, error: errorMessage };
    }
  };

  return {
    saveNow,
    isDirty: JSON.stringify(builderData) !== lastSavedDataRef.current,
  };
};

export default useAutoSave;
