"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Search, MessageSquare, Mic, Filter, Trash2, ChevronRight, Calendar } from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";

const HISTORY_ITEMS = [
  { id: 1, title: "Weather & Morning Briefing", preview: "What's the weather today? I need to plan my day...", date: "Today, 9:12 AM", type: "chat", messages: 8 },
  { id: 2, title: "Email Drafting Session", preview: "Help me write a professional follow-up email to...", date: "Today, 8:30 AM", type: "chat", messages: 12 },
  { id: 3, title: "Voice Commands — Spotify", preview: "Play my morning playlist, skip this song, volume up...", date: "Yesterday, 7:45 AM", type: "voice", messages: 5 },
  { id: 4, title: "Quantum Computing Explained", preview: "Can you explain quantum entanglement in simple terms?", date: "Yesterday, 3:20 PM", type: "chat", messages: 24 },
  { id: 5, title: "Smart Home Automation", preview: "Turn off all lights, set thermostat to 22°C...", date: "Dec 28, 2025", type: "voice", messages: 7 },
  { id: 6, title: "Trip Planning — Goa", preview: "Plan a 3-day trip to Goa with budget under ₹15,000...", date: "Dec 27, 2025", type: "chat", messages: 31 },
  { id: 7, title: "Coding Help — React Hooks", preview: "Explain how useCallback differs from useMemo...", date: "Dec 26, 2025", type: "chat", messages: 18 },
  { id: 8, title: "Recipe Suggestions", preview: "What can I make with chicken, tomatoes, and cheese?", date: "Dec 25, 2025", type: "chat", messages: 9 },
];

export default function HistoryPage() {
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");

  const filtered = HISTORY_ITEMS.filter((item) => {
    const matchSearch = item.title.toLowerCase().includes(search.toLowerCase()) ||
      item.preview.toLowerCase().includes(search.toLowerCase());
    const matchFilter = filter === "all" || item.type === filter;
    return matchSearch && matchFilter;
  });

  return (
    <div>
      <TopBar title="History" />
      <main className="page-body">
        {/* Search + Filter */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
            <input
              type="text"
              placeholder="Search conversations..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input pl-9"
            />
          </div>
          <div className="flex gap-2">
            {["all", "chat", "voice"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-4 py-2 rounded-xl text-sm font-medium capitalize transition-all ${
                  filter === f
                    ? "bg-violet-500/20 text-violet-300 border border-violet-500/30"
                    : "glass text-white/50 hover:text-white"
                }`}
              >
                {f === "all" ? "All" : f === "chat" ? "💬 Chat" : "🎙️ Voice"}
              </button>
            ))}
          </div>
        </div>

        {/* Stats Row */}
        <div className="flex gap-4 mb-6">
          <div className="glass px-4 py-2 rounded-xl text-sm">
            <span className="text-white/40">Total: </span>
            <span className="font-semibold">{HISTORY_ITEMS.length} conversations</span>
          </div>
          <div className="glass px-4 py-2 rounded-xl text-sm">
            <span className="text-white/40">This week: </span>
            <span className="font-semibold">4 sessions</span>
          </div>
        </div>

        {/* History List */}
        <div className="space-y-2">
          {filtered.map((item, i) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.06 }}
              className="card card-hover flex items-center gap-4 cursor-pointer py-4"
            >
              <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                item.type === "voice"
                  ? "bg-cyan-500/10 border border-cyan-500/20"
                  : "bg-violet-500/10 border border-violet-500/20"
              }`}>
                {item.type === "voice"
                  ? <Mic size={16} className="text-cyan-400" />
                  : <MessageSquare size={16} className="text-violet-400" />
                }
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <div className="font-semibold text-sm truncate">{item.title}</div>
                  <div className={`badge text-xs ${item.type === "voice" ? "badge-free" : "badge-new"}`}>
                    {item.messages} msgs
                  </div>
                </div>
                <p className="text-xs text-white/40 truncate">{item.preview}</p>
              </div>

              <div className="flex items-center gap-3 flex-shrink-0">
                <div className="text-xs text-white/30 whitespace-nowrap">{item.date}</div>
                <ChevronRight size={14} className="text-white/20" />
              </div>
            </motion.div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20">
            <MessageSquare size={48} className="mx-auto mb-3 opacity-20" />
            <p className="text-white/30">No conversations found</p>
          </div>
        )}
      </main>
    </div>
  );
}
