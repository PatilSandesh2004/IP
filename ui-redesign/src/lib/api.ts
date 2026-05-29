import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8100",
  headers: {
    "Content-Type": "application/json"
  }
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const raw = window.localStorage.getItem("interviewos-redesign-auth");
    if (raw) {
      try {
        const parsed = JSON.parse(raw) as { access_token?: string };
        if (parsed.access_token) {
          config.headers.Authorization = `Bearer ${parsed.access_token}`;
        }
      } catch {
        // ignore malformed local storage values
      }
    }
  }

  return config;
});

export default api;