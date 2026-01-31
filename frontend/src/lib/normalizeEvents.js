const normalizeType = (value) => {
  const raw = String(value || "").toLowerCase();
  if (raw.includes("flood")) return "Flood";
  if (raw.includes("fire") || raw.includes("wildfire")) return "Fire";
  return "Fire";
};

const normalizeConfidence = (value) => {
  const num = Number(value ?? 0);
  if (!Number.isFinite(num)) return 0;
  const scaled = num > 0 && num <= 1 ? num * 100 : num;
  return Math.max(0, Math.min(100, Math.round(scaled)));
};

const toNumber = (value) => {
  const num = Number(value);
  return Number.isFinite(num) ? num : null;
};

export const normalizeEvents = (input) => {
  const list = Array.isArray(input)
    ? input
    : Array.isArray(input?.events)
    ? input.events
    : [];

  return list
    .map((raw, index) => {
      const lat = toNumber(raw.lat ?? raw.latitude);
      const lng = toNumber(raw.lng ?? raw.lon ?? raw.longitude);

      return {
        id: String(raw.id ?? raw.event_id ?? raw.eventId ?? `evt-${index + 1}`),
        type: normalizeType(raw.type ?? raw.event_type ?? raw.eventType),
        confidence: normalizeConfidence(raw.confidence ?? raw.score),
        lat,
        lng,
        title: String(raw.title ?? raw.headline ?? raw.name ?? "Untitled event"),
        source: String(raw.source ?? raw.source_name ?? "Unknown source"),
        timestamp: String(raw.timestamp ?? raw.time ?? raw.datetime ?? new Date().toISOString()),
        details: String(raw.details ?? raw.description ?? raw.summary ?? ""),
      };
    })
    .filter((event) => Number.isFinite(event.lat) && Number.isFinite(event.lng));
};
