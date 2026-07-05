"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";

export function AppProvider({ children }: { children: React.ReactNode }) {
  const initialize = useAuthStore((s) => s.initialize);

  useEffect(() => {
    initialize();
  }, [initialize]);

  return <>{children}</>;
}
