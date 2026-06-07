"use client";

import { useCallback } from "react";
import Link from "next/link";
import {
  TrendingUp,
  BookOpen,
  Beaker,
  Trophy,
  Shield,
  Sparkles,
  ArrowRight,
  Check,
  BarChart3,
  Zap,
} from "lucide-react";
import { useScrollReveal } from "@/lib/use-scroll-reveal";

const features = [
  {
    icon: BarChart3,
    title: "Live Charts",
    desc: "Real-time candlestick charts with technical indicators. Monitor any market from a single workspace.",
  },
  {
    icon: BookOpen,
    title: "Trade Journal",
    desc: "Log every trade with notes, tags, screenshots, and emotions. Track what works and what doesn't.",
  },
  {
    icon: Beaker,
    title: "Strategy Backtesting",
    desc: "Test your strategies against historical data before risking capital. Know your edge before you trade.",
  },
  {
    icon: Trophy,
    title: "Leaderboards",
    desc: "Compete with verified traders. Performance is public — reputation is earned through results.",
  },
  {
    icon: Shield,
    title: "Verified Profiles",
    desc: "Verified traders can prove their track record. No fake P&Ls, no anonymous gurus.",
  },
  {
    icon: Sparkles,
    title: "AI Insights",
    desc: "Get pattern recognition, risk analysis, and behavioral feedback powered by AI.",
  },
];

const plans = [
  {
    name: "Free",
    price: "$0",
    desc: "Get started with basic tools",
    features: ["5 trades per month", "Basic charts", "Community access"],
  },
  {
    name: "Pro",
    price: "$19",
    desc: "For active traders",
    popular: true,
    features: [
      "Unlimited trades",
      "Real-time charts",
      "Backtesting engine",
      "AI trade analysis",
      "Priority support",
    ],
  },
  {
    name: "Elite",
    price: "$49",
    desc: "For verified professionals",
    features: [
      "Everything in Pro",
      "Verified profile",
      "Creator monetization",
      "Custom indicators",
      "API access",
      "Dedicated support",
    ],
  },
];

const steps = [
  {
    step: "01",
    title: "Track everything",
    desc: "Log every trade with notes, screenshots, and emotions. Know exactly what works.",
  },
  {
    step: "02",
    title: "Prove your results",
    desc: "Get verified, build your reputation, and let performance speak for itself.",
  },
  {
    step: "03",
    title: "Grow and monetize",
    desc: "Earn followers, publish your track record, and monetize your trading expertise.",
  },
];

function useTilt() {
  const handleMouseMove = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -8;
    const rotateY = ((x - centerX) / centerX) * 8;
    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
  }, []);

  const handleMouseLeave = useCallback((e: React.MouseEvent<HTMLDivElement>) => {
    e.currentTarget.style.transform =
      "perspective(800px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)";
  }, []);

  return { handleMouseMove, handleMouseLeave };
}

