"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send, Mic, MicOff, Paperclip, RotateCcw, Copy, ThumbsUp,
  ThumbsDown, Volume2, VolumeX, Sparkles, Bot, User, Loader2
} from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";
import toast from "react-hot-toast";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

const SUGGESTED_PROMPTS = [
  "What's the weather today?",
  "Help me write a professional email",
  "Tell me a fun fact",
  "Set a reminder for 6 PM",
  "Explain quantum computing simply",
  "What should I cook for dinner?",
];

function TypingIndicator() {
  return (
    <div className="flex items-center gap-3 px-4 py-3">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-600 to-cyan-400 flex items-center justify-center flex-shrink-0">
        <Bot size={14} className="text-white" />
      </div>
      <div className="chat-bubble-ai flex items-center gap-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2 h-2 rounded-full bg-violet-400"
            style={{ animation: `wave 1.2s ease-in-out infinite`, animationDelay: `${i * 0.2}s` }}
          />
        ))}
      </div>
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === "user";
  const [copied, setCopied] = useState(false);

  const copyText = () => {
    navigator.clipboard.writeText(msg.content);
    setCopied(true);
    toast.success("Copied!");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex items-end gap-3 px-4 py-2 group ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isUser
          ? "bg-gradient-to-br from-violet-500 to-pink-500"
          : "bg-gradient-to-br from-violet-600 to-cyan-400"
      }`}>
        {isUser ? <User size={14} className="text-white" /> : <Bot size={14} className="text-white" />}
      </div>

      {/* Bubble */}
      <div className={isUser ? "chat-bubble-user" : "chat-bubble-ai"}>
        <p className="leading-relaxed">{msg.content}</p>
        <div className={`text-xs mt-1 ${isUser ? "text-white/60" : "text-white/30"}`}>
          {msg.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </div>
      </div>

      {/* Actions (AI only) */}
      {!isUser && (
        <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity mb-6">
          <button onClick={copyText} className="btn-ghost p-1.5" title="Copy">
            <Copy size={12} />
          </button>
          <button className="btn-ghost p-1.5" title="Read aloud">
            <Volume2 size={12} />
          </button>
          <button className="btn-ghost p-1.5" title="Good response">
            <ThumbsUp size={12} />
          </button>
          <button className="btn-ghost p-1.5" title="Bad response">
            <ThumbsDown size={12} />
          </button>
        </div>
      )}
    </motion.div>
  );
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content: "Hello! I'm Nova, your AI assistant. I can help you with anything — from answering questions and writing emails to controlling your smart home and scheduling meetings. What can I do for you today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages, isTyping]);

  const sendMessage = async (text?: string) => {
    const content = (text || input).trim();
    if (!content) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Simulate AI response (replace with real API call)
    setTimeout(() => {
      const responses: Record<string, string> = {
        weather: "Based on your location (New Delhi), today it's 28°C with partly cloudy skies. There's a 20% chance of rain in the evening. Would you like a full 7-day forecast?",
        email: "I'd be happy to help! Please tell me: Who is the recipient, what's the subject, and what key points should the email cover? I'll draft it for you in seconds.",
        fact: "Here's a fascinating one: Honey never spoils. Archaeologists have found 3,000-year-old honey in Egyptian tombs that was still perfectly edible! 🍯",
        reminder: "Done! I've set a reminder for 6:00 PM today. I'll notify you 5 minutes before with a voice alert. Would you like me to add a note to this reminder?",
        default: "That's a great question! I'm here to help you with anything — whether it's information, tasks, smart home control, or just a friendly chat. What specific aspect would you like me to address?",
      };
      const key = content.toLowerCase().includes("weather") ? "weather"
        : content.toLowerCase().includes("email") ? "email"
        : content.toLowerCase().includes("fact") ? "fact"
        : content.toLowerCase().includes("reminder") ? "reminder"
        : "default";

      const aiMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: responses[key],
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1500 + Math.random() * 1000);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([{
      id: "welcome-new",
      role: "assistant",
      content: "Chat cleared! How can I help you today?",
      timestamp: new Date(),
    }]);
    toast.success("Chat cleared");
  };

  return (
    <div className="flex flex-col h-screen">
      {/* Top Bar with extra actions */}
      <div className="page-header gap-4">
        <div className="flex items-center gap-3 flex-1">
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-violet-600 to-cyan-400 flex items-center justify-center">
            <Bot size={16} className="text-white" />
          </div>
          <div>
            <div className="text-base font-semibold">Nova AI</div>
            <div className="flex items-center gap-1.5">
              <div className="status-dot online" />
              <span className="text-xs text-white/40">Online · GPT-4</span>
            </div>
          </div>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setIsMuted(!isMuted)} className="btn-ghost p-2">
            {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
          </button>
          <button onClick={clearChat} className="btn-ghost p-2" title="Clear chat">
            <RotateCcw size={16} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto scroll-area py-4" style={{ background: "var(--bg-base)" }}>

        {/* Suggested prompts (show only at start) */}
        {messages.length === 1 && (
          <div className="px-6 py-4">
            <p className="text-xs font-semibold text-white/30 uppercase tracking-wider mb-3">
              Suggested
            </p>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {SUGGESTED_PROMPTS.map((prompt) => (
                <button
                  key={prompt}
                  onClick={() => sendMessage(prompt)}
                  className="text-left p-3 rounded-xl glass glass-hover text-sm text-white/60 hover:text-white transition-colors"
                >
                  <Sparkles size={12} className="text-violet-400 mb-1.5" />
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg) => (
          <MessageBubble key={msg.id} msg={msg} />
        ))}

        <AnimatePresence>
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
            >
              <TypingIndicator />
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-white/[0.06]" style={{ background: "rgba(10,10,15,0.9)", backdropFilter: "blur(20px)" }}>
        <div className="flex items-end gap-3 max-w-4xl mx-auto">
          <button className="btn-ghost p-2.5 flex-shrink-0">
            <Paperclip size={18} />
          </button>
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask Nova anything... (Shift+Enter for new line)"
              rows={1}
              className="input resize-none py-3 pr-12 min-h-[48px] max-h-32"
              style={{ scrollbarWidth: "none" }}
            />
          </div>
          <button
            onClick={() => setIsListening(!isListening)}
            className={`p-3 rounded-full flex-shrink-0 transition-all ${
              isListening
                ? "bg-violet-500 text-white animate-pulse-glow"
                : "glass border border-white/10 text-white/60 hover:text-white"
            }`}
          >
            {isListening ? <MicOff size={18} /> : <Mic size={18} />}
          </button>
          <button
            onClick={() => sendMessage()}
            disabled={!input.trim() || isTyping}
            className="btn-primary p-3 flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none"
          >
            {isTyping ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
          </button>
        </div>
        <p className="text-center text-xs text-white/20 mt-2">
          Nova AI can make mistakes. Verify important information.
        </p>
      </div>
    </div>
  );
}
