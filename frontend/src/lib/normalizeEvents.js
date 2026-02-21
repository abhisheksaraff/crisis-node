
const normalizeType = (value) => {
  if (!value) return "Unknown";
  const raw = String(value).trim().toLowerCase();
  // Capitalize the first letter (e.g., "flood" -> "Flood")
  return raw.charAt(0).toUpperCase() + raw.slice(1);
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
    : Array.isArray(input?.alerts) 
    ? input.alerts
    : [];

  return list
    .map((raw, index) => {
      const lat = toNumber(raw.location?.lat ?? raw.lat ?? raw.latitude);
      const lng = toNumber(raw.location?.lon ?? raw.lng ?? raw.longitude);

      const rawDate = raw.created_at ?? raw.timestamp ?? raw.time_stamp;
      const standardizedDate = rawDate 
        ? new Date(rawDate).toISOString() 
        : new Date().toISOString();

      // Ensure source is always an array of objects
      const sourcesArray = Array.isArray(raw.sources) 
        ? raw.sources 
        : Array.isArray(raw.source) 
        ? raw.source 
        : [{ name: raw.source || "Unknown source", url: "#" }];

      return {
        id: String(raw.alert_id ?? raw.id ?? `evt-${index + 1}`),
        type: normalizeType(raw.event ?? raw.type),
        lat,
        lng,
        name: raw.location?.name || raw.name || "Unknown Location",
        title: String(raw.title ?? "Untitled event"),
        source: sourcesArray, 
        timestamp: standardizedDate,
        details: String(raw.content ?? raw.details ?? raw.description ?? ""),
        actions: raw.actions || [],
        is_active: raw.is_active ?? true,
      };
    })
    .filter((event) => event.lat !== null && event.lng !== null);
};
