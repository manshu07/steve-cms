/**
 * RenderedComponent - wraps core components with drag handles and selection state.
 */

import React, { memo, useCallback } from 'react';
import { Box } from '@mui/material';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { BuilderComponent } from '~types/index';
import { renderComponent } from '../Core';

interface RenderedComponentProps {
  component: BuilderComponent;
  isSelected?: boolean;
  isHovered?: boolean;
  onClick?: (id: string) => void;
  onHover?: (id: string | null) => void;
}

export const RenderedComponent: React.FC<RenderedComponentProps> = memo(({
  component,
  isSelected,
  isHovered,
  onClick,
  onHover,
}) => {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: component.id,
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const handleClick = useCallback(() => {
    onClick?.(component.id);
  }, [component.id, onClick]);

  const handleMouseEnter = useCallback(() => {
    onHover?.(component.id);
  }, [component.id, onHover]);

  const handleMouseLeave = useCallback(() => {
    onHover?.(null);
  }, [onHover]);

  const wrapperStyles = {
    position: 'relative' as const,
    mb: 2,
    ...style,
  };

  // Drag handle (visible on hover/selection)
  const dragHandle = isSelected || isHovered ? (
    <Box
      sx={{
        position: 'absolute',
        top: -12,
        left: 0,
        right: 0,
        height: 24,
        bgcolor: 'primary.main',
        color: 'primary.contrastText',
        borderRadius: '4px 4px 0 0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '0.75rem',
        fontWeight: 600,
        cursor: 'grab',
        userSelect: 'none',
        zIndex: 10,
        ...attributes,
        ...listeners,
      }}
    >
      {component.type}
    </Box>
  ) : null;

  return (
    <Box
      ref={setNodeRef}
      sx={wrapperStyles}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {dragHandle}
      {renderComponent(component.type, component.props as any, isSelected, handleClick)}
    </Box>
  );
});

RenderedComponent.displayName = 'RenderedComponent';

export default RenderedComponent;
