/**
 * Property Editor - edit selected component properties.
 * Displays form fields based on component schema.
 */

import React, { memo, useCallback, useMemo } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  Button,
  Divider,
  Stack,
} from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';
import type { ComponentSchema, PropertySchema, BuilderComponent } from '~types/index';
import { useBuilderStore } from '../../stores/useBuilderStore';

interface PropertyEditorProps {
  component: BuilderComponent;
  schema: ComponentSchema;
}

export const PropertyEditor: React.FC<PropertyEditorProps> = memo(({ component, schema }) => {
  const { updateComponent, deleteComponent, clearSelection } = useBuilderStore();

  // Handle property change
  const handlePropertyChange = useCallback((propertyName: string, value: any) => {
    updateComponent(component.id, {
      props: {
        ...component.props,
        [propertyName]: value,
      },
    });
  }, [component.id, component.props, updateComponent]);

  // Handle style change
  const handleStyleChange = useCallback((styleProperty: string, value: any) => {
    updateComponent(component.id, {
      props: {
        ...component.props,
        styles: {
          ...component.props.styles,
          [styleProperty]: value,
        },
      },
    });
  }, [component.id, component.props, updateComponent]);

  // Handle delete
  const handleDelete = useCallback(() => {
    if (window.confirm('Are you sure you want to delete this component?')) {
      deleteComponent(component.id);
      clearSelection();
    }
  }, [component.id, deleteComponent, clearSelection]);

  // Render property input based on schema
  const renderPropertyInput = useCallback((
    propertyName: string,
    propertySchema: PropertySchema,
    value: any
  ) => {
    const commonProps = {
      fullWidth: true,
      size: 'small' as const,
      margin: 'dense' as const,
    };

    switch (propertySchema.type) {
      case 'string':
        if (propertySchema.enum) {
          // Select dropdown
          return (
            <FormControl {...commonProps} key={propertyName}>
              <InputLabel>{propertySchema.title}</InputLabel>
              <Select
                value={value || propertySchema.default || ''}
                label={propertySchema.title}
                onChange={(e) => handlePropertyChange(propertyName, e.target.value)}
              >
                {propertySchema.enum.map((enumValue) => (
                  <MenuItem key={enumValue} value={enumValue}>
                    {enumValue}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          );
        }
        // Text input
        return (
          <TextField
            key={propertyName}
            label={propertySchema.title}
            value={value || propertySchema.default || ''}
            onChange={(e) => handlePropertyChange(propertyName, e.target.value)}
            helperText={propertySchema.description}
            {...commonProps}
          />
        );

      case 'number':
      case 'integer':
        return (
          <TextField
            key={propertyName}
            label={propertySchema.title}
            type="number"
            value={value || propertySchema.default || 0}
            onChange={(e) => handlePropertyChange(propertyName, parseInt(e.target.value))}
            helperText={propertySchema.description}
            {...commonProps}
          />
        );

      case 'boolean':
        return (
          <Stack
            key={propertyName}
            direction="row"
            spacing={1}
            alignItems="center"
            sx={{ mt: 1 }}
          >
            <Typography variant="body2">{propertySchema.title}</Typography>
            <Switch
              checked={value || propertySchema.default || false}
              onChange={(e) => handlePropertyChange(propertyName, e.target.checked)}
            />
          </Stack>
        );

      default:
        return (
          <TextField
            key={propertyName}
            label={propertySchema.title}
            value={JSON.stringify(value) || ''}
            disabled
            helperText={`Unsupported type: ${propertySchema.type}`}
            {...commonProps}
          />
        );
    }
  }, [handlePropertyChange]);

  // Get all properties from schema
  const properties = useMemo(() => {
    return Object.entries(schema.properties || {});
  }, [schema.properties]);

  return (
    <Box
      sx={{
        width: 320,
        height: '100%',
        borderLeft: 1,
        borderColor: 'divider',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.paper',
      }}
    >
      {/* Header */}
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
        <Typography variant="h6" gutterBottom>
          Properties
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {component.type}
        </Typography>
      </Box>

      {/* Properties Form */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
        {/* Component Properties */}
        <Typography variant="subtitle2" gutterBottom sx={{ mt: 2, mb: 1 }}>
          Component Properties
        </Typography>

        {properties.map(([propertyName, propertySchema]) => {
          const value = component.props[propertyName];
          return (
            <Box key={propertyName} sx={{ mb: 1 }}>
              {renderPropertyInput(propertyName, propertySchema, value)}
            </Box>
          );
        })}

        <Divider sx={{ my: 2 }} />

        {/* Styles */}
        <Typography variant="subtitle2" gutterBottom sx={{ mt: 2, mb: 1 }}>
          Styles
        </Typography>

        <TextField
          fullWidth
          size="small"
          label="Grid Span (1-12)"
          type="number"
          value={component.props.styles?.gridSpan || 12}
          onChange={(e) => handleStyleChange('gridSpan', parseInt(e.target.value))}
          inputProps={{ min: 1, max: 12 }}
          sx={{ mb: 1 }}
        />

        <TextField
          fullWidth
          size="small"
          label="Padding"
          value={component.props.styles?.padding || ''}
          onChange={(e) => handleStyleChange('padding', e.target.value)}
          sx={{ mb: 1 }}
        />

        <TextField
          fullWidth
          size="small"
          label="Margin"
          value={component.props.styles?.margin || ''}
          onChange={(e) => handleStyleChange('margin', e.target.value)}
          sx={{ mb: 1 }}
        />

        <TextField
          fullWidth
          size="small"
          label="Background Color"
          value={component.props.styles?.background || ''}
          onChange={(e) => handleStyleChange('background', e.target.value)}
          sx={{ mb: 1 }}
        />
      </Box>

      {/* Footer Actions */}
      <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
        <Button
          fullWidth
          variant="outlined"
          color="error"
          startIcon={<DeleteIcon />}
          onClick={handleDelete}
        >
          Delete Component
        </Button>
      </Box>
    </Box>
  );
});

PropertyEditor.displayName = 'PropertyEditor';

export default PropertyEditor;
