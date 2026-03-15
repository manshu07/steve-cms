/**
 * Heading component renderer.
 * Displays H1-H6 headings with alignment options.
 */

import React, { memo } from 'react';
import { Typography, Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { HeadingProps } from '~types/index';

interface HeadingRendererProps {
  props: HeadingProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Heading: React.FC<HeadingRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { text, level, align, styles = {} } = props;

  const headingStyles: SxProps<Theme> = {
    p: styles.padding || undefined,
    textAlign: align,
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
    },
  };

  const headingVariant = `h${level.slice(1)}` as const;

  return (
    <Box sx={headingStyles} onClick={onClick}>
      <Typography variant={headingVariant} component={level}>
        {text}
      </Typography>
    </Box>
  );
});

Heading.displayName = 'Heading';

export default Heading;
