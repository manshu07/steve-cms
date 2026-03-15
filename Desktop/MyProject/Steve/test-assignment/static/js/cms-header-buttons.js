/**
 * CMS Header Buttons Builder
 * Manages header buttons for navigation
 */

(function() {
    'use strict';

    function safeJsonParse(str, fallback) {
        try {
            return JSON.parse(str);
        } catch (e) {
            return fallback;
        }
    }

    function el(tag, attrs, children) {
        const elem = document.createElement(tag);
        if (attrs) {
            for (const key in attrs) {
                if (key === 'className') {
                    elem.className = attrs[key];
                } else if (key === 'style' && typeof attrs[key] === 'object') {
                    Object.assign(elem.style, attrs[key]);
                } else if (key.startsWith('on')) {
                    const event = key.substring(2).toLowerCase();
                    elem.addEventListener(event, attrs[key]);
                } else {
                    elem.setAttribute(key, attrs[key]);
                }
            }
        }
        if (children) {
            if (Array.isArray(children)) {
                children.forEach(child => {
                    if (typeof child === 'string') {
                        elem.appendChild(document.createTextNode(child));
                    } else if (child) {
                        elem.appendChild(child);
                    }
                });
            } else if (typeof children === 'string') {
                elem.appendChild(document.createTextNode(children));
            } else if (children) {
                elem.appendChild(children);
            }
        }
        return elem;
    }

    const ICONS = {
        trash: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>',
        plus: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>'
    };

    function initHeaderButtonsBuilder() {
        const builder = document.querySelector('[data-header-buttons-builder]');
        if (!builder) return;

        const input = document.querySelector('[data-header-buttons-input]');
        if (!input) return;

        // Parse initial state
        let buttons = safeJsonParse(input.value, []);

        // Sync function
        function sync() {
            input.value = JSON.stringify(buttons);
        }

        // Rerender function
        function rerender() {
            renderButtons();
        }

        // Render a single button item
        function renderButtonItem(button, index) {
            const wrapper = el('div', { className: 'bg-muted/30 p-4 rounded-md border border-border space-y-3' }, [
                el('div', { className: 'flex items-center justify-between mb-2' }, [
                    el('h4', { className: 'cms-form-label mb-0' }, `Button ${index + 1}`),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive',
                        onclick: () => {
                            buttons.splice(index, 1);
                            sync();
                            rerender();
                        }
                    }, ICONS.trash + ' Remove')
                ]),

                // Label field
                el('div', { className: 'cms-form-group' }, [
                    el('label', { className: 'cms-form-label' }, 'Button Label'),
                    el('input', {
                        type: 'text',
                        className: 'cms-form-input',
                        value: button.label || '',
                        placeholder: 'Book a Demo',
                        onchange: (e) => {
                            buttons[index].label = e.target.value;
                            sync();
                        }
                    })
                ]),

                // URL field
                el('div', { className: 'cms-form-group' }, [
                    el('label', { className: 'cms-form-label' }, 'Button URL'),
                    el('input', {
                        type: 'text',
                        className: 'cms-form-input',
                        value: button.url || '',
                        placeholder: 'https://calendly.com/...',
                        onchange: (e) => {
                            buttons[index].url = e.target.value;
                            sync();
                        }
                    })
                ]),

                // Style field
                el('div', { className: 'cms-form-group' }, [
                    el('label', { className: 'cms-form-label' }, 'Button Style'),
                    el('select', {
                        className: 'cms-form-select',
                        value: button.style || 'primary',
                        onchange: (e) => {
                            buttons[index].style = e.target.value;
                            sync();
                        }
                    }, [
                        el('option', { value: 'primary' }, 'Primary (Filled)'),
                        el('option', { value: 'secondary' }, 'Secondary (Outline)'),
                        el('option', { value: 'ghost' }, 'Ghost (Minimal)')
                    ])
                ]),

                // Open in new tab checkbox
                el('div', { className: 'cms-form-group' }, [
                    el('label', { className: 'cms-form-label flex items-center gap-2' }, [
                        el('input', {
                            type: 'checkbox',
                            checked: button.open_new_tab || false,
                            onchange: (e) => {
                                buttons[index].open_new_tab = e.target.checked;
                                sync();
                            }
                        }),
                        'Open in new tab'
                    ])
                ])
            ]);

            return wrapper;
        }

        // Render all buttons
        function renderButtons() {
            builder.innerHTML = '';

            // Add "Add button" button
            const addBtn = el('button', {
                type: 'button',
                className: 'cms-btn cms-btn-sm cms-btn-ghost',
                onclick: () => {
                    buttons.push({
                        label: 'New Button',
                        url: '',
                        style: 'primary',
                        open_new_tab: true
                    });
                    sync();
                    rerender();
                }
            }, ICONS.plus + ' Add Header Button');

            builder.appendChild(addBtn);

            // Render button items
            if (buttons.length === 0) {
                builder.appendChild(
                    el('p', { className: 'text-sm text-muted-foreground text-center py-4' },
                        'No header buttons yet. Click "Add Header Button" to create one.')
                );
            } else {
                buttons.forEach((button, index) => {
                    builder.appendChild(renderButtonItem(button, index));
                });
            }
        }

        // Initial render
        renderButtons();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHeaderButtonsBuilder);
    } else {
        initHeaderButtonsBuilder();
    }

})();
