"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  MessageSquare, Mic, Brain, Zap, TrendingUp, Clock,
  Star, ArrowRight, Volume2, Calendar, Cloud, Music,
  Settings, ChevronRight, Sparkles
} from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";

const QUICK_ACTIONS = [
  { href: "/chat", icon: MessageSquare, label: "AI Chat", color: "#6C63FF", desc: "Start a conversation" },
  { href: "/voice", icon: Mic, label: "Voice Mode", color: "#00D4FF", desc: "Talk to Nova" },
  { href: "/memory", icon: Brain, label: "My Memory", color: "#FF6B9D", desc: "View saved info" },
  { href: "/settings", icon: Settings, label: "Settings", color: "#FFD700", desc: "Configure Nova" },
];

const STATS = [
  { label: "Conversations", value: "142", change: "+12%", icon: MessageSquare, color: "#6C63FF" },
  { label: "Voice Commands", value: "3,847", change: "+28%", icon: Mic, color: "#00D4FF" },
  { label: "Tasks Automated", value: "89", change: "+5%", icon: Zap, color: "#FF6B9D" },
  { label: "Hours Saved", value: "47.2h", change: "+19%", icon: Clock, color: "#22c55e" },
];

const RECENT_CHATS = [
  { id: 1, message: "What's the weather like today?", time: "2 min ago", type: "weather" },
  { id: 2, message: "Remind me to take medicine at 8 PM", time: "15 min ago", type: "reminder" },
  { id: 3, message: "Play lo-fi music on Spotify", time: "1 hr ago", type: "music" },
  { id: 4, message: "Summarize my emails from today", time: "3 hr ago", type: "email" },
  { id: 5, message: "Set an alarm for 7 AM tomorrow", time: "Yesterday", type: "alarm" },
];

const FEATURES_SPOTLIGHT = [
  { icon: Calendar, label: "Schedule a Meeting", color: "#6C63FF" },
  { icon: Cloud, label: "Weather Update", color: "#00D4FF" },
  { icon: Music, label: "Music Control", color: "#FF6B9D" },
  { icon: Brain, label: "AI Research", color: "#A855F7" },
];

