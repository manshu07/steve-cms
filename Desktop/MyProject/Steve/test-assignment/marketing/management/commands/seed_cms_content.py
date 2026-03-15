"""
Django management command to seed CMS with sample content.
Usage: python manage.py seed_cms_content
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketing.models import Page, Post, Category, Tag, NavMenu, Footer
from marketing.models import PublishedStatus
import json


class Command(BaseCommand):
    help = 'Seed CMS with sample pages, posts, categories, tags, nav, and footer'

    def handle(self, *args, **options):
        self.stdout.write('Seeding CMS content...')

        # Get or create superuser
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.WARNING('No superuser found. Skipping content creation.'))
            return

        # Clear existing content
        Page.objects.all().delete()
        Post.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        NavMenu.objects.all().delete()
        Footer.objects.all().delete()

        # Create Categories
        categories_data = [
            {'name': 'Industry News', 'slug': 'industry-news'},
            {'name': 'Product Updates', 'slug': 'product-updates'},
            {'name': 'Case Studies', 'slug': 'case-studies'},
            {'name': 'How-To Guides', 'slug': 'how-to-guides'},
            {'name': 'Company', 'slug': 'company'},
        ]
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat.name] = cat
            self.stdout.write(f'  {"Created" if created else "Found"} category: {cat.name}')

        # Create Tags
        tags_data = [
            {'name': 'AI Automation', 'slug': 'ai-automation'},
            {'name': 'Debt Collection', 'slug': 'debt-collection'},
            {'name': 'Compliance', 'slug': 'compliance'},
            {'name': 'EU Regulations', 'slug': 'eu-regulations'},
        ]
        tags = {}
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                slug=tag_data['slug'],
                defaults={'name': tag_data['name']}
            )
            tags[tag.name] = tag
            self.stdout.write(f'  {"Created" if created else "Found"} tag: {tag.name}')

        # Create Pages
        pages_data = [
            {
                'title': 'About BeyondCode AI',
                'slug': 'about',
                'status': PublishedStatus.PUBLISHED,
                'seo_title': 'About BeyondCode AI - Intelligent Debt Collection Automation',
                'seo_description': 'Learn how BeyondCode AI transforms debt collection with enterprise-grade automation, AI-powered compliance, and seamless payment solutions.',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'blocks': [
                                    {'type': 'header', 'data': {'text': 'About BeyondCode AI', 'level': 1}},
                                    {'type': 'paragraph', 'data': {'text': 'BeyondCode AI brings enterprise-grade automation to debt collection, helping agencies recover more while maintaining compliance and customer relationships.'}},
                                ]
                            }
                        },
                        {
                            'type': 'feature_grid',
                            'content': {
                                'heading': 'Our Mission',
                                'features': json.dumps([
                                    {
                                        'icon': '🤖',
                                        'title': 'AI-Powered Automation',
                                        'description': 'Intelligent workflows that adapt to each debtor\'s communication preferences.'
                                    },
                                    {
                                        'icon': '🔒',
                                        'title': 'Compliance First',
                                        'description': 'Built-in safeguards for GDPR, FDCPA, and EU debt collection regulations.'
                                    },
                                    {
                                        'icon': '💳',
                                        'title': 'Seamless Payments',
                                        'description': 'Integrated payment processing with multiple methods and instant confirmation.'
                                    },
                                    {
                                        'icon': '📊',
                                        'title': 'Real-Time Analytics',
                                        'description': 'Track performance, recovery rates, and team productivity in one dashboard.'
                                    },
                                ])
                            }
                        },
                        {
                            'type': 'callout',
                            'content': {
                                'type': 'info',
                                'heading': 'Trusted by Leading Agencies',
                                'body': 'BeyondCode AI powers debt collection for agencies across Europe, processing millions of communications while maintaining 99.9% compliance with regulatory requirements.'
                            }
                        },
                        {
                            'type': 'cta',
                            'content': {
                                'heading': 'Ready to Transform Your Collections?',
                                'body': 'Join the agencies using BeyondCode AI to recover more, faster.',
                                'button_text': 'Get Started',
                                'button_url': '/contact',
                                'variant': 'primary'
                            }
                        },
                    ]
                }
            },
            {
                'title': 'Pricing',
                'slug': 'pricing',
                'status': PublishedStatus.PUBLISHED,
                'seo_title': 'Pricing Plans - BeyondCode AI',
                'seo_description': 'Transparent pricing for debt collection automation. Choose the plan that fits your agency\'s needs.',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'blocks': [
                                    {'type': 'header', 'data': {'text': 'Simple, Transparent Pricing', 'level': 1}},
                                    {'type': 'paragraph', 'data': {'text': 'Choose the plan that fits your agency\'s volume and needs. All plans include our core automation features.'}},
                                ]
                            }
                        },
                        {
                            'type': 'pricing_table',
                            'content': {
                                'heading': 'Choose Your Plan',
                                'plans': json.dumps([
                                    {
                                        'name': 'Starter',
                                        'price': '€299',
                                        'period': 'month',
                                        'description': 'Perfect for small agencies',
                                        'features': [
                                            'Up to 1,000 debtors/month',
                                            'Email automation',
                                            'Basic analytics',
                                            'Email support'
                                        ],
                                        'button_text': 'Start Free Trial',
                                        'button_url': '/contact',
                                        'highlight': False
                                    },
                                    {
                                        'name': 'Professional',
                                        'price': '€799',
                                        'period': 'month',
                                        'description': 'For growing agencies',
                                        'features': [
                                            'Up to 5,000 debtors/month',
                                            'Email + SMS automation',
                                            'Advanced analytics',
                                            'Priority support',
                                            'Custom workflows'
                                        ],
                                        'button_text': 'Start Free Trial',
                                        'button_url': '/contact',
                                        'highlight': True
                                    },
                                    {
                                        'name': 'Enterprise',
                                        'price': 'Custom',
                                        'period': '',
                                        'description': 'For large operations',
                                        'features': [
                                            'Unlimited debtors',
                                            'All communication channels',
                                            'Dedicated account manager',
                                            'Custom integrations',
                                            'SLA guarantee'
                                        ],
                                        'button_text': 'Contact Sales',
                                        'button_url': '/contact',
                                        'highlight': False
                                    },
                                ])
                            }
                        },
                        {
                            'type': 'faq',
                            'content': {
                                'heading': 'Frequently Asked Questions',
                                'items': json.dumps([
                                    {
                                        'question': 'Can I change plans later?',
                                        'answer': 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect at the start of your next billing cycle.'
                                    },
                                    {
                                        'question': 'What payment methods do you accept?',
                                        'answer': 'We accept all major credit cards, bank transfers, and SEPA payments for EU customers.'
                                    },
                                    {
                                        'question': 'Is there a free trial?',
                                        'answer': 'Yes, all plans come with a 14-day free trial. No credit card required to start.'
                                    },
                                ])
                            }
                        },
                    ]
                }
            },
            {
                'title': 'Contact',
                'slug': 'contact',
                'status': PublishedStatus.PUBLISHED,
                'seo_title': 'Contact Us - BeyondCode AI',
                'seo_description': 'Get in touch with the BeyondCode AI team. We\'re here to help you automate your debt collection.',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'blocks': [
                                    {'type': 'header', 'data': {'text': 'Get in Touch', 'level': 1}},
                                    {'type': 'paragraph', 'data': {'text': 'Have questions about BeyondCode AI? Our team is here to help you find the right solution for your agency.'}},
                                ]
                            }
                        },
                        {
                            'type': 'feature_grid',
                            'content': {
                                'heading': 'Contact Options',
                                'features': json.dumps([
                                    {
                                        'icon': '📧',
                                        'title': 'Email Us',
                                        'description': 'info@beyondcode.ai'
                                    },
                                    {
                                        'icon': '📞',
                                        'title': 'Call Us',
                                        'description': '+1 (555) 123-4567'
                                    },
                                    {
                                        'icon': '💬',
                                        'title': 'Live Chat',
                                        'description': 'Available 9AM-6PM CET'
                                    },
                                    {
                                        'icon': '🏢',
                                        'title': 'Office',
                                        'description': 'Berlin, Germany'
                                    },
                                ])
                            }
                        },
                        {
                            'type': 'callout',
                            'content': {
                                'type': 'success',
                                'heading': 'Ready to Get Started?',
                                'body': 'Schedule a demo with our team to see how BeyondCode AI can transform your debt collection operations.'
                            }
                        },
                    ]
                }
            },
        ]

        for page_data in pages_data:
            page = Page.objects.create(**page_data)
            self.stdout.write(self.style.SUCCESS(f'  OK - Created page: {page.title}'))

        # Create Blog Posts
        posts_data = [
            {
                'title': 'The Future of Debt Collection: AI Automation in 2024',
                'slug': 'future-of-debt-collection-ai-automation',
                'author_name': 'Sarah Chen',
                'status': PublishedStatus.PUBLISHED,
                'excerpt': 'Discover how AI is transforming debt collection, from intelligent chatbots to predictive analytics.',
                'cover_image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=630&fit=crop',
                'seo_title': 'The Future of Debt Collection: AI Automation in 2024',
                'seo_description': 'Explore how AI automation is revolutionizing debt collection with intelligent communication, predictive analytics, and compliance safeguards.',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'blocks': [
                                    {'type': 'paragraph', 'data': {'text': 'The debt collection industry is undergoing a massive transformation, driven by artificial intelligence and automation. Agencies that embrace these technologies are seeing dramatic improvements in recovery rates, customer satisfaction, and operational efficiency.'}},
                                    {'type': 'header', 'data': {'text': 'Key Trends Shaping 2024', 'level': 2}},
                                ]
                            }
                        },
                        {
                            'type': 'feature_grid',
                            'content': {
                                'heading': '',
                                'features': json.dumps([
                                    {
                                        'icon': '🤖',
                                        'title': 'Intelligent Chatbots',
                                        'description': '24/7 debtor engagement with natural language processing.'
                                    },
                                    {
                                        'icon': '📈',
                                        'title': 'Predictive Analytics',
                                        'description': 'Machine learning models that predict the best time and channel to contact debtors.'
                                    },
                                    {
                                        'icon': '🎯',
                                        'title': 'Personalization',
                                        'description': 'Tailored communication strategies based on debtor behavior and preferences.'
                                    },
                                ])
                            }
                        },
                        {
                            'type': 'quote',
                            'content': {
                                'text': 'Agencies using AI-powered automation are seeing 30-40% improvement in recovery rates while reducing operational costs by 50%.',
                                'author': 'Industry Report 2024',
                                'role': 'Debt Collection Technology Association'
                            }
                        },
                        {
                            'type': 'callout',
                            'content': {
                                'type': 'warning',
                                'heading': 'Compliance Remains Critical',
                                'body': 'While AI offers tremendous potential, maintaining compliance with GDPR, FDCPA, and EU debt collection regulations is more important than ever. Modern AI systems include built-in compliance safeguards.'
                            }
                        },
                    ]
                }
            },
            {
                'title': 'EU Debt Collection Regulations: A Complete Compliance Guide',
                'slug': 'eu-debt-collection-regulations-guide',
                'author_name': 'Marcus Weber',
                'status': PublishedStatus.PUBLISHED,
                'excerpt': 'Everything you need to know about complying with EU debt collection regulations across different member states.',
                'cover_image': 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&h=630&fit=crop',
                'seo_title': 'EU Debt Collection Regulations: Complete Compliance Guide',
                'seo_description': 'Learn the essential requirements for compliant debt collection across EU member states, including GDPR, consumer protection laws, and best practices.',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'blocks': [
                                    {'type': 'paragraph', 'data': {'text': 'Navigating the complex landscape of EU debt collection regulations is challenging but essential for any agency operating in Europe. This guide breaks down the key requirements across major markets.'}},
                                    {'type': 'header', 'data': {'text': 'Core Regulatory Framework', 'level': 2}},
                                ]
                            }
                        },
                        {
                            'type': 'comparison_table',
                            'content': {
                                'heading': 'Regulations by Country',
                                'headers': json.dumps(['Country', 'Key Law', 'Contact Hours', 'Documentation']),
                                'rows': json.dumps([
                                    ['Germany', 'BDU Code of Conduct', '8AM-8PM weekdays', 'Written notice required'],
                                    ['UK', 'Financial Conduct Authority', '8AM-9PM daily', 'Default notice required'],
                                    ['France', 'Consumer Code', '9AM-8PM weekdays', 'Formal demand letter'],
                                    ['Netherlands', 'Code of Conduct', '9AM-9PM daily', 'Written confirmation'],
                                ])
                            }
                        },
                        {
                            'type': 'callout',
                            'content': {
                                'type': 'info',
                                'heading': 'GDPR Implications',
                                'body': 'All debt collection activities must comply with GDPR, including proper data minimization, storage limitations, and the right to be forgotten. Debtors have the right to request all personal data and its deletion.'
                            }
                        },
                    ]
                }
            },
            {
                'title': '5 Ways Automation Improves Debt Collection Recovery Rates',
                'slug': '5-ways-automation-improves-debt-collection',
                'author_name': 'Sarah Chen',
                'status': PublishedStatus.DRAFT,
                'excerpt': 'Learn how automation technology is helping agencies recover more debt while improving customer relationships.',
                'cover_image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=630&fit=crop',
                'seo_title': '5 Ways Automation Improves Debt Collection Recovery Rates',
                'seo_description': 'Discover the five key ways automation technology is transforming debt collection and improving recovery rates for modern agencies.',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'blocks': [
                                    {'type': 'header', 'data': {'text': '1. Timely, Consistent Communication', 'level': 3}},
                                    {'type': 'paragraph', 'data': {'text': 'Automation ensures that debtors receive regular, on-time reminders through their preferred channels. This consistency builds trust and increases the likelihood of payment.'}},
                                    {'type': 'header', 'data': {'text': '2. Optimal Timing', 'level': 3}},
                                    {'type': 'paragraph', 'data': {'text': 'AI-powered systems analyze debtor behavior to determine the optimal time to send reminders, increasing engagement rates by up to 40%.'}},
                                ]
                            }
                        },
                    ]
                }
            },
        ]

        for post_data in posts_data:
            post = Post.objects.create(**post_data)
            # Add categories and tags
            if post.title == 'The Future of Debt Collection: AI Automation in 2024':
                post.categories.add(categories['Industry News'], categories['Product Updates'])
                post.tags.add(tags['AI Automation'], tags['Debt Collection'])
            elif post.title == 'EU Debt Collection Regulations: A Complete Compliance Guide':
                post.categories.add(categories['How-To Guides'])
                post.tags.add(tags['Compliance'], tags['EU Regulations'])
            elif post.title == '5 Ways Automation Improves Debt Collection Recovery Rates':
                post.categories.add(categories['Product Updates'])
                post.tags.add(tags['AI Automation'])
            self.stdout.write(self.style.SUCCESS(f'  OK - Created post: {post.title}'))

        # Create Navigation Menu
        nav_menu = NavMenu.objects.create(
            items_json=json.dumps([
                {'label': 'Home', 'url': '/', 'order': 1},
                {'label': 'About', 'url': '/about/', 'order': 2},
                {'label': 'Pricing', 'url': '/pricing/', 'order': 3},
                {'label': 'Blog', 'url': '/blog/', 'order': 4},
                {'label': 'Contact', 'url': '/contact/', 'order': 5},
            ])
        )
        self.stdout.write(self.style.SUCCESS('  OK - Created navigation menu'))

        # Create Footer
        footer = Footer.objects.create(
            columns_json=json.dumps([
                {
                    'heading': 'Product',
                    'links': [
                        {'label': 'Features', 'url': '/#features'},
                        {'label': 'Pricing', 'url': '/pricing/'},
                        {'label': 'Case Studies', 'url': '/blog/?category=case-studies'},
                    ]
                },
                {
                    'heading': 'Company',
                    'links': [
                        {'label': 'About', 'url': '/about/'},
                        {'label': 'Blog', 'url': '/blog/'},
                        {'label': 'Careers', 'url': '#'},
                    ]
                },
                {
                    'heading': 'Legal',
                    'links': [
                        {'label': 'Privacy Policy', 'url': '/privacy/'},
                        {'label': 'Terms of Service', 'url': '/terms/'},
                        {'label': 'Sitemap', 'url': '/sitemap.xml'},
                    ]
                },
            ]),
            cta_title='Ready to Transform Your Debt Collection?',
            cta_body='Join agencies across Europe using BeyondCode AI to recover more, faster.',
            cta_button_label='Get Started',
            cta_button_url='/contact/',
            legal_text='© 2024 BeyondCode AI. All rights reserved.'
        )
        self.stdout.write(self.style.SUCCESS('  OK - Created footer'))

        self.stdout.write(self.style.SUCCESS('\n*** CMS content seeded successfully! ***'))
        self.stdout.write(self.style.SUCCESS(f'\nCreated {Page.objects.count()} pages'))
        self.stdout.write(self.style.SUCCESS(f'Created {Post.objects.count()} posts'))
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
        self.stdout.write(self.style.SUCCESS(f'Created {Tag.objects.count()} tags'))
        self.stdout.write(self.style.SUCCESS('\nYou can now:'))
        self.stdout.write('  - Visit the homepage at: /')
        self.stdout.write('  - Access the CMS at: /cms/')
        self.stdout.write('  - View the blog at: /blog/')
        self.stdout.write('  - View the sitemap at: /sitemap.xml')
