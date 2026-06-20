import { describe, it, expect } from "vitest";

describe("Auth Store", () => {
  it("should start with null user", () => {
    // Clear any stored data
    localStorage.clear();
    const { default: useAuthStore } = require("../stores/authStore");
    const state = useAuthStore.getState();
    expect(state.user).toBeNull();
  });

  it("should report not authenticated when no tokens", () => {
    localStorage.clear();
    const { default: useAuthStore } = require("../stores/authStore");
    expect(useAuthStore.getState().isAuthenticated()).toBe(false);
  });
});

describe("API helpers exist", () => {
  it("should export all API modules", () => {
    const api = require("../services/api");
    expect(api.authAPI).toBeDefined();
    expect(api.courseAPI).toBeDefined();
    expect(api.assignmentAPI).toBeDefined();
    expect(api.quizAPI).toBeDefined();
    expect(api.forumAPI).toBeDefined();
    expect(api.paymentAPI).toBeDefined();
  });
});
