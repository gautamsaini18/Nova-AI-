"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, Plus, Search, Trash2, Tag, Clock, Star, Lock, Filter } from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";
import toast from "react-hot-toast";

const MEMORY_ITEMS = [
  { id: "1", type: "preference", content: "User prefers dark mode and minimal UI designs.", tags: ["ui", "preference"], createdAt: "Today", starred: true },
  { id: "2", type: "fact", content: "User's name is Gautam Saini. Lives in India.", tags: ["personal"], createdAt: "2 days ago", starred: true },
  { id: "3", type: "preference", content: "Favorite music genre: Lo-fi and ambient electronic.", tags: ["music", "preference"], createdAt: "1 week ago", starred: false },
  { id: "4", type: "note", content: "Meeting with team every Monday at 10 AM IST.", tags: ["work", "schedule"], createdAt: "1 week ago", starred: false },
  { id: "5", type: "fact", content: "Currently working on an AI Voice Assistant project.", tags: ["project", "work"], createdAt: "2 weeks ago", starred: true },
  { id: "6", type: "preference", content: "Prefers concise answers, not overly verbose responses.", tags: ["conversation", "preference"], createdAt: "2 weeks ago", starred: false },
  { id: "7", type: "note", content: "Reminder: Renew domain subscription in January.", tags: ["reminder", "tech"], createdAt: "3 weeks ago", starred: false },
  { id: "8", type: "fact", content: "Allergic to peanuts. Prefers vegetarian food suggestions.", tags: ["health", "personal"], createdAt: "1 month ago", starred: false },
];

const TYPE_COLORS: Record<string, string> = {
  preference: "#6C63FF",
  fact: "#00D4FF",
  note: "#FF6B9D",
  conversation: "#22c55e",
};

const TYPE_LABELS: Record<string, string> = {
  preference: "🎯 Preference",
  fact: "📋 Fact",
  note: "📝 Note",
  conversation: "💬 Conversation",
};

export default function MemoryPage() {
  const [items, setItems] = useState(MEMORY_ITEMS);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("all");
  const [newMemory, setNewMemory] = useState("");
  const [showAdd, setShowAdd] = useState(false);

  const filtered = items.filter((item) => {
    const matchSearch = item.content.toLowerCase().includes(search.toLowerCase()) ||
      item.tags.some(t => t.includes(search.toLowerCase()));
    const matchFilter = filter === "all" || item.type === filter || (filter === "starred" && item.starred);
    return matchSearch && matchFilter;
  });

  const deleteMemory = (id: string) => {
    setItems((prev) => prev.filter(m => m.id !== id));
    toast.success("Memory deleted");
  };

  const toggleStar = (id: string) => {
    setItems((prev) => prev.map(m => m.id === id ? { ...m, starred: !m.starred } : m));
  };

  const addMemory = () => {
    if (!newMemory.trim()) return;
    setItems((prev) => [{
      id: Date.now().toString(),
      type: "note",
      content: newMemory,
      tags: ["manual"],
      createdAt: "Just now",
      starred: false,
    }, ...prev]);
    setNewMemory("");
    setShowAdd(false);
    toast.success("Memory saved!");
  };

  return (
    <div>
      <TopBar title="Memory" />
      <main className="page-body">

        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-white/40 text-sm">{items.length} memories stored • {items.filter(m => m.starred).length} starred</p>
          </div>
          <button onClick={() => setShowAdd(!showAdd)} className="btn-primary text-sm">
            <Plus size={15} />
            Add Memory
          </button>
        </div>

        {/* Add Memory */}
        <AnimatePresence>
          {showAdd && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="card mb-6 border-violet-500/20"
            >
              <textarea
                value={newMemory}
                onChange={(e) => setNewMemory(e.target.value)}
                placeholder="Enter something Nova should remember about you..."
                rows={3}
                className="input resize-none mb-3"
              />
              <div className="flex gap-2 justify-end">
                <button onClick={() => setShowAdd(false)} className="btn-ghost text-sm">Cancel</button>
                <button onClick={addMemory} className="btn-primary text-sm">Save Memory</button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Search + Filter */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
            <input
              type="text"
              placeholder="Search memories..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input pl-9"
            />
          </div>
          <div className="flex gap-2 flex-wrap">
            {["all", "preference", "fact", "note", "starred"].map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-2 rounded-xl text-xs font-medium capitalize transition-all ${
                  filter === f
                    ? "bg-violet-500/20 text-violet-300 border border-violet-500/30"
                    : "glass text-white/50 hover:text-white"
                }`}
              >
                {f === "starred" ? "⭐ Starred" : f}
              </button>
            ))}
          </div>
        </div>

        {/* Memory Grid */}
        <div className="grid md:grid-cols-2 gap-3">
          {filtered.map((item, i) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.04 }}
              layout
              className="card group relative"
              style={{ borderColor: `${TYPE_COLORS[item.type]}20` }}
            >
              {/* Type badge */}
              <div className="flex items-center justify-between mb-3">
                <div className="badge text-xs" style={{ background: `${TYPE_COLORS[item.type]}15`, color: TYPE_COLORS[item.type], border: `1px solid ${TYPE_COLORS[item.type]}30` }}>
                  {TYPE_LABELS[item.type]}
                </div>
                <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button onClick={() => toggleStar(item.id)} className="btn-ghost p-1.5">
                    <Star size={12} className={item.starred ? "text-yellow-400 fill-yellow-400" : ""} />
                  </button>
                  <button onClick={() => deleteMemory(item.id)} className="btn-ghost p-1.5 text-red-400">
                    <Trash2 size={12} />
                  </button>
                </div>
              </div>

              <p className="text-sm text-white/80 mb-3 leading-relaxed">{item.content}</p>

              <div className="flex items-center justify-between">
                <div className="flex gap-1.5 flex-wrap">
                  {item.tags.map((tag) => (
                    <span key={tag} className="feature-tag text-xs">
                      <Tag size={8} />
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="flex items-center gap-1 text-xs text-white/30">
                  <Clock size={10} />
                  {item.createdAt}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="text-center py-20">
            <Brain size={48} className="mx-auto mb-3 opacity-20" />
            <p className="text-white/30">No memories found</p>
          </div>
        )}

        {/* Privacy note */}
        <div className="mt-8 flex items-center gap-2 text-xs text-white/20">
          <Lock size={10} />
          All memories are encrypted and stored securely. Only you can access them.
        </div>
      </main>
    </div>
  );
}
