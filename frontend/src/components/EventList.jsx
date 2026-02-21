import { formatTimestamp } from "../lib/time";

export default function EventList({ events, selectedId, onSelect }) {
  if (!events.length) {
    return <div className="event-meta">No events match the filters.</div>;
  }

  return (
    <div className="event-list">
      {events.map((event) => (
        <button
          key={event.id}
          type="button"
          className={`event-item ${
            selectedId === event.id ? "selected" : ""
          }`}
          onClick={() => onSelect(event.id)}
        >
          <h4>{event.title}</h4>
          <div className="event-meta">
            <span>{event.source[0]?.name ?? "Unknown source"}</span>
            <span>{formatTimestamp(event.timestamp)}</span>
          </div>
          <div className="event-meta">
            <span className={`badge ${event.type.toLowerCase()}`}>
              {event.type}
            </span>
          </div>
        </button>
      ))}
    </div>
  );
}
