import { normalizeEvents } from "./normalizeEvents";

export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const fetchWithTimeout = async (url, options = {}) => {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    return response;
  } finally {
    clearTimeout(timeout);
  }
};

export const getEvents = async () => {
  const response = await fetchWithTimeout(`${API_BASE}/events`);
  if (!response.ok) {
    throw new Error(`Events request failed: ${response.status}`);
  }
  const data = await response.json();
  return normalizeEvents(data);
};

export const getPlan = async (eventId) => {
  const response = await fetchWithTimeout(`${API_BASE}/events/${eventId}/plan`);
  if (!response.ok) {
    throw new Error(`Plan request failed: ${response.status}`);
  }

  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
};
