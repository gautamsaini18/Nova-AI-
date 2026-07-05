"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Volume2, Mic, Brain, Shield, Globe, Bell, Palette,
  ChevronRight, Check, Play, Crown, Search, Zap, Sliders
} from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";
import toast from "react-hot-toast";

// ── Voice Data ────────────────────────────────────────────────────────────────
interface Voice {
  id: string; name: string; category: string;
  gender: string; description: string; color: string; isPremium: boolean;
}

const VOICE_CATEGORIES: Record<string, Voice[]> = {
  "Modern & Premium": [
    { id: "nova", name: "Nova", category: "Modern & Premium", gender: "Female", description: "Crisp, modern, and articulate. The default Nova AI voice.", color: "#6C63FF", isPremium: false },
    { id: "aria", name: "Aria", category: "Modern & Premium", gender: "Female", description: "Elegant and expressive with a warm professional tone.", color: "#8B85FF", isPremium: true },
    { id: "lyra", name: "Lyra", category: "Modern & Premium", gender: "Female", description: "Smooth and melodic — inspired by the constellation.", color: "#A855F7", isPremium: false },
    { id: "kaia", name: "Kaia", category: "Modern & Premium", gender: "Female", description: "Bold and confident with a modern edge.", color: "#7C3AED", isPremium: true },
    { id: "nexa", name: "Nexa", category: "Modern & Premium", gender: "Female", description: "Next-generation clarity with a futuristic undertone.", color: "#6366F1", isPremium: false },
    { id: "ziva", name: "Ziva", category: "Modern & Premium", gender: "Female", description: "Energetic and dynamic, perfect for productivity.", color: "#818CF8", isPremium: false },
    { id: "elio", name: "Elio", category: "Modern & Premium", gender: "Male", description: "Deep and authoritative with a premium finish.", color: "#5B21B6", isPremium: true },
    { id: "aven", name: "Aven", category: "Modern & Premium", gender: "Male", description: "Calm, collected, and distinctly modern.", color: "#4F46E5", isPremium: false },
    { id: "orion", name: "Orion", category: "Modern & Premium", gender: "Male", description: "Resonant and trustworthy — stellar clarity.", color: "#7C3AED", isPremium: false },
    { id: "solis", name: "Solis", category: "Modern & Premium", gender: "Neutral", description: "Bright and balanced like sunlight. Genderless warmth.", color: "#6C63FF", isPremium: false },
  ],
  "Friendly & Human": [
    { id: "maya", name: "Maya", category: "Friendly & Human", gender: "Female", description: "Warm, caring, and endlessly patient. Like a best friend.", color: "#FF6B9D", isPremium: false },
    { id: "ava", name: "Ava", category: "Friendly & Human", gender: "Female", description: "Sweet and helpful with natural conversational flow.", color: "#EC4899", isPremium: false },
    { id: "luna", name: "Luna", category: "Friendly & Human", gender: "Female", description: "Gentle and soothing — perfect for late-night chats.", color: "#DB2777", isPremium: false },
    { id: "mia", name: "Mia", category: "Friendly & Human", gender: "Female", description: "Cheerful and upbeat. Makes every interaction enjoyable.", color: "#F43F5E", isPremium: false },
    { id: "zoe", name: "Zoe", category: "Friendly & Human", gender: "Female", description: "Playful and fun with a bright, youthful personality.", color: "#FB7185", isPremium: false },
    { id: "emma", name: "Emma", category: "Friendly & Human", gender: "Female", description: "Professional yet approachable. Classic and reliable.", color: "#FDA4AF", isPremium: false },
    { id: "leo", name: "Leo", category: "Friendly & Human", gender: "Male", description: "Friendly and enthusiastic — always ready to help.", color: "#FF6B9D", isPremium: false },
    { id: "noah", name: "Noah", category: "Friendly & Human", gender: "Male", description: "Calm and thoughtful with genuine human warmth.", color: "#F43F5E", isPremium: false },
    { id: "ivy", name: "Ivy", category: "Friendly & Human", gender: "Female", description: "Soft-spoken and kind with excellent clarity.", color: "#EC4899", isPremium: false },
    { id: "theo", name: "Theo", category: "Friendly & Human", gender: "Male", description: "Laid-back and likeable. Like chatting with a buddy.", color: "#DB2777", isPremium: false },
  ],
  "Futuristic": [
    { id: "syna", name: "Syna", category: "Futuristic", gender: "Female", description: "Synth-inspired, otherworldly, and mesmerizing.", color: "#A855F7", isPremium: true },
    { id: "voxa", name: "Voxa", category: "Futuristic", gender: "Female", description: "Crisp digital tones with a futuristic edge.", color: "#9333EA", isPremium: false },
    { id: "neura", name: "Neura", category: "Futuristic", gender: "Female", description: "Neural-network inspired. Precise and intelligent.", color: "#7C3AED", isPremium: true },
    { id: "quantix", name: "Quantix", category: "Futuristic", gender: "Neutral", description: "Quantum-speed communication with sci-fi flair.", color: "#6D28D9", isPremium: false },
    { id: "aether", name: "Aether", category: "Futuristic", gender: "Neutral", description: "Ethereal, weightless, and infinitely calm.", color: "#5B21B6", isPremium: false },
    { id: "zenox", name: "Zenox", category: "Futuristic", gender: "Male", description: "Zero-latency clarity with alien precision.", color: "#4C1D95", isPremium: true },
    { id: "nexis", name: "Nexis", category: "Futuristic", gender: "Female", description: "Connected and relentless — the next evolution.", color: "#8B5CF6", isPremium: false },
    { id: "kairo", name: "Kairo", category: "Futuristic", gender: "Male", description: "Ancient wisdom meets future tech.", color: "#7C3AED", isPremium: false },
    { id: "xyra", name: "Xyra", category: "Futuristic", gender: "Female", description: "Extraterrestrial tones, beautifully articulate.", color: "#A78BFA", isPremium: true },
    { id: "vexa", name: "Vexa", category: "Futuristic", gender: "Female", description: "Vector-precise, digitally enhanced voice.", color: "#8B5CF6", isPremium: false },
  ],
  "Tech-Inspired": [
    { id: "cortex", name: "Cortex", category: "Tech-Inspired", gender: "Male", description: "Deep, commanding — like your brain's CEO.", color: "#00D4FF", isPremium: true },
    { id: "nexus", name: "Nexus", category: "Tech-Inspired", gender: "Male", description: "The hub of all knowledge. Clear and central.", color: "#06B6D4", isPremium: false },
    { id: "pixel", name: "Pixel", category: "Tech-Inspired", gender: "Female", description: "Sharp and precise, pixel-perfect delivery.", color: "#0891B2", isPremium: false },
    { id: "echo", name: "Echo", category: "Tech-Inspired", gender: "Neutral", description: "Resonant, clear echoes of intelligence.", color: "#0E7490", isPremium: false },
    { id: "prism", name: "Prism", category: "Tech-Inspired", gender: "Female", description: "Multi-dimensional clarity, refracting knowledge.", color: "#22D3EE", isPremium: true },
    { id: "vertex", name: "Vertex", category: "Tech-Inspired", gender: "Male", description: "At the cutting edge — sharp, decisive, accurate.", color: "#67E8F9", isPremium: false },
    { id: "atlas", name: "Atlas", category: "Tech-Inspired", gender: "Male", description: "Carries the weight of the world's knowledge.", color: "#00D4FF", isPremium: false },
    { id: "cipher", name: "Cipher", category: "Tech-Inspired", gender: "Neutral", description: "Encrypted intelligence with crystal-clear output.", color: "#06B6D4", isPremium: false },
    { id: "pulse", name: "Pulse", category: "Tech-Inspired", gender: "Female", description: "Rhythmic and alive — feeling the beat of data.", color: "#0891B2", isPremium: false },
    { id: "orbit", name: "Orbit", category: "Tech-Inspired", gender: "Male", description: "Circling knowledge from every angle.", color: "#0E7490", isPremium: false },
  ],
  "Short & Easy": [
    { id: "aira", name: "Aira", category: "Short & Easy", gender: "Female", description: "Light and airy — effortless to remember.", color: "#22c55e", isPremium: false },
    { id: "nori", name: "Nori", category: "Short & Easy", gender: "Female", description: "Tiny name, enormous personality.", color: "#16a34a", isPremium: false },
    { id: "kiro", name: "Kiro", category: "Short & Easy", gender: "Male", description: "Quick and snappy — get things done fast.", color: "#15803d", isPremium: false },
    { id: "riva", name: "Riva", category: "Short & Easy", gender: "Female", description: "River-like flow, natural and easy.", color: "#166534", isPremium: false },
    { id: "sora", name: "Sora", category: "Short & Easy", gender: "Female", description: "Sky-inspired tranquility in a tiny name.", color: "#4ade80", isPremium: false },
    { id: "niva", name: "Niva", category: "Short & Easy", gender: "Female", description: "Fresh and clean — crisp mountain air.", color: "#22c55e", isPremium: false },
    { id: "eon", name: "Eon", category: "Short & Easy", gender: "Neutral", description: "Timeless and infinite. One syllable, endless power.", color: "#86efac", isPremium: false },
    { id: "luma", name: "Luma", category: "Short & Easy", gender: "Female", description: "Luminous and bright — lights up every conversation.", color: "#4ade80", isPremium: false },
    { id: "vero", name: "Vero", category: "Short & Easy", gender: "Male", description: "Truthful and sincere. Vero means truth.", color: "#16a34a", isPremium: false },
    { id: "zeno", name: "Zeno", category: "Short & Easy", gender: "Male", description: "Philosophical calm with zen-like presence.", color: "#15803d", isPremium: false },
  ],
  "Powerful AI Brands": [
    { id: "omnia-ai", name: "Omnia AI", category: "Powerful AI Brands", gender: "Neutral", description: "All-encompassing intelligence. Omnia means everything.", color: "#FFD700", isPremium: true },
    { id: "novamind", name: "NovaMind", category: "Powerful AI Brands", gender: "Female", description: "A new mind born from the cosmos of data.", color: "#FFC107", isPremium: true },
    { id: "intellix", name: "IntelliX", category: "Powerful AI Brands", gender: "Neutral", description: "Intelligence amplified. X marks the next level.", color: "#FF8C42", isPremium: true },
    { id: "neurocore", name: "NeuroCore", category: "Powerful AI Brands", gender: "Male", description: "Deep neural intelligence at its very core.", color: "#F59E0B", isPremium: true },
    { id: "zenith-ai", name: "Zenith AI", category: "Powerful AI Brands", gender: "Neutral", description: "The absolute peak of AI capability.", color: "#D97706", isPremium: true },
    { id: "aether-ai", name: "Aether AI", category: "Powerful AI Brands", gender: "Female", description: "Beyond the clouds — pure ethereal intelligence.", color: "#FFD700", isPremium: true },
    { id: "synapse-ai", name: "Synapse AI", category: "Powerful AI Brands", gender: "Neutral", description: "The connection between thought and action.", color: "#FCD34D", isPremium: true },
    { id: "infinity-ai", name: "Infinity AI", category: "Powerful AI Brands", gender: "Neutral", description: "Limitless knowledge, infinite possibilities.", color: "#F59E0B", isPremium: true },
    { id: "quantum-ai", name: "Quantum AI", category: "Powerful AI Brands", gender: "Male", description: "Quantum computing power in your voice assistant.", color: "#D97706", isPremium: true },
    { id: "cognexa", name: "Cognexa", category: "Powerful AI Brands", gender: "Female", description: "Cognitive nexus — where all intelligence converges.", color: "#FFC107", isPremium: true },
  ],
};

