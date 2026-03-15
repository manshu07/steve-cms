/**
 * Page Builder - main component orchestrating the entire builder interface.
 * Combines Palette, Canvas, Properties, and Toolbar.
 */

import React, { memo, useEffect, useCallback } from 'react';
import { Box, Alert, CircularProgress } from '@mui/material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { builderApi } from './api/builderApi';
import { useBuilderStore } from './stores/useBuilderStore';
import { ComponentPalette } from './components/Palette/ComponentPalette';
import { BuilderCanvas } from './components/Canvas/BuilderCanvas';
import { BuilderToolbar } from './components/Toolbar/BuilderToolbar';
import { PropertyEditor } from './components/Properties/PropertyEditor';
import { selectSelectedComponent, selectComponentById } from './stores/useBuilderStore';

interface PageBuilderProps {
  pageId: number;
  pageName?: string;
}

export const PageBuilder: React.FC<PageBuilderProps> = memo(({ pageId, pageName }) => {
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
    saveState,
    history,
  } = useBuilderStore();

  const selectedComponent = useBuilderStore(selectSelectedComponent);
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

  // Auto-save on changes (debounced would be better)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (history.present !== pageData?.builder_data) {
        saveState();
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [history.present, pageData, saveState]);

  // Handle save
  const handleSave = useCallback(async () => {
    try {
      await builderApi.updateBuilderPage(pageId, history.present);
      alert('Page saved successfully!');
    } catch (error) {
      console.error('Failed to save page:', error);
      alert('Failed to save page. Please try again.');
    }
  }, [pageId, history.present]);

  // Handle publish
  const handlePublish = useCallback(async () => {
    try {
      await builderApi.publishBuilderPage(pageId, history.present);
      alert('Page published successfully!');
    } catch (error) {
      console.error('Failed to publish page:', error);
      alert('Failed to publish page. Please try again.');
    }
  }, [pageId, history.present]);

  // Loading state
  if (isLoadingRegistry || isLoadingPage) {
    return (
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
        }}
      >
        <CircularProgress />
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
      {/* Toolbar */}
      <BuilderToolbar
        pageId={pageId}
        pageName={pageName}
        onSave={handleSave}
        onPublish={handlePublish}
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

PageBuilder.displayName = 'PageBuilder';

export default PageBuilder;
