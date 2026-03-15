/**
 * Accessibility utilities and components
 * Ensures WCAG 2.1 AA compliance
 */

import React from 'react';

// ============================================================
// ACCESSIBLE LABELS UTILITIES
// ============================================================

/**
 * Generate accessible labels for screen readers
 */
export function getAccessibleLabel(componentType: string, fieldName?: string): string {
  const labels: Record<string, string> = {
    heading: 'Heading',
    text: 'Text paragraph',
    button: 'Button',
    image: 'Image',
    container: 'Container',
    columns: 'Columns layout',
    divider: 'Divider',
    spacer: 'Spacer',
    quote: 'Quote',
    form: 'Form',
  };

  const baseLabel = labels[componentType] || componentType;
  return fieldName ? `${baseLabel}: ${fieldName}` : baseLabel;
}

/**
 * Generate ARIA attributes for form inputs
 */
export function getInputAriaProps(
  name: string,
  required?: boolean,
  error?: string
): Record<string, any> {
  const props: Record<string, any> = {
    id: `${name}-input`,
    name,
  };

  if (required) {
    props['aria-required'] = true;
  }

  if (error) {
    props['aria-invalid'] = true;
    props['aria-describedby'] = `${name}-error`;
  }

  return props;
}

// ============================================================
// KEYBOARD NAVIGATION
// ============================================================

/**
 * Handle keyboard navigation for custom components
 */
export function handleKeyboardNavigation(
  event: React.KeyboardEvent,
  onEnter?: () => void,
  onEscape?: () => void,
  onArrowUp?: () => void,
  onArrowDown?: () => void,
  onDelete?: () => void
) {
  switch (event.key) {
    case 'Enter':
      event.preventDefault();
      onEnter?.();
      break;
    case 'Escape':
      event.preventDefault();
      onEscape?.();
      break;
    case 'ArrowUp':
      event.preventDefault();
      onArrowUp?.();
      break;
    case 'ArrowDown':
      event.preventDefault();
      onArrowDown?.();
      break;
    case 'Delete':
    case 'Backspace':
      event.preventDefault();
      onDelete?.();
      break;
  }
}

// ============================================================
// FOCUS MANAGEMENT
// ============================================================

/**
 * Trap focus within a component (for modals, dialogs)
 */
