/**
 * Text Paragraph component renderer.
 * Displays rich text content.
 */

import React, { memo } from 'react';
import { Typography, Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { TextProps } from '~types/index';

interface TextRendererProps {
  props: TextProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Text: React.FC<TextRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { content, styles = {} } = props;

  const textStyles: SxProps<Theme> = {
    p: styles.padding || undefined,
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
    },
  };

  return (
    <Box sx={textStyles} onClick={onClick}>
      <Typography variant="body1" component="p">
        {content}
      </Typography>
    </Box>
  );
});

Text.displayName = 'Text';

export default Text;
