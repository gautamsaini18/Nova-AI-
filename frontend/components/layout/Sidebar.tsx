"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard, MessageSquare, Mic, History, Settings,
  User, Brain, CreditCard, ChevronLeft, ChevronRight,
  Sparkles, LogOut, Bell, Search, Zap
} from "lucide-react";
import { useState } from "react";

const NAV_ITEMS = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/chat", icon: MessageSquare, label: "AI Chat" },
  { href: "/voice", icon: Mic, label: "Voice Chat" },
  { href: "/history", icon: History, label: "History" },
  { href: "/memory", icon: Brain, label: "Memory" },
  { href: "/settings", icon: Settings, label: "Settings" },
  { href: "/profile", icon: User, label: "Profile" },
  { href: "/subscription", icon: CreditCard, label: "Subscription" },
];

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <motion.aside
      animate={{ width: collapsed ? 72 : 260 }}
      transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
      className="fixed left-0 top-0 h-screen z-50 flex flex-col overflow-hidden"
      style={{
        background: "var(--bg-surface)",
        borderRight: "var(--border-subtle)",
      }}
    >
      {/* ── Logo ── */}
      <div className="flex items-center gap-3 px-4 h-16 border-b border-white/[0.06] flex-shrink-0">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-600 to-cyan-400 flex items-center justify-center flex-shrink-0 shadow-lg shadow-violet-500/30">
          <Mic size={16} className="text-white" />
        </div>
        <AnimatePresence>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.15 }}
              className="overflow-hidden"
            >
              <span className="text-lg font-bold font-display gradient-text whitespace-nowrap">
                Nova AI
              </span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* ── Navigation ── */}
      <nav className="flex-1 overflow-y-auto py-4 px-3 scroll-area">
        <div className="space-y-1">
          {NAV_ITEMS.map(({ href, icon: Icon, label }) => {
            const active = pathname === href || pathname.startsWith(href + "/");
            return (
              <Link key={href} href={href}>
                <div
                  className={`sidebar-nav-item ${active ? "active" : ""}`}
                  title={collapsed ? label : undefined}
                >
                  <Icon size={18} className={`flex-shrink-0 nav-icon ${active ? "text-violet-400" : ""}`} />
                  <AnimatePresence>
                    {!collapsed && (
                      <motion.span
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.1 }}
                        className="whitespace-nowrap"
                      >
                        {label}
                      </motion.span>
                    )}
                  </AnimatePresence>
                  {active && !collapsed && (
                    <motion.div
                      layoutId="active-indicator"
                      className="ml-auto w-1.5 h-1.5 rounded-full bg-violet-400"
                    />
                  )}
                </div>
              </Link>
            );
          })}
        </div>

        {/* ── Quick Actions ── */}
        {!collapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mt-6"
          >
            <div className="text-xs font-semibold text-white/30 uppercase tracking-wider px-3 mb-2">
              Quick Actions
            </div>
            <div className="glass rounded-xl p-3 space-y-2">
              <button className="w-full flex items-center gap-3 text-sm text-white/60 hover:text-white transition-colors py-1.5 px-2 rounded-lg hover:bg-white/[0.04]">
                <Zap size={14} className="text-yellow-400" />
                Voice Command
              </button>
              <button className="w-full flex items-center gap-3 text-sm text-white/60 hover:text-white transition-colors py-1.5 px-2 rounded-lg hover:bg-white/[0.04]">
                <Search size={14} className="text-cyan-400" />
                Search Memory
              </button>
            </div>
          </motion.div>
        )}
      </nav>

      {/* ── User Section ── */}
      <div className="px-3 py-4 border-t border-white/[0.06] flex-shrink-0">
        <div className={`flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-white/[0.04] cursor-pointer transition-colors ${collapsed ? "justify-center" : ""}`}>
          <div className="relative flex-shrink-0">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-pink-500 flex items-center justify-center text-sm font-bold text-white">
              G
            </div>
            <div className="status-dot online absolute -bottom-0.5 -right-0.5 border-2 border-[var(--bg-surface)]" />
          </div>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex-1 min-w-0"
            >
              <div className="text-sm font-semibold text-white truncate">Gautam Saini</div>
              <div className="text-xs text-white/40 truncate">Pro Plan</div>
            </motion.div>
          )}
          {!collapsed && (
            <LogOut size={14} className="text-white/30 hover:text-white/60 flex-shrink-0 transition-colors" />
          )}
        </div>
      </div>

      {/* ── Collapse Toggle ── */}
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="absolute top-1/2 -right-3 w-6 h-6 rounded-full flex items-center justify-center z-50 transition-all hover:scale-110"
        style={{
          background: "var(--bg-elevated)",
          border: "var(--border-subtle)",
          color: "var(--text-secondary)",
        }}
      >
        {collapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
      </button>
    </motion.aside>
  );
}

export function TopBar({ title }: { title: string }) {
  return (
    <header
      className="page-header gap-4"
      style={{
        background: "rgba(10, 10, 15, 0.85)",
        borderBottom: "var(--border-subtle)",
      }}
    >
      <h1 className="text-xl font-semibold font-display flex-1">{title}</h1>
      <div className="flex items-center gap-3">
        <button className="btn-ghost p-2 relative">
          <Bell size={18} />
          <div className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-violet-500" />
        </button>
        <button className="btn-ghost p-2">
          <Search size={18} />
        </button>
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-pink-500 flex items-center justify-center text-sm font-bold text-white cursor-pointer">
          G
        </div>
      </div>
    </header>
  );
}
