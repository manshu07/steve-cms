/**
 * Divider component renderer.
 * Displays horizontal or vertical separators.
 */

import React, { memo } from 'react';
import { Divider as MuiDivider, Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { DividerProps } from '~types/index';

interface DividerRendererProps {
  props: DividerProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Divider: React.FC<DividerRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { orientation, thickness, color, styles = {} } = props;

  const dividerStyles: SxProps<Theme> = {
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    py: 1,
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
    },
    ...styles,
  };

  return (
    <Box sx={dividerStyles} onClick={onClick}>
      <MuiDivider
        orientation={orientation}
        flexItem={orientation === 'vertical'}
        sx={{
          borderColor: color,
          borderBottomWidth: thickness,
        }}
      />
    </Box>
  );
});

Divider.displayName = 'Divider';

export default Divider;
