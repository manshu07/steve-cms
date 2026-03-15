/**
 * CMS Block Builder
 * Client-side JavaScript for building and managing content blocks
 * Supports 12 block types with drag-and-drop and EditorJS integration
 */

(function() {
    'use strict';

    // ===== Helpers =====
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

    // Icons
    const ICONS = {
        drag: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="12" r="1"/><circle cx="9" cy="5" r="1"/><circle cx="9" cy="19" r="1"/><circle cx="15" cy="12" r="1"/><circle cx="15" cy="5" r="1"/><circle cx="15" cy="19" r="1"/></svg>',
        trash: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>',
        chevronDown: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
        plus: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12h14"/></svg>',
        edit: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg>'
    };

    // Block type labels
    const BLOCK_LABELS = {
        rich_text: 'Rich Text',
        code: 'Code Embed',
        cta: 'Call to Action',
        callout: 'Callout',
        feature_grid: 'Feature Grid',
        faq: 'FAQ',
        quote: 'Quote',
        comparison_table: 'Comparison Table',
        pricing_table: 'Pricing Table',
        logo_cloud: 'Logo Cloud',
        image_gallery: 'Image Gallery',
        table: 'Table',
        button: 'Button'
    };

    // ===== Block Defaults =====
    function blockDefaults(type) {
        switch (type) {
            case 'rich_text':
                return { type: type, content: { blocks: [] } };
            case 'code':
                return { type: type, html: '' };
            case 'cta':
                return { type: type, title: '', body: '', button_label: '', button_url: '' };
            case 'callout':
                return { type: type, title: '', body: '' };
            case 'feature_grid':
                return { type: type, items: [{ title: '', body: '' }] };
            case 'faq':
                return { type: type, items: [{ question: '', answer: '' }] };
            case 'quote':
                return { type: type, quote: '', author: '' };
            case 'comparison_table':
                return { type: type, headers: ['Feature', 'Plan A', 'Plan B'], rows: [['', '', '']] };
            case 'pricing_table':
                return { type: type, plans: [{ title: '', price: '', features: [''] }] };
            case 'logo_cloud':
                return { type: type, logos: [{ src: '', alt: '' }] };
            case 'image_gallery':
                return { type: type, title: '', layout: 'grid', images: [{ src: '', alt: '', caption: '' }] };
            case 'table':
                return { type: type, headers: ['Column 1', 'Column 2'], rows: [['', '']] };
            case 'button':
                return { type: type, label: 'Click Me', url: '', style: 'primary', open_new_tab: false, icon: '' };
            default:
                return { type: type };
        }
    }

    // ===== Field Builders =====
    function fieldInput(props) {
        const { label, value, onChange, placeholder } = props;
        return el('div', { className: 'cms-form-group' }, [
            el('label', { className: 'cms-form-label' }, label),
            el('input', {
                type: 'text',
                className: 'cms-form-input',
                value: value || '',
                placeholder: placeholder || '',
                onchange: (e) => onChange(e.target.value)
            })
        ]);
    }

    function fieldTextarea(props) {
        const { label, value, onChange, placeholder } = props;
        return el('div', { className: 'cms-form-group' }, [
            el('label', { className: 'cms-form-label' }, label),
            el('textarea', {
                className: 'cms-form-textarea',
                placeholder: placeholder || '',
                onchange: (e) => onChange(e.target.value)
            }, value || '')
        ]);
    }

    // ===== Block Type Renderers =====
    function renderRichTextFields(block, sync, rerender) {
        const container = el('div', { className: 'cms-rich-text-editor' });
        const holderId = 'editorjs-' + Math.random().toString(36).substr(2, 9);

        container.innerHTML = `
            <div id="${holderId}" class="min-h-[150px] border border-border rounded-md bg-background cms-editorjs-wrapper">
                <div class="cms-editorjs-loading">
                    <div class="flex items-center justify-center py-8">
                        <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mr-2"></div>
                        <span class="text-sm text-muted-foreground">Loading editor...</span>
                    </div>
                </div>
            </div>
        `;

        // Wait for EditorJS to be available, then initialize
        const initEditor = () => {
            // Check if EditorJS is available
            const holder = document.getElementById(holderId);
            if (typeof EditorJS === 'undefined') {
                if (holder) {
                    holder.innerHTML = `
                        <div class="p-4 bg-destructive/10 border border-destructive rounded-md">
                            <p class="text-destructive text-sm font-medium">EditorJS failed to load.</p>
                            <p class="text-destructive/70 text-xs mt-1">Please refresh the page or check your internet connection.</p>
                        </div>
                    `;
                }
                console.error('EditorJS is not available');
                return;
            }

            // Helper function to get plugin class (handles different global variable names)
            const getPluginClass = (possibleNames) => {
                for (const name of possibleNames) {
                    if (typeof window[name] !== 'undefined') {
                        return window[name];
                    }
                }
                return null;
            };

            // Get all plugin classes - use actual global names that are loaded
            const HeaderClass = getPluginClass(['Header', 'HeaderTool']);
            const ListClass = getPluginClass(['EditorjsList', 'List', 'ListTool']);
            const QuoteClass = getPluginClass(['Quote', 'QuoteTool']);
            const TableClass = getPluginClass(['Table', 'TableTool', 'EditorjsTable']);
            const CodeClass = getPluginClass(['CodeTool', 'Code', 'EditorjsCode']);

            // Only check for core plugins that actually work
            const missingPlugins = [];
            if (!HeaderClass) missingPlugins.push('Header');
            if (!ListClass) missingPlugins.push('List');
            if (!QuoteClass) missingPlugins.push('Quote');

            // Delimiter and Warning are optional - skip if not available
            const DelimiterClass = getPluginClass(['Delimiter', 'DelimiterTool']);
            const WarningClass = getPluginClass(['Warning', 'WarningTool']);

            if (missingPlugins.length > 0) {
                if (holder) {
                    holder.innerHTML = `
                        <div class="p-4 bg-destructive/10 border border-destructive rounded-md">
                            <p class="text-destructive text-sm font-medium">Missing required plugins: ${missingPlugins.join(', ')}</p>
                            <p class="text-destructive/70 text-xs mt-1">Please refresh the page.</p>
                        </div>
                    `;
                }
                console.error('Missing EditorJS plugins:', missingPlugins);
                console.log('Available EditorJS globals:', Object.keys(window).filter(k => k.match(/^(Header|Editorjs|Quote|Table|Code|Delimiter|Warning)/i)));
                return;
            }

            // Build tools object - only include plugins that are available
            const tools = {
                header: {
                    class: HeaderClass,
                    config: {
                        levels: [1, 2, 3, 4],
                        defaultLevel: 2
                    }
                },
                list: {
                    class: ListClass,
                    inlineToolbar: true
                },
                quote: QuoteClass
            };

            // Add optional plugins if available
            if (TableClass) {
                tools.table = {
                    class: TableClass,
                    inlineToolbar: true
                };
            }
            if (CodeClass) {
                tools.code = CodeClass;
            }
            if (DelimiterClass) {
                tools.delimiter = DelimiterClass;
            }
            if (WarningClass) {
                tools.warning = WarningClass;
            }

            // Initialize EditorJS with available plugins
            try {
                // Clear loading indicator
                if (holder) {
                    holder.innerHTML = '';
                }

                const editorConfig = {
                    holder: holderId,
                    tools: tools,
                    data: block.content || { blocks: [] },
                    onChange: async () => {
                        try {
                            const outputData = await editor.save();
                            block.content = outputData;
                            sync();
                        } catch (e) {
                            console.error('EditorJS save error:', e);
                        }
                    },
                    placeholder: 'Start writing your content...',
                    autofocus: false,
                    minHeight: 150
                };

                const editor = new EditorJS(editorConfig);

                // Store instance for form submission
                container._editorInstance = editor;

                // Add success class
                if (holder) {
                    holder.classList.add('cms-editorjs-loaded');
                    holder.classList.remove('cms-editorjs-wrapper');
                }

            } catch (error) {
                if (holder) {
                    holder.innerHTML = `
                        <div class="p-4 bg-destructive/10 border border-destructive rounded-md">
                            <p class="text-destructive text-sm font-medium">Failed to initialize editor</p>
                            <p class="text-destructive/70 text-xs mt-1">${error.message}</p>
                        </div>
                    `;
                }
                console.error('EditorJS initialization error:', error);
            }
        };

        // Wait for DOM to be ready and libraries to load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => setTimeout(initEditor, 100));
        } else {
            setTimeout(initEditor, 100);
        }

        return container;
    }

    function renderCodeFields(block, sync) {
        const container = el('div', { className: 'space-y-4' }, [
            el('div', { className: 'cms-form-group' }, [
                el('label', { className: 'cms-form-label' }, 'HTML/JS Code'),
                el('textarea', {
                    className: 'cms-form-textarea font-mono text-xs',
                    placeholder: '<p>Your trusted HTML/JS code here</p>',
                    value: block.html || '',
                    onchange: (e) => {
                        block.html = e.target.value;
                        sync();
                    }
                })
            ]),
            el('p', { className: 'cms-form-hint' }, 'This code will be rendered as-is. Use only trusted code.')
        ]);
        return container;
    }

    function renderCalloutFields(block, sync) {
        return el('div', { className: 'space-y-4' }, [
            fieldInput({
                label: 'Title',
                value: block.title,
                onChange: (val) => { block.title = val; sync(); }
            }),
            fieldTextarea({
                label: 'Body',
                value: block.body,
                onChange: (val) => { block.body = val; sync(); }
            })
        ]);
    }

    function renderCtaFields(block, sync) {
        return el('div', { className: 'space-y-4' }, [
            fieldInput({
                label: 'Title',
                value: block.title,
                onChange: (val) => { block.title = val; sync(); }
            }),
            fieldTextarea({
                label: 'Body',
                value: block.body,
                onChange: (val) => { block.body = val; sync(); }
            }),
            fieldInput({
                label: 'Button Label',
                value: block.button_label,
                onChange: (val) => { block.button_label = val; sync(); }
            }),
            fieldInput({
                label: 'Button URL',
                value: block.button_url,
                placeholder: 'https://',
                onChange: (val) => { block.button_url = val; sync(); }
            })
        ]);
    }

    function renderFeatureGridFields(block, sync) {
        return el('div', { className: 'cms-feature-grid-editor space-y-4' }, [
            el('div', { className: 'flex items-center justify-between mb-4' }, [
                el('h4', { className: 'cms-form-label mb-0' }, 'Features'),
                el('button', {
                    type: 'button',
                    className: 'cms-btn cms-btn-sm cms-btn-ghost',
                    onclick: () => {
                        block.items.push({ title: '', body: '' });
                        sync();
                        rerender();
                    }
                }, ICONS.plus + ' Add Feature')
            ]),
            el('div', { className: 'space-y-3' }, block.items.map((item, index) => {
                return el('div', { className: 'bg-muted/30 p-4 rounded-md border border-border' }, [
                    fieldInput({
                        label: 'Title',
                        value: item.title,
                        onChange: (val) => {
                            block.items[index].title = val;
                            sync();
                        }
                    }),
                    fieldTextarea({
                        label: 'Description',
                        value: item.body,
                        onChange: (val) => {
                            block.items[index].body = val;
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive mt-2',
                        onclick: () => {
                            block.items.splice(index, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove')
                ]);
            }))
        ]);
    }

    function renderFaqFields(block, sync) {
        return el('div', { className: 'cms-faq-editor space-y-4' }, [
            el('div', { className: 'flex items-center justify-between mb-4' }, [
                el('h4', { className: 'cms-form-label mb-0' }, 'Questions & Answers'),
                el('button', {
                    type: 'button',
                    className: 'cms-btn cms-btn-sm cms-btn-ghost',
                    onclick: () => {
                        block.items.push({ question: '', answer: '' });
                        sync();
                        rerender();
                    }
                }, ICONS.plus + ' Add FAQ')
            ]),
            el('div', { className: 'space-y-3' }, block.items.map((item, index) => {
                return el('div', { className: 'bg-muted/30 p-4 rounded-md border border-border' }, [
                    fieldTextarea({
                        label: 'Question',
                        value: item.question,
                        onChange: (val) => {
                            block.items[index].question = val;
                            sync();
                        }
                    }),
                    fieldTextarea({
                        label: 'Answer',
                        value: item.answer,
                        onChange: (val) => {
                            block.items[index].answer = val;
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive mt-2',
                        onclick: () => {
                            block.items.splice(index, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove')
                ]);
            }))
        ]);
    }

    function renderQuoteFields(block, sync) {
        return el('div', { className: 'space-y-4' }, [
            fieldTextarea({
                label: 'Quote',
                value: block.quote,
                onChange: (val) => { block.quote = val; sync(); }
            }),
            fieldInput({
                label: 'Author',
                value: block.author,
                onChange: (val) => { block.author = val; sync(); }
            })
        ]);
    }

    function renderComparisonTableFields(block, sync) {
        // Simplified version - full implementation would have column/row management
        return el('div', { className: 'cms-table-editor space-y-4' }, [
            el('p', { className: 'cms-form-hint' }, 'Edit headers and rows. Use | to separate values.'),
            fieldTextarea({
                label: 'Headers (comma-separated)',
                value: block.headers ? block.headers.join(', ') : '',
                onChange: (val) => {
                    block.headers = val.split(',').map(h => h.trim());
                    sync();
                }
            }),
            el('div', { className: 'space-y-2' }, block.rows.map((row, rowIndex) => {
                return el('div', { className: 'flex items-center gap-2' }, [
                    fieldInput({
                        label: 'Row ' + (rowIndex + 1),
                        value: row.join(', '),
                        onChange: (val) => {
                            block.rows[rowIndex] = val.split(',').map(c => c.trim());
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive',
                        onclick: () => {
                            block.rows.splice(rowIndex, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove')
                ]);
            })),
            el('button', {
                type: 'button',
                className: 'cms-btn cms-btn-sm cms-btn-ghost',
                onclick: () => {
                    const cols = block.headers ? block.headers.length : 3;
                    block.rows.push(new Array(cols).fill(''));
                    sync();
                    rerender();
                }
            }, ICONS.plus + ' Add Row')
        ]);
    }

    function renderPricingTableFields(block, sync) {
        return el('div', { className: 'cms-pricing-editor space-y-4' }, [
            el('div', { className: 'flex items-center justify-between mb-4' }, [
                el('h4', { className: 'cms-form-label mb-0' }, 'Pricing Plans'),
                el('button', {
                    type: 'button',
                    className: 'cms-btn cms-btn-sm cms-btn-ghost',
                    onclick: () => {
                        block.plans.push({ title: '', price: '', features: [''] });
                        sync();
                        rerender();
                    }
                }, ICONS.plus + ' Add Plan')
            ]),
            el('div', { className: 'space-y-4' }, block.plans.map((plan, index) => {
                return el('div', { className: 'bg-muted/30 p-4 rounded-md border border-border' }, [
                    fieldInput({
                        label: 'Plan Name',
                        value: plan.title,
                        onChange: (val) => {
                            block.plans[index].title = val;
                            sync();
                        }
                    }),
                    fieldInput({
                        label: 'Price',
                        value: plan.price,
                        onChange: (val) => {
                            block.plans[index].price = val;
                            sync();
                        }
                    }),
                    fieldTextarea({
                        label: 'Features (one per line)',
                        value: plan.features ? plan.features.join('\\n') : '',
                        placeholder: 'Feature 1\\nFeature 2\\nFeature 3',
                        onChange: (val) => {
                            block.plans[index].features = val.split('\\n').filter(f => f.trim());
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive mt-2',
                        onclick: () => {
                            block.plans.splice(index, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove Plan')
                ]);
            }))
        ]);
    }

    function renderLogoCloudFields(block, sync) {
        return el('div', { className: 'cms-logo-editor space-y-4' }, [
            el('div', { className: 'flex items-center justify-between mb-4' }, [
                el('h4', { className: 'cms-form-label mb-0' }, 'Logos'),
                el('button', {
                    type: 'button',
                    className: 'cms-btn cms-btn-sm cms-btn-ghost',
                    onclick: () => {
                        block.logos.push({ src: '', alt: '' });
                        sync();
                        rerender();
                    }
                }, ICONS.plus + ' Add Logo')
            ]),
            el('div', { className: 'grid md:grid-cols-2 gap-4' }, block.logos.map((logo, index) => {
                return el('div', { className: 'bg-muted/30 p-4 rounded-md border border-border space-y-3' }, [
                    fieldInput({
                        label: 'Image URL',
                        value: logo.src,
                        placeholder: 'https://',
                        onChange: (val) => {
                            block.logos[index].src = val;
                            sync();
                        }
                    }),
                    fieldInput({
                        label: 'Alt Text',
                        value: logo.alt,
                        onChange: (val) => {
                            block.logos[index].alt = val;
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive',
                        onclick: () => {
                            block.logos.splice(index, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove')
                ]);
            }))
        ]);
    }

    function renderImageGalleryFields(block, sync) {
        return el('div', { className: 'cms-gallery-editor space-y-4' }, [
            fieldInput({
                label: 'Gallery Title',
                value: block.title,
                onChange: (val) => { block.title = val; sync(); }
            }),
            el('div', { className: 'cms-form-group' }, [
                el('label', { className: 'cms-form-label' }, 'Layout'),
                el('select', {
                    className: 'cms-form-select',
                    value: block.layout || 'grid',
                    onchange: (e) => {
                        block.layout = e.target.value;
                        sync();
                    }
                }, [
                    el('option', { value: 'grid' }, 'Grid'),
                    el('option', { value: 'masonry' }, 'Masonry'),
                    el('option', { value: 'carousel' }, 'Carousel')
                ])
            ]),
            el('div', { className: 'flex items-center justify-between mb-4' }, [
                el('h4', { className: 'cms-form-label mb-0' }, 'Images'),
                el('button', {
                    type: 'button',
                    className: 'cms-btn cms-btn-sm cms-btn-ghost',
                    onclick: () => {
                        block.images.push({ src: '', alt: '', caption: '' });
                        sync();
                        rerender();
                    }
                }, ICONS.plus + ' Add Image')
            ]),
            el('div', { className: 'grid md:grid-cols-2 gap-4' }, block.images.map((img, index) => {
                return el('div', { className: 'bg-muted/30 p-4 rounded-md border border-border space-y-3' }, [
                    fieldInput({
                        label: 'Image URL',
                        value: img.src,
                        placeholder: 'https://',
                        onChange: (val) => {
                            block.images[index].src = val;
                            sync();
                        }
                    }),
                    fieldInput({
                        label: 'Alt Text',
                        value: img.alt,
                        onChange: (val) => {
                            block.images[index].alt = val;
                            sync();
                        }
                    }),
                    fieldInput({
                        label: 'Caption',
                        value: img.caption,
                        onChange: (val) => {
                            block.images[index].caption = val;
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive',
                        onclick: () => {
                            block.images.splice(index, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove')
                ]);
            }))
        ]);
    }

    function renderTableFields(block, sync) {
        return el('div', { className: 'cms-table-editor space-y-4' }, [
            fieldTextarea({
                label: 'Headers (comma-separated)',
                value: block.headers ? block.headers.join(', ') : '',
                onChange: (val) => {
                    block.headers = val.split(',').map(h => h.trim());
                    sync();
                }
            }),
            el('div', { className: 'space-y-2' }, block.rows.map((row, rowIndex) => {
                return el('div', { className: 'flex items-center gap-2' }, [
                    fieldInput({
                        label: 'Row ' + (rowIndex + 1),
                        value: row.join(', '),
                        onChange: (val) => {
                            block.rows[rowIndex] = val.split(',').map(c => c.trim());
                            sync();
                        }
                    }),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive',
                        onclick: () => {
                            block.rows.splice(rowIndex, 1);
                            sync();
                            rerender();
                        }
                    }, 'Remove')
                ]);
            })),
            el('button', {
                type: 'button',
                className: 'cms-btn cms-btn-sm cms-btn-ghost',
                onclick: () => {
                    const cols = block.headers ? block.headers.length : 2;
                    block.rows.push(new Array(cols).fill(''));
                    sync();
                    rerender();
                }
            }, ICONS.plus + ' Add Row')
        ]);
    }

    function renderButtonFields(block, sync) {
        return el('div', { className: 'cms-button-editor space-y-4' }, [
            fieldInput({
                label: 'Button Label',
                value: block.label || 'Click Me',
                placeholder: 'Click Me',
                onChange: (val) => { block.label = val; sync(); }
            }),
            fieldInput({
                label: 'Button URL',
                value: block.url || '',
                placeholder: 'https://example.com',
                onChange: (val) => { block.url = val; sync(); }
            }),
            el('div', { className: 'cms-form-group' }, [
                el('label', { className: 'cms-form-label' }, 'Button Style'),
                el('select', {
                    className: 'cms-form-select',
                    value: block.style || 'primary',
                    onchange: (e) => {
                        block.style = e.target.value;
                        sync();
                    }
                }, [
                    el('option', { value: 'primary' }, 'Primary (Filled)'),
                    el('option', { value: 'secondary' }, 'Secondary (Outline)'),
                    el('option', { value: 'ghost' }, 'Ghost (Minimal)'),
                    el('option', { value: 'destructive' }, 'Destructive (Red)')
                ])
            ]),
            el('div', { className: 'cms-form-group' }, [
                el('label', { className: 'cms-form-label flex items-center gap-2' }, [
                    el('input', {
                        type: 'checkbox',
                        checked: block.open_new_tab || false,
                        onchange: (e) => {
                            block.open_new_tab = e.target.checked;
                            sync();
                        }
                    }),
                    'Open in new tab'
                ])
            ]),
            fieldInput({
                label: 'Icon (optional)',
                value: block.icon || '',
                placeholder: 'hero-icon-name or SVG path',
                onChange: (val) => { block.icon = val; sync(); }
            })
        ]);
    }

    // ===== Main Block Builder =====
    function initBlocksBuilder() {
        const builder = document.querySelector('[data-blocks-builder]');
        if (!builder) return;

        const input = document.querySelector('[data-blocks-input]');
        if (!input) return;

        // Parse initial state
        const parsedValue = safeJsonParse(input.value, null);

        let state = {
            blocks: []
        };

        // Handle different value formats
        if (parsedValue && parsedValue.blocks && Array.isArray(parsedValue.blocks)) {
            state.blocks = parsedValue.blocks;
        } else if (parsedValue && Array.isArray(parsedValue)) {
            state.blocks = parsedValue;
        }

        // Normalize state
        if (!Array.isArray(state.blocks)) {
            state.blocks = [];
        }

        // Sync function
        function sync() {
            input.value = JSON.stringify({ blocks: state.blocks });
        }

        // Rerender function
        function rerender() {
            renderBlocks();
        }

        // Render block item
        function renderBlockItem(block, index) {
            const wrapper = el('div', {
                className: 'cms-block-item',
                draggable: true,
                dataset: { index: index }
            });

            const header = el('div', { className: 'cms-block-header' }, [
                el('div', { className: 'flex items-center justify-between w-full' }, [
                    el('span', { className: 'cms-block-title cursor-move' }, ICONS.drag + ' ' + (BLOCK_LABELS[block.type] || block.type)),
                    el('button', {
                        type: 'button',
                        className: 'cms-btn cms-btn-sm cms-btn-destructive cms-delete-block-btn',
                        title: 'Delete this block',
                        'aria-label': 'Delete block',
                        onclick: () => {
                            if (confirm('Are you sure you want to delete this ' + (BLOCK_LABELS[block.type] || block.type) + ' block?')) {
                                state.blocks.splice(index, 1);
                                sync();
                                rerender();
                            }
                        }
                    }, ICONS.trash + ' Delete')
                ])
            ]);

            const content = el('div', { className: 'cms-block-content' });

            // Render fields based on block type
            let contentRenderer;
            switch (block.type) {
                case 'rich_text':
                    contentRenderer = renderRichTextFields(block, sync, rerender);
                    break;
                case 'code':
                    contentRenderer = renderCodeFields(block, sync);
                    break;
                case 'cta':
                    contentRenderer = renderCtaFields(block, sync);
                    break;
                case 'callout':
                    contentRenderer = renderCalloutFields(block, sync);
                    break;
                case 'feature_grid':
                    contentRenderer = renderFeatureGridFields(block, sync, rerender);
                    break;
                case 'faq':
                    contentRenderer = renderFaqFields(block, sync, rerender);
                    break;
                case 'quote':
                    contentRenderer = renderQuoteFields(block, sync);
                    break;
                case 'comparison_table':
                    contentRenderer = renderComparisonTableFields(block, sync, rerender);
                    break;
                case 'pricing_table':
                    contentRenderer = renderPricingTableFields(block, sync, rerender);
                    break;
                case 'logo_cloud':
                    contentRenderer = renderLogoCloudFields(block, sync, rerender);
                    break;
                case 'image_gallery':
                    contentRenderer = renderImageGalleryFields(block, sync, rerender);
                    break;
                case 'table':
                    contentRenderer = renderTableFields(block, sync, rerender);
                    break;
                case 'button':
                    contentRenderer = renderButtonFields(block, sync);
                    break;
                default:
                    contentRenderer = el('p', { className: 'text-muted-foreground' }, 'Unknown block type');
            }

            content.appendChild(contentRenderer);
            wrapper.appendChild(header);
            wrapper.appendChild(content);

            return wrapper;
        }

        // Render all blocks
        function renderBlocks() {
            builder.innerHTML = '';

            // Add "Add block" bar at top with clear all option
            const topBar = el('div', { className: 'cms-add-block-bar' }, [
                el('span', { className: 'text-sm font-medium text-muted-foreground mr-2' }, 'Add block:'),
                state.blocks.length > 0 ? el('button', {
                    type: 'button',
                    className: 'cms-btn cms-btn-sm cms-btn-destructive cms-clear-all-btn',
                    title: 'Delete all blocks',
                    onclick: () => {
                        if (confirm('Are you sure you want to delete ALL blocks? This action cannot be undone.')) {
                            state.blocks = [];
                            sync();
                            rerender();
                        }
                    }
                }, ICONS.trash + ' Clear All') : null
            ]);

            Object.keys(BLOCK_LABELS).forEach(type => {
                const btn = el('button', {
                    type: 'button',
                    className: 'cms-add-block-btn',
                    onclick: () => {
                        state.blocks.push(blockDefaults(type));
                        sync();
                        rerender();
                    }
                }, BLOCK_LABELS[type]);
                topBar.appendChild(btn);
            });

            builder.appendChild(topBar);

            // Render blocks
            const content = el('div', { className: 'cms-blocks-builder-content' });

            if (state.blocks.length === 0) {
                content.innerHTML = `
                    <div class="text-center py-12 text-muted-foreground">
                        <p class="mb-2">No blocks yet</p>
                        <p class="text-sm">Add blocks from the bar above to build your content</p>
                    </div>
                `;
            } else {
                state.blocks.forEach((block, index) => {
                    content.appendChild(renderBlockItem(block, index));
                });
            }

            builder.appendChild(content);

            // Add "Add block" bar at bottom
            const bottomBar = el('div', { className: 'cms-add-block-bar' }, [
                el('span', { className: 'text-sm font-medium text-muted-foreground mr-2' }, 'Add block:')
            ]);

            Object.keys(BLOCK_LABELS).forEach(type => {
                const btn = el('button', {
                    type: 'button',
                    className: 'cms-add-block-btn',
                    onclick: () => {
                        state.blocks.push(blockDefaults(type));
                        sync();
                        rerender();
                    }
                }, BLOCK_LABELS[type]);
                bottomBar.appendChild(btn);
            });

            builder.appendChild(bottomBar);

            // Setup drag and drop
            setupDragAndDrop();
        }

        // Drag and drop
        function setupDragAndDrop() {
            const blocks = builder.querySelectorAll('.cms-block-item');
            let draggedEl = null;

            blocks.forEach(block => {
                block.addEventListener('dragstart', function(e) {
                    draggedEl = this;
                    this.classList.add('dragging');
                    e.dataTransfer.effectAllowed = 'move';
                });

                block.addEventListener('dragend', function() {
                    this.classList.remove('dragging');
                    draggedEl = null;
                });

                block.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    if (this !== draggedEl) {
                        const rect = this.getBoundingClientRect();
                        const midY = rect.top + rect.height / 2;
                        if (e.clientY < midY) {
                            this.parentNode.insertBefore(draggedEl, this);
                        } else {
                            this.parentNode.insertBefore(draggedEl, this.nextSibling);
                        }
                        updateBlockOrder();
                    }
                });
            });
        }

        function updateBlockOrder() {
            const newOrder = [];
            const blocks = builder.querySelectorAll('.cms-block-item');
            blocks.forEach(block => {
                const index = parseInt(block.dataset.index);
                newOrder.push(state.blocks[index]);
            });
            state.blocks = newOrder;
            sync();
        }

        // Form submit hook - CRITICAL: Save EditorJS instances first
        const form = input.closest('form');
        if (form) {
            form.addEventListener('submit', async function(e) {
                // Find all EditorJS instances and save them
                const editors = builder.querySelectorAll('.cms-rich-text-editor');
                const savePromises = [];

                editors.forEach(editorContainer => {
                    if (editorContainer._editorInstance) {
                        const savePromise = editorContainer._editorInstance.save()
                            .then(outputData => {
                                // Update the block content
                                const index = parseInt(editorContainer.closest('.cms-block-item').dataset.index);
                                if (state.blocks[index]) {
                                    state.blocks[index].content = outputData;
                                }
                            })
                            .catch(err => {
                                console.error('EditorJS save error:', err);
                            });
                        savePromises.push(savePromise);
                    }
                });

                // Wait for all EditorJS instances to save
                if (savePromises.length > 0) {
                    e.preventDefault();
                    await Promise.all(savePromises);
                    sync(); // Update hidden input
                    form.submit(); // Now submit the form
                }
            });
        }

        // Initial render
        renderBlocks();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initBlocksBuilder);
    } else {
        initBlocksBuilder();
    }

})();
