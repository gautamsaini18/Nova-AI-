"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { motion, useScroll, useTransform, AnimatePresence } from "framer-motion";
import {
  Mic, Brain, Zap, Shield, Globe, Headphones, ChevronRight,
  Star, Play, CheckCircle, ArrowRight, Sparkles, Volume2,
  MessageSquare, Music, Home, Phone, Calendar, Cloud, Navigation,
  Eye, Cpu, Wifi, Moon, Sun, Menu, X
} from "lucide-react";

// ── Data ──────────────────────────────────────────────────────────────────────

const FEATURES = [
  { icon: Mic, title: "Voice Recognition", description: "Whisper-powered STT with noise cancellation and multi-language support", color: "#6C63FF" },
  { icon: Brain, title: "AI Reasoning", description: "GPT-4 powered conversations with context awareness and long-term memory", color: "#00D4FF" },
  { icon: Volume2, title: "60+ Premium Voices", description: "Choose from Nova, Maya, Cortex, Aether AI and 56 more stunning voices", color: "#FF6B9D" },
  { icon: Home, title: "Smart Home Control", description: "Control lights, AC, locks, cameras and all IoT devices seamlessly", color: "#FFD700" },
  { icon: Shield, title: "Privacy First", description: "End-to-end encryption, voice authentication, and private mode", color: "#22c55e" },
  { icon: Globe, title: "Multi-Language", description: "Communicate naturally in 50+ languages with real-time translation", color: "#FF8C42" },
  { icon: MessageSquare, title: "Omni-Channel", description: "WhatsApp, Telegram, SMS, Slack, Discord integration built-in", color: "#A855F7" },
  { icon: Zap, title: "Workflow Automation", description: "Custom voice shortcuts, macros, and intelligent task automation", color: "#06B6D4" },
];

const VOICE_SHOWCASE = [
  { id: "nova", name: "Nova", category: "Modern & Premium", color: "#6C63FF" },
  { id: "maya", name: "Maya", category: "Friendly & Human", color: "#FF6B9D" },
  { id: "cortex", name: "Cortex", category: "Tech-Inspired", color: "#00D4FF" },
  { id: "aether", name: "Aether", category: "Futuristic", color: "#A855F7" },
  { id: "neurocore", name: "NeuroCore", category: "AI Brand", color: "#FFD700" },
  { id: "luna", name: "Luna", category: "Friendly & Human", color: "#22c55e" },
];

const STATS = [
  { value: "60+", label: "Voice Options" },
  { value: "50+", label: "Languages" },
  { value: "100+", label: "Integrations" },
  { value: "< 500ms", label: "Response Time" },
];

const CAPABILITIES = [
  { icon: Phone, label: "Calls & SMS" },
  { icon: Music, label: "Music Control" },
  { icon: Navigation, label: "Navigation" },
  { icon: Calendar, label: "Calendar" },
  { icon: Cloud, label: "Weather" },
  { icon: Eye, label: "Vision AI" },
  { icon: Cpu, label: "Device Control" },
  { icon: Wifi, label: "Smart Home" },
];

const PRICING = [
  {
    name: "Free",
    price: "₹0",
    period: "/month",
    description: "Perfect to get started",
    features: [
      "10 voice commands/day",
      "5 voice options",
      "Basic AI chat",
      "Weather & news",
      "2 smart home devices",
    ],
    cta: "Get Started Free",
    highlighted: false,
  },
  {
    name: "Pro",
    price: "₹499",
    period: "/month",
    description: "For power users",
    features: [
      "Unlimited voice commands",
      "All 60+ voice options",
      "GPT-4 conversations",
      "Long-term memory",
      "All integrations",
      "Smart home unlimited",
      "Priority support",
    ],
    cta: "Start Pro Trial",
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "For organizations",
    features: [
      "Everything in Pro",
      "Custom wake word",
      "On-premise deployment",
      "Custom AI training",
      "Dedicated API",
      "SLA guarantee",
      "24/7 support",
    ],
    cta: "Contact Sales",
    highlighted: false,
  },
];

// ── Sub-Components ──────────────────────────────────────────────────────────

