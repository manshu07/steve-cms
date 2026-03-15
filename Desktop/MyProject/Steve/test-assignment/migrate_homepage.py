import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
django.setup()

from marketing.models import Page

# Create comprehensive blocks_json for homepage matching the hardcoded template
homepage_blocks = {
    "blocks": [
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "Bring Your Money Home",
                            "level": 1
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "Automate debtor outreach across active portfolios so every account is contacted on time—without growing your team or losing compliance control."
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "AI-Powered Debt Collection Platform"
                        }
                    }
                ]
            }
        },
        {
            "type": "cta",
            "title": "Get Started Today",
            "body": "Book a demo to see how BeyondCode AI can transform your debt collection operations.",
            "button_label": "Book a Quick Demo",
            "button_url": "https://calendly.com/henri-beyondcode/ai-collections-demo",
            "secondary_button_label": "See How It Works",
            "secondary_button_url": "#how-it-works"
        },
        {
            "type": "logo_cloud",
            "logos": [
                {"src": "", "alt": "BONDORA"},
                {"src": "", "alt": "RAHA24"},
                {"src": "", "alt": "BB-FINANCE"},
                {"src": "", "alt": "HYBA FINANCE"},
                {"src": "", "alt": "THEMIS LAW BUREAU"},
                {"src": "", "alt": "BALTASAR LEASING"}
            ]
        },
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "One Platform for Compliant AI Collections",
                            "level": 2
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "Unify your outreach, compliance, and analytics in one platform—saving time and cutting costs."
                        }
                    }
                ]
            }
        },
        {
            "type": "feature_grid",
            "items": [
                {
                    "title": "Automated Outreach at Scale",
                    "body": "Every debtor on your list gets contacted on time, every cycle. Scale from hundreds to thousands of calls without adding headcount."
                },
                {
                    "title": "GDPR-Compliant by Design",
                    "body": "Calling windows, retry rules, and consent guardrails enforced automatically. Audit-ready evidence logs for every interaction."
                },
                {
                    "title": "Predictable Recovery Operations",
                    "body": "Turn collections into measurable weekly output with real-time analytics, coverage reports, and structured outcome tracking."
                }
            ]
        },
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "Real Results From a Live Portfolio",
                            "level": 2
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "Measurable impact from a single month of automated AI collection on an EU-regulated portfolio."
                        }
                    }
                ]
            }
        },
        {
            "type": "callout",
            "title": "Case Study · 1 Month Results",
            "body": "**Stats:**\n\n• 4,000 AI Calls Completed\n• €20,000 In Promised Payments\n• 150 Debtors Reached\n• 87 Hours Saved\n• 0 Manual Work Required"
        },
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "Hear From a Law Bureau Running Live Collections",
                            "level": 2
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "See how Themis Law Bureau uses BeyondCode to automate debtor outreach at scale."
                        }
                    }
                ]
            }
        },
        {
            "type": "html_embed",
            "html": '<div class="relative aspect-video rounded-xl overflow-hidden border border-border shadow-lg"><iframe src="https://www.youtube.com/embed/qltjKKA6wFc?controls=1&rel=0" title="Client testimonial – Themis Law Bureau" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen class="absolute inset-0 w-full h-full"></iframe></div>'
        },
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "Transform Your Debt Collection With Our Compliant AI Solution",
                            "level": 2
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "Everything you need to automate, scale, and audit your collection operations—in one platform."
                        }
                    }
                ]
            }
        },
        {
            "type": "feature_grid",
            "items": [
                {
                    "title": "GDPR-Compliant Calling",
                    "body": "Automated enforcement of calling windows, consent rules, and data retention policies."
                },
                {
                    "title": "Personalized Scripts & Tone",
                    "body": "Tailored conversation flows per debtor profile, segment, and debt stage."
                },
                {
                    "title": "Automated Conversations",
                    "body": "Identity verification, debt notification, and payment agreement—handled automatically."
                },
                {
                    "title": "Zero Manual Dialing",
                    "body": "Free your team from repetitive chasing. Humans only for exceptions and disputes."
                }
            ]
        },
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "How It Works",
                            "level": 2
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "Four structured steps from onboarding to go-live. Built for fast deployment and clear operational readiness."
                        }
                    }
                ]
            }
        },
        {
            "type": "feature_grid",
            "items": [
                {
                    "title": "01 - Launch Sprint",
                    "body": "One guided setup window — live before we end. Accounts + billing ready in days, not months."
                },
                {
                    "title": "02 - Telecom Clearance",
                    "body": "Telephony KYC fast-track with country checklist, path, and next actions. No bureaucratic delays."
                },
                {
                    "title": "03 - System Alignment",
                    "body": "Inputs → decisions → outputs. We map the data flow and connect in phases."
                },
                {
                    "title": "04 - Go-Live Readiness",
                    "body": "End-to-end test until stable + handover pack. You're operational with full documentation."
                }
            ]
        },
        {
            "type": "rich_text",
            "content": {
                "blocks": [
                    {
                        "type": "header",
                        "data": {
                            "text": "Operational Delivery Commitment",
                            "level": 2
                        }
                    },
                    {
                        "type": "paragraph",
                        "data": {
                            "text": "Within 40 business days of payment, for the agreed rollout scope:"
                        }
                    }
                ]
            }
        },
        {
            "type": "callout",
            "title": "Our Commitment",
            "body": "**✓ 100% contact-attempt coverage** across the approved debtor list\n\n**✓ Auditable evidence logs** for attempts, timestamps, and outcomes\n\n**✓ 30 days of remediation** for delivery gaps\n\n**✓ Implementation fee reimbursement** if standards remain unmet"
        },
        {
            "type": "cta",
            "title": "Ready to Transform Your Collections?",
            "body": "Book a demo to see how BeyondCode AI can help you achieve 100% contact-attempt coverage with audit-ready evidence logs.",
            "button_label": "See If It Fits",
            "button_url": "https://calendly.com/henri-beyondcode/ai-collections-demo"
        }
    ]
}

