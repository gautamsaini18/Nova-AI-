"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import {
  Activity, Users, MessageSquare, Brain, Clock, Bell,
  Database, Shield, BarChart3, Plug, Settings, RefreshCw,
  CheckCircle, XCircle, ChevronRight, HardDrive, Zap,
} from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";

interface SystemStats {
  total_users: number;
  total_conversations: number;
  total_messages: number;
  total_memories: number;
  total_reminders: number;
  active_timers: number;
  active_stopwatches: number;
  active_plugins: number;
  database_size_bytes: number;
  uptime_seconds: number;
  version: string;
}

interface UserItem {
  id: string;
  name: string;
  email: string;
  plan: string;
  is_active: boolean;
  created_at: string;
  last_active: string | null;
  conversation_count: number;
}

interface PluginItem {
  name: string;
  version: string;
  enabled: boolean;
  description: string;
}

const STAT_CARDS = [
  { key: "total_users" as const, label: "Total Users", icon: Users, color: "#6C63FF" },
  { key: "total_conversations" as const, label: "Conversations", icon: MessageSquare, color: "#00D4FF" },
  { key: "total_messages" as const, label: "Messages", icon: Activity, color: "#22c55e" },
  { key: "total_memories" as const, label: "Memory Entries", icon: Brain, color: "#FF6B9D" },
  { key: "total_reminders" as const, label: "Reminders", icon: Bell, color: "#FFD700" },
  { key: "active_plugins" as const, label: "Active Plugins", icon: Plug, color: "#A855F7" },
];

