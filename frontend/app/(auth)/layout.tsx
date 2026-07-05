import type { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    template: "%s | Nova AI",
    default: "Auth | Nova AI",
  },
};

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div
      className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden"
      style={{ background: "var(--bg-base)" }}
    >
      {/* Ambient blobs */}
      <div className="absolute top-1/4 left-1/4 w-80 h-80 rounded-full opacity-15 pointer-events-none"
        style={{ background: "radial-gradient(circle, #6C63FF, transparent)", filter: "blur(80px)" }} />
      <div className="absolute bottom-1/4 right-1/4 w-60 h-60 rounded-full opacity-10 pointer-events-none"
        style={{ background: "radial-gradient(circle, #00D4FF, transparent)", filter: "blur(80px)" }} />
      {children}
    </div>
  );
}
