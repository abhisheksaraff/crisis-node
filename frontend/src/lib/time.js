const formatAbsolute = (date) =>
  new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);

// export const formatTimestamp = (value) => {
//   if (!value) return "Unknown time";
//   const date = new Date(value);
//   if (Number.isNaN(date.getTime())) return "Unknown time";

//   const now = Date.now();
//   const diffMs = now - date.getTime();
//   if (diffMs <= 0) return "just now";

//   const seconds = Math.floor(diffMs / 1000);
//   if (seconds < 10) return "just now";
//   if (seconds < 60) return `${seconds}s ago`;

//   const minutes = Math.floor(seconds / 60);
//   if (minutes < 60) return `${minutes}m ago`;

//   const hours = Math.floor(minutes / 60);
//   if (hours < 24) return `${hours}h ago`;

//   const days = Math.floor(hours / 24);
//   if (days < 7) return `${days}d ago`;

//   return formatAbsolute(date);
// };

export const formatTimestamp = (isoString) => {
  if (!isoString) return "Unknown time";
  
  const date = new Date(String(isoString).replace(" ", "T"));
  
  if (isNaN(date.getTime())) return "Unknown time";

  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};