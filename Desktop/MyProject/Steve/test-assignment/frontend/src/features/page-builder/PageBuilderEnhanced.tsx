/**
 * Enhanced Page Builder with Week 5-6 features.
 * Integrates auto-save, notifications, keyboard shortcuts, and advanced features.
 */

import React, { memo, useEffect, useCallback, useState } from 'react';
import { Box, Alert, CircularProgress, LinearProgress } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { builderApi } from './api/builderApi';
import { useBuilderStore } from './stores/useBuilderStore';
import { ComponentPalette } from './components/Palette/ComponentPalette';
import { BuilderCanvas } from './components/Canvas/BuilderCanvas';
import { BuilderToolbar } from './components/Toolbar/BuilderToolbar';
import { PropertyEditor } from './components/Properties/PropertyEditor';
import { useAutoSave } from './hooks/useAutoSave';
import { useKeyboardShortcuts } from './hooks/useKeyboardShortcuts';
import { useNotifications } from '~/hooks/useNotifications';

interface PageBuilderProps {
  pageId: number;
  pageName?: string;
}

export const PageBuilderEnhanced: React.FC<PageBuilderProps> = memo(({ pageId, pageName }) => {
  // Notification hooks
  const { showSuccess, showError, showWarning } = useNotifications();

  // Fetch component registry
  const { data: componentRegistry, isLoading: isLoadingRegistry, error: registryError } = useSuspenseQuery({
    queryKey: ['component-registry'],
    queryFn: () => builderApi.getComponentRegistry(),
  });

  // Fetch page data
  const { data: pageData, isLoading: isLoadingPage, error: pageError } = useSuspenseQuery({
    queryKey: ['builder-page', pageId],
    queryFn: () => builderApi.getBuilderPage(pageId),
  });

  // Store actions
  const {
    setComponentRegistry,
    loadPage,
    history,
    saveState,
  } = useBuilderStore();

  const selectedComponent = useBuilderStore((state) => {
    const selectedId = state.selection.selectedId;
    if (!selectedId) return null;

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

    return findComponent(state.builderData.components, selectedId);
  });

  const componentSchema = useBuilderStore((state) =>
    selectedComponent ? state.getComponentSchema(selectedComponent.type) : undefined
  );

  // Initialize component registry
  useEffect(() => {
    if (componentRegistry) {
      setComponentRegistry(componentRegistry);
    }
  }, [componentRegistry, setComponentRegistry]);

  // Load page data
  useEffect(() => {
    if (pageData) {
      loadPage(pageId, pageData.builder_data);
    }
  }, [pageData, pageId, loadPage]);

  // Auto-save with debouncing
  const { isDirty } = useAutoSave({
    delay: 3000,
    enabled: true,
    pageId,
    onSave: (success, error) => {
      if (success) {
        showSuccess('Page auto-saved', 'Auto-Save');
      } else {
        showError(`Auto-save failed: ${error}`, 'Auto-Save Error');
      }
    },
  });

  // Keyboard shortcuts
  useKeyboardShortcuts(pageId);

  // Handle manual save
  const handleSave = useCallback(async () => {
    try {
      await builderApi.updateBuilderPage(pageId, history.present);
      showSuccess('Page saved successfully!', 'Save');
    } catch (error) {
      console.error('Failed to save page:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      showError(`Failed to save page: ${errorMessage}`, 'Save Error');
    }
  }, [pageId, history.present, showSuccess, showError]);

  // Handle publish
  const handlePublish = useCallback(async () => {
    if (isDirty) {
      showWarning('Page has unsaved changes. Save before publishing.', 'Unsaved Changes');
      return;
    }

    try {
      await builderApi.publishBuilderPage(pageId, history.present);
      showSuccess('Page published successfully!', 'Publish');
    } catch (error) {
      console.error('Failed to publish page:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      showError(`Failed to publish page: ${errorMessage}`, 'Publish Error');
    }
  }, [pageId, history.present, isDirty, showSuccess, showWarning, showError]);

  // Loading state
  if (isLoadingRegistry || isLoadingPage) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          gap: 2,
        }}
      >
        <CircularProgress />
        <Typography variant="body1" color="text.secondary">
          Loading page builder...
        </Typography>
      </Box>
    );
  }

  // Error state
  if (registryError || pageError) {
    return (
      <Box sx={{ p: 2 }}>
        <Alert severity="error">
          Failed to load page builder. Please refresh the page.
        </Alert>
      </Box>
    );
  }

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        overflow: 'hidden',
      }}
    >
      {/* Auto-save indicator */}
      {isDirty && (
        <LinearProgress
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 9999,
          }}
        />
      )}

      {/* Toolbar */}
      <BuilderToolbar
        pageId={pageId}
        pageName={pageName}
        onSave={handleSave}
        onPublish={handlePublish}
        isDirty={isDirty}
      />

      {/* Main Content */}
      <Box sx={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        {/* Component Palette */}
        <ComponentPalette components={componentRegistry || []} />

        {/* Builder Canvas */}
        <BuilderCanvas pageId={pageId} />

        {/* Property Editor */}
        {selectedComponent && componentSchema && (
          <PropertyEditor
            component={selectedComponent}
            schema={componentSchema.schema}
          />
        )}
      </Box>
    </Box>
  );
});

PageBuilderEnhanced.displayName = 'PageBuilderEnhanced';

export default PageBuilderEnhanced;