function AnimatedOrb({ size = 160, className = "" }: { size?: number; className?: string }) {
  return (
    <div className={`relative flex items-center justify-center ${className}`} style={{ width: size, height: size }}>
      {/* Outer glow rings */}
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="absolute rounded-full border border-violet-500/20"
          style={{
            width: size + i * 40,
            height: size + i * 40,
            animation: `ripple ${2 + i * 0.5}s ease-out infinite`,
            animationDelay: `${i * 0.4}s`,
          }}
        />
      ))}
      {/* Core orb */}
      <div
        className="orb animate-float"
        style={{ width: size, height: size }}
      >
        <div className="absolute inset-0 flex items-center justify-center">
          <Mic size={size * 0.35} className="text-white/90 z-10" />
        </div>
      </div>
    </div>
  );
}

function WaveformDemo() {
  const heights = [20, 40, 60, 80, 60, 100, 80, 60, 80, 100, 60, 40, 60, 80, 40, 20, 40, 60, 80, 60];
  return (
    <div className="flex items-center gap-1 h-16">
      {heights.map((h, i) => (
        <div
          key={i}
          className="waveform-bar"
          style={{
            height: `${h}%`,
            animationDuration: `${0.8 + (i % 5) * 0.15}s`,
            animationDelay: `${i * 0.06}s`,
          }}
        />
      ))}
    </div>
  );
}

function NavBar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handler);
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? "glass border-b border-white/[0.06]" : ""
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-violet-500/30">
            <Mic size={18} className="text-white" />
          </div>
          <span className="text-xl font-bold font-display gradient-text">Nova AI</span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-8">
          {["Features", "Voices", "Pricing", "Docs"].map((item) => (
            <a
              key={item}
              href={`#${item.toLowerCase()}`}
              className="text-sm font-medium text-white/60 hover:text-white transition-colors"
            >
              {item}
            </a>
          ))}
        </div>

        {/* CTA */}
        <div className="hidden md:flex items-center gap-3">
          <Link href="/login" className="btn-ghost text-sm">Sign In</Link>
          <Link href="/register" className="btn-primary text-sm">
            Get Started <ArrowRight size={14} />
          </Link>
        </div>

        {/* Mobile menu button */}
        <button
          className="md:hidden btn-ghost p-2"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {menuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden glass border-t border-white/[0.06] px-6 pb-6"
          >
            <div className="flex flex-col gap-4 pt-4">
              {["Features", "Voices", "Pricing", "Docs"].map((item) => (
                <a key={item} href={`#${item.toLowerCase()}`} className="text-sm text-white/70">
                  {item}
                </a>
              ))}
              <div className="flex flex-col gap-2 pt-2 border-t border-white/[0.06]">
                <Link href="/login" className="btn-secondary text-sm text-center">Sign In</Link>
                <Link href="/register" className="btn-primary text-sm text-center">Get Started</Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
}

// ── Main Page ──────────────────────────────────────────────────────────────

