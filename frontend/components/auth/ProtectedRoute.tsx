"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuthStore } from "@/store/authStore";
import { Loader2 } from "lucide-react";

const PUBLIC_ROUTES = ["/login", "/register", "/"];

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, token, initialized, loading } = useAuthStore();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!initialized || loading) return;

    const isPublic = PUBLIC_ROUTES.some((route) => pathname.startsWith(route)) || pathname === "/";
    const isAuthenticated = !!token && !!user;

    if (!isAuthenticated && !isPublic && pathname !== "/login" && pathname !== "/register") {
      router.replace("/login");
    }

    if (isAuthenticated && (pathname === "/login" || pathname === "/register")) {
      router.replace("/dashboard");
    }
  }, [initialized, loading, token, user, pathname, router]);

  if (!initialized || loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#0a0a0f]">
        <div className="flex flex-col items-center gap-3">
          <Loader2 size={32} className="text-violet-400 animate-spin" />
          <p className="text-sm text-white/40">Loading...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
