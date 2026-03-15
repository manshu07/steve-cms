/**
 * Component Palette - displays draggable builder components.
 * Organized by category (content, form, layout, media).
 */

import React, { memo, useCallback, useMemo } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  TextField,
  InputAdornment,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { useDrag } from '@dnd-kit/core';
import type { ComponentRegistry, ComponentCategory } from '~types/index';
import { useBuilderStore } from '../../stores/useBuilderStore';

interface ComponentPaletteProps {
  components: ComponentRegistry[];
}

interface ComponentCardProps {
  component: ComponentRegistry;
}

const CATEGORY_LABELS: Record<ComponentCategory, string> = {
  content: 'Content',
  form: 'Form',
  layout: 'Layout',
  media: 'Media',
};

export const ComponentCard: React.FC<ComponentCardProps> = memo(({ component }) => {
  const { attributes, listeners, setNodeRef, isDragging } = useDrag({
    id: component.name,
    type: 'component',
    data: {
      component,
    },
  });

  const cardStyles = {
    cursor: 'grab',
    opacity: isDragging ? 0.5 : 1,
    userSelect: 'none' as const,
  };

  return (
    <Card
      ref={setNodeRef}
      sx={cardStyles}
      {...attributes}
      {...listeners}
    >
      <CardContent sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
          <Typography variant="h5">{component.icon}</Typography>
          <Typography variant="subtitle2" fontWeight={600}>
            {component.label}
          </Typography>
        </Box>
        <Typography variant="caption" color="text.secondary">
          {component.category}
        </Typography>
      </CardContent>
    </Card>
  );
});

ComponentCard.displayName = 'ComponentCard';

export const ComponentPalette: React.FC<ComponentPaletteProps> = memo(({ components }) => {
  const [searchQuery, setSearchQuery] = React.useState('');
  const [selectedCategory, setSelectedCategory] = React.useState<ComponentCategory | 'all'>('all');

  // Group components by category
  const componentsByCategory = useMemo(() => {
    const grouped: Record<string, ComponentRegistry[]> = {};

    components.forEach((component) => {
      const category = component.category;
      if (!grouped[category]) {
        grouped[category] = [];
      }
      grouped[category].push(component);
    });

    return grouped;
  }, [components]);

  // Filter components by search query
  const filteredComponents = useMemo(() => {
    if (!searchQuery) return components;

    const query = searchQuery.toLowerCase();
    return components.filter(
      (component) =>
        component.label.toLowerCase().includes(query) ||
        component.name.toLowerCase().includes(query) ||
        component.category.toLowerCase().includes(query)
    );
  }, [components, searchQuery]);

  const handleSearchChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(event.target.value);
  }, []);

  return (
    <Box
      sx={{
        width: 280,
        height: '100%',
        borderRight: 1,
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
      }}
    >
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" gutterBottom>
          Components
        </Typography>
        <TextField
          fullWidth
          size="small"
          placeholder="Search components..."
          value={searchQuery}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon fontSize="small" />
              </InputAdornment>
            ),
          }}
        />
      </Box>

      {/* Category Filter */}
      <Box sx={{ px: 2, py: 1, borderBottom: 1, borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
          <Button
            size="small"
            variant={selectedCategory === 'all' ? 'contained' : 'outlined'}
            onClick={() => setSelectedCategory('all')}
          >
            All
          </Button>
          {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
            <Button
              key={key}
              size="small"
              variant={selectedCategory === key ? 'contained' : 'outlined'}
              onClick={() => setSelectedCategory(key as ComponentCategory)}
            >
              {label}
            </Button>
          ))}
        </Box>
      </Box>

      {/* Components List */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {searchQuery ? (
          // Show search results
          <Grid container spacing={1}>
            {filteredComponents.map((component) => (
              <Grid size={12} key={component.id}>
                <ComponentCard component={component} />
              </Grid>
            ))}
          </Grid>
        ) : selectedCategory === 'all' ? (
          // Show all categories
          Object.entries(componentsByCategory).map(([category, categoryComponents]) => (
            <Box key={category} sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="text.secondary" gutterBottom sx={{ textTransform: 'uppercase', fontSize: '0.75rem', fontWeight: 600 }}>
                {CATEGORY_LABELS[category as ComponentCategory]}
              </Typography>
              <Grid container spacing={1}>
                {categoryComponents.map((component) => (
                  <Grid size={12} key={component.id}>
                    <ComponentCard component={component} />
                  </Grid>
                ))}
              </Grid>
            </Box>
          ))
        ) : (
          // Show selected category
          <Grid container spacing={1}>
            {componentsByCategory[selectedCategory]?.map((component) => (
              <Grid size={12} key={component.id}>
                <ComponentCard component={component} />
              </Grid>
            ))}
          </Grid>
        )}
      </Box>
    </Box>
  );
});

ComponentPalette.displayName = 'ComponentPalette';

export default ComponentPalette;
