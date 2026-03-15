/**
 * Container component renderer.
 * Displays boxed or full-width containers with background color.
 */

import React, { memo } from 'react';
import { Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { ContainerProps } from '~types/index';

interface ContainerRendererProps {
  props: ContainerProps;
  isSelected?: boolean;
  onClick?: () => void;
  children?: React.ReactNode;
}

export const Container: React.FC<ContainerRendererProps> = memo(
  ({ props, isSelected, onClick, children }) => {
    const { background_color, padding, boxed, styles = {} } = props;

    const containerStyles: SxProps<Theme> = {
      bgcolor: background_color,
      p: padding || undefined,
      maxWidth: boxed ? 'lg' : '100%',
      mx: boxed ? 'auto' : 0,
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
      <Box sx={containerStyles} onClick={onClick}>
        {children}
      </Box>
    );
  }
);

Container.displayName = 'Container';

export default Container;
