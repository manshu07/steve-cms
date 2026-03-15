/**
 * Page Builder Feature - Public API exports
 */

// Main Component
export { PageBuilder } from './PageBuilder';

// Core Components
export {
  CORE_COMPONENTS,
  getComponentRenderer,
  renderComponent,
  Heading,
  Text,
  Button,
  Image,
  Container,
  Columns,
  Divider,
  Spacer,
  Quote,
  Form,
} from './components/Core';

// UI Components
export { ComponentPalette } from './components/Palette/ComponentPalette';
export { BuilderCanvas } from './components/Canvas/BuilderCanvas';
export { RenderedComponent } from './components/Canvas/RenderedComponent';
export { PropertyEditor } from './components/Properties/PropertyEditor';
export { BuilderToolbar } from './components/Toolbar/BuilderToolbar';

// Store
export { useBuilderStore } from './stores/useBuilderStore';
export { selectComponentById, selectSelectedComponent, selectComponentsByParent } from './stores/useBuilderStore';

// API
export { builderApi } from './api/builderApi';

// Types
export type {
  ComponentCategory,
  ComponentSchema,
  PropertySchema,
  ComponentStyle,
  ComponentProps,
  ComponentRegistry,
  BuilderComponent,
  BuilderPage,
  BuilderData,
  BuilderSettings,
  ViewportMode,
  BuilderPageSettings,
  CanvasPosition,
  DragHandle,
  SelectionState,
  PropertyEditorProps,
  PropertyInfo,
  HistoryState,
  HistoryAction,
  ApiResponse,
  ComponentRegistryResponse,
  BuilderPageResponse,
  ComponentPropsType,
  HeadingProps,
  TextProps,
  ButtonProps,
  ImageProps,
  ContainerProps,
  ColumnsProps,
  DividerProps,
  SpacerProps,
  QuoteProps,
  FormProps,
} from '~types/index';
