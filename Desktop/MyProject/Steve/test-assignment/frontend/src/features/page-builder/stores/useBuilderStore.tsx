/**
 * Zustand store for page builder state management.
 * Manages components, selection, history (undo/redo), and settings.
 */

import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';
import type {
  BuilderComponent,
  BuilderData,
  BuilderSettings,
  ComponentRegistry,
  ViewportMode,
  SelectionState,
  HistoryState,
} from '~types/index';

// ============================================================
// INITIAL STATE
// ============================================================

const initialBuilderData: BuilderData = {
  components: [],
  settings: {
    viewport: 'desktop',
    breakpoints: {
      mobile: 768,
      tablet: 1024,
    },
  },
  version: 1,
};

const initialSelection: SelectionState = {
  selectedId: null,
  hoveredId: null,
  isDragging: false,
};

const initialHistory: HistoryState = {
  past: [],
  present: initialBuilderData,
  future: [],
};

// ============================================================
// BUILDER STORE INTERFACE
// ============================================================

interface BuilderStore {
  // Data
  componentRegistry: ComponentRegistry[];
  builderData: BuilderData;
  currentPageId: number | null;

  // Selection
  selection: SelectionState;

  // History (Undo/Redo)
  history: HistoryState;

  // Canvas settings
  canvasSettings: {
    gridEnabled: boolean;
    snapToGrid: boolean;
    gridSize: number;
    showOutlines: boolean;
    currentViewport: ViewportMode;
  };

  // ==========================================================
  // ACTIONS: Component Registry
  // ==========================================================

  setComponentRegistry: (registry: ComponentRegistry[]) => void;
  getComponentSchema: (componentName: string) => ComponentRegistry | undefined;

  // ==========================================================
  // ACTIONS: Components
  // ==========================================================

  addComponent: (component: BuilderComponent, parentId?: string, index?: number) => void;
  updateComponent: (id: string, updates: Partial<BuilderComponent>) => void;
  deleteComponent: (id: string) => void;
  duplicateComponent: (id: string) => void;
  moveComponent: (id: string, newParentId?: string, newIndex?: number) => void;

  // ==========================================================
  // ACTIONS: Selection
  // ==========================================================

  selectComponent: (id: string | null) => void;
  hoverComponent: (id: string | null) => void;
  setDragging: (isDragging: boolean) => void;
  clearSelection: () => void;

  // ==========================================================
  // ACTIONS: History (Undo/Redo)
  // ==========================================================

  undo: () => void;
  redo: () => void;
  saveState: () => void;
  canUndo: () => boolean;
  canRedo: () => boolean;

  // ==========================================================
  // ACTIONS: Canvas Settings
  // ==========================================================

  setViewport: (viewport: ViewportMode) => void;
  toggleGrid: () => void;
  toggleSnapToGrid: () => void;
  toggleOutlines: () => void;
  setGridSize: (size: number) => void;

  // ==========================================================
  // ACTIONS: Page
  // ==========================================================

  loadPage: (pageId: number, builderData: BuilderData) => void;
  resetBuilder: () => void;
}

// ============================================================
// HELPER FUNCTIONS
// ============================================================

/**
 * Find component by ID recursively.
 */
const findComponent = (
  components: BuilderComponent[],
  id: string
): { component: BuilderComponent; parent?: BuilderComponent; index?: number } | undefined => {
  for (let i = 0; i < components.length; i++) {
    if (components[i].id === id) {
      return { component: components[i], index: i };
    }
    if (components[i].children) {
      const found = findComponent(components[i].children!, id);
      if (found) {
        return found;
      }
    }
  }
  return undefined;
};

/**
 * Remove component from tree by ID.
 */
const removeComponent = (components: BuilderComponent[], id: string): BuilderComponent[] => {
  return components
    .filter((c) => c.id !== id)
    .map((c) => ({
      ...c,
      children: c.children ? removeComponent(c.children, id) : undefined,
    }));
};

/**
 * Update component in tree by ID.
 */
const updateComponentInTree = (
  components: BuilderComponent[],
  id: string,
  updates: Partial<BuilderComponent>
): BuilderComponent[] => {
  return components.map((c) => {
    if (c.id === id) {
      return { ...c, ...updates };
    }
    if (c.children) {
      return {
        ...c,
        children: updateComponentInTree(c.children, id, updates),
      };
    }
    return c;
  });
};

// ============================================================
// STORE IMPLEMENTATION
// ============================================================

