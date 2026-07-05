import { Sidebar } from "@/components/layout/Sidebar";
import { AuthGuard } from "@/components/auth/ProtectedRoute";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    template: "%s | Nova AI",
    default: "Dashboard | Nova AI",
  },
};

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthGuard>
      <div className="dashboard-layout">
        <Sidebar />
        <div className="main-content">{children}</div>
      </div>
    </AuthGuard>
  );
}
