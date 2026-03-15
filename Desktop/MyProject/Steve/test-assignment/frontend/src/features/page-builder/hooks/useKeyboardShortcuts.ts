/**
 * Keyboard shortcuts hook for page builder.
 * Handles common keyboard shortcuts for builder operations.
 */

import { useEffect, useCallback } from 'react';
import { useBuilderStore } from '../stores/useBuilderStore';
import { useNotifications } from '~/hooks/useNotifications';

interface KeyboardShortcut {
  key: string;
  ctrlKey?: boolean;
  shiftKey?: boolean;
  altKey?: boolean;
  metaKey?: boolean;
  description: string;
  action: () => void;
}

export const useKeyboardShortcuts = (pageId: number) => {
  const {
    selection,
    undo,
    redo,
    canUndo,
    canRedo,
    deleteComponent,
    duplicateComponent,
    clearSelection,
    builderData,
  } = useBuilderStore();

  const { showSuccess, showInfo, showError } = useNotifications();

  // Copy component to clipboard
  const handleCopy = useCallback(() => {
    if (!selection.selectedId) return;

    const component = findComponent(builderData.components, selection.selectedId);
    if (component) {
      // Copy to clipboard as JSON
      navigator.clipboard.writeText(JSON.stringify(component));
      showInfo('Component copied to clipboard', 'Copy');
    }
  }, [selection.selectedId, builderData, showInfo]);

  // Paste component from clipboard
  const handlePaste = useCallback(async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      const component = JSON.parse(clipboardText);

      // Generate new ID to avoid conflicts
      const newComponent = {
        ...component,
        id: crypto.randomUUID(),
      };

      // Add to canvas (will be added after parent component is implemented)
      showInfo('Component ready to paste', 'Paste');
    } catch (error) {
      showError('No valid component in clipboard', 'Paste Error');
    }
  }, [showError, showInfo]);

  // Delete selected component
  const handleDelete = useCallback(() => {
    if (!selection.selectedId) return;

    deleteComponent(selection.selectedId);
    clearSelection();
    showSuccess('Component deleted', 'Delete');
  }, [selection.selectedId, deleteComponent, clearSelection, showSuccess]);

  // Duplicate selected component
  const handleDuplicate = useCallback(() => {
    if (!selection.selectedId) return;

    duplicateComponent(selection.selectedId);
    showSuccess('Component duplicated', 'Duplicate');
  }, [selection.selectedId, duplicateComponent, showSuccess]);

  // Clear selection
  const handleEscape = useCallback(() => {
    clearSelection();
  }, [clearSelection]);

  // Undo
  const handleUndo = useCallback(() => {
    if (canUndo()) {
      undo();
      showInfo('Undo successful', 'Undo');
    }
  }, [canUndo, undo, showInfo]);

  // Redo
  const handleRedo = useCallback(() => {
    if (canRedo()) {
      redo();
      showInfo('Redo successful', 'Redo');
    }
  }, [canRedo, redo, showInfo]);

  // Find component helper
  const findComponent = (components: any[], id: string): any => {
    for (const component of components) {
      if (component.id === id) return component;
      if (component.children) {
        const found = findComponent(component.children, id);
        if (found) return found;
      }
    }
    return undefined;
  };

  // Keyboard shortcuts configuration
  const shortcuts: KeyboardShortcut[] = [
    // Delete
    {
      key: 'Delete',
      description: 'Delete selected component',
      action: handleDelete,
    },
    {
      key: 'Backspace',
      description: 'Delete selected component',
      action: handleDelete,
    },
    // Escape
    {
      key: 'Escape',
      description: 'Clear selection',
      action: handleEscape,
    },
    // Undo/Redo
    {
      key: 'z',
      ctrlKey: true,
      description: 'Undo',
      action: handleUndo,
    },
    {
      key: 'y',
      ctrlKey: true,
      description: 'Redo',
      action: handleRedo,
    },
    // Copy/Paste
    {
      key: 'c',
      ctrlKey: true,
      description: 'Copy component',
      action: handleCopy,
    },
    {
      key: 'v',
      ctrlKey: true,
      description: 'Paste component',
      action: handlePaste,
    },
    // Duplicate
    {
      key: 'd',
      ctrlKey: true,
      description: 'Duplicate component',
      action: handleDuplicate,
    },
    // Save
    {
      key: 's',
      ctrlKey: true,
      description: 'Save page',
      action: () => showInfo('Saving page...', 'Save'),
    },
  ];

  // Setup keyboard event listeners
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ignore if typing in input/textarea
      const target = event.target as HTMLElement;
      if (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable
      ) {
        return;
      }

      // Check each shortcut
      for (const shortcut of shortcuts) {
        const keyMatch = event.key.toLowerCase() === shortcut.key.toLowerCase();
        const ctrlMatch = shortcut.ctrlKey ? event.ctrlKey || event.metaKey : !event.ctrlKey && !event.metaKey;
        const shiftMatch = shortcut.shiftKey ? event.shiftKey : !event.shiftKey;
        const altMatch = shortcut.altKey ? event.altKey : !event.altKey;
        const metaMatch = shortcut.metaKey ? event.metaKey : !event.metaKey;

        if (keyMatch && ctrlMatch && shiftMatch && altMatch && metaMatch) {
          event.preventDefault();
          shortcut.action();
          break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts]);

  return {
    shortcuts: shortcuts.map((s) => ({
      key: s.key,
      ctrlKey: s.ctrlKey,
      description: s.description,
    })),
  };
};

export default useKeyboardShortcuts;
