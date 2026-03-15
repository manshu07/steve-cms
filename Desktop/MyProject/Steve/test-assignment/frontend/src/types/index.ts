/**
 * Type definitions for the drag/drop page builder.
 */

import type { CSSProperties } from 'react';

// ============================================================
// COMPONENT REGISTRY TYPES
// ============================================================

export type ComponentCategory = 'content' | 'form' | 'layout' | 'media';

export interface ComponentSchema {
  type: 'object';
  properties: Record<string, PropertySchema>;
}

export interface PropertySchema {
  type: 'string' | 'number' | 'boolean' | 'integer' | 'array';
  title: string;
  default?: any;
  enum?: string[];
  description?: string;
}

export interface ComponentStyle {
  gridSpan?: number;
  padding?: string;
  margin?: string;
  background?: string;
  textAlign?: 'left' | 'center' | 'right';
  [key: string]: any;
}

export interface ComponentProps {
  type: string;
  [key: string]: any;
  styles?: ComponentStyle;
}

export interface ComponentRegistry {
  id: number;
  name: string;
  label: string;
  category: ComponentCategory;
  icon: string;
  schema: ComponentSchema;
  default_props: ComponentProps;
  is_enabled: boolean;
  requires_asset: boolean;
  is_editable: boolean;
  render_component: string;
  order: number;
}

// ============================================================
// BUILDER STATE TYPES
// ============================================================

export interface BuilderComponent {
  id: string;
  type: string;
  props: ComponentProps;
  children?: BuilderComponent[];
  parentId?: string;
  index?: number;
}

export interface BuilderPage {
  id: number;
  title: string;
  slug: string;
  builder_data: BuilderData;
  builder_settings?: BuilderPageSettings;
}

export interface BuilderData {
  components: BuilderComponent[];
  settings: BuilderSettings;
  version: number;
}

export interface BuilderSettings {
  viewport: ViewportMode;
  breakpoints: {
    mobile: number;
    tablet: number;
  };
}

export type ViewportMode = 'desktop' | 'tablet' | 'mobile';

export interface BuilderPageSettings {
  grid_enabled: boolean;
  snap_to_grid: boolean;
  grid_size: number;
  current_viewport: ViewportMode;
  show_rulers: boolean;
  show_outlines: boolean;
}

// ============================================================
// CANVAS TYPES
// ============================================================

export interface CanvasPosition {
  x: number;
  y: number;
}

export interface DragHandle {
  componentId: string;
  type: 'move' | 'resize';
}

export interface SelectionState {
  selectedId: string | null;
  hoveredId: string | null;
  isDragging: boolean;
}

// ============================================================
// PROPERTY EDITOR TYPES
// ============================================================

export interface PropertyEditorProps {
  component: BuilderComponent;
  schema: ComponentSchema;
  onChange: (props: ComponentProps) => void;
}

export interface PropertyInfo {
  name: string;
  schema: PropertySchema;
  value: any;
}

// ============================================================
// HISTORY TYPES (UNDO/REDO)
// ============================================================

export interface HistoryState {
  past: BuilderData[];
  present: BuilderData;
  future: BuilderData[];
}

export interface HistoryAction {
  type: 'UNDO' | 'REDO' | 'SAVE';
  payload?: BuilderData;
}

// ============================================================
// API RESPONSE TYPES
// ============================================================

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface ComponentRegistryResponse {
  success: boolean;
  components: ComponentRegistry[];
}

export interface BuilderPageResponse {
  success: boolean;
  page: BuilderPage;
}

// ============================================================
// COMPONENT-SPECIFIC PROP TYPES
// ============================================================

export interface HeadingProps extends ComponentProps {
  type: 'heading';
  text: string;
  level: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  align: 'left' | 'center' | 'right';
  styles: ComponentStyle;
}

export interface TextProps extends ComponentProps {
  type: 'text';
  content: string;
  styles: ComponentStyle;
}

export interface ButtonProps extends ComponentProps {
  type: 'button';
  text: string;
  variant: 'primary' | 'secondary' | 'text';
  url: string;
  open_new_tab: boolean;
  styles: ComponentStyle;
}

export interface ImageProps extends ComponentProps {
  type: 'image';
  url: string;
  alt_text: string;
  width: number;
  align: 'left' | 'center' | 'right';
  styles: ComponentStyle;
}

export interface ContainerProps extends ComponentProps {
  type: 'container';
  background_color: string;
  padding: string;
  boxed: boolean;
  styles: ComponentStyle;
}

export interface ColumnsProps extends ComponentProps {
  type: 'columns';
  columns: 2 | 3;
  gap: string;
  styles: ComponentStyle;
}

export interface DividerProps extends ComponentProps {
  type: 'divider';
  orientation: 'horizontal' | 'vertical';
  thickness: number;
  color: string;
  styles: ComponentStyle;
}

export interface SpacerProps extends ComponentProps {
  type: 'spacer';
  height: string;
  styles: ComponentStyle;
}

export interface QuoteProps extends ComponentProps {
  type: 'quote';
  text: string;
  author: string;
  align: 'left' | 'center' | 'right';
  styles: ComponentStyle;
}

export interface FormProps extends ComponentProps {
  type: 'form';
  form_title: string;
  submit_button_text: string;
  success_message: string;
  styles: ComponentStyle;
}

// ============================================================
// UTILITY TYPES
// ============================================================

export type ComponentPropsType =
  | HeadingProps
  | TextProps
  | ButtonProps
  | ImageProps
  | ContainerProps
  | ColumnsProps
  | DividerProps
  | SpacerProps
  | QuoteProps
  | FormProps;

export type ComponentByName = {
  [K in ComponentRegistry['name']]: Extract<ComponentPropsType, { type: K }>;
};
