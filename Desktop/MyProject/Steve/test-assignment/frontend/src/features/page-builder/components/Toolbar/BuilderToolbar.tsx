/**
 * Builder Toolbar - top bar with viewport switching, undo/redo, and actions.
 */

import React, { memo, useCallback } from 'react';
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Stack,
  Divider,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Undo as UndoIcon,
  Redo as RedoIcon,
  Save as SaveIcon,
  ViewDesktop as DesktopIcon,
  ViewTablet as TabletIcon,
  ViewMobile as MobileIcon,
  GridOn as GridIcon,
  MoreVert as MoreIcon,
} from '@mui/icons-material';
import type { ViewportMode } from '~types/index';
import { useBuilderStore } from '../../stores/useBuilderStore';

interface BuilderToolbarProps {
  pageId?: number;
  pageName?: string;
  onSave?: () => void;
  onPublish?: () => void;
}

const VIEWPORT_OPTIONS: { value: ViewportMode; label: string; icon: React.ElementType }[] = [
  { value: 'desktop', label: 'Desktop', icon: DesktopIcon },
  { value: 'tablet', label: 'Tablet', icon: TabletIcon },
  { value: 'mobile', label: 'Mobile', icon: MobileIcon },
];

export const BuilderToolbar: React.FC<BuilderToolbarProps> = memo(({
  pageId,
  pageName = 'Untitled Page',
  onSave,
  onPublish,
}) => {
  const {
    canvasSettings,
    selection,
    undo,
    redo,
    canUndo,
    canRedo,
    setViewport,
    toggleGrid,
    clearSelection,
  } = useBuilderStore();

  const [menuAnchor, setMenuAnchor] = React.useState<null | HTMLElement>(null);

  // Handle viewport change
  const handleViewportChange = useCallback((viewport: ViewportMode) => {
    setViewport(viewport);
  }, [setViewport]);

  // Handle undo
  const handleUndo = useCallback(() => {
    undo();
  }, [undo]);

  // Handle redo
  const handleRedo = useCallback(() => {
    redo();
  }, [redo]);

  // Handle save
  const handleSave = useCallback(() => {
    onSave?.();
  }, [onSave]);

  // Handle publish
  const handlePublish = useCallback(() => {
    onPublish?.();
  }, [onPublish]);

  // Handle menu open
  const handleMenuOpen = useCallback((event: React.MouseEvent<HTMLElement>) => {
    setMenuAnchor(event.currentTarget);
  }, []);

  // Handle menu close
  const handleMenuClose = useCallback(() => {
    setMenuAnchor(null);
  }, []);

  // Handle clear selection
  const handleClearSelection = useCallback(() => {
    clearSelection();
  }, [clearSelection]);

  return (
    <AppBar position="static" elevation={1} color="default">
      <Toolbar variant="dense">
        {/* Left Section - Page Title */}
        <Box sx={{ flexGrow: 0, mr: 2 }}>
          <Typography variant="h6" noWrap component="div">
            {pageName}
          </Typography>
        </Box>

        <Divider orientation="vertical" flexItem sx={{ mx: 1 }} />

        {/* Middle Section - Viewport & Tools */}
        <Stack direction="row" spacing={1} alignItems="center" sx={{ flexGrow: 1 }}>
          {/* Viewport Switcher */}
          <Stack direction="row" spacing={0.5}>
            {VIEWPORT_OPTIONS.map((option) => {
              const Icon = option.icon;
              return (
                <IconButton
                  key={option.value}
                  size="small"
                  color={canvasSettings.currentViewport === option.value ? 'primary' : 'default'}
                  onClick={() => handleViewportChange(option.value)}
                  title={option.label}
                >
                  <Icon fontSize="small" />
                </IconButton>
              );
            })}
          </Stack>

          <Divider orientation="vertical" flexItem />

          {/* Undo/Redo */}
          <Stack direction="row" spacing={0.5}>
            <IconButton
              size="small"
              onClick={handleUndo}
              disabled={!canUndo()}
              title="Undo (Ctrl+Z)"
            >
              <UndoIcon fontSize="small" />
            </IconButton>
            <IconButton
              size="small"
              onClick={handleRedo}
              disabled={!canRedo()}
              title="Redo (Ctrl+Y)"
            >
              <RedoIcon fontSize="small" />
            </IconButton>
          </Stack>

          <Divider orientation="vertical" flexItem />

          {/* Grid Toggle */}
          <IconButton
            size="small"
            color={canvasSettings.gridEnabled ? 'primary' : 'default'}
            onClick={toggleGrid}
            title="Toggle Grid"
          >
            <GridIcon fontSize="small" />
          </IconButton>
        </Stack>

        {/* Right Section - Actions */}
        <Stack direction="row" spacing={1} alignItems="center" sx={{ flexGrow: 0 }}>
          {/* Selection Info */}
          {selection.selectedId && (
            <>
              <Typography variant="caption" color="text.secondary">
                {selection.selectedId.slice(0, 8)}...
              </Typography>
              <Button size="small" onClick={handleClearSelection}>
                Clear
              </Button>
              <Divider orientation="vertical" flexItem />
            </>
          )}

          {/* Save & Publish */}
          <Button
            size="small"
            variant="outlined"
            startIcon={<SaveIcon />}
            onClick={handleSave}
          >
            Save
          </Button>
          <Button
            size="small"
            variant="contained"
            color="primary"
            onClick={handlePublish}
          >
            Publish
          </Button>

          {/* More Menu */}
          <IconButton
            size="small"
            onClick={handleMenuOpen}
          >
            <MoreIcon />
          </IconButton>
          <Menu
            anchorEl={menuAnchor}
            open={Boolean(menuAnchor)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={() => { handleMenuClose(); window.open('/preview', '_blank'); }}>
              Preview
            </MenuItem>
            <MenuItem onClick={() => { handleMenuClose(); console.log('Export...'); }}>
              Export HTML
            </MenuItem>
            <MenuItem onClick={() => { handleMenuClose(); console.log('Settings...'); }}>
              Page Settings
            </MenuItem>
          </Menu>
        </Stack>
      </Toolbar>
    </AppBar>
  );
});

BuilderToolbar.displayName = 'BuilderToolbar';

export default BuilderToolbar;