export const useBuilderStore = create<BuilderStore>()(
  immer((set, get) => ({
    // ============================================================
    // INITIAL STATE
    // ============================================================

    componentRegistry: [],
    builderData: initialBuilderData,
    currentPageId: null,
    selection: initialSelection,
    history: initialHistory,
    canvasSettings: {
      gridEnabled: true,
      snapToGrid: true,
      gridSize: 12,
      showOutlines: true,
      currentViewport: 'desktop',
    },

    // ============================================================
    // ACTIONS: Component Registry
    // ============================================================

    setComponentRegistry: (registry) =>
      set((state) => {
        state.componentRegistry = registry;
      }),

    getComponentSchema: (componentName) => {
      return get().componentRegistry.find((c) => c.name === componentName);
    },

    // ============================================================
    // ACTIONS: Components
    // ============================================================

    addComponent: (component, parentId, index) =>
      set((state) => {
        const newComponent = { ...component, id: component.id || crypto.randomUUID() };

        if (parentId) {
          // Add as child of parent component
          const addToParent = (components: BuilderComponent[]): boolean => {
            for (const c of components) {
              if (c.id === parentId) {
                if (!c.children) c.children = [];
                if (index !== undefined) {
                  c.children.splice(index, 0, newComponent);
                } else {
                  c.children.push(newComponent);
                }
                return true;
              }
              if (c.children && addToParent(c.children)) {
                return true;
              }
            }
            return false;
          };
          addToParent(state.builderData.components);
        } else {
          // Add to root
          if (index !== undefined) {
            state.builderData.components.splice(index, 0, newComponent);
          } else {
            state.builderData.components.push(newComponent);
          }
        }

        state.selection.selectedId = newComponent.id;
      }),

    updateComponent: (id, updates) =>
      set((state) => {
        state.builderData.components = updateComponentInTree(
          state.builderData.components,
          id,
          updates
        );
      }),

    deleteComponent: (id) =>
      set((state) => {
        state.builderData.components = removeComponent(state.builderData.components, id);
        if (state.selection.selectedId === id) {
          state.selection.selectedId = null;
        }
      }),

    duplicateComponent: (id) =>
      set((state) => {
        const found = findComponent(state.builderData.components, id);
        if (!found) return;

        const duplicated: BuilderComponent = {
          ...JSON.parse(JSON.stringify(found.component)),
          id: crypto.randomUUID(),
        };

        if (found.index !== undefined) {
          state.builderData.components.splice(found.index + 1, 0, duplicated);
        }

        state.selection.selectedId = duplicated.id;
      }),

    moveComponent: (id, newParentId, newIndex) =>
      set((state) => {
        // Remove from current location
        const removed = removeComponent(state.builderData.components, id);
        state.builderData.components = removed;

        // Find the component to move
        const found = findComponent(state.builderData.components, id);
        if (!found) return;

        if (newParentId) {
          // Move to new parent
          const addToParent = (components: BuilderComponent[]): boolean => {
            for (const c of components) {
              if (c.id === newParentId) {
                if (!c.children) c.children = [];
                if (newIndex !== undefined) {
                  c.children.splice(newIndex, 0, found.component);
                } else {
                  c.children.push(found.component);
                }
                return true;
              }
              if (c.children && addToParent(c.children)) {
                return true;
              }
            }
            return false;
          };
          addToParent(state.builderData.components);
        } else {
          // Move to root
          if (newIndex !== undefined) {
            state.builderData.components.splice(newIndex, 0, found.component);
          } else {
            state.builderData.components.push(found.component);
          }
        }
      }),

    // ============================================================
    // ACTIONS: Selection
    // ============================================================

    selectComponent: (id) =>
      set((state) => {
        state.selection.selectedId = id;
      }),

    hoverComponent: (id) =>
      set((state) => {
        state.selection.hoveredId = id;
      }),

    setDragging: (isDragging) =>
      set((state) => {
        state.selection.isDragging = isDragging;
      }),

    clearSelection: () =>
      set((state) => {
        state.selection.selectedId = null;
        state.selection.hoveredId = null;
      }),

    // ============================================================
    // ACTIONS: History (Undo/Redo)
    // ============================================================

    undo: () =>
      set((state) => {
        const { past, present } = state.history;
        if (past.length === 0) return;

        const previous = past[past.length - 1];
        const newPast = past.slice(0, past.length - 1);

        state.history = {
          past: newPast,
          present: previous,
          future: [present, ...state.history.future],
        };

        state.builderData = previous;
      }),

    redo: () =>
      set((state) => {
        const { future, present } = state.history;
        if (future.length === 0) return;

        const next = future[0];
        const newFuture = future.slice(1);

        state.history = {
          past: [...state.history.past, present],
          present: next,
          future: newFuture,
        };

        state.builderData = next;
      }),

    saveState: () =>
      set((state) => {
        state.history = {
          past: [...state.history.past, state.builderData],
          present: state.builderData,
          future: [],
        };

        // Limit history to 50 states
        if (state.history.past.length > 50) {
          state.history.past = state.history.past.slice(-50);
        }
      }),

    canUndo: () => {
      return get().history.past.length > 0;
    },

    canRedo: () => {
      return get().history.future.length > 0;
    },

    // ============================================================
    // ACTIONS: Canvas Settings
    // ============================================================

    setViewport: (viewport) =>
      set((state) => {
        state.canvasSettings.currentViewport = viewport;
        state.builderData.settings.viewport = viewport;
      }),

    toggleGrid: () =>
      set((state) => {
        state.canvasSettings.gridEnabled = !state.canvasSettings.gridEnabled;
      }),

    toggleSnapToGrid: () =>
      set((state) => {
        state.canvasSettings.snapToGrid = !state.canvasSettings.snapToGrid;
      }),

    toggleOutlines: () =>
      set((state) => {
        state.canvasSettings.showOutlines = !state.canvasSettings.showOutlines;
      }),

    setGridSize: (size) =>
      set((state) => {
        state.canvasSettings.gridSize = size;
      }),

    // ============================================================
    // ACTIONS: Page
    // ============================================================

    loadPage: (pageId, builderData) =>
      set((state) => {
        state.currentPageId = pageId;
        state.builderData = builderData;
        state.history = {
          past: [],
          present: builderData,
          future: [],
        };
      }),

    resetBuilder: () =>
      set((state) => {
        state.builderData = initialBuilderData;
        state.currentPageId = null;
        state.selection = initialSelection;
        state.history = initialHistory;
      }),
  }))
);

// ============================================================
// SELECTORS
// ============================================================

export const selectComponentById = (id: string | null) => (state: BuilderStore) => {
  if (!id) return undefined;
  return findComponent(state.builderData.components, id)?.component;
};

export const selectSelectedComponent = () => (state: BuilderStore) => {
  return selectComponentById(state.selection.selectedId)(state);
};

export const selectComponentsByParent = (parentId?: string) => (state: BuilderStore) => {
  if (!parentId) {
    return state.builderData.components;
  }

  const parent = findComponent(state.builderData.components, parentId)?.component;
  return parent?.children || [];
};
