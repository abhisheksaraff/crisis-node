
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

// const normalizeType = (value) => {
//   const raw = String(value || "").toLowerCase();
//   if (raw.includes("flood")) return "Flood";
//   if (raw.includes("fire") || raw.includes("wildfire")) return "Fire";
//   return "Fire";
// };

// export const normalizeEvents = (input) => {
//   const list = Array.isArray(input)
//     ? input
//     : Array.isArray(input?.events)
//     ? input.events
//     : [];

//   return list
//     .map((raw, index) => {
//       const lat = toNumber(raw.lat ?? raw.latitude);
//       const lng = toNumber(raw.lng ?? raw.lon ?? raw.longitude);

//       const rawDate = raw.timestamp ?? raw.time_stamp ?? raw.time ?? raw.datetime;
//       const standardizedDate = rawDate 
//         ? new Date(String(rawDate).replace(" ", "T")).toISOString() 
//         : new Date().toISOString();

//       const sourceName = Array.isArray(raw.source)
//         ? (raw.source[0]?.name ?? raw.source[0]?.outlet)
//         : (raw.source ?? raw.source_name);

//       return {
//         id: String(raw.id ?? raw.event_id ?? raw.eventId ?? `evt-${index + 1}`),
//         type: normalizeType(raw.type ?? raw.event_type ?? raw.eventType),
//         lat,
//         lng,
//         title: String(raw.title ?? raw.headline ?? raw.name ?? "Untitled event"),
//         source: String(sourceName ?? "Unknown source"),
//         timestamp: standardizedDate,
//         details: String(raw.details ?? raw.description ?? raw.summary ?? ""),
//       };
//     })
//     .filter((event) => Number.isFinite(event.lat) && Number.isFinite(event.lng));
// };
