/**
 * Tests for useBuilderStore
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useBuilderStore } from './useBuilderStore';
import type { BuilderComponent, ComponentRegistry } from '~types/index';

describe('useBuilderStore', () => {
  beforeEach(() => {
    // Reset store before each test
    const { result } = renderHook(() => useBuilderStore());
    act(() => {
      result.current.resetBuilder();
    });
  });

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useBuilderStore());

    expect(result.current.builderData.components).toEqual([]);
    expect(result.current.selection.selectedId).toBeNull();
    expect(result.current.history.past).toHaveLength(0);
    expect(result.current.history.future).toHaveLength(0);
  });

  it('adds component to canvas', () => {
    const { result } = renderHook(() => useBuilderStore());

    const component: BuilderComponent = {
      id: 'test-1',
      type: 'heading',
      props: {
        type: 'heading',
        text: 'Test',
        level: 'h1',
        align: 'left',
      },
    };

    act(() => {
      result.current.addComponent(component);
    });

    expect(result.current.builderData.components).toHaveLength(1);
    expect(result.current.builderData.components[0].id).toBe('test-1');
  });

  it('selects component', () => {
    const { result } = renderHook(() => useBuilderStore());

    const component: BuilderComponent = {
      id: 'test-1',
      type: 'heading',
      props: {
        type: 'heading',
        text: 'Test',
        level: 'h1',
        align: 'left',
      },
    };

    act(() => {
      result.current.addComponent(component);
      result.current.selectComponent('test-1');
    });

    expect(result.current.selection.selectedId).toBe('test-1');
  });

  it('updates component', () => {
    const { result } = renderHook(() => useBuilderStore());

    const component: BuilderComponent = {
      id: 'test-1',
      type: 'heading',
      props: {
        type: 'heading',
        text: 'Test',
        level: 'h1',
        align: 'left',
      },
    };

    act(() => {
      result.current.addComponent(component);
      result.current.updateComponent('test-1', {
        props: {
          ...component.props,
          text: 'Updated Text',
        },
      });
    });

    expect(result.current.builderData.components[0].props.text).toBe('Updated Text');
  });

  it('deletes component', () => {
    const { result } = renderHook(() => useBuilderStore());

    const component: BuilderComponent = {
      id: 'test-1',
      type: 'heading',
      props: {
        type: 'heading',
        text: 'Test',
        level: 'h1',
        align: 'left',
      },
    };

    act(() => {
      result.current.addComponent(component);
      result.current.deleteComponent('test-1');
    });

    expect(result.current.builderData.components).toHaveLength(0);
  });

  it('duplicates component', () => {
    const { result } = renderHook(() => useBuilderStore());

    const component: BuilderComponent = {
      id: 'test-1',
      type: 'heading',
      props: {
        type: 'heading',
        text: 'Test',
        level: 'h1',
        align: 'left',
      },
    };

    act(() => {
      result.current.addComponent(component);
      result.current.duplicateComponent('test-1');
    });

    expect(result.current.builderData.components).toHaveLength(2);
    expect(result.current.builderData.components[0].props.text).toBe('Test');
    expect(result.current.builderData.components[1].props.text).toBe('Test');
    expect(result.current.builderData.components[0].id).not.toBe(result.current.builderData.components[1].id);
  });

  it('clears selection', () => {
    const { result } = renderHook(() => useBuilderStore());

    act(() => {
      result.current.selectComponent('test-1');
      result.current.clearSelection();
    });

    expect(result.current.selection.selectedId).toBeNull();
  });

  it('sets viewport', () => {
    const { result } = renderHook(() => useBuilderStore());

    act(() => {
      result.current.setViewport('mobile');
    });

    expect(result.current.canvasSettings.currentViewport).toBe('mobile');
    expect(result.current.builderData.settings.viewport).toBe('mobile');
  });

  it('toggles grid', () => {
    const { result } = renderHook(() => useBuilderStore());

    const initialGridState = result.current.canvasSettings.gridEnabled;

    act(() => {
      result.current.toggleGrid();
    });

    expect(result.current.canvasSettings.gridEnabled).toBe(!initialGridState);
  });

  it('sets component registry', () => {
    const { result } = renderHook(() => useBuilderStore());

    const registry: ComponentRegistry[] = [
      {
        id: 1,
        name: 'heading',
        label: 'Heading',
        category: 'content',
        icon: 'mdi:format-title',
        schema: { type: 'object', properties: {} },
        default_props: {
          type: 'heading',
          text: 'Heading',
          level: 'h1',
          align: 'left',
        },
        is_enabled: true,
        requires_asset: false,
        is_editable: true,
        render_component: 'Heading',
        order: 1,
      },
    ];

    act(() => {
      result.current.setComponentRegistry(registry);
    });

    expect(result.current.componentRegistry).toHaveLength(1);
    expect(result.current.componentRegistry[0].name).toBe('heading');
  });

  it('gets component schema by name', () => {
    const { result } = renderHook(() => useBuilderStore());

    const registry: ComponentRegistry[] = [
      {
        id: 1,
        name: 'heading',
        label: 'Heading',
        category: 'content',
        icon: 'mdi:format-title',
        schema: { type: 'object', properties: {} },
        default_props: {
          type: 'heading',
          text: 'Heading',
          level: 'h1',
          align: 'left',
        },
        is_enabled: true,
        requires_asset: false,
        is_editable: true,
        render_component: 'Heading',
        order: 1,
      },
    ];

    act(() => {
      result.current.setComponentRegistry(registry);
    });

    const schema = result.current.getComponentSchema('heading');
    expect(schema).toBeDefined();
    expect(schema?.name).toBe('heading');
  });

  it('undoes and redoes actions', () => {
    const { result } = renderHook(() => useBuilderStore());

    const component: BuilderComponent = {
      id: 'test-1',
      type: 'heading',
      props: {
        type: 'heading',
        text: 'Test',
        level: 'h1',
        align: 'left',
      },
    };

    // Add component
    act(() => {
      result.current.addComponent(component);
      result.current.saveState();
    });

    expect(result.current.builderData.components).toHaveLength(1);

    // Undo
    act(() => {
      result.current.undo();
    });

    expect(result.current.builderData.components).toHaveLength(0);

    // Redo
    act(() => {
      result.current.redo();
    });

    expect(result.current.builderData.components).toHaveLength(1);
  });
});