const ALL_CATEGORIES = Object.keys(VOICE_CATEGORIES);
const GENDER_ICONS: Record<string, string> = { Female: "♀", Male: "♂", Neutral: "⊕" };

// ── Settings Tabs ─────────────────────────────────────────────────────────────
const TABS = [
  { id: "voice", label: "Voice", icon: Volume2 },
  { id: "general", label: "General", icon: Sliders },
  { id: "privacy", label: "Privacy", icon: Shield },
  { id: "language", label: "Language", icon: Globe },
  { id: "notifications", label: "Alerts", icon: Bell },
];

// ── Voice Card Component ──────────────────────────────────────────────────────
function VoiceCard({ voice, isSelected, onSelect, onPreview }: {
  voice: Voice; isSelected: boolean;
  onSelect: () => void; onPreview: () => void;
}) {
  return (
    <div
      className={`voice-card ${isSelected ? "selected" : ""} relative`}
      onClick={onSelect}
    >
      {/* Premium Badge */}
      {voice.isPremium && (
        <div className="absolute top-2 right-2">
          <div className="badge badge-premium">
            <Crown size={8} />
            PRO
          </div>
        </div>
      )}

      {/* Avatar */}
      <div
        className="w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold text-white mb-3"
        style={{ background: `radial-gradient(circle, ${voice.color}50, ${voice.color}20)`, border: `1px solid ${voice.color}40` }}
      >
        {voice.name[0]}
      </div>

      {/* Info */}
      <div className="font-semibold text-sm mb-0.5">{voice.name}</div>
      <div className="text-xs text-white/40 mb-1">{GENDER_ICONS[voice.gender]} {voice.gender}</div>
      <p className="text-xs text-white/50 leading-relaxed line-clamp-2 mb-3">{voice.description}</p>

      {/* Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={(e) => { e.stopPropagation(); onPreview(); }}
          className="flex items-center gap-1.5 text-xs font-medium px-2.5 py-1.5 rounded-lg transition-colors"
          style={{ background: `${voice.color}20`, color: voice.color }}
        >
          <Play size={10} fill="currentColor" />
          Preview
        </button>
        {isSelected && (
          <div className="flex items-center gap-1 text-xs text-violet-400 ml-auto">
            <Check size={12} />
            Active
          </div>
        )}
      </div>
    </div>
  );
}

// ── Main Settings Page ────────────────────────────────────────────────────────
export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("voice");
  const [selectedVoice, setSelectedVoice] = useState("nova");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [speechSpeed, setSpeechSpeed] = useState(1.0);
  const [wakeWord, setWakeWord] = useState("hey nova");
  const [noiseCancel, setNoiseCancel] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  const [privacyMode, setPrivacyMode] = useState(false);
  const [previewingVoice, setPreviewingVoice] = useState<string | null>(null);

  // Filter voices
  const allVoices = Object.values(VOICE_CATEGORIES).flat();
  const filteredVoices = (() => {
    let voices = selectedCategory === "All" ? allVoices : (VOICE_CATEGORIES[selectedCategory] || []);
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      voices = voices.filter(v =>
        v.name.toLowerCase().includes(q) ||
        v.category.toLowerCase().includes(q) ||
        v.description.toLowerCase().includes(q) ||
        v.gender.toLowerCase().includes(q)
      );
    }
    return voices;
  })();

  const handlePreview = (voiceId: string) => {
    setPreviewingVoice(voiceId);
    toast.success(`Previewing ${voiceId}...`);
    setTimeout(() => setPreviewingVoice(null), 3000);
  };

  const handleSaveVoice = () => {
    toast.success(`Voice updated to ${allVoices.find(v => v.id === selectedVoice)?.name}!`);
  };

  return (
    <div>
      <TopBar title="Settings" />
      <main className="page-body">

        <div className="flex flex-col lg:flex-row gap-6">
          {/* Sidebar tabs */}
          <div className="lg:w-52 flex-shrink-0">
            <div className="space-y-1">
              {TABS.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all text-left ${
                      activeTab === tab.id
                        ? "bg-violet-500/15 text-violet-300 border border-violet-500/20"
                        : "text-white/50 hover:text-white hover:bg-white/[0.04]"
                    }`}
                  >
                    <Icon size={16} />
                    {tab.label}
                    {activeTab === tab.id && <ChevronRight size={14} className="ml-auto" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <AnimatePresence mode="wait">
              {/* ── VOICE TAB ── */}
              {activeTab === "voice" && (
                <motion.div
                  key="voice"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  <h2 className="text-xl font-bold font-display mb-6">Voice Selection</h2>

                  {/* Selected voice preview */}
                  {(() => {
                    const v = allVoices.find(voice => voice.id === selectedVoice);
                    if (!v) return null;
                    return (
                      <div className="rounded-2xl p-5 mb-6 flex items-center gap-4"
                        style={{ background: `${v.color}12`, border: `1px solid ${v.color}30` }}>
                        <div className="w-16 h-16 rounded-full flex items-center justify-center text-2xl font-bold text-white flex-shrink-0"
                          style={{ background: `radial-gradient(circle, ${v.color}60, ${v.color}20)`, border: `1px solid ${v.color}50` }}>
                          {v.name[0]}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-bold text-lg">{v.name}</span>
                            {v.isPremium && <span className="badge badge-premium"><Crown size={8} />PRO</span>}
                          </div>
                          <div className="text-sm text-white/50 mb-1">{v.category} · {v.gender}</div>
                          <p className="text-sm text-white/60">{v.description}</p>
                        </div>
                        <div className="flex gap-2">
                          <button onClick={() => handlePreview(v.id)} className="btn-secondary text-sm">
                            <Play size={14} />
                            Preview
                          </button>
                          <button onClick={handleSaveVoice} className="btn-primary text-sm">
                            <Check size={14} />
                            Save
                          </button>
                        </div>
                      </div>
                    );
                  })()}

                  {/* Speech Speed */}
                  <div className="card mb-6">
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <div className="font-semibold">Speech Speed</div>
                        <div className="text-sm text-white/40">Adjust voice playback rate</div>
                      </div>
                      <div className="text-lg font-bold gradient-text">{speechSpeed.toFixed(1)}x</div>
                    </div>
                    <input
                      type="range"
                      min="0.5" max="2.0" step="0.1"
                      value={speechSpeed}
                      onChange={(e) => setSpeechSpeed(parseFloat(e.target.value))}
                      className="w-full accent-violet-500 cursor-pointer"
                    />
                    <div className="flex justify-between text-xs text-white/30 mt-1">
                      <span>0.5x Slow</span>
                      <span>1.0x Normal</span>
                      <span>2.0x Fast</span>
                    </div>
                  </div>

                  {/* Search + Category Filter */}
                  <div className="flex flex-col sm:flex-row gap-3 mb-5">
                    <div className="relative flex-1">
                      <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
                      <input
                        type="text"
                        placeholder="Search voices..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="input pl-9"
                      />
                    </div>
                    <div className="flex gap-2 overflow-x-auto pb-1">
                      {["All", ...ALL_CATEGORIES].map((cat) => (
                        <button
                          key={cat}
                          onClick={() => setSelectedCategory(cat)}
                          className={`px-3 py-2 rounded-xl text-xs font-medium whitespace-nowrap transition-all flex-shrink-0 ${
                            selectedCategory === cat
                              ? "bg-violet-500/20 text-violet-300 border border-violet-500/30"
                              : "glass text-white/50 hover:text-white"
                          }`}
                        >
                          {cat}
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Count */}
                  <div className="text-xs text-white/30 mb-4 flex items-center gap-2">
                    <Zap size={10} className="text-violet-400" />
                    {filteredVoices.length} voice{filteredVoices.length !== 1 ? "s" : ""} available
                    {searchQuery && ` for "${searchQuery}"`}
                  </div>

                  {/* Voice Grid */}
                  <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    <AnimatePresence>
                      {filteredVoices.map((voice, i) => (
                        <motion.div
                          key={voice.id}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.9 }}
                          transition={{ delay: i * 0.02 }}
                        >
                          <VoiceCard
                            voice={voice}
                            isSelected={selectedVoice === voice.id}
                            onSelect={() => setSelectedVoice(voice.id)}
                            onPreview={() => handlePreview(voice.id)}
                          />
                        </motion.div>
                      ))}
                    </AnimatePresence>
                  </div>

                  {filteredVoices.length === 0 && (
                    <div className="text-center py-16 text-white/30">
                      <Volume2 size={40} className="mx-auto mb-3 opacity-30" />
                      <p>No voices found for "{searchQuery}"</p>
                    </div>
                  )}
                </motion.div>
              )}

              {/* ── GENERAL TAB ── */}
              {activeTab === "general" && (
                <motion.div key="general" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                  <h2 className="text-xl font-bold font-display mb-6">General Settings</h2>
                  <div className="space-y-4">

                    <div className="card">
                      <div className="font-semibold mb-1">Wake Word</div>
                      <div className="text-sm text-white/40 mb-3">The phrase that activates Nova AI</div>
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={wakeWord}
                          onChange={(e) => setWakeWord(e.target.value)}
                          className="input flex-1"
                          placeholder="e.g., hey nova"
                        />
                        <button className="btn-primary text-sm px-4">Save</button>
                      </div>
                    </div>

                    {[
                      { label: "Noise Cancellation", desc: "Filter background noise during voice input", value: noiseCancel, setter: setNoiseCancel },
                      { label: "Auto-Save Conversations", desc: "Automatically save all chat histories", value: autoSave, setter: setAutoSave },
                    ].map(({ label, desc, value, setter }) => (
                      <div key={label} className="card flex items-center justify-between">
                        <div>
                          <div className="font-semibold">{label}</div>
                          <div className="text-sm text-white/40">{desc}</div>
                        </div>
                        <button
                          onClick={() => setter(!value)}
                          className={`relative w-12 h-6 rounded-full transition-colors duration-200 ${value ? "bg-violet-500" : "bg-white/10"}`}
                        >
                          <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-all duration-200 ${value ? "left-6.5" : "left-0.5"}`} />
                        </button>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* ── PRIVACY TAB ── */}
              {activeTab === "privacy" && (
                <motion.div key="privacy" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                  <h2 className="text-xl font-bold font-display mb-6">Privacy & Security</h2>
                  <div className="space-y-4">
                    <div className="card flex items-center justify-between">
                      <div>
                        <div className="font-semibold">Privacy Mode</div>
                        <div className="text-sm text-white/40">No data is stored when enabled</div>
                      </div>
                      <button
                        onClick={() => setPrivacyMode(!privacyMode)}
                        className={`relative w-12 h-6 rounded-full transition-colors duration-200 ${privacyMode ? "bg-violet-500" : "bg-white/10"}`}
                      >
                        <div className={`absolute top-0.5 w-5 h-5 rounded-full bg-white shadow transition-all ${privacyMode ? "left-6.5" : "left-0.5"}`} />
                      </button>
                    </div>
                    <div className="card">
                      <div className="font-semibold mb-2 flex items-center gap-2">
                        <Shield size={16} className="text-green-400" />
                        End-to-End Encryption
                      </div>
                      <p className="text-sm text-white/50">All your conversations are encrypted in transit and at rest using AES-256.</p>
                      <div className="mt-3 flex items-center gap-2 text-green-400 text-sm">
                        <Check size={14} />
                        Active and protecting your data
                      </div>
                    </div>
                    <button className="btn-secondary text-sm w-full py-3 text-red-400 border-red-500/20 hover:bg-red-500/10">
                      Delete All My Data
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Other tabs placeholder */}
              {(activeTab === "language" || activeTab === "notifications") && (
                <motion.div key={activeTab} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                  <h2 className="text-xl font-bold font-display mb-6">
                    {activeTab === "language" ? "Language & Region" : "Notifications"}
                  </h2>
                  <div className="card text-center py-12">
                    <Globe size={40} className="mx-auto mb-3 text-violet-400 opacity-60" />
                    <p className="text-white/40">Coming soon in the next update.</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
}
