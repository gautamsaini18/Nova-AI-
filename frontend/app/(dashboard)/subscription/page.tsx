"use client";

import { motion } from "framer-motion";
import { Check, Zap, Crown, Sparkles, Star, ArrowRight } from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";
import Link from "next/link";

const PLANS = [
  {
    id: "free",
    name: "Free",
    price: "₹0",
    period: "/month",
    color: "#6C63FF",
    description: "Get started with Nova AI basics",
    features: [
      "10 voice commands/day",
      "5 voice options",
      "Basic AI chat (GPT-3.5)",
      "Weather & news",
      "2 smart home devices",
      "Community support",
    ],
    missing: ["Long-term memory", "All 60+ voices", "Priority processing"],
    cta: "Current Plan",
    current: true,
  },
  {
    id: "pro",
    name: "Pro",
    price: "₹499",
    period: "/month",
    color: "#A855F7",
    description: "Unlock the full Nova AI experience",
    features: [
      "Unlimited voice commands",
      "All 60+ premium voices",
      "GPT-4 powered AI",
      "Long-term memory (1000 items)",
      "All integrations (WhatsApp, Slack, etc.)",
      "Smart home unlimited devices",
      "Priority processing (<200ms)",
      "Custom wake word",
      "Email & priority support",
    ],
    missing: [],
    cta: "Upgrade to Pro",
    current: false,
    highlighted: true,
  },
  {
    id: "enterprise",
    name: "Enterprise",
    price: "Custom",
    period: "",
    color: "#FFD700",
    description: "For organizations and teams",
    features: [
      "Everything in Pro",
      "Custom AI model training",
      "On-premise deployment",
      "Dedicated API with SLA",
      "Team management dashboard",
      "Audit logs & compliance",
      "24/7 dedicated support",
      "Custom integrations",
    ],
    missing: [],
    cta: "Contact Sales",
    current: false,
  },
];

const USAGE_ITEMS = [
  { label: "Voice Commands", used: 7, limit: 10, color: "#6C63FF" },
  { label: "AI Chat Messages", used: 45, limit: 100, color: "#00D4FF" },
  { label: "Memory Entries", used: 23, limit: 50, color: "#FF6B9D" },
  { label: "Smart Home Devices", used: 2, limit: 2, color: "#FFD700" },
];

export default function SubscriptionPage() {
  return (
    <div>
      <TopBar title="Subscription" />
      <main className="page-body">

        {/* Current Usage */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card mb-8"
        >
          <h2 className="text-lg font-semibold font-display mb-4 flex items-center gap-2">
            <Zap size={18} className="text-violet-400" />
            Current Plan Usage
            <span className="badge badge-new ml-2">Free</span>
          </h2>
          <div className="grid sm:grid-cols-2 gap-4">
            {USAGE_ITEMS.map((item) => {
              const pct = Math.round((item.used / item.limit) * 100);
              return (
                <div key={item.label}>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm font-medium">{item.label}</span>
                    <span className="text-xs text-white/40">{item.used}/{item.limit}</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-white/[0.06] overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${pct}%`,
                        background: pct >= 90 ? "#FF6B9D" : item.color,
                      }}
                    />
                  </div>
                  <div className="text-xs text-right mt-1" style={{ color: pct >= 90 ? "#FF6B9D" : "rgba(255,255,255,0.3)" }}>
                    {pct}% used
                  </div>
                </div>
              );
            })}
          </div>
          <div className="mt-4 flex items-center gap-2 text-xs text-white/30">
            Usage resets on the 1st of each month.
          </div>
        </motion.div>

        {/* Plans */}
        <h2 className="text-xl font-bold font-display mb-6">Choose Your Plan</h2>
        <div className="grid md:grid-cols-3 gap-5">
          {PLANS.map((plan, i) => (
            <motion.div
              key={plan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className={`relative rounded-2xl p-6 flex flex-col ${
                plan.highlighted
                  ? "border-2 border-purple-500/40"
                  : "border border-white/[0.06]"
              }`}
              style={{
                background: plan.highlighted
                  ? "linear-gradient(135deg, rgba(168,85,247,0.12), rgba(108,99,255,0.06))"
                  : "var(--bg-surface)",
              }}
            >
              {plan.highlighted && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <div className="flex items-center gap-1 bg-gradient-to-r from-purple-600 to-violet-500 text-white text-xs font-bold px-4 py-1.5 rounded-full">
                    <Crown size={10} />
                    BEST VALUE
                  </div>
                </div>
              )}

              {/* Header */}
              <div className="mb-5">
                <div className="flex items-center gap-2 mb-2">
                  <span className="text-sm font-semibold text-white/50">{plan.name}</span>
                  {plan.current && <span className="badge badge-free">Current</span>}
                </div>
                <div className="flex items-end gap-1 mb-1">
                  <span className="text-4xl font-bold font-display" style={{ color: plan.color }}>{plan.price}</span>
                  <span className="text-white/40 pb-1 text-sm">{plan.period}</span>
                </div>
                <p className="text-sm text-white/40">{plan.description}</p>
              </div>

              {/* Features */}
              <ul className="space-y-2.5 flex-1 mb-6">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-white/70">
                    <Check size={13} className="flex-shrink-0 mt-0.5" style={{ color: plan.color }} />
                    {f}
                  </li>
                ))}
                {plan.missing.map((f) => (
                  <li key={f} className="flex items-start gap-2.5 text-sm text-white/25 line-through">
                    <span className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 border border-white/10 rounded-full" />
                    {f}
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <button
                className={`w-full py-3 rounded-xl font-semibold text-sm transition-all flex items-center justify-center gap-2 ${
                  plan.current
                    ? "glass text-white/50 cursor-default border border-white/10"
                    : plan.highlighted
                    ? "btn-primary"
                    : "btn-secondary"
                }`}
                disabled={plan.current}
              >
                {plan.highlighted && <Sparkles size={14} />}
                {plan.cta}
                {!plan.current && <ArrowRight size={14} />}
              </button>
            </motion.div>
          ))}
        </div>

        {/* FAQ Note */}
        <div className="mt-8 text-center text-sm text-white/30">
          All plans include 7-day free trial. Cancel anytime. Prices in INR.
        </div>
      </main>
    </div>
  );
}
