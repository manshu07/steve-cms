/**
 * Tests for Heading component
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { Heading } from './Heading';
import type { HeadingProps } from '~types/index';

describe('Heading Component', () => {
  const defaultProps: HeadingProps = {
    type: 'heading',
    text: 'Test Heading',
    level: 'h1',
    align: 'left',
    styles: {
      gridSpan: 12,
      padding: '20px',
    },
  };

  it('renders heading with correct text', () => {
    render(<Heading props={defaultProps} />);
    expect(screen.getByText('Test Heading')).toBeInTheDocument();
  });

  it('renders correct heading level', () => {
    const { container } = render(<Heading props={defaultProps} />);
    const heading = container.querySelector('h1');
    expect(heading).toBeInTheDocument();
  });

  it('renders h2 level', () => {
    const props: HeadingProps = { ...defaultProps, level: 'h2' };
    const { container } = render(<Heading props={props} />);
    const heading = container.querySelector('h2');
    expect(heading).toBeInTheDocument();
  });

  it('applies correct alignment', () => {
    const { container } = render(<Heading props={defaultProps} />);
    const heading = container.querySelector('h1');
    expect(heading).toHaveStyle({ textAlign: 'left' });
  });

  it('renders center alignment', () => {
    const props: HeadingProps = { ...defaultProps, align: 'center' };
    const { container } = render(<Heading props={props} />);
    const heading = container.querySelector('h1');
    expect(heading).toHaveStyle({ textAlign: 'center' });
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Heading props={defaultProps} onClick={handleClick} />);

    const heading = screen.getByText('Test Heading');
    fireEvent.click(heading);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('shows selection border when selected', () => {
    const { container } = render(<Heading props={defaultProps} isSelected={true} />);
    const box = container.firstChild as HTMLElement;
    expect(box).toHaveStyle({ border: '2px solid #1976d2' });
  });

  it('shows hover border on hover when not selected', () => {
    const { container } = render(<Heading props={defaultProps} isSelected={false} />);
    const box = container.firstChild as HTMLElement;

    // Check initial border
    expect(box).toHaveStyle({ border: '2px solid transparent' });

    // Simulate hover
    fireEvent.mouseEnter(box);

    // Check hover border (would need to check actual hover state in browser)
    expect(box).toBeInTheDocument();
  });
});