export default function DashboardPage() {
  const currentHour = new Date().getHours();
  const greeting =
    currentHour < 12 ? "Good Morning" : currentHour < 17 ? "Good Afternoon" : "Good Evening";

  return (
    <div>
      <TopBar title="Dashboard" />
      <main className="page-body">

        {/* ── Welcome Banner ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative rounded-3xl p-8 mb-8 overflow-hidden"
          style={{
            background: "linear-gradient(135deg, rgba(108,99,255,0.2) 0%, rgba(0,212,255,0.08) 100%)",
            border: "1px solid rgba(108,99,255,0.2)",
          }}
        >
          <div className="absolute right-8 top-1/2 -translate-y-1/2 w-32 h-32 rounded-full opacity-20"
            style={{ background: "radial-gradient(circle, #6C63FF, transparent)", filter: "blur(20px)" }} />
          <div className="relative z-10">
            <div className="flex items-center gap-2 text-violet-300 text-sm font-medium mb-2">
              <Sparkles size={14} />
              {greeting}, Gautam!
            </div>
            <h2 className="text-3xl font-bold font-display mb-2">
              Welcome back to{" "}
              <span className="gradient-text">Nova AI</span>
            </h2>
            <p className="text-white/50 mb-6">
              You have 3 pending reminders and 2 new email summaries ready.
            </p>
            <div className="flex gap-3">
              <Link href="/voice" className="btn-primary text-sm">
                <Mic size={15} />
                Start Voice Session
              </Link>
              <Link href="/chat" className="btn-secondary text-sm">
                <MessageSquare size={15} />
                Open Chat
              </Link>
            </div>
          </div>
        </motion.div>

        {/* ── Stats Grid ── */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {STATS.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08 }}
                className="card"
              >
                <div className="flex items-center justify-between mb-4">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center"
                    style={{ background: `${stat.color}18`, border: `1px solid ${stat.color}30` }}
                  >
                    <Icon size={18} style={{ color: stat.color }} />
                  </div>
                  <div className="flex items-center gap-1 text-xs font-medium text-green-400">
                    <TrendingUp size={10} />
                    {stat.change}
                  </div>
                </div>
                <div className="text-2xl font-bold font-display mb-1">{stat.value}</div>
                <div className="text-sm text-white/40">{stat.label}</div>
              </motion.div>
            );
          })}
        </div>

        {/* ── Quick Actions ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="text-lg font-semibold font-display mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {QUICK_ACTIONS.map((action) => {
              const Icon = action.icon;
              return (
                <Link key={action.href} href={action.href}>
                  <div className="card card-hover cursor-pointer">
                    <div
                      className="w-12 h-12 rounded-xl flex items-center justify-center mb-3"
                      style={{ background: `${action.color}18`, border: `1px solid ${action.color}30` }}
                    >
                      <Icon size={22} style={{ color: action.color }} />
                    </div>
                    <div className="font-semibold text-sm mb-1">{action.label}</div>
                    <div className="text-xs text-white/40">{action.desc}</div>
                  </div>
                </Link>
              );
            })}
          </div>
        </motion.div>

        {/* ── Two Column: Recent + Spotlight ── */}
        <div className="grid lg:grid-cols-3 gap-6">

          {/* Recent Conversations */}
          <div className="lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold font-display">Recent Conversations</h2>
              <Link href="/history" className="text-sm text-violet-400 hover:text-violet-300 flex items-center gap-1">
                View all <ChevronRight size={14} />
              </Link>
            </div>
            <div className="space-y-2">
              {RECENT_CHATS.map((chat, i) => (
                <motion.div
                  key={chat.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + i * 0.06 }}
                  className="flex items-center gap-4 p-4 rounded-xl glass glass-hover cursor-pointer"
                >
                  <div className="w-10 h-10 rounded-full bg-violet-500/10 border border-violet-500/20 flex items-center justify-center flex-shrink-0">
                    <MessageSquare size={14} className="text-violet-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-white/90 truncate">{chat.message}</div>
                    <div className="text-xs text-white/40 mt-0.5">{chat.time}</div>
                  </div>
                  <ArrowRight size={14} className="text-white/20 flex-shrink-0" />
                </motion.div>
              ))}
            </div>
          </div>

          {/* Feature Spotlight */}
          <div>
            <h2 className="text-lg font-semibold font-display mb-4">Try These</h2>
            <div className="space-y-3">
              {FEATURES_SPOTLIGHT.map((feat, i) => {
                const Icon = feat.icon;
                return (
                  <motion.div
                    key={feat.label}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.4 + i * 0.08 }}
                    className="flex items-center gap-3 p-4 rounded-xl glass glass-hover cursor-pointer"
                  >
                    <div
                      className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
                      style={{ background: `${feat.color}18`, border: `1px solid ${feat.color}30` }}
                    >
                      <Icon size={16} style={{ color: feat.color }} />
                    </div>
                    <span className="text-sm font-medium">{feat.label}</span>
                    <ChevronRight size={14} className="text-white/20 ml-auto" />
                  </motion.div>
                );
              })}

              {/* AI Voice Selection CTA */}
              <Link href="/settings">
                <div className="p-4 rounded-xl mt-2 cursor-pointer overflow-hidden relative"
                  style={{ background: "linear-gradient(135deg, rgba(108,99,255,0.2), rgba(0,212,255,0.1))", border: "1px solid rgba(108,99,255,0.3)" }}>
                  <Volume2 size={20} className="text-violet-400 mb-2" />
                  <div className="text-sm font-semibold mb-1">Change Your Voice</div>
                  <div className="text-xs text-white/50">60+ premium voices available</div>
                  <div className="text-xs text-violet-400 mt-2 flex items-center gap-1">
                    Browse voices <ChevronRight size={12} />
                  </div>
                </div>
              </Link>
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}
