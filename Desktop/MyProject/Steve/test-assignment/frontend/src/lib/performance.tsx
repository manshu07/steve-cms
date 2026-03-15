/**
 * Performance optimization utilities
 * Includes code splitting, lazy loading, and performance monitoring
 */

import React, { lazy, Suspense } from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

// ============================================================
// LAZY LOADING UTILITIES
// ============================================================

/**
 * Suspense loading fallback component
 */
export const SuspenseLoader: React.FC<{ message?: string }> = ({ message = 'Loading...' }) => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: 200,
      gap: 2,
    }}
  >
    <CircularProgress size={40} />
    <Typography variant="body2" color="text.secondary">
      {message}
    </Typography>
  </Box>
);

/**
 * Higher-order component for lazy loading with Suspense
 */
export function withLazyLoading<P extends object>(
  importFunc: () => Promise<{ default: React.ComponentType<P> }>,
  fallback?: React.ReactNode
) {
  const LazyComponent = lazy(importFunc);

  return (props: P) => (
    <Suspense fallback={fallback || <SuspenseLoader />}>
      <LazyComponent {...props} />
    </Suspense>
  );
}

// ============================================================
// CODE SPLITTING CONFIGURATION
// ============================================================

/**
 * Lazy load heavy components
 */
export const LazyTemplateModal = withLazyLoading(
  () => import('../features/page-builder/components/Templates/TemplateModal')
);

export const LazyImageUploader = withLazyLoading(
  () => import('../features/page-builder/components/Assets/ImageUploader')
);

export const LazyPropertyEditor = withLazyLoading(
  () => import('../features/page-builder/components/Properties/PropertyEditor')
);

// ============================================================
// PERFORMANCE MONITORING
// ============================================================

/**
 * Performance metrics utility
 */
export class PerformanceMonitor {
  private marks: Map<string, number> = new Map();

  /**
   * Start measuring performance
   */
  startMark(name: string): void {
    this.marks.set(name, performance.now());
  }

  /**
   * End measuring performance and log result
   */
  endMark(name: string): number {
    const startTime = this.marks.get(name);
    if (!startTime) {
      console.warn(`Performance mark "${name}" not found`);
      return 0;
    }

    const duration = performance.now() - startTime;
    console.log(`[Performance] ${name}: ${duration.toFixed(2)}ms`);
    this.marks.delete(name);

    return duration;
  }

  /**
   * Measure async operation performance
   */
  async measure<T>(name: string, fn: () => Promise<T>): Promise<T> {
    this.startMark(name);
    try {
      const result = await fn();
      this.endMark(name);
      return result;
    } catch (error) {
      this.endMark(name);
      throw error;
    }
  }

  /**
   * Log Web Vitals
   */
  logWebVitals(): void {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          console.log('[Web Vital]', entry.name, entry.value);
        }
      });

      try {
        observer.observe({ entryTypes: ['paint', 'navigation', 'largest-contentful-paint'] });
      } catch (e) {
        // PerformanceObserver not fully supported
        console.warn('PerformanceObserver not fully supported');
      }
    }
  }
}

// Export singleton instance
export const performanceMonitor = new PerformanceMonitor();

// ============================================================
// BUNDLE SIZE ANALYSIS
// ============================================================

/**
 * Get bundle size information
 */
export async function getBundleSizeInfo(): Promise<{
  total: number;
  chunks: Array<{ name: string; size: number }>;
}> {
  try {
    const response = await fetch('/__bundle_analysis.json');
    const data = await response.json();
    return data;
  } catch (error) {
    console.warn('Bundle size analysis not available:', error);
    return {
      total: 0,
      chunks: [],
    };
  }
}

// ============================================================
// IMAGE OPTIMIZATION
// ============================================================

/**
 * Generate responsive image srcset
 */
export function generateSrcset(baseUrl: string, widths: number[]): string {
  return widths
    .map((width) => `${baseUrl}?w=${width} ${width}w`)
    .join(', ');
}

/**
 * Generate lazy loading attributes for images
 */
export function getLazyImageProps() {
  return {
    loading: 'lazy' as const,
    decoding: 'async' as const,
  };
}

// ============================================================
// VIRTUAL SCROLLING UTILITIES
// ============================================================

/**
 * Calculate visible range for virtual scrolling
 */
export function getVisibleRange(
  scrollTop: number,
  viewportHeight: number,
  itemHeight: number,
  totalItems: number
): { startIndex: number; endIndex: number; visibleCount: number } {
  const startIndex = Math.floor(scrollTop / itemHeight);
  const visibleCount = Math.ceil(viewportHeight / itemHeight) + 1;
  const endIndex = Math.min(startIndex + visibleCount, totalItems - 1);

  return {
    startIndex: Math.max(0, startIndex),
    endIndex,
    visibleCount: endIndex - startIndex + 1,
  };
}

/**
 * Memoization helper for expensive computations
 */
export function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map<string, ReturnType<T>>();

  return ((...args: any[]) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

export default PerformanceMonitor;
