/**
 * API service for page builder backend integration.
 * Handles all communication with Django REST API.
 */

import axios from 'axios';
import type {
  ApiResponse,
  BuilderPage,
  BuilderData,
  ComponentRegistry,
  ComponentRegistryResponse,
  BuilderPageResponse,
} from '~types/index';

// ============================================================
// API CLIENT
// ============================================================

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/builder';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // For session authentication
});

// ============================================================
// COMPONENT REGISTRY API
// ============================================================

/**
 * Fetch all available builder components.
 * Public endpoint - no authentication required.
 */
export const getComponentRegistry = async (): Promise<ComponentRegistry[]> => {
  const response = await apiClient.get<ComponentRegistryResponse>('/components/');
  return response.data.components;
};

// ============================================================
// BUILDER PAGE API
// ============================================================

/**
 * Fetch page with builder data.
 * Requires authentication and builder permissions.
 */
export const getBuilderPage = async (pageId: number): Promise<BuilderPage> => {
  const response = await apiClient.get<BuilderPageResponse>(`/pages/${pageId}/`);
  return response.data.page;
};

/**
 * Update page builder data.
 * Requires authentication and builder permissions.
 */
export const updateBuilderPage = async (
  pageId: number,
  builderData: BuilderData
): Promise<BuilderPage> => {
  const response = await apiClient.put<BuilderPageResponse>(`/pages/${pageId}/update/`, {
    builder_data: builderData,
  });
  return response.data.page;
};

/**
 * Publish page (make it live).
 * Requires authentication and publish permissions.
 */
export const publishBuilderPage = async (
  pageId: number,
  builderData: BuilderData
): Promise<BuilderPage> => {
  const response = await apiClient.post<BuilderPageResponse>(`/pages/${pageId}/publish/`, {
    builder_data: builderData,
  });
  return response.data.page;
};

// ============================================================
// TEMPLATES API
// ============================================================

/**
 * Fetch all available page templates.
 * Requires authentication and builder permissions.
 */
export const getBuilderTemplates = async (): Promise<any[]> => {
  const response = await apiClient.get('/templates/');
  return response.data.templates;
};

// ============================================================
// ASSETS API
// ============================================================

/**
 * Upload asset (image/video) via Cloudinary.
 * Requires authentication and asset upload permissions.
 */
export const uploadBuilderAsset = async (file: File, metadata: any = {}): Promise<any> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('metadata', JSON.stringify(metadata));

  const response = await apiClient.post('/assets/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data.asset;
};

/**
 * Fetch user's uploaded assets.
 * Requires authentication and builder permissions.
 */
export const getUserAssets = async (): Promise<any[]> => {
  const response = await apiClient.get('/assets/');
  return response.data.assets;
};

// ============================================================
// EXPORT API OBJECT
// ============================================================

export const builderApi = {
  // Component Registry
  getComponentRegistry,

  // Pages
  getBuilderPage,
  updateBuilderPage,
  publishBuilderPage,

  // Templates
  getBuilderTemplates,

  // Assets
  uploadBuilderAsset,
  getUserAssets,
};

export default builderApi;
