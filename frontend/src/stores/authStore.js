import { create } from "zustand";
import { authAPI } from "../services/api";

const useAuthStore = create((set, get) => ({
  user: JSON.parse(localStorage.getItem("user") || "null"),
  tokens: JSON.parse(localStorage.getItem("tokens") || "null"),
  loading: false,

  login: async (email, password) => {
    set({ loading: true });
    try {
      const { data } = await authAPI.login({ email, password });
      const tokens = { access: data.access, refresh: data.refresh };
      localStorage.setItem("tokens", JSON.stringify(tokens));
      // Fetch full profile
      const profile = await authAPI.profile();
      localStorage.setItem("user", JSON.stringify(profile.data));
      set({ user: profile.data, tokens, loading: false });
      return profile.data;
    } catch (err) {
      set({ loading: false });
      throw err;
    }
  },

  register: async (formData) => {
    set({ loading: true });
    try {
      const { data } = await authAPI.register(formData);
      localStorage.setItem("tokens", JSON.stringify(data.tokens));
      localStorage.setItem("user", JSON.stringify(data.user));
      set({ user: data.user, tokens: data.tokens, loading: false });
      return data.user;
    } catch (err) {
      set({ loading: false });
      throw err;
    }
  },

  logout: async () => {
    const tokens = get().tokens;
    try {
      if (tokens?.refresh) await authAPI.logout({ refresh: tokens.refresh });
    } catch {}
    localStorage.removeItem("tokens");
    localStorage.removeItem("user");
    set({ user: null, tokens: null });
  },

  updateUser: (user) => {
    localStorage.setItem("user", JSON.stringify(user));
    set({ user });
  },

  isAuthenticated: () => !!get().tokens?.access,
}));

export default useAuthStore;
