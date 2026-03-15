/**
 * Form Container component renderer.
 * Displays form wrapper with title and submit button.
 */

import React, { memo } from 'react';
import { Typography, Box, Paper, TextField, Button } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { FormProps } from '~types/index';

interface FormRendererProps {
  props: FormProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Form: React.FC<FormRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { form_title, submit_button_text, success_message, styles = {} } = props;

  const formStyles: SxProps<Theme> = {
    p: styles.padding || 3,
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
    },
    ...styles,
  };

  return (
    <Paper sx={formStyles} onClick={onClick} elevation={1}>
      <Box component="form">
        <Typography variant="h6" gutterBottom>
          {form_title}
        </Typography>

        {/* Sample form fields - in production, these would be dynamic */}
        <TextField
          fullWidth
          label="Name"
          variant="outlined"
          margin="normal"
          size="small"
          disabled
        />
        <TextField
          fullWidth
          label="Email"
          variant="outlined"
          margin="normal"
          size="small"
          disabled
        />
        <TextField
          fullWidth
          label="Message"
          variant="outlined"
          margin="normal"
          size="small"
          multiline
          rows={3}
          disabled
        />

        <Button variant="contained" sx={{ mt: 2 }} disabled>
          {submit_button_text}
        </Button>

        {success_message && (
          <Typography variant="caption" color="success.main" sx={{ display: 'block', mt: 1 }}>
            {success_message}
          </Typography>
        )}
      </Box>
    </Paper>
  );
});

Form.displayName = 'Form';

export default Form;
