/**
 * Quote component renderer.
 * Displays testimonials with author attribution.
 */

import React, { memo } from 'react';
import { Typography, Box, Paper } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import { FormatQuote as QuoteIcon } from '@mui/icons-material';
import type { QuoteProps } from '~types/index';

interface QuoteRendererProps {
  props: QuoteProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Quote: React.FC<QuoteRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { text, author, align, styles = {} } = props;

  const quoteStyles: SxProps<Theme> = {
    p: styles.padding || 3,
    fontStyle: 'italic',
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
    <Paper sx={quoteStyles} onClick={onClick} elevation={1}>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: align === 'center' ? 'center' : 'flex-start' }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
          <QuoteIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Box sx={{ flex: 1 }}>
            <Typography variant="body1" component="blockquote" sx={{ mb: author ? 1 : 0 }}>
              {text}
            </Typography>
            {author && (
              <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
                — {author}
              </Typography>
            )}
          </Box>
        </Box>
      </Box>
    </Paper>
  );
});

Quote.displayName = 'Quote';

export default Quote;
