/**
 * Button component renderer.
 * Displays CTA buttons with different variants.
 */

import React, { memo } from 'react';
import { Button as MuiButton, Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { ButtonProps } from '~types/index';

interface ButtonRendererProps {
  props: ButtonProps;
  isSelected?: boolean;
  onClick?: () => void;
}

export const Button: React.FC<ButtonRendererProps> = memo(({ props, isSelected, onClick }) => {
  const { text, variant, url, open_new_tab, styles = {} } = props;

  const buttonStyles: SxProps<Theme> = {
    display: 'inline-block',
    p: styles.padding || undefined,
    textAlign: styles.textAlign || undefined,
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
    },
  };

  const muiVariant = variant === 'text' ? 'text' : variant === 'secondary' ? 'outlined' : 'contained';

  return (
    <Box sx={buttonStyles} onClick={onClick}>
      <MuiButton
        variant={muiVariant}
        href={url}
        target={open_new_tab ? '_blank' : undefined}
        rel={open_new_tab ? 'noopener noreferrer' : undefined}
      >
        {text}
      </MuiButton>
    </Box>
  );
});

Button.displayName = 'Button';

export default Button;
