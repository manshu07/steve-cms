/**
 * EditorJS Inline Button Tool
 * Allows inserting button links within rich text content
 */

class InlineButton {
  constructor({ data, config, api, readOnly }) {
    this.data = data;
    this.config = config || {};
    this.api = api;
    this.readOnly = readOnly;
    this.button = null;
  }

  static get toolbox() {
    return {
      title: 'Button',
      icon: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><path d="M9 9h6"></path><path d="M9 13h6"></path><path d="M9 17h3"></path></svg>'
    };
  }

  /**
   * Renders button in the editor
   * @returns {HTMLElement}
   */
  render() {
    this.button = document.createElement('a');

    if (!this.readOnly) {
      this.button.addEventListener('click', (event) => {
        event.preventDefault();
        this.showSettings(this.button);
      });
    }

    this.applyStyles();
    this.applyData();

    return this.button;
  }

  /**
   * Apply button styles
   */
  applyStyles() {
    this.button.classList.add(
      'inline-flex',
      'items-center',
      'justify-center',
      'gap-2',
      'whitespace-nowrap',
      'rounded-lg',
      'font-semibold',
      'ring-offset-background',
      'transition-all',
      'duration-300',
      'hover:shadow-lg',
      'h-9',
      'px-5',
      'py-2',
      'text-sm',
      'inline-flex',
      'items-center',
      'justify-center',
      'cursor-pointer',
      'no-underline',
      'hover:underline'
    );

    // Apply style variant
    const style = this.data.style || 'primary';
    switch (style) {
      case 'primary':
        this.button.classList.add('bg-primary', 'text-primary-foreground', 'hover:bg-primary/90');
        break;
      case 'secondary':
        this.button.classList.add('border', 'border-border', 'bg-transparent', 'text-foreground', 'hover:bg-secondary', 'hover:border-secondary');
        break;
      case 'ghost':
        this.button.classList.add('bg-transparent', 'text-muted-foreground', 'hover:text-foreground', 'hover:bg-secondary');
        break;
      case 'destructive':
        this.button.classList.add('bg-destructive', 'text-destructive-foreground', 'hover:bg-destructive/90');
        break;
    }
  }

  /**
   * Apply data attributes and content
   */
  applyData() {
    const { url, label, openNewTab } = this.data;

    this.button.textContent = label || 'Button';
    this.button.href = url || '#';

    if (openNewTab) {
      this.button.target = '_blank';
      this.button.rel = 'noopener noreferrer';
    }
  }

  /**
   * Show settings modal
   */
  showSettings(element) {
    const modal = document.createElement('div');
    modal.className = 'editorjs-button-modal fixed inset-0 bg-black/50 flex items-center justify-center z-50';

    const content = document.createElement('div');
    content.className = 'bg-background rounded-lg shadow-xl p-6 max-w-md w-full mx-4';

    content.innerHTML = `
      <h3 class="text-lg font-semibold mb-4">Button Settings</h3>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Button Label</label>
          <input type="text" id="button-label" class="w-full px-3 py-2 border rounded-md" value="${this.data.label || ''}">
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Button URL</label>
          <input type="text" id="button-url" class="w-full px-3 py-2 border rounded-md" value="${this.data.url || ''}">
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Style</label>
          <select id="button-style" class="w-full px-3 py-2 border rounded-md">
            <option value="primary" ${this.data.style === 'primary' ? 'selected' : ''}>Primary</option>
            <option value="secondary" ${this.data.style === 'secondary' ? 'selected' : ''}>Secondary</option>
            <option value="ghost" ${this.data.style === 'ghost' ? 'selected' : ''}>Ghost</option>
            <option value="destructive" ${this.data.style === 'destructive' ? 'selected' : ''}>Destructive</option>
          </select>
        </div>

        <div class="flex items-center gap-2">
          <input type="checkbox" id="button-new-tab" ${this.data.openNewTab ? 'checked' : ''}>
          <label for="button-new-tab" class="text-sm">Open in new tab</label>
        </div>

        <div class="flex justify-end gap-2 mt-6">
          <button type="button" id="button-cancel" class="px-4 py-2 text-sm border rounded-md hover:bg-secondary">Cancel</button>
          <button type="button" id="button-save" class="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90">Save</button>
        </div>
      </div>
    `;

    modal.appendChild(content);
    document.body.appendChild(modal);

    // Event listeners
    const cancelBtn = content.querySelector('#button-cancel');
    const saveBtn = content.querySelector('#button-save');

    cancelBtn.addEventListener('click', () => {
      document.body.removeChild(modal);
    });

    saveBtn.addEventListener('click', () => {
      this.data.label = content.querySelector('#button-label').value;
      this.data.url = content.querySelector('#button-url').value;
      this.data.style = content.querySelector('#button-style').value;
      this.data.openNewTab = content.querySelector('#button-new-tab').checked;

      this.applyStyles();
      this.applyData();

      document.body.removeChild(modal);
    });

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        document.body.removeChild(modal);
      }
    });
  }

  /**
   * Extract button data
   * @returns {Object}
   */
  save(buttonContent) {
    return this.data;
  }

  /**
   * Get toolbox configuration
   * @returns {Object}
   */
  static get sanitize() {
    return {
      url: true,
      label: true,
      style: true,
      openNewTab: false
    };
  }
}

// Export for use
window.InlineButton = InlineButton;
