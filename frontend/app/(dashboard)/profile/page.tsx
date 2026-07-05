"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { User, Camera, Edit3, Mail, Phone, Globe, Lock, Shield, LogOut, ChevronRight, Star } from "lucide-react";
import { TopBar } from "@/components/layout/Sidebar";
import toast from "react-hot-toast";

const PROFILE_STATS = [
  { label: "Conversations", value: "142" },
  { label: "Voice Sessions", value: "89" },
  { label: "Days Active", value: "67" },
  { label: "Memories", value: "23" },
];

export default function ProfilePage() {
  const [name, setName] = useState("Gautam Saini");
  const [email, setEmail] = useState("gautam@example.com");
  const [phone, setPhone] = useState("+91 98765 43210");
  const [editing, setEditing] = useState(false);

  const handleSave = () => {
    setEditing(false);
    toast.success("Profile updated successfully!");
  };

  return (
    <div>
      <TopBar title="Profile" />
      <main className="page-body">
        <div className="max-w-2xl">

          {/* Profile Header Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card mb-6 relative overflow-hidden"
          >
            {/* Background gradient */}
            <div className="absolute inset-0 opacity-20"
              style={{ background: "linear-gradient(135deg, #6C63FF 0%, #00D4FF 100%)" }} />

            <div className="relative flex flex-col sm:flex-row items-start sm:items-center gap-5">
              {/* Avatar */}
              <div className="relative">
                <div className="w-20 h-20 rounded-full bg-gradient-to-br from-violet-500 to-pink-500 flex items-center justify-center text-3xl font-bold text-white">
                  {name[0]}
                </div>
                <button className="absolute -bottom-1 -right-1 w-7 h-7 rounded-full glass border border-white/20 flex items-center justify-center hover:bg-white/10 transition-colors">
                  <Camera size={12} />
                </button>
                <div className="status-dot online absolute top-1 right-1 border-2 border-[var(--bg-surface)]" />
              </div>

              {/* Info */}
              <div className="flex-1">
                <div className="text-2xl font-bold font-display mb-1">{name}</div>
                <div className="text-white/50 text-sm mb-2">{email}</div>
                <div className="flex items-center gap-2">
                  <div className="badge badge-premium">
                    <Star size={8} fill="currentColor" />
                    Pro Plan
                  </div>
                  <div className="badge badge-new">Active</div>
                </div>
              </div>

              <button
                onClick={() => setEditing(!editing)}
                className="btn-secondary text-sm"
              >
                <Edit3 size={14} />
                {editing ? "Cancel" : "Edit Profile"}
              </button>
            </div>

            {/* Stats */}
            <div className="glow-divider" />
            <div className="grid grid-cols-4 gap-4">
              {PROFILE_STATS.map((stat) => (
                <div key={stat.label} className="text-center">
                  <div className="text-xl font-bold font-display gradient-text">{stat.value}</div>
                  <div className="text-xs text-white/40">{stat.label}</div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Edit Form */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card mb-4"
          >
            <h3 className="font-semibold mb-4">Personal Information</h3>
            <div className="space-y-4">
              {[
                { label: "Full Name", value: name, setter: setName, icon: User },
                { label: "Email Address", value: email, setter: setEmail, icon: Mail },
                { label: "Phone Number", value: phone, setter: setPhone, icon: Phone },
              ].map(({ label, value, setter, icon: Icon }) => (
                <div key={label}>
                  <label className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-2 block">{label}</label>
                  <div className="relative">
                    <Icon size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/30" />
                    <input
                      type="text"
                      value={value}
                      onChange={(e) => setter(e.target.value)}
                      disabled={!editing}
                      className="input pl-9 disabled:opacity-60 disabled:cursor-not-allowed"
                    />
                  </div>
                </div>
              ))}
            </div>
            {editing && (
              <div className="flex gap-2 mt-4 justify-end">
                <button onClick={() => setEditing(false)} className="btn-ghost text-sm">Cancel</button>
                <button onClick={handleSave} className="btn-primary text-sm">Save Changes</button>
              </div>
            )}
          </motion.div>

          {/* Account Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <h3 className="font-semibold mb-4">Account</h3>
            <div className="space-y-2">
              {[
                { icon: Lock, label: "Change Password", color: "text-white/60" },
                { icon: Shield, label: "Security Settings", color: "text-white/60" },
                { icon: Globe, label: "Connected Accounts", color: "text-white/60" },
                { icon: LogOut, label: "Sign Out", color: "text-red-400" },
              ].map(({ icon: Icon, label, color }) => (
                <button key={label} className={`w-full flex items-center gap-3 p-3 rounded-xl hover:bg-white/[0.04] transition-colors ${color}`}>
                  <Icon size={16} />
                  <span className="text-sm font-medium">{label}</span>
                  <ChevronRight size={14} className="ml-auto text-white/20" />
                </button>
              ))}
            </div>
          </motion.div>
        </div>
      </main>
    </div>
  );
}