export default function LandingPage() {
  const { scrollYProgress } = useScroll();
  const heroY = useTransform(scrollYProgress, [0, 0.3], [0, -80]);

  return (
    <div className="min-h-screen" style={{ background: "var(--bg-base)" }}>
      <NavBar />

      {/* Ambient Background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/3 w-[600px] h-[600px] rounded-full opacity-10"
          style={{ background: "radial-gradient(circle, #6C63FF 0%, transparent 70%)", filter: "blur(80px)" }} />
        <div className="absolute bottom-1/3 right-0 w-[400px] h-[400px] rounded-full opacity-8"
          style={{ background: "radial-gradient(circle, #00D4FF 0%, transparent 70%)", filter: "blur(80px)" }} />
        <div className="absolute top-1/2 left-0 w-[300px] h-[300px] rounded-full opacity-6"
          style={{ background: "radial-gradient(circle, #FF6B9D 0%, transparent 70%)", filter: "blur(80px)" }} />
      </div>

      {/* ── HERO ─────────────────────────────────────────────────────── */}
      <section className="relative min-h-screen flex items-center justify-center pt-16 overflow-hidden">
        <motion.div
          style={{ y: heroY }}
          className="relative z-10 max-w-6xl mx-auto px-6 text-center"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-violet-500/20 mb-8"
          >
            <Sparkles size={14} className="text-violet-400" />
            <span className="text-xs font-semibold text-violet-300 tracking-wider uppercase">
              Next-Generation AI Voice Assistant
            </span>
            <span className="px-2 py-0.5 rounded-full bg-violet-500/20 text-violet-300 text-xs font-bold">NEW</span>
          </motion.div>

          {/* Hero Title */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.7 }}
            className="text-6xl md:text-8xl font-bold font-display mb-6 leading-tight tracking-tight"
          >
            Meet{" "}
            <span className="gradient-text">Nova AI</span>
            <br />
            <span className="text-white/80 text-5xl md:text-6xl">Your Intelligent</span>
            <br />
            <span className="gradient-text-accent text-5xl md:text-7xl">Voice Assistant</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-lg md:text-xl text-white/60 max-w-2xl mx-auto mb-10 leading-relaxed"
          >
            Human-like conversations, 60+ premium voices, smart home control, and limitless AI capabilities.
            The assistant that thinks, remembers, and acts like a real person.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
          >
            <Link href="/register" className="btn-primary text-base px-8 py-4">
              <Sparkles size={18} />
              Start For Free
              <ArrowRight size={16} />
            </Link>
            <Link href="/voice" className="btn-secondary text-base px-8 py-4">
              <Play size={18} />
              Try Voice Demo
            </Link>
          </motion.div>

          {/* Central Orb + Waveform */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3, duration: 0.8, type: "spring" }}
            className="flex flex-col items-center gap-8"
          >
            <AnimatedOrb size={180} />
            <div className="glass rounded-2xl px-8 py-4 border border-white/[0.06]">
              <WaveformDemo />
              <p className="text-sm text-white/40 mt-2 text-center">
                "Hey Nova, play my morning playlist and show today's weather."
              </p>
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* ── STATS ────────────────────────────────────────────────────── */}
      <section className="relative py-20 border-y border-white/[0.06]">
        <div className="max-w-5xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {STATS.map((stat, i) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-bold font-display gradient-text mb-2">
                  {stat.value}
                </div>
                <div className="text-sm text-white/50 font-medium">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FEATURES ──────────────────────────────────────────────────── */}
      <section id="features" className="py-32 relative">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <div className="feature-tag mx-auto mb-4">
              <Zap size={12} />
              Powerful Features
            </div>
            <h2 className="text-4xl md:text-6xl font-bold font-display mb-4">
              Everything You Need,{" "}
              <span className="gradient-text">Nothing You Don't</span>
            </h2>
            <p className="text-lg text-white/50 max-w-2xl mx-auto">
              From smart home automation to AI-powered research — Nova AI handles it all with a single voice command.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            {FEATURES.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.08 }}
                  className="card card-hover group cursor-default"
                >
                  <div
                    className="w-12 h-12 rounded-xl flex items-center justify-center mb-4 transition-all duration-300 group-hover:scale-110"
                    style={{ background: `${feature.color}18`, border: `1px solid ${feature.color}30` }}
                  >
                    <Icon size={22} style={{ color: feature.color }} />
                  </div>
                  <h3 className="text-base font-semibold mb-2">{feature.title}</h3>
                  <p className="text-sm text-white/50 leading-relaxed">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ── VOICE SHOWCASE ───────────────────────────────────────────── */}
      <section id="voices" className="py-32 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-violet-950/20 to-transparent pointer-events-none" />
        <div className="max-w-7xl mx-auto px-6 relative">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <div className="feature-tag mx-auto mb-4">
              <Headphones size={12} />
              60+ Voice Options
            </div>
            <h2 className="text-4xl md:text-6xl font-bold font-display mb-4">
              Your Voice,{" "}
              <span className="gradient-text">Your Choice</span>
            </h2>
            <p className="text-lg text-white/50 max-w-xl mx-auto">
              From friendly human-like voices to futuristic AI personas — find the voice that feels like home.
            </p>
          </motion.div>

          {/* Voice Cards Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-12">
            {VOICE_SHOWCASE.map((voice, i) => (
              <motion.div
                key={voice.id}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="voice-card text-center"
              >
                <div
                  className="w-14 h-14 rounded-full mx-auto mb-3 flex items-center justify-center text-2xl font-bold"
                  style={{
                    background: `radial-gradient(circle, ${voice.color}40, ${voice.color}15)`,
                    border: `1px solid ${voice.color}40`,
                  }}
                >
                  {voice.name[0]}
                </div>
                <div className="font-semibold text-sm mb-1">{voice.name}</div>
                <div className="text-xs text-white/40 leading-tight">{voice.category}</div>
                <button
                  className="mt-3 flex items-center gap-1 mx-auto text-xs font-medium transition-colors"
                  style={{ color: voice.color }}
                >
                  <Play size={10} fill="currentColor" />
                  Preview
                </button>
              </motion.div>
            ))}
          </div>

          <div className="text-center">
            <Link href="/settings" className="btn-secondary inline-flex">
              Explore All 60+ Voices
              <ChevronRight size={16} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── CAPABILITIES TICKER ──────────────────────────────────────── */}
      <section className="py-16 border-y border-white/[0.06] overflow-hidden">
        <div className="flex gap-6 animate-[spin-slow_30s_linear_infinite]">
          {[...CAPABILITIES, ...CAPABILITIES, ...CAPABILITIES].map((cap, i) => {
            const Icon = cap.icon;
            return (
              <div key={i} className="flex items-center gap-3 glass px-6 py-3 rounded-full whitespace-nowrap flex-shrink-0">
                <Icon size={16} className="text-violet-400" />
                <span className="text-sm font-medium text-white/70">{cap.label}</span>
              </div>
            );
          })}
        </div>
      </section>

      {/* ── PRICING ──────────────────────────────────────────────────── */}
      <section id="pricing" className="py-32">
        <div className="max-w-6xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <div className="feature-tag mx-auto mb-4">
              <Star size={12} />
              Pricing
            </div>
            <h2 className="text-4xl md:text-6xl font-bold font-display mb-4">
              Simple,{" "}
              <span className="gradient-text">Transparent Pricing</span>
            </h2>
            <p className="text-lg text-white/50">Start free, scale as you grow.</p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {PRICING.map((plan, i) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className={`relative rounded-2xl p-8 border transition-all duration-300 hover:transform hover:-translate-y-2 ${
                  plan.highlighted
                    ? "border-violet-500/40 bg-gradient-to-b from-violet-950/50 to-transparent"
                    : "border-white/[0.06] bg-white/[0.02]"
                }`}
              >
                {plan.highlighted && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                    <div className="bg-gradient-to-r from-violet-600 to-cyan-400 text-white text-xs font-bold px-4 py-1.5 rounded-full">
                      ✨ MOST POPULAR
                    </div>
                  </div>
                )}
                <div className="mb-6">
                  <div className="text-sm font-semibold text-white/50 mb-1">{plan.name}</div>
                  <div className="flex items-end gap-1 mb-1">
                    <span className="text-4xl font-bold font-display">{plan.price}</span>
                    <span className="text-white/40 pb-1">{plan.period}</span>
                  </div>
                  <p className="text-sm text-white/40">{plan.description}</p>
                </div>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-3 text-sm text-white/70">
                      <CheckCircle size={14} className="text-violet-400 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link
                  href="/register"
                  className={`block text-center py-3 px-6 rounded-full font-semibold text-sm transition-all ${
                    plan.highlighted
                      ? "btn-primary"
                      : "btn-secondary"
                  }`}
                >
                  {plan.cta}
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA BANNER ───────────────────────────────────────────────── */}
      <section className="py-32">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative rounded-3xl p-12 overflow-hidden"
            style={{
              background: "linear-gradient(135deg, rgba(108,99,255,0.2) 0%, rgba(0,212,255,0.1) 100%)",
              border: "1px solid rgba(108,99,255,0.3)",
            }}
          >
            <div className="absolute inset-0 opacity-30"
              style={{ background: "radial-gradient(circle at 50% 50%, #6C63FF 0%, transparent 70%)" }} />
            <div className="relative z-10">
              <div className="text-6xl mb-6">🎙️</div>
              <h2 className="text-4xl md:text-5xl font-bold font-display mb-4">
                Ready to Experience the{" "}
                <span className="gradient-text">Future of AI?</span>
              </h2>
              <p className="text-lg text-white/60 mb-8 max-w-xl mx-auto">
                Join thousands of users already using Nova AI. Start your free account today — no credit card required.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link href="/register" className="btn-primary text-base px-10 py-4">
                  <Sparkles size={18} />
                  Start For Free Today
                </Link>
                <Link href="/chat" className="btn-secondary text-base px-10 py-4">
                  <MessageSquare size={18} />
                  Try AI Chat
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── FOOTER ──────────────────────────────────────────────────── */}
      <footer className="border-t border-white/[0.06] py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-600 to-cyan-400 flex items-center justify-center">
                <Mic size={14} className="text-white" />
              </div>
              <span className="font-bold gradient-text text-lg">Nova AI</span>
            </div>
            <div className="flex gap-6 text-sm text-white/40">
              {["Privacy", "Terms", "API Docs", "Status", "Contact"].map((item) => (
                <a key={item} href="#" className="hover:text-white/70 transition-colors">
                  {item}
                </a>
              ))}
            </div>
            <div className="text-sm text-white/30">
              © 2026 Nova AI. Built with ❤️ for the future.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
