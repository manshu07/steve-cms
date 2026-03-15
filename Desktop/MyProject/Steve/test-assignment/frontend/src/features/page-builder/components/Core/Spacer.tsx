/**
 * Spacer component renderer.
 * Displays vertical spacing control.
 */

import React, { memo } from 'react';
import { Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { SpacerProps } from '~types/index';

interface SpacerRendererProps {
  props: SpacerProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Spacer: React.FC<SpacerRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { height, styles = {} } = props;

  const spacerStyles: SxProps<Theme> = {
    height: height || '20px',
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px dashed transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    bgcolor: 'action.hover',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '0.75rem',
    color: 'text.secondary',
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
      bgcolor: 'action.selected',
    },
    ...styles,
  };

  return (
    <Box sx={spacerStyles} onClick={onClick}>
      {height}
    </Box>
  );
});

Spacer.displayName = 'Spacer';

export default Spacer;
