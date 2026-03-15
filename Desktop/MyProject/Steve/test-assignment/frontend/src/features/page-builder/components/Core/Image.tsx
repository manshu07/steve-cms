/**
 * Image component renderer.
 * Displays responsive images with alignment options.
 */

import React, { memo } from 'react';
import { Box } from '@mui/material';
import type { SxProps, Theme } from '@mui/material';
import type { ImageProps } from '~types/index';
import { ImageUploader } from '../Assets/ImageUploader';

interface ImageRendererProps {
  props: ImageProps;
  isSelected?: boolean;
  onClick?: () => void;
  onUpdate?: (props: ImageProps) => void;
}

export const Image: React.FC<ImageRendererProps> = memo(({ props, isSelected, onClick, onUpdate }) => {
  const { url, alt_text, width, align, styles = {} } = props;

  const imageStyles: SxProps<Theme> = {
    display: 'block',
    maxWidth: width || '100%',
    height: 'auto',
    mx: align === 'center' ? 'auto' : align === 'right' ? 'auto' : 0,
    cursor: 'pointer',
    border: isSelected ? '2px solid #1976d2' : '2px solid transparent',
    borderRadius: 1,
    transition: 'border-color 0.2s',
    '&:hover': {
      borderColor: isSelected ? undefined : 'rgba(25, 118, 210, 0.5)',
    },
  };

  const handleImageSelect = useCallback((imageUrl: string, altText?: string) => {
    onUpdate?.({
      ...props,
      url: imageUrl,
      alt_text: altText || '',
    });
  }, [props, onUpdate]);

  if (isSelected) {
    return (
      <Box sx={imageStyles}>
        <ImageUploader
          currentImage={url}
          onImageSelect={handleImageSelect}
        />
      </Box>
    );
  }

  if (!url) {
    return (
      <Box
        sx={{
          ...imageStyles,
          width: width || '100%',
          height: 200,
          bgcolor: 'grey.200',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'text.secondary',
        }}
        onClick={onClick}
      >
        No image selected
      </Box>
    );
  }

  return (
    <Box component="img" src={url} alt={alt_text || ''} sx={imageStyles} onClick={onClick} />
  );
});

Image.displayName = 'Image';

export default Image;