export default function LandingPage() {
  const { handleMouseMove, handleMouseLeave } = useTilt();
  const { ref: featuresRef, isVisible: featuresVisible } = useScrollReveal<HTMLDivElement>();
  const { ref: stepsRef, isVisible: stepsVisible } = useScrollReveal<HTMLDivElement>();
  const { ref: pricingRef, isVisible: pricingVisible } = useScrollReveal<HTMLDivElement>();
  const { ref: ctaRef, isVisible: ctaVisible } = useScrollReveal<HTMLDivElement>();

  return (
    <div className="min-h-screen bg-background">
      <header className="fixed top-0 z-50 w-full border-b border-transparent bg-background/60 backdrop-blur-xl">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          <Link href="/" className="flex items-center gap-2 font-semibold tracking-tight">
            <TrendingUp className="h-5 w-5 text-primary" aria-hidden="true" />
            <span className="text-foreground">TradeSaaS</span>
          </Link>
          <nav className="flex items-center gap-1 text-sm">
            <Link
              href="#features"
              className="rounded-md px-3 py-1.5 text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Features
            </Link>
            <Link
              href="#pricing"
              className="rounded-md px-3 py-1.5 text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Pricing
            </Link>
            <Link
              href="/auth/login"
              className="rounded-md px-3 py-1.5 text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Sign in
            </Link>
            <Link
              href="/auth/register"
              className="ml-2 inline-flex h-8 items-center rounded-md bg-primary px-3 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Get Started
            </Link>
          </nav>
        </div>
      </header>

      <section className="relative overflow-hidden border-b border-border/40">
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          <div className="absolute -top-40 right-0 h-[600px] w-[600px] rounded-full bg-primary/5 blur-3xl animate-float-slow" />
          <div className="absolute -bottom-40 left-0 h-[500px] w-[500px] rounded-full bg-accent/5 blur-3xl animate-float" />

          <div className="absolute left-[15%] top-[20%] h-3 w-3 rounded-full bg-primary/30 animate-float" style={{ animationDelay: "-2s" }} />
          <div className="absolute right-[20%] top-[30%] h-2 w-2 rounded-full bg-accent/40 animate-float-slow" style={{ animationDelay: "-4s" }} />
          <div className="absolute left-[25%] bottom-[25%] h-2.5 w-2.5 rounded-full bg-primary/20 animate-float" style={{ animationDuration: "7s" }} />
          <div className="absolute right-[30%] bottom-[30%] h-3 w-3 rounded-full bg-accent/20 animate-float-slow" style={{ animationDelay: "-6s" }} />
          <div className="absolute left-[50%] top-[15%] h-1 w-1 rounded-full bg-primary/40 animate-float" style={{ animationDelay: "-1s" }} />
          <div className="absolute right-[10%] top-[60%] h-1.5 w-1.5 rounded-full bg-accent/30 animate-float-slow" style={{ animationDelay: "-3s" }} />

          <svg
            className="absolute inset-0 h-full w-full opacity-[0.03]"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
                <path d="M 60 0 L 0 0 0 60" fill="none" stroke="currentColor" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
          </svg>
        </div>

        <div className="relative mx-auto max-w-6xl px-4 pb-28 pt-32 text-center">
          <div className="animate-fade-up">
            <div className="mb-6 inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-xs font-medium text-primary">
              <Zap className="h-3 w-3" aria-hidden="true" />
              Now in public beta
            </div>
          </div>

          <h1 className="animate-fade-up-delay-1 text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
            The all-in-one
            <br />
            <span className="bg-gradient-to-r from-primary via-primary to-secondary bg-clip-text text-transparent">
              trading workspace
            </span>
          </h1>

          <p className="animate-fade-up-delay-2 mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-muted-foreground">
            Live charts, trade journaling, strategy backtesting, verified profiles, and community
            &mdash; everything a serious trader needs in one platform.
          </p>

          <div className="animate-fade-up-delay-2 mt-8 flex items-center justify-center gap-4">
            <Link
              href="/auth/register"
              className="animate-pulse-glow inline-flex h-11 items-center gap-2 rounded-md bg-primary px-6 text-sm font-medium text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:bg-primary/90 hover:shadow-xl hover:shadow-primary/25 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              Start for free
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" aria-hidden="true" />
            </Link>
            <Link
              href="#features"
              className="inline-flex h-11 items-center rounded-md border border-border bg-card px-6 text-sm font-medium text-foreground transition-colors hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
            >
              See features
            </Link>
          </div>
        </div>
      </section>

      <section id="features" className="border-b border-border/40">
        <div className="mx-auto max-w-6xl px-4 py-20">
          <div
            ref={featuresRef}
            className={`text-center transition-all duration-700 ${
              featuresVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
          >
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Everything a trader needs
            </h2>
            <p className="mt-2 text-muted-foreground">
              Ten integrated modules. One cohesive platform.
            </p>
          </div>
          <div className="mt-12 grid gap-px rounded-xl border border-border/40 bg-border/20 overflow-hidden sm:grid-cols-2 lg:grid-cols-3">
            {features.map((f, i) => (
              <div
                key={f.title}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                className="card-tilt group relative bg-card p-6 transition-colors hover:bg-muted/50"
                style={{
                  transitionDelay: featuresVisible ? `${i * 0.08}s` : "0s",
                  opacity: featuresVisible ? 1 : 0,
                  transform: featuresVisible
                    ? "translateY(0)"
                    : "translateY(20px)",
                  transitionProperty: "transform, opacity, background-color",
                  transitionDuration: "0.5s",
                  transitionTimingFunction: "ease-out",
                }}
              >
                <div className="relative z-10">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary transition-all duration-300 group-hover:bg-primary/20 group-hover:shadow-lg group-hover:shadow-primary/10">
                    <f.icon className="h-5 w-5" aria-hidden="true" />
                  </div>
                  <h3 className="mt-4 font-semibold">{f.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                    {f.desc}
                  </p>
                </div>
                <div
                  className="pointer-events-none absolute inset-0 rounded-xl opacity-0 transition-opacity duration-300 group-hover:opacity-100"
                  style={{
                    background:
                      "radial-gradient(600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), hsl(var(--primary) / 0.06), transparent 40%)",
                  }}
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="relative border-b border-border/40 overflow-hidden">
        <div className="absolute inset-0" aria-hidden="true">
          <div className="absolute left-1/2 top-0 h-px w-1/3 bg-gradient-to-r from-transparent via-primary/20 to-transparent" />
        </div>
        <div className="mx-auto max-w-6xl px-4 py-20">
          <div
            ref={stepsRef}
            className={`text-center transition-all duration-700 ${
              stepsVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
          >
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Built for serious traders
            </h2>
            <p className="mt-2 text-muted-foreground">
              From aspiring retail traders to verified professionals.
            </p>
          </div>
          <div className="relative mt-12 grid gap-8 md:grid-cols-3">
            <div
              className="absolute left-[16.6%] right-[16.6%] top-9 hidden h-px bg-gradient-to-r from-primary/40 via-primary/20 to-transparent md:block"
              style={{ width: "66.8%" }}
            />
            {steps.map((item, i) => (
              <div
                key={item.step}
                className="relative text-center"
                style={{
                  transitionDelay: stepsVisible ? `${i * 0.15}s` : "0s",
                  opacity: stepsVisible ? 1 : 0,
                  transform: stepsVisible ? "translateY(0)" : "translateY(24px)",
                  transitionProperty: "transform, opacity",
                  transitionDuration: "0.6s",
                  transitionTimingFunction: "ease-out",
                }}
              >
                <div className="relative mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-primary to-secondary text-lg font-bold text-primary-foreground shadow-lg shadow-primary/20">
                  {item.step}
                </div>
                <h3 className="mt-4 font-semibold">{item.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="pricing" className="relative border-b border-border/40">
        <div className="absolute inset-0 overflow-hidden" aria-hidden="true">
          <div className="absolute right-0 top-1/2 h-[400px] w-[400px] -translate-y-1/2 rounded-full bg-primary/[0.02] blur-3xl" />
        </div>
        <div className="relative mx-auto max-w-6xl px-4 py-20">
          <div
            ref={pricingRef}
            className={`text-center transition-all duration-700 ${
              pricingVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
            }`}
          >
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Simple pricing</h2>
            <p className="mt-2 text-muted-foreground">Start free. Upgrade when you grow.</p>
          </div>
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {plans.map((plan, i) => (
              <div
                key={plan.name}
                onMouseMove={handleMouseMove}
                onMouseLeave={handleMouseLeave}
                className={`card-tilt relative flex flex-col rounded-xl border bg-card p-6 ${
                  plan.popular
                    ? "border-primary/40 ring-1 ring-primary/20 shadow-lg shadow-primary/5"
                    : "border-border/40"
                }`}
                style={{
                  transitionDelay: pricingVisible ? `${i * 0.12}s` : "0s",
                  opacity: pricingVisible ? 1 : 0,
                  transform: pricingVisible
                    ? "translateY(0)"
                    : "translateY(20px)",
                  transitionProperty: "transform, opacity",
                  transitionDuration: "0.5s",
                  transitionTimingFunction: "ease-out",
                }}
              >
                {plan.popular && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-gradient-to-r from-primary to-secondary px-3 py-0.5 text-xs font-semibold text-primary-foreground shadow-lg">
                    Most popular
                  </span>
                )}
                <h3 className="text-lg font-semibold">{plan.name}</h3>
                <p className="mt-1 text-3xl font-bold tracking-tight">
                  {plan.price}
                  <span className="ml-0.5 text-sm font-normal text-muted-foreground">/mo</span>
                </p>
                <p className="mt-1 text-sm text-muted-foreground">{plan.desc}</p>
                <ul className="mt-6 flex-1 space-y-3">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm">
                      <Check className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/auth/register"
                  className={`mt-6 inline-flex h-10 w-full items-center justify-center rounded-md text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background ${
                    plan.popular
                      ? "bg-primary text-primary-foreground shadow-lg shadow-primary/20 hover:bg-primary/90 hover:shadow-xl hover:shadow-primary/25"
                      : "border border-border/60 bg-card text-foreground hover:bg-muted"
                  }`}
                >
                  Get Started
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section
        ref={ctaRef}
        className="relative overflow-hidden border-b border-border/40"
      >
        <div className="absolute inset-0" aria-hidden="true">
          <div className="absolute left-1/2 top-1/2 h-[400px] w-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary/[0.02] blur-3xl animate-pulse-glow" />
          <div className="absolute left-[20%] top-[30%] h-2 w-2 rounded-full bg-primary/30 animate-float" style={{ animationDelay: "-3s" }} />
          <div className="absolute right-[25%] bottom-[25%] h-1.5 w-1.5 rounded-full bg-accent/30 animate-float-slow" style={{ animationDelay: "-5s" }} />
        </div>
        <div
          className={`relative mx-auto max-w-6xl px-4 py-20 text-center transition-all duration-700 ${
            ctaVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
          }`}
        >
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Ready to level up your trading?
          </h2>
          <p className="mt-2 text-muted-foreground">
            Join thousands of traders who track, verify, and grow on TradeSaaS.
          </p>
          <Link
            href="/auth/register"
            className="animate-pulse-glow mt-8 inline-flex h-11 items-center gap-2 rounded-md bg-primary px-8 text-sm font-medium text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:bg-primary/90 hover:shadow-xl hover:shadow-primary/25 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background"
          >
            Start for free
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </Link>
        </div>
      </section>

      <footer className="border-t border-border/40 bg-card/50">
        <div className="mx-auto max-w-6xl px-4 py-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <TrendingUp className="h-4 w-4 text-primary" aria-hidden="true" />
              <span>&copy; 2026 TradeSaaS. All rights reserved.</span>
            </div>
            <nav className="flex gap-6 text-sm" aria-label="Footer">
              <Link
                href="/privacy"
                className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-md px-1"
              >
                Privacy
              </Link>
              <Link
                href="/terms"
                className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-md px-1"
              >
                Terms
              </Link>
              <Link
                href="/contact"
                className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-md px-1"
              >
                Contact
              </Link>
            </nav>
          </div>
        </div>
      </footer>
    </div>
  );
}