# Update the homepage in CMS
try:
    home_page = Page.objects.get(slug='home')
    home_page.blocks_json = homepage_blocks
    home_page.title = "Home"
    home_page.status = 'published'
    home_page.seo_title = "BeyondCode AI | Collections Automation for EU Lenders"
    home_page.seo_description = "Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days."
    home_page.og_title = "BeyondCode AI | Collections Automation for EU Lenders"
    home_page.og_description = "Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days."
    home_page.save()
    print(f"[SUCCESS] Successfully updated homepage '{home_page.title}' with {len(homepage_blocks['blocks'])} content blocks")
    print(f"   - Page ID: {home_page.id}")
    print(f"   - Status: {home_page.status}")
    print(f"   - Slug: {home_page.slug}")
except Page.DoesNotExist:
    print("[ERROR] Homepage with slug='home' not found. Creating new homepage...")
    home_page = Page.objects.create(
        title="Home",
        slug="home",
        status="published",
        blocks_json=homepage_blocks,
        seo_title="BeyondCode AI | Collections Automation for EU Lenders",
        seo_description="Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days.",
        og_title="BeyondCode AI | Collections Automation for EU Lenders",
        og_description="Turn collections backlogs into predictable throughput. 100% contact-attempt coverage with audit-ready evidence logs within 40 business days."
    )
    print(f"[SUCCESS] Successfully created homepage '{home_page.title}' with {len(homepage_blocks['blocks'])} content blocks")
    print(f"   - Page ID: {home_page.id}")
    print(f"   - Status: {home_page.status}")
    print(f"   - Slug: {home_page.slug}")

print("\n[INFO] Homepage content blocks:")
for i, block in enumerate(homepage_blocks['blocks'], 1):
    print(f"   {i}. {block['type']}: {block.get('title', block.get('content', {}).get('blocks', [{}])[0].get('data', {}).get('text', ''))[:50]}")
