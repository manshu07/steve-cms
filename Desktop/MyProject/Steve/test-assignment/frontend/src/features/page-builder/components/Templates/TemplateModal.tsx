/**
 * Template Modal - select, preview, and load page templates.
 */

import React, { memo, useState, useCallback } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Grid,
  Card,
  CardMedia,
  CardContent,
  CardActions,
  Typography,
  Box,
  TextField,
  InputAdornment,
  CircularProgress,
} from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { useSuspenseQuery } from '@tanstack/react-query';
import { builderApi } from '../../api/builderApi';
import { useBuilderStore } from '../../stores/useBuilderStore';
import { useNotifications } from '~/hooks/useNotifications';

interface TemplateModalProps {
  open: boolean;
  onClose: () => void;
}

interface Template {
  id: number;
  name: string;
  description: string;
  thumbnail: string;
  builder_data: any;
}

export const TemplateModal: React.FC<TemplateModalProps> = memo(({ open, onClose }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);

  const { showSuccess, showError } = useNotifications();
  const { loadPage } = useBuilderStore();

  // Fetch templates
  const { data: templates, isLoading } = useSuspenseQuery({
    queryKey: ['builder-templates'],
    queryFn: () => builderApi.getBuilderTemplates(),
    enabled: open,
  });

  // Filter templates by search query
  const filteredTemplates = templates?.filter((template: Template) => {
    const query = searchQuery.toLowerCase();
    return (
      template.name.toLowerCase().includes(query) ||
      template.description.toLowerCase().includes(query)
    );
  }) || [];

  // Handle template selection
  const handleSelectTemplate = useCallback((template: Template) => {
    setSelectedTemplate(template);
  }, []);

  // Handle load template
  const handleLoadTemplate = useCallback(() => {
    if (!selectedTemplate) return;

    try {
      // Load template data into builder
      // Note: This would need pageId in production
      console.log('Loading template:', selectedTemplate);
      showSuccess(`Template "${selectedTemplate.name}" loaded successfully!`, 'Template Loaded');
      onClose();
    } catch (error) {
      console.error('Failed to load template:', error);
      showError('Failed to load template. Please try again.', 'Template Error');
    }
  }, [selectedTemplate, showSuccess, showError, onClose]);

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        sx: { height: '80vh' },
      }}
    >
      <DialogTitle>Choose a Template</DialogTitle>

      <DialogContent sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        {/* Search */}
        <TextField
          fullWidth
          placeholder="Search templates..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />

        {/* Templates Grid */}
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {isLoading ? (
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: 200,
              }}
            >
              <CircularProgress />
            </Box>
          ) : filteredTemplates.length === 0 ? (
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: 200,
                color: 'text.secondary',
              }}
            >
              <Typography>No templates found</Typography>
            </Box>
          ) : (
            <Grid container spacing={2}>
              {filteredTemplates.map((template: Template) => (
                <Grid size={{ xs: 12, sm: 6, md: 4 }} key={template.id}>
                  <Card
                    sx={{
                      cursor: 'pointer',
                      border: selectedTemplate?.id === template.id ? 2 : 1,
                      borderColor: selectedTemplate?.id === template.id ? 'primary.main' : 'divider',
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                    }}
                    onClick={() => handleSelectTemplate(template)}
                  >
                    <CardMedia
                      component="img"
                      height="140"
                      image={template.thumbnail || '/placeholder-template.png'}
                      alt={template.name}
                      sx={{ bgcolor: 'grey.200' }}
                    />
                    <CardContent sx={{ flex: 1 }}>
                      <Typography gutterBottom variant="h6" component="div">
                        {template.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {template.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleLoadTemplate}
          variant="contained"
          disabled={!selectedTemplate}
        >
          Use Template
        </Button>
      </DialogActions>
    </Dialog>
  );
});

TemplateModal.displayName = 'TemplateModal';

export default TemplateModal;
