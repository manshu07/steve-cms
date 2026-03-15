/**
 * Columns component renderer.
 * Displays 2 or 3 column layouts.
 */

import React, { memo } from 'react';
import { Box, Grid } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { ColumnsProps } from '~types/index';

interface ColumnsRendererProps {
  props: ColumnsProps;
  isSelected?: boolean;
  onClick?: () => void;
  children?: React.ReactNode[];
}

export const Columns: React.FC<ColumnsRendererProps> = memo(
  ({ props, isSelected, onClick, children }) => {
    const { columns: columnCount, gap, styles = {} } = props;

    const columnStyles: SxProps<Theme> = {
      gap: gap || undefined,
      cursor: 'pointer',
      border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
      borderRadius: 1,
      transition: 'border-color 0.2s',
      p: 1,
      '&:hover': {
        borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
      },
      ...styles,
    };

    // Calculate grid size for each column
    const gridSize = Math.floor(12 / columnCount);

    return (
      <Box sx={columnStyles} onClick={onClick}>
        <Grid container spacing={2}>
          {Array.from({ length: columnCount }).map((_, index) => (
            <Grid size={{ xs: 12, md: gridSize }} key={index}>
              <Box
                sx={{
                  minHeight: 100,
                  border: '1px dashed',
                  borderColor: 'grey.300',
                  borderRadius: 1,
                  p: 2,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'text.secondary',
                }}
              >
                {children && children[index] ? (
                  children[index]
                ) : (
                  <Box>Column {index + 1}</Box>
                )}
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }
);

Columns.displayName = 'Columns';

export default Columns;
