"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Mic, MicOff, Volume2, VolumeX, Settings, ChevronDown, Sparkles } from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";

type OrbState = "idle" | "listening" | "processing" | "speaking";

const WAVEFORM_HEIGHTS = [15, 30, 50, 70, 90, 70, 100, 80, 60, 80, 100, 70, 50, 30, 50, 70, 90, 70, 50, 30, 15];

const TRANSCRIPT_EXAMPLES = [
  "Hey Nova, what's the weather in Mumbai today?",
  "Play some relaxing lo-fi music on Spotify.",
  "Remind me to call mom at 7 PM.",
  "Turn off the living room lights.",
  "What's the latest news in technology?",
];

const RECENT_COMMANDS = [
  { cmd: "Play lo-fi beats", time: "2 min ago", icon: "🎵" },
  { cmd: "Weather update", time: "15 min ago", icon: "🌤️" },
  { cmd: "Set reminder", time: "1 hr ago", icon: "⏰" },
  { cmd: "Turn on bedroom lights", time: "3 hr ago", icon: "💡" },
];

function VoiceOrb({ state, onClick }: { state: OrbState; onClick: () => void }) {
  const colors: Record<OrbState, string[]> = {
    idle: ["#6C63FF", "#00D4FF"],
    listening: ["#FF6B9D", "#6C63FF"],
    processing: ["#FFD700", "#FF8C42"],
    speaking: ["#00D4FF", "#6C63FF"],
  };

  const [c1, c2] = colors[state];

  return (
    <div className="relative flex items-center justify-center cursor-pointer" onClick={onClick}>
      {/* Outer rings */}
      {state !== "idle" && [1, 2, 3].map((i) => (
        <div
          key={i}
          className="absolute rounded-full"
          style={{
            width: 200 + i * 48,
            height: 200 + i * 48,
            border: `1px solid ${c1}${state === "listening" ? "40" : "20"}`,
            animation: `ripple ${1.5 + i * 0.4}s ease-out infinite`,
            animationDelay: `${i * 0.3}s`,
          }}
        />
      ))}

      {/* Orb */}
      <motion.div
        animate={{
          scale: state === "speaking" ? [1, 1.08, 1] : state === "listening" ? [1, 1.04, 1] : 1,
          boxShadow: state !== "idle"
            ? `0 0 60px ${c1}60, 0 0 120px ${c1}30`
            : `0 0 30px ${c1}30`,
        }}
        transition={{ duration: 0.8, repeat: state !== "idle" ? Infinity : 0 }}
        className="w-48 h-48 rounded-full flex items-center justify-center relative overflow-hidden"
        style={{
          background: `radial-gradient(circle at 35% 35%, ${c1}cc, ${c2}66, ${c1}33)`,
        }}
      >
        {/* Inner glow */}
        <div className="absolute inset-0 rounded-full"
          style={{ background: `radial-gradient(circle at 35% 35%, rgba(255,255,255,0.15), transparent)` }} />

        {/* Conic border animation */}
        {state !== "idle" && (
          <div
            className="absolute inset-[-2px] rounded-full animate-spin-slow"
            style={{ background: `conic-gradient(from 0deg, ${c1}, ${c2}, ${c1})`, zIndex: -1 }}
          />
        )}

        {/* Icon */}
        <div className="relative z-10">
          {state === "idle" && <Mic size={52} className="text-white/90" />}
          {state === "listening" && (
            <motion.div
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.6, repeat: Infinity }}
            >
              <Mic size={52} className="text-white" />
            </motion.div>
          )}
          {state === "processing" && (
            <div className="flex gap-2">
              {[0, 1, 2].map((i) => (
                <div key={i} className="w-3 h-3 rounded-full bg-white"
                  style={{ animation: `wave 0.8s ease-in-out infinite`, animationDelay: `${i * 0.15}s` }} />
              ))}
            </div>
          )}
          {state === "speaking" && <Volume2 size={52} className="text-white/90" />}
        </div>
      </motion.div>
    </div>
  );
}

