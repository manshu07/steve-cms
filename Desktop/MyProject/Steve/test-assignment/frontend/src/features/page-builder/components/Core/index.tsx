/**
 * Core component renderers registry.
 * Maps component names to their React renderer components.
 */

import { Heading } from './Heading';
import { Text } from './Text';
import { Button } from './Button';
import { Image } from './Image';
import { Container } from './Container';
import { Columns } from './Columns';
import { Divider } from './Divider';
import { Spacer } from './Spacer';
import { Quote } from './Quote';
import { Form } from './Form';
import type { ComponentPropsType } from '~types/index';

// Component registry mapping
export const CORE_COMPONENTS = {
  heading: Heading,
  text: Text,
  button: Button,
  image: Image,
  container: Container,
  columns: Columns,
  divider: Divider,
  spacer: Spacer,
  quote: Quote,
  form: Form,
} as const;

export type ComponentName = keyof typeof CORE_COMPONENTS;

/**
 * Get renderer component by name.
 */
export const getComponentRenderer = (name: string) => {
  return CORE_COMPONENTS[name as ComponentName];
};

/**
 * Render component by type with props.
 */
export const renderComponent = (
  type: string,
  props: ComponentPropsType,
  isSelected?: boolean,
  onClick?: () => void,
  children?: React.ReactNode
) => {
  const Component = getComponentRenderer(type);

  if (!Component) {
    console.warn(`No renderer found for component type: ${type}`);
    return null;
  }

  return <Component key={props.id} props={props as any} isSelected={isSelected} onClick={onClick}>
    {children}
  </Component>;
};

// Export all components
export { Heading, Text, Button, Image, Container, Columns, Divider, Spacer, Quote, Form };
export default CORE_COMPONENTS;