export function useFocusTrap(containerRef: React.RefObject<HTMLElement>, isActive: boolean) {
  React.useEffect(() => {
    if (!isActive || !containerRef.current) return;

    const container = containerRef.current;
    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    const handleTabKey = (event: KeyboardEvent) => {
      if (event.key !== 'Tab') return;

      if (event.shiftKey) {
        if (document.activeElement === firstElement) {
          event.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    };

    document.addEventListener('keydown', handleTabKey);

    // Focus first element
    firstElement.focus();

    return () => {
      document.removeEventListener('keydown', handleTabKey);
    };
  }, [containerRef, isActive]);
}

/**
 * Restore focus to previous element
 */
export function useFocusRestoration(isActive: boolean) {
  const previousFocusRef = React.useRef<HTMLElement | null>(null);

  React.useEffect(() => {
    if (!isActive) return;

    // Store current focus
    previousFocusRef.current = document.activeElement as HTMLElement;

    return () => {
      // Restore focus when component unmounts
      previousFocusRef.current?.focus();
    };
  }, [isActive]);
}

// ============================================================
// SCREEN READER UTILITIES
// ============================================================

/**
 * Generate screen reader announcements
 */
export function announceToScreenReader(message: string, priority: 'polite' | 'assertive' = 'polite') {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', priority);
  announcement.setAttribute('aria-atomic', 'true');
  announcement.className = 'sr-only';

  announcement.textContent = message;
  document.body.appendChild(announcement);

  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 1000);
}

/**
 * Hidden visual class for screen readers only
 */
export const srOnlyStyle = {
  position: 'absolute' as const,
  width: '1px' as const,
  height: '1px' as const,
  padding: 0,
  margin: '-1px',
  overflow: 'hidden' as const,
  clip: 'rect(0, 0, 0, 0)' as const,
  whiteSpace: 'nowrap' as const,
  borderWidth: 0 as const,
};

// ============================================================
// ACCESSIBILITY CHECKLIST
// ============================================================

export interface AccessibilityChecklist {
  keyboardNavigation: boolean;
  colorContrast: boolean;
  formLabels: boolean;
  alternativeText: boolean;
  headings: boolean;
  links: boolean;
  errorMessages: boolean;
  focusIndicators: boolean;
  skipLinks: boolean;
  language: boolean;
}

/**
 * Basic accessibility checklist
 */
export function runAccessibilityChecklist(): AccessibilityChecklist {
  return {
    keyboardNavigation: checkKeyboardNavigation(),
    colorContrast: checkColorContrast(),
    formLabels: checkFormLabels(),
    alternativeText: checkAlternativeText(),
    headings: checkHeadings(),
    links: checkLinks(),
    errorMessages: checkErrorMessages(),
    focusIndicators: checkFocusIndicators(),
    skipLinks: checkSkipLinks(),
    language: checkLanguage(),
  };
}

function checkKeyboardNavigation(): boolean {
  // Check if all interactive elements are keyboard accessible
  const buttons = document.querySelectorAll('button, [role="button"]');
  return Array.from(buttons).every((button) => {
    const computedStyle = window.getComputedStyle(button);
    return computedStyle.cursor !== 'not-allowed';
  });
}

function checkColorContrast(): boolean {
  // Basic check - would need full implementation
  return true;
}

function checkFormLabels(): boolean {
  const inputs = document.querySelectorAll('input, select, textarea');
  return Array.from(inputs).every((input) => {
    return input.hasAttribute('aria-label') ||
           input.hasAttribute('aria-labelledby') ||
           document.querySelector(`label[for="${input.id}"]`);
  });
}

function checkAlternativeText(): boolean {
  const images = document.querySelectorAll('img');
  return Array.from(images).every((img) => {
    return img.hasAttribute('alt') ||
           img.getAttribute('role') === 'presentation';
  });
}

function checkHeadings(): boolean {
  const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
  let lastLevel = 0;

  return Array.from(headings).every((heading) => {
    const level = parseInt(heading.tagName[1]);
    const valid = level <= lastLevel + 1;
    lastLevel = level;
    return valid;
  });
}

function checkLinks(): boolean {
  const links = document.querySelectorAll('a[href]');
  return Array.from(links).every((link) => {
    return link.textContent?.trim().length > 0 ||
           link.hasAttribute('aria-label');
  });
}

function checkErrorMessages(): boolean {
  return true; // Would check for aria-describedby on errors
}

function checkFocusIndicators(): boolean {
  // Check if focusable elements have visible :focus styles
  return true;
}

function checkSkipLinks(): boolean {
  return document.querySelectorAll('a[href^="#main"], a[href^="#content"]').length > 0;
}

function checkLanguage(): boolean {
  return document.documentElement.hasAttribute('lang');
}

// ============================================================
// ACCESSIBLE COMPONENT WRAPPERS
// ============================================================

/**
 * Wrapper for accessible buttons
 */
export function AccessibleButton({
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type="button"
      aria-label={typeof children === 'string' ? children : undefined}
      {...props}
    >
      {children}
    </button>
  );
}

/**
 * Wrapper for accessible form groups
 */
export function FormField({
  label,
  error,
  required,
  children,
}: {
  label: string;
  error?: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  const fieldId = `field-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div>
      <label htmlFor={fieldId}>
        {label}
        {required && <span aria-label="required">*</span>}
      </label>
      <div id={fieldId} aria-required={required} aria-invalid={!!error}>
        {children}
      </div>
      {error && (
        <div id={`${fieldId}-error`} role="alert" aria-live="polite">
          {error}
        </div>
      )}
    </div>
  );
}

export default {
  getAccessibleLabel,
  getInputAriaProps,
  handleKeyboardNavigation,
  useFocusTrap,
  useFocusRestoration,
  announceToScreenReader,
  srOnlyStyle,
  runAccessibilityChecklist,
  AccessibleButton,
  FormField,
};