export default function VoicePage() {
  const [orbState, setOrbState] = useState<OrbState>("idle");
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [transcriptIndex, setTranscriptIndex] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [selectedVoice, setSelectedVoice] = useState("Nova");

  const toggleListening = () => {
    if (orbState !== "idle") {
      setOrbState("idle");
      setTranscript("");
      setResponse("");
      return;
    }

    setOrbState("listening");
    setTranscript("");

    // Simulate transcript appearing
    const example = TRANSCRIPT_EXAMPLES[transcriptIndex % TRANSCRIPT_EXAMPLES.length];
    let i = 0;
    const typeInterval = setInterval(() => {
      setTranscript(example.slice(0, ++i));
      if (i >= example.length) {
        clearInterval(typeInterval);
        setOrbState("processing");

        setTimeout(() => {
          setOrbState("speaking");
          setResponse("Sure! Current weather in Mumbai: 32°C, humid with a sea breeze. Chance of evening showers. Perfect day to stay cool indoors!");
          setTimeout(() => {
            setOrbState("idle");
            setTranscriptIndex((p) => p + 1);
          }, 4000);
        }, 1500);
      }
    }, 60);
  };

  const stateLabels: Record<OrbState, string> = {
    idle: "Tap to speak",
    listening: "Listening...",
    processing: "Thinking...",
    speaking: "Speaking...",
  };

  const stateColors: Record<OrbState, string> = {
    idle: "text-white/40",
    listening: "text-pink-400",
    processing: "text-yellow-400",
    speaking: "text-cyan-400",
  };

  return (
    <div className="flex flex-col h-screen overflow-hidden">
      <TopBar title="Voice Chat" />

      <main className="flex-1 flex overflow-hidden">
        {/* Left: Main Voice UI */}
        <div className="flex-1 flex flex-col items-center justify-center p-8 gap-8 relative">

          {/* Background ambient */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] rounded-full opacity-10"
              style={{ background: "radial-gradient(circle, #6C63FF, transparent)", filter: "blur(80px)" }} />
          </div>

          {/* Voice Orb */}
          <VoiceOrb state={orbState} onClick={toggleListening} />

          {/* State Label */}
          <div className="text-center">
            <motion.p
              key={orbState}
              initial={{ opacity: 0, y: 5 }}
              animate={{ opacity: 1, y: 0 }}
              className={`text-lg font-semibold font-display ${stateColors[orbState]}`}
            >
              {stateLabels[orbState]}
            </motion.p>
            {orbState === "idle" && (
              <p className="text-sm text-white/30 mt-1">Say "Hey Nova" or tap the orb</p>
            )}
          </div>

          {/* Waveform */}
          <div className="flex items-center gap-1 h-20">
            {WAVEFORM_HEIGHTS.map((h, i) => (
              <div
                key={i}
                className="waveform-bar transition-all"
                style={{
                  height: orbState === "idle" ? "4px" : `${h}%`,
                  opacity: orbState === "idle" ? 0.2 : 1,
                  animationPlayState: orbState === "idle" ? "paused" : "running",
                  animationDuration: `${0.6 + (i % 5) * 0.15}s`,
                  animationDelay: `${i * 0.05}s`,
                }}
              />
            ))}
          </div>

          {/* Transcript */}
          <AnimatePresence>
            {transcript && (
              <motion.div
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20 }}
                className="w-full max-w-lg glass rounded-2xl p-5 border border-white/[0.06]"
              >
                <div className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-2 flex items-center gap-2">
                  <Mic size={10} className="text-pink-400" />
                  You said
                </div>
                <p className="text-base font-medium text-white/90">{transcript}</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* AI Response */}
          <AnimatePresence>
            {response && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="w-full max-w-lg rounded-2xl p-5"
                style={{ background: "rgba(108,99,255,0.1)", border: "1px solid rgba(108,99,255,0.3)" }}
              >
                <div className="text-xs font-semibold text-violet-400 uppercase tracking-wider mb-2 flex items-center gap-2">
                  <Sparkles size={10} />
                  Nova responds
                </div>
                <p className="text-base text-white/90">{response}</p>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Controls */}
          <div className="flex gap-4">
            <button
              onClick={() => setIsMuted(!isMuted)}
              className={`btn-secondary p-3 rounded-full ${isMuted ? "border-pink-500/40" : ""}`}
            >
              {isMuted ? <VolumeX size={18} className="text-pink-400" /> : <Volume2 size={18} />}
            </button>
            <button className="btn-secondary p-3 rounded-full">
              <Settings size={18} />
            </button>
          </div>
        </div>

        {/* Right: Panel */}
        <div className="w-80 border-l border-white/[0.06] flex flex-col overflow-hidden">

          {/* Voice selector */}
          <div className="p-5 border-b border-white/[0.06]">
            <div className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-3">
              Active Voice
            </div>
            <div className="flex items-center gap-3 p-3 glass rounded-xl cursor-pointer hover:bg-white/[0.04] transition-colors">
              <div className="w-9 h-9 rounded-full bg-gradient-to-br from-violet-500 to-cyan-400 flex items-center justify-center text-sm font-bold text-white">
                N
              </div>
              <div className="flex-1">
                <div className="text-sm font-semibold">{selectedVoice}</div>
                <div className="text-xs text-white/40">Modern & Premium</div>
              </div>
              <ChevronDown size={14} className="text-white/30" />
            </div>
          </div>

          {/* Recent Commands */}
          <div className="flex-1 overflow-y-auto scroll-area p-5">
            <div className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-3">
              Recent Commands
            </div>
            <div className="space-y-2">
              {RECENT_COMMANDS.map((cmd, i) => (
                <div key={i} className="flex items-center gap-3 p-3 rounded-xl glass glass-hover cursor-pointer">
                  <span className="text-lg">{cmd.icon}</span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium truncate">{cmd.cmd}</div>
                    <div className="text-xs text-white/30">{cmd.time}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Wake word hint */}
            <div className="mt-6 p-4 rounded-xl"
              style={{ background: "rgba(108,99,255,0.08)", border: "1px solid rgba(108,99,255,0.2)" }}>
              <div className="text-xs font-semibold text-violet-400 mb-2">💡 Wake Word</div>
              <div className="text-sm text-white/60">
                Say <span className="text-white font-semibold">"Hey Nova"</span> to activate hands-free mode even when the screen is off.
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
