"""
Django management command to seed the component registry with MVP components.

Usage: python manage.py seed_component_registry
"""

from django.core.management.base import BaseCommand
from marketing.builder.models import ComponentRegistry


class Command(BaseCommand):
    help = 'Seed component registry with MVP components'

    def handle(self, *args, **options):
        """Seed component registry with all 10 MVP components."""
        self.stdout.write(self.style.SUCCESS('Seeding component registry with MVP components...'))

        components = [
            {
                'name': 'heading',
                'label': 'Heading',
                'category': 'content',
                'icon': 'mdi:format-title',
                'order': 1,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'text': {
                            'type': 'string',
                            'title': 'Text Content',
                            'default': 'Heading Text'
                        },
                        'level': {
                            'type': 'string',
                            'title': 'Heading Level',
                            'enum': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
                            'default': 'h1'
                        },
                        'align': {
                            'type': 'string',
                            'title': 'Alignment',
                            'enum': ['left', 'center', 'right'],
                            'default': 'left'
                        }
                    }
                },
                'default_props': {
                    'type': 'heading',
                    'text': 'Heading Text',
                    'level': 'h1',
                    'align': 'left',
                    'styles': {
                        'gridSpan': 12,
                        'padding': '20px'
                    }
                },
                'is_editable': True,
                'render_component': 'Heading'
            },
            {
                'name': 'text',
                'label': 'Text Paragraph',
                'category': 'content',
                'icon': 'mdi:format-text',
                'order': 2,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'content': {
                            'type': 'string',
                            'title': 'Text Content',
                            'default': 'Your paragraph text here.'
                        }
                    }
                },
                'default_props': {
                    'type': 'text',
                    'content': 'Your paragraph text here.',
                    'styles': {
                        'gridSpan': 12,
                        'padding': '16px'
                    }
                },
                'is_editable': True,
                'render_component': 'Text'
            },
            {
                'name': 'button',
                'label': 'Button',
                'category': 'form',
                'icon': 'mdi:gesture-tap-button',
                'order': 3,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'text': {
                            'type': 'string',
                            'title': 'Button Text',
                            'default': 'Click Me'
                        },
                        'variant': {
                            'type': 'string',
                            'title': 'Button Style',
                            'enum': ['primary', 'secondary', 'text'],
                            'default': 'primary'
                        },
                        'url': {
                            'type': 'string',
                            'title': 'Link URL',
                            'default': '#'
                        },
                        'open_new_tab': {
                            'type': 'boolean',
                            'title': 'Open in New Tab',
                            'default': False
                        }
                    }
                },
                'default_props': {
                    'type': 'button',
                    'text': 'Click Me',
                    'variant': 'primary',
                    'url': '#',
                    'open_new_tab': False,
                    'styles': {
                        'gridSpan': 12,
                        'textAlign': 'center'
                    }
                },
                'is_editable': True,
                'render_component': 'Button'
            },
            {
                'name': 'image',
                'label': 'Image',
                'category': 'media',
                'icon': 'mdi:image',
                'order': 4,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'url': {
                            'type': 'string',
                            'title': 'Image URL',
                            'default': ''
                        },
                        'alt_text': {
                            'type': 'string',
                            'title': 'Alt Text',
                            'default': ''
                        },
                        'width': {
                            'type': 'number',
                            'title': 'Width (px)',
                            'default': 1200
                        },
                        'align': {
                            'type': 'string',
                            'title': 'Alignment',
                            'enum': ['left', 'center', 'right'],
                            'default': 'center'
                        }
                    }
                },
                'default_props': {
                    'type': 'image',
                    'url': '',
                    'alt_text': '',
                    'width': 1200,
                    'align': 'center',
                    'styles': {
                        'gridSpan': 12
                    }
                },
                'requires_asset': True,
                'is_editable': False,
                'render_component': 'Image'
            },
            {
                'name': 'container',
                'label': 'Container',
                'category': 'layout',
                'icon': 'mdi:rectangle-outline',
                'order': 5,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'background_color': {
                            'type': 'string',
                            'title': 'Background Color',
                            'default': '#ffffff'
                        },
                        'padding': {
                            'type': 'string',
                            'title': 'Padding',
                            'default': '20px'
                        },
                        'boxed': {
                            'type': 'boolean',
                            'title': 'Boxed Container',
                            'default': False
                        }
                    }
                },
                'default_props': {
                    'type': 'container',
                    'background_color': '#ffffff',
                    'padding': '20px',
                    'boxed': False,
                    'styles': {
                        'gridSpan': 12
                    }
                },
                'is_editable': False,
                'render_component': 'Container'
            },
            {
                'name': 'columns',
                'label': 'Columns',
                'category': 'layout',
                'icon': 'mdi:view-column',
                'order': 6,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'columns': {
                            'type': 'integer',
                            'title': 'Number of Columns',
                            'enum': [2, 3],
                            'default': 2
                        },
                        'gap': {
                            'type': 'string',
                            'title': 'Column Gap',
                            'default': '16px'
                        }
                    }
                },
                'default_props': {
                    'type': 'columns',
                    'columns': 2,
                    'gap': '16px',
                    'styles': {
                        'gridSpan': 12
                    }
                },
                'is_editable': False,
                'render_component': 'Columns'
            },
            {
                'name': 'divider',
                'label': 'Divider',
                'category': 'layout',
                'icon': 'mdi:minus',
                'order': 7,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'orientation': {
                            'type': 'string',
                            'title': 'Orientation',
                            'enum': ['horizontal', 'vertical'],
                            'default': 'horizontal'
                        },
                        'thickness': {
                            'type': 'integer',
                            'title': 'Thickness (px)',
                            'default': 1
                        },
                        'color': {
                            'type': 'string',
                            'title': 'Line Color',
                            'default': '#e0e0e0'
                        }
                    }
                },
                'default_props': {
                    'type': 'divider',
                    'orientation': 'horizontal',
                    'thickness': 1,
                    'color': '#e0e0e0',
                    'styles': {
                        'gridSpan': 12,
                        'margin': '20px 0'
                    }
                },
                'is_editable': False,
                'render_component': 'Divider'
            },
            {
                'name': 'spacer',
                'label': 'Spacer',
                'category': 'layout',
                'icon': 'mdi:arrow-expand-horizontal',
                'order': 8,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'height': {
                            'type': 'string',
                            'title': 'Spacer Height',
                            'default': '20px'
                        }
                    }
                },
                'default_props': {
                    'type': 'spacer',
                    'height': '20px',
                    'styles': {
                        'gridSpan': 12
                    }
                },
                'is_editable': False,
                'render_component': 'Spacer'
            },
            {
                'name': 'quote',
                'label': 'Quote',
                'category': 'content',
                'icon': 'mdi:format-quote-close',
                'order': 9,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'text': {
                            'type': 'string',
                            'title': 'Quote Text',
                            'default': 'This is a testimonial quote from a satisfied customer.'
                        },
                        'author': {
                            'type': 'string',
                            'title': 'Author Name',
                            'default': ''
                        },
                        'align': {
                            'type': 'string',
                            'title': 'Alignment',
                            'enum': ['left', 'center', 'right'],
                            'default': 'center'
                        }
                    }
                },
                'default_props': {
                    'type': 'quote',
                    'text': 'This is a testimonial quote from a satisfied customer.',
                    'author': '',
                    'align': 'center',
                    'styles': {
                        'gridSpan': 12,
                        'padding': '20px',
                        'fontStyle': 'italic'
                    }
                },
                'is_editable': True,
                'render_component': 'Quote'
            },
            {
                'name': 'form',
                'label': 'Form Container',
                'category': 'form',
                'icon': 'mdi:form-textbox',
                'order': 10,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'form_title': {
                            'type': 'string',
                            'title': 'Form Title',
                            'default': 'Contact Us'
                        },
                        'submit_button_text': {
                            'type': 'string',
                            'title': 'Submit Button Text',
                            'default': 'Send'
                        },
                        'success_message': {
                            'type': 'string',
                            'title': 'Success Message',
                            'default': 'Thank you! We will get back to you soon.'
                        }
                    }
                },
                'default_props': {
                    'type': 'form',
                    'form_title': 'Contact Us',
                    'submit_button_text': 'Send',
                    'success_message': 'Thank you! We will get back to you soon.',
                    'styles': {
                        'gridSpan': 12
                    }
                },
                'is_editable': True,
                'render_component': 'Form'
            },
        ]

        created_count = 0
        for component_data in components:
            component, created = ComponentRegistry.objects.get_or_create(
                name=component_data['name'],
                defaults=component_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"  [OK] Created component: {component_data['label']}")
            else:
                self.stdout.write(f"  [INFO] Component already exists: {component_data['label']}")

        self.stdout.write(self.style.SUCCESS(f'\n[OK] Seeded {created_count} components'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Total components in registry: {ComponentRegistry.objects.count()}'))