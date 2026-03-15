"""
Update homepage content to match pixel-perfect design
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_cms.settings')
django.setup()

from marketing.models import Page
import json

# Get the homepage
home = Page.objects.filter(slug='home').first()

if home:
    # Create exact blocks to match the pixel-perfect design
    blocks_data = {
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
                        }
                    ]
                }
            },
            {
                "type": "code",
                "html": """
                <!-- Hero Section -->
                <section class="relative overflow-hidden">
                    <header class="relative z-20 flex items-center justify-between px-6 md:px-12 lg:px-20 py-5 max-w-7xl mx-auto">
                        <div class="flex items-center gap-3">
                            <img src="/static/assets/logo-icon.png" alt="BeyondCode AI" class="h-9">
                            <span class="font-bold text-foreground text-lg tracking-tight">BeyondCode</span>
                        </div>
                        <div class="flex items-center gap-3">
                            <a href="#how-it-works" class="items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 hover:bg-secondary h-11 px-6 py-2 hidden md:inline-flex text-muted-foreground hover:text-foreground text-sm">How it works</a>
                            <a href="https://calendly.com/henri-beyondcode/ai-collections-demo" target="_blank" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 hover:shadow-lg h-11 bg-primary text-primary-foreground hover:bg-primary/90 text-sm px-5 py-2.5">Book a Quick Demo<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right w-4 h-4 ml-1.5"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a>
                        </div>
                    </header>
                    <div class="relative z-10 text-center px-6 pt-8 pb-6 md:pt-12 md:pb-8 max-w-4xl mx-auto">
                        <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-accent text-accent-foreground text-sm font-medium rounded-full mb-8">
                            <span class="w-2 h-2 rounded-full bg-primary"></span>
                            AI-Powered Debt Collection Platform
                        </div>
                        <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-[1.1] mb-6 text-foreground tracking-tight">Bring Your <span class="text-primary">Money Home</span></h1>
                        <p class="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">Automate debtor outreach across active portfolios so every account is contacted on time—without growing your team or losing compliance control.</p>
                        <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
                            <a href="https://calendly.com/henri-beyondcode/ai-collections-demo" target="_blank" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg ring-offset-background transition-all duration-300 hover:shadow-lg h-11 bg-primary text-primary-foreground hover:bg-primary/90 px-8 py-6 text-base font-semibold shadow-lg shadow-primary/20">Book a Quick Demo<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right w-5 h-5 ml-2"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></a>
                            <a href="#how-it-works" class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 border bg-transparent hover:border-primary/50 h-11 px-8 py-6 text-base border-border text-foreground hover:bg-secondary">See How It Works</a>
                        </div>
                        <div class="py-6">
                            <p class="text-center text-muted-foreground text-sm font-medium tracking-wide uppercase mb-6">Trusted by EU-regulated financial institutions</p>
                            <div class="flex flex-wrap items-center justify-center gap-x-10 gap-y-4 px-6">
                                <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BONDORA</span>
                                <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">RAHA24</span>
                                <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BB-FINANCE</span>
                                <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">HYBA FINANCE</span>
                                <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">THEMIS LAW BUREAU</span>
                                <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BALTASAR LEASING</span>
                            </div>
                        </div>
                    </div>
                </section>
                """
            },
            {
                "type": "code",
                "html": """
                <!-- One Platform Section -->
                <section class="section-padding bg-background">
                    <div class="max-w-6xl mx-auto px-6">
                        <div class="text-center mb-8">
                            <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">One Platform for Compliant AI Collections</h2>
                            <p class="text-muted-foreground text-lg max-w-2xl mx-auto">Unify your outreach, compliance, and analytics in one platform—saving time and cutting costs.</p>
                        </div>
                        <div class="grid md:grid-cols-3 gap-6">
                            <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                                <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap w-5 h-5 text-primary"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path></svg>
                                </div>
                                <h3 class="text-lg font-bold mb-2">Automated Outreach at Scale</h3>
                                <p class="text-sm leading-relaxed text-muted-foreground">Every debtor on your list gets contacted on time, every cycle. Scale from hundreds to thousands of calls without adding headcount.</p>
                            </div>
                            <div class="rounded-xl p-7 border transition-all bg-primary text-primary-foreground border-primary shadow-lg">
                                <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-primary-foreground/20">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield w-5 h-5 text-primary-foreground"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path></svg>
                                </div>
                                <h3 class="text-lg font-bold mb-2">GDPR-Compliant by Design</h3>
                                <p class="text-sm leading-relaxed text-primary-foreground/80">Calling windows, retry rules, and consent guardrails enforced automatically. Audit-ready evidence logs for every interaction.</p>
                            </div>
                            <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                                <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-column w-5 h-5 text-primary"><path d="M3 3v16a2 2 0 0 0 2 2h16"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>
                                </div>
                                <h3 class="text-lg font-bold mb-2">Predictable Recovery Operations</h3>
                                <p class="text-sm leading-relaxed text-muted-foreground">Turn collections into measurable weekly output with real-time analytics, coverage reports, and structured outcome tracking.</p>
                            </div>
                        </div>
                    </div>
                </section>
                """
            }
        ]
    }

    # Update the homepage
    home.blocks_json = blocks_data
    home.save()

    print("Homepage updated with pixel-perfect content!")
else:
    print("No homepage found with slug 'home'")
