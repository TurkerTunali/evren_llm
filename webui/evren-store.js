import { createStore } from "/js/AlpineStore.js";
import * as API from "/js/api.js";
import { store as notificationStore } from "/components/notifications/notification-store.js";

const EVREN_API = "/plugins/evren_llm/evren_info";

function toast(text, type) {
  notificationStore.addFrontendToastOnly(type, text, "EVREN LLM", 5);
}

function fmt(n) {
  const v = Number(n);
  return Number.isFinite(v) ? v.toLocaleString("tr-TR") : "-";
}

export const store = createStore("evrenStore", {
  // --- state ---
  loading: false,
  connected: null, // null=unknown, true/false after test
  models: 0,
  quota: null,
  terms: null,

  init() {},
  cleanup() {},

  // Called from config.html when the settings modal opens.
  async onOpen(apiKey) {
    if (!apiKey) {
      this.connected = null;
      this.quota = null;
      return;
    }
    await this.refresh(apiKey);
  },

  // Full refresh: connection + terms + quota. Never throws.
  async refresh(apiKey) {
    if (!apiKey) return;
    this.loading = true;
    try {
      const conn = await API.callJsonApi(EVREN_API, { api_key: apiKey, action: "test" });
      this.connected = !!conn.ok;
      this.models = conn.models || 0;
      if (conn.ok) {
        try {
          const t = await API.callJsonApi(EVREN_API, { api_key: apiKey, action: "terms" });
          this.terms = t.terms || null;
        } catch (e) { this.terms = null; }
        await this.refreshQuota(apiKey);
        toast("Connected - " + this.models + " models available", "success");
      } else {
        this.quota = null;
        const msg = conn.error === "terms_not_accepted"
          ? "Terms must be accepted before use"
          : "Connection failed: " + (conn.error || "unknown error");
        toast(msg, "error");
      }
    } catch (error) {
      this.connected = false;
      toast("EVREN test failed: " + error.message, "error");
    } finally {
      this.loading = false;
    }
  },

  // Cheap quota-only refresh for the live stats widget.
  async refreshQuota(apiKey) {
    if (!apiKey) return;
    try {
      const q = await API.callJsonApi(EVREN_API, { api_key: apiKey, action: "quota" });
      this.quota = q.quota || null;
    } catch (e) { /* quota is optional; keep last value */ }
  },

  async acceptTerms(apiKey, version) {
    try {
      await API.callJsonApi(EVREN_API, { api_key: apiKey, action: "accept_terms", version });
      this.terms = (await API.callJsonApi(EVREN_API, { api_key: apiKey, action: "terms" })).terms;
      toast("Terms accepted - you can start chatting", "success");
    } catch (error) {
      toast("Could not accept terms: " + error.message, "error");
    }
  },

  // --- display helpers (kept in the store so templates stay thin) ---
  get dailyUsed() { return this.quota ? fmt(this.quota.daily_used_tokens) : "-"; },
  get dailyLimit() { return this.quota ? fmt(this.quota.daily_limit_tokens) : "-"; },
  get dailyRemaining() { return this.quota ? fmt(this.quota.daily_remaining_tokens) : "-"; },
  get dailyPercent() {
    if (!this.quota || !this.quota.daily_limit_tokens) return 0;
    return Math.min(100, Math.round((this.quota.daily_used_tokens / this.quota.daily_limit_tokens) * 100));
  },
  get windowPercent() {
    return this.quota && Number.isFinite(this.quota.usage_ratio)
      ? Math.round(this.quota.usage_ratio * 100) : 0;
  },
  get creditsRemaining() { return this.quota ? this.quota.remaining_cr : "-"; },
  get dailyReset() { return this.quota ? (this.quota.daily_reset_at || "-") : "-"; },
  get needsTerms() { return !!this.terms && !this.terms.accepted; }
});
