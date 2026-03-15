/**
 * Builder Canvas - main drop zone for page builder.
 * Renders components on a 12-column grid with drag and drop.
 */

import React, { memo, useCallback, useMemo } from 'react';
import {
  Box,
  Paper,
  Grid,
  Typography,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import { DndContext, DragEndEvent, DragOverEvent, DragStartEvent, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, arrayMove } from '@dnd-kit/sortable';
import type { ViewportMode, BuilderComponent } from '~types/index';
import { useBuilderStore } from '../../stores/useBuilderStore';
import { renderComponent } from '../Core';
import { RenderedComponent } from './RenderedComponent';

interface BuilderCanvasProps {
  pageId?: number;
}

const VIEWPORT_WIDTHS: Record<ViewportMode, number> = {
  desktop: 1200,
  tablet: 768,
  mobile: 375,
};

export const BuilderCanvas: React.FC<BuilderCanvasProps> = memo(({ pageId }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const {
    builderData,
    selection,
    canvasSettings,
    addComponent,
    updateComponent,
    moveComponent,
    selectComponent,
    hoverComponent,
    setDragging,
    clearSelection,
  } = useBuilderStore();

  const components = builderData.components;
  const currentViewport = canvasSettings.currentViewport;

  // DnD sensors
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8, // 8px movement required to start drag
      },
    })
  );

  // Handle drag start
  const handleDragStart = useCallback((event: DragStartEvent) => {
    setDragging(true);
    const { active } = event;

    // If dragging a component from canvas, select it
    if (active.id && typeof active.id === 'string') {
      selectComponent(active.id);
    }
  }, [setDragging, selectComponent]);

  // Handle drag over
  const handleDragOver = useCallback((event: DragOverEvent) => {
    const { active, over } = event;

    if (!over) return;

    // Handle reordering within canvas
    if (active.id !== over.id) {
      const oldIndex = components.findIndex((c) => c.id === active.id);
      const newIndex = components.findIndex((c) => c.id === over.id);

      if (oldIndex !== -1 && newIndex !== -1) {
        // Reorder components (handled in drag end)
      }
    }
  }, [components]);

  // Handle drag end
  const handleDragEnd = useCallback((event: DragEndEvent) => {
    setDragging(false);
    const { active, over } = event;

    if (!over) {
      clearSelection();
      return;
    }

    // Check if dragging new component from palette
    if (active.data.current?.type === 'component') {
      const componentData = active.data.current.component;

      // Create new component instance
      const newComponent: BuilderComponent = {
        id: crypto.randomUUID(),
        type: componentData.name,
        props: {
          ...componentData.default_props,
          id: crypto.randomUUID(),
        },
      };

      // Add to canvas
      addComponent(newComponent);
    } else if (active.id !== over.id) {
      // Reorder existing components
      const oldIndex = components.findIndex((c) => c.id === active.id);
      const newIndex = components.findIndex((c) => c.id === over.id);

      if (oldIndex !== -1 && newIndex !== -1) {
        const reordered = arrayMove(components, oldIndex, newIndex);
        // Update store with new order
        reordered.forEach((component, index) => {
          updateComponent(component.id, { index });
        });
      }
    }

    clearSelection();
  }, [components, addComponent, updateComponent, setDragging, clearSelection]);

  // Handle component selection
  const handleComponentClick = useCallback((componentId: string) => {
    selectComponent(componentId);
  }, [selectComponent]);

  // Handle component hover
  const handleComponentHover = useCallback((componentId: string | null) => {
    hoverComponent(componentId);
  }, [hoverComponent]);

  // Canvas styles based on viewport
  const canvasWidth = isMobile ? '100%' : `${VIEWPORT_WIDTHS[currentViewport]}px`;
  const showGrid = canvasSettings.gridEnabled;

  return (
    <Box
      sx={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        bgcolor: 'background.default',
      }}
    >
      {/* Viewport Label */}
      <Box
        sx={{
          px: 2,
          py: 1,
          borderBottom: 1,
          borderColor: 'divider',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Typography variant="subtitle2" color="text.secondary">
          Canvas - {currentViewport}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {components.length} {components.length === 1 ? 'component' : 'components'}
        </Typography>
      </Box>

      {/* Canvas Area */}
      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          p: 2,
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <DndContext
          sensors={sensors}
          onDragStart={handleDragStart}
          onDragOver={handleDragOver}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={components.map((c) => c.id)}
            strategy={verticalListSortingStrategy}
          >
            <Paper
              sx={{
                width: canvasWidth,
                minHeight: 800,
                bgcolor: 'background.paper',
                boxShadow: 3,
                p: 2,
                position: 'relative',
              }}
            >
              {/* 12-Column Grid Overlay */}
              {showGrid && (
                <Box
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    pointerEvents: 'none',
                    opacity: 0.1,
                    zIndex: 0,
                  }}
                >
                  <Grid container spacing={0} sx={{ height: '100%' }}>
                    {Array.from({ length: 12 }).map((_, index) => (
                      <Grid size={1} key={index}>
                        <Box
                          sx={{
                            height: '100%',
                            borderLeft: 1,
                            borderColor: 'divider',
                          }}
                        />
                      </Grid>
                    ))}
                  </Grid>
                </Box>
              )}

              {/* Empty State */}
              {components.length === 0 && (
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: 400,
                    color: 'text.secondary',
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    Start Building Your Page
                  </Typography>
                  <Typography variant="body2">
                    Drag components from the palette on the left
                  </Typography>
                </Box>
              )}

              {/* Rendered Components */}
              <Box sx={{ position: 'relative', zIndex: 1 }}>
                {components.map((component) => (
                  <RenderedComponent
                    key={component.id}
                    component={component}
                    isSelected={selection.selectedId === component.id}
                    isHovered={selection.hoveredId === component.id}
                    onClick={handleComponentClick}
                    onHover={handleComponentHover}
                  />
                ))}
              </Box>
            </Paper>
          </SortableContext>
        </DndContext>
      </Box>
    </Box>
  );
});

BuilderCanvas.displayName = 'BuilderCanvas';

export default BuilderCanvas;