export default function AdminPage() {
  const [stats, setStats] = useState<SystemStats | null>(null);
  const [users, setUsers] = useState<UserItem[]>([]);
  const [plugins, setPlugins] = useState<PluginItem[]>([]);
  const [activeTab, setActiveTab] = useState<"overview" | "users" | "plugins">("overview");
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [statsRes, usersRes, pluginsRes] = await Promise.all([
        fetch("http://localhost:8000/api/v1/admin/stats"),
        fetch("http://localhost:8000/api/v1/admin/users"),
        fetch("http://localhost:8000/api/v1/admin/plugins"),
      ]);
      if (statsRes.ok) setStats(await statsRes.json());
      if (usersRes.ok) setUsers(await usersRes.json());
      if (pluginsRes.ok) setPlugins(await pluginsRes.json());
    } catch {
      // Backend not running — use fallback
    }
    setLoading(false);
  };

  useEffect(() => { fetchData(); }, []);

  const formatUptime = (s: number) => {
    const h = Math.floor(s / 3600);
    const m = Math.floor((s % 3600) / 60);
    return `${h}h ${m}m`;
  };

  const formatBytes = (b: number) => {
    if (b < 1024) return `${b} B`;
    if (b < 1024 ** 2) return `${(b / 1024).toFixed(1)} KB`;
    return `${(b / 1024 ** 2).toFixed(1)} MB`;
  };

  return (
    <div>
      <TopBar title="Admin" />
      <main className="page-body">

        {/* ── Header ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <div>
            <h1 className="text-2xl font-bold font-display mb-1">System Administration</h1>
            <p className="text-sm text-white/50">Monitor and manage Nova AI</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-xs text-white/40">
              <Shield size={14} className="text-green-400" />
              v{stats?.version || "1.0.0"}
            </div>
            <button onClick={fetchData} className="btn-ghost text-sm" disabled={loading}>
              <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
              Refresh
            </button>
          </div>
        </motion.div>

        {/* ── Tabs ── */}
        <div className="flex gap-1 mb-8 p-1 rounded-2xl glass inline-flex">
          {(["overview", "users", "plugins"] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-xl text-sm font-medium capitalize transition-all ${
                activeTab === tab
                  ? "bg-violet-500/20 text-violet-300 border border-violet-500/30"
                  : "text-white/50 hover:text-white/80"
              }`}
            >
              {tab === "overview" && <BarChart3 size={14} className="inline mr-1.5" />}
              {tab === "users" && <Users size={14} className="inline mr-1.5" />}
              {tab === "plugins" && <Plug size={14} className="inline mr-1.5" />}
              {tab}
            </button>
          ))}
        </div>

        {/* ── Overview Tab ── */}
        {activeTab === "overview" && (
          <>
            <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-8">
              {STAT_CARDS.map((card, i) => {
                const Icon = card.icon;
                const value = stats ? stats[card.key] : "--";
                return (
                  <motion.div
                    key={card.key}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.06 }}
                    className="card"
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <div
                        className="w-9 h-9 rounded-xl flex items-center justify-center"
                        style={{ background: `${card.color}18`, border: `1px solid ${card.color}30` }}
                      >
                        <Icon size={16} style={{ color: card.color }} />
                      </div>
                    </div>
                    <div className="text-2xl font-bold font-display mb-1">{value}</div>
                    <div className="text-sm text-white/40">{card.label}</div>
                  </motion.div>
                );
              })}
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* System Info */}
              <div className="card">
                <h3 className="text-lg font-semibold font-display mb-4 flex items-center gap-2">
                  <HardDrive size={16} className="text-violet-400" />
                  System
                </h3>
                <div className="space-y-3">
                  {[
                    { label: "Uptime", value: stats ? formatUptime(stats.uptime_seconds) : "--" },
                    { label: "Database Size", value: stats ? formatBytes(stats.database_size_bytes) : "--" },
                    { label: "Active Timers", value: stats?.active_timers ?? "--" },
                    { label: "Active Stopwatches", value: stats?.active_stopwatches ?? "--" },
                  ].map((item) => (
                    <div key={item.label} className="flex items-center justify-between py-2 border-b border-white/[0.04] last:border-0">
                      <span className="text-sm text-white/60">{item.label}</span>
                      <span className="text-sm font-semibold">{item.value}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div className="card">
                <h3 className="text-lg font-semibold font-display mb-4 flex items-center gap-2">
                  <Zap size={16} className="text-yellow-400" />
                  Quick Actions
                </h3>
                <div className="space-y-2">
                  {[
                    { icon: RefreshCw, label: "Clear System Cache", color: "#6C63FF" },
                    { icon: Bell, label: "Broadcast Notification", color: "#00D4FF" },
                    { icon: Settings, label: "Maintenance Mode", color: "#FF6B9D" },
                    { icon: Database, label: "Optimize Database", color: "#22c55e" },
                  ].map((action) => {
                    const Icon = action.icon;
                    return (
                      <div
                        key={action.label}
                        className="flex items-center gap-3 p-3 rounded-xl glass glass-hover cursor-pointer"
                      >
                        <Icon size={15} style={{ color: action.color }} />
                        <span className="text-sm font-medium flex-1">{action.label}</span>
                        <ChevronRight size={14} className="text-white/20" />
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </>
        )}

        {/* ── Users Tab ── */}
        {activeTab === "users" && (
          <div className="card overflow-hidden p-0">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/[0.06] text-left">
                    <th className="p-4 text-xs font-semibold text-white/40 uppercase tracking-wider">Name</th>
                    <th className="p-4 text-xs font-semibold text-white/40 uppercase tracking-wider">Email</th>
                    <th className="p-4 text-xs font-semibold text-white/40 uppercase tracking-wider">Plan</th>
                    <th className="p-4 text-xs font-semibold text-white/40 uppercase tracking-wider">Status</th>
                    <th className="p-4 text-xs font-semibold text-white/40 uppercase tracking-wider">Conversations</th>
                    <th className="p-4 text-xs font-semibold text-white/40 uppercase tracking-wider">Joined</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 && (
                    <tr>
                      <td colSpan={6} className="p-8 text-center text-white/30">No users found</td>
                    </tr>
                  )}
                  {users.map((user, i) => (
                    <motion.tr
                      key={user.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: i * 0.03 }}
                      className="border-b border-white/[0.04] hover:bg-white/[0.02] transition-colors"
                    >
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-pink-500 flex items-center justify-center text-xs font-bold text-white">
                            {user.name.charAt(0)}
                          </div>
                          <span className="font-medium">{user.name}</span>
                        </div>
                      </td>
                      <td className="p-4 text-white/60">{user.email}</td>
                      <td className="p-4">
                        <span className={`badge ${user.plan === "pro" ? "badge-premium" : "badge-free"}`}>
                          {user.plan}
                        </span>
                      </td>
                      <td className="p-4">
                        {user.is_active ? (
                          <span className="flex items-center gap-1.5 text-green-400 text-xs">
                            <CheckCircle size={12} /> Active
                          </span>
                        ) : (
                          <span className="flex items-center gap-1.5 text-red-400 text-xs">
                            <XCircle size={12} /> Inactive
                          </span>
                        )}
                      </td>
                      <td className="p-4 text-white/60">{user.conversation_count}</td>
                      <td className="p-4 text-white/40 text-xs">
                        {new Date(user.created_at).toLocaleDateString()}
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ── Plugins Tab ── */}
        {activeTab === "plugins" && (
          <div className="grid md:grid-cols-2 gap-4">
            {plugins.length === 0 && (
              <div className="md:col-span-2 p-12 text-center text-white/30">
                <Plug size={32} className="mx-auto mb-3 opacity-30" />
                No plugins loaded
              </div>
            )}
            {plugins.map((plugin, i) => (
              <motion.div
                key={plugin.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.06 }}
                className="card"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <Plug size={16} className="text-violet-400" />
                    <span className="font-semibold">{plugin.name}</span>
                  </div>
                  <span className={`badge ${plugin.enabled ? "badge-premium" : "badge-free"}`}>
                    {plugin.enabled ? "Enabled" : "Disabled"}
                  </span>
                </div>
                <p className="text-sm text-white/50 mb-2">{plugin.description || "No description"}</p>
                <div className="text-xs text-white/30">v{plugin.version}</div>
              </motion.div>
            ))}
          </div>
        )}

      </main>
    </div>
  );
}
