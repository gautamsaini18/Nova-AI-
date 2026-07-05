import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import {
  auth,
  googleProvider,
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendPasswordResetEmail,
  signOut as firebaseSignOut,
  isFirebaseConfigured,
} from "@/lib/firebase";
import { apiClient, configureApi } from "@/lib/api";
import type { User, AuthResponse } from "@/types";

interface AuthStore {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  loading: boolean;
  error: string | null;
  initialized: boolean;

  initialize: () => void;
  loginWithGoogle: () => Promise<void>;
  loginWithEmail: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  sendPasswordReset: (email: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshSession: () => Promise<void>;
  fetchProfile: () => Promise<void>;
  setUser: (user: User | null) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => {
      configureApi(
        () => get().token,
        () => get().logout()
      );

      return {
        user: null,
        token: null,
        refreshToken: null,
        loading: false,
        error: null,
        initialized: false,

        initialize: () => {
          const { token, refreshToken, fetchProfile } = get();
          if (token && refreshToken) {
            fetchProfile();
          }
          set({ initialized: true });
        },

        loginWithGoogle: async () => {
          if (!isFirebaseConfigured()) {
            set({ error: "Firebase is not configured. Please set up Firebase credentials." });
            return;
          }
          if (!auth) {
            set({ error: "Firebase auth is not available." });
            return;
          }
          set({ loading: true, error: null });
          try {
            const result = await signInWithPopup(auth, googleProvider);
            const idToken = await result.user.getIdToken();

            const data = await apiClient.post<AuthResponse>(
              "/auth/firebase",
              { id_token: idToken },
              { skipAuth: true }
            );

            localStorage.setItem("auth-token", data.access_token);
            localStorage.setItem("auth-refresh-token", data.refresh_token);

            set({
              user: data.user,
              token: data.access_token,
              refreshToken: data.refresh_token,
              loading: false,
              error: null,
            });
          } catch (err) {
            const message = err instanceof Error ? err.message : "Google sign-in failed";
            set({ loading: false, error: message });
            throw err;
          }
        },

        loginWithEmail: async (email, password) => {
          set({ loading: true, error: null });

          if (isFirebaseConfigured() && auth) {
            try {
              await signInWithEmailAndPassword(auth, email, password);
            } catch {
              // Fall through to backend login if Firebase fails
            }
          }

          try {
            const data = await apiClient.post<AuthResponse>(
              "/auth/login",
              { email, password },
              { skipAuth: true }
            );

            localStorage.setItem("auth-token", data.access_token);
            localStorage.setItem("auth-refresh-token", data.refresh_token);

            set({
              user: data.user,
              token: data.access_token,
              refreshToken: data.refresh_token,
              loading: false,
              error: null,
            });
          } catch (err) {
            const message = err instanceof Error ? err.message : "Login failed";
            set({ loading: false, error: message });
            throw err;
          }
        },

        register: async (email, password, name) => {
          set({ loading: true, error: null });

          if (isFirebaseConfigured() && auth) {
            try {
              await createUserWithEmailAndPassword(auth, email, password);
            } catch {
              // Fall through to backend register
            }
          }

          try {
            const data = await apiClient.post<AuthResponse>(
              "/auth/register",
              { email, password, name },
              { skipAuth: true }
            );

            localStorage.setItem("auth-token", data.access_token);
            localStorage.setItem("auth-refresh-token", data.refresh_token);

            set({
              user: data.user,
              token: data.access_token,
              refreshToken: data.refresh_token,
              loading: false,
              error: null,
            });
          } catch (err) {
            const message = err instanceof Error ? err.message : "Registration failed";
            set({ loading: false, error: message });
            throw err;
          }
        },

        sendPasswordReset: async (email) => {
          set({ loading: true, error: null });
          try {
            if (isFirebaseConfigured() && auth) {
              await sendPasswordResetEmail(auth, email);
            }
            await apiClient.post(
              "/auth/password-reset",
              { email },
              { skipAuth: true }
            );
            set({ loading: false });
          } catch (err) {
            const message = err instanceof Error ? err.message : "Password reset failed";
            set({ loading: false, error: message });
            throw err;
          }
        },

        logout: async () => {
          try {
            if (auth) {
              await firebaseSignOut(auth);
            }
          } catch {
            // Ignore Firebase sign-out errors
          }

          localStorage.removeItem("auth-token");
          localStorage.removeItem("auth-refresh-token");

          set({
            user: null,
            token: null,
            refreshToken: null,
            loading: false,
            error: null,
          });
        },

        refreshSession: async () => {
          const { refreshToken } = get();
          if (!refreshToken) return;

          try {
            const data = await apiClient.post<{ access_token: string }>(
              "/auth/refresh",
              { refresh_token: refreshToken },
              { skipAuth: true }
            );

            localStorage.setItem("auth-token", data.access_token);
            set({ token: data.access_token });
          } catch {
            get().logout();
          }
        },

        fetchProfile: async () => {
          const { token } = get();
          if (!token) return;

          try {
            const user = await apiClient.get<User>("/auth/me");
            set({ user });
          } catch {
            get().logout();
          }
        },

        setUser: (user) => set({ user }),
        clearError: () => set({ error: null }),
      };
    },
    {
      name: "nova-auth",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        refreshToken: state.refreshToken,
        user: state.user,
      }),
    }
  )
);
