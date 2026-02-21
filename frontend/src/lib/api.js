import { normalizeEvents } from "./normalizeEvents";

export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const checkHealth = async () => {
  try {
    const response = await fetchWithTimeout(`${API_BASE}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};

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
  const response = await fetchWithTimeout(`${API_BASE}/user/alerts`);
  if (!response.ok) {
    throw new Error(`Events request failed: ${response.status}`);
  }
  const data = await response.json();
  return normalizeEvents(data);
};

export const updateTaskStatus = async (alertId, index, done) => {
  const url = `${API_BASE}/user/alerts/${alertId}/actions/${index}?done=${done}`;
  const response = await fetchWithTimeout(url, {
    method: "PATCH",
  });

  if (!response.ok) {
    throw new Error(`Failed to update task: ${response.status}`);
  }
  return response.json();
};

export const resolveAlert = async (alertId) => {
  const response = await fetchWithTimeout(`${API_BASE}/user/alerts/${alertId}/resolve`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error(`Failed to resolve alert: ${response.status}`);
  }
  return response.json();
};