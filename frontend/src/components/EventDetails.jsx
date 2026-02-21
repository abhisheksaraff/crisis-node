import { useEffect, useState } from "react";
import { formatTimestamp } from "../lib/time";

export default function EventDetails({ event, onUpdateEvent }) {
  const [localActions, setLocalActions] = useState([]);
  const [localActive, setLocalActive] = useState(true);

  useEffect(() => {
    if (event) {
      setLocalActions(event.actions || []);
      setLocalActive(event.is_active);
    }
  }, [event?.id]);

  if (!event) return <div className="panel-title">Select an event</div>;

  // COMPARISON LOGIC: Check if current local state differs from the original prop
  const actionsChanged = JSON.stringify(localActions) !== JSON.stringify(event.actions || []);
  const statusChanged = localActive !== event.is_active;
  const hasChanges = actionsChanged || statusChanged;

  const isLocked = event.is_active === false;

  const handleToggleLocalAction = (index) => {
    const updated = localActions.map((a, i) =>
      i === index ? { ...a, done: !a.done } : a,
    );
    setLocalActions(updated);
  };

  const handleToggleActive = () => {
    setLocalActive(!localActive);
  };

  const handlePushUpdates = () => {
    onUpdateEvent(event.id, {
      actions: localActions,
      is_active: localActive,
    });
  };

  return (
    <div className="event-details">
      <div className="panel-title">
        Event Details{" "}
        {isLocked && <span className="status-locked">(LOCKED/RESOLVED)</span>}
      </div>
      <h3>{event.title}</h3>

      <div className="details-grid">
        <div className="detail-card">
          <div>
            <strong>Type</strong> {event.type}
          </div>
          <div>
            <strong>Location</strong> {event.name}
          </div>
        </div>
        <div className="detail-card">
          <strong>Source</strong>
          <div>
            <a
              href={event.source[0]?.url}
              target="_blank"
              rel="noopener noreferrer"
              className="source-link"
            >
              {event.source[0]?.name || "View Source"}
            </a>
          </div>
        </div>
        <div className="detail-card">
          <strong>Time</strong> {formatTimestamp(event.timestamp)}
        </div>
      </div>

      <div style={{ marginTop: "10px" }}>{event.details || "No Details Found"}</div>
      <br />

      <div className="plan-section">
        <div className="plan-header">
          <strong>Response Plan</strong>
          {hasChanges && <span className="unsaved-tag">Unsaved Changes</span>}
        </div>

        <ul className="plan-list" style={{ listStyle: "none", padding: 0 }}>
          {/* 1. Crisis Status Toggle */}
          <li
            className="action-item"
            style={{
              marginBottom: "20px",
              paddingBottom: "10px",
              borderBottom: "1px solid #eee",
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              {isLocked ? (
                <span style={{ color: "#f44336", fontWeight: "bold" }}>
                  [inactive]
                </span>
              ) : (
                <input
                  type="checkbox"
                  checked={!localActive}
                  onChange={handleToggleActive}
                  style={{ width: "18px", height: "18px", cursor: "pointer" }}
                />
              )}
              <strong style={{ color: localActive ? "#000" : "#666" }}>
                {localActive ? "Crisis is Active" : "Mark as Resolved"}
              </strong>
            </div>
            <div
              style={{
                marginLeft: "28px",
                fontSize: "0.7rem",
                fontWeight: "bold",
              }}
            >
              {isLocked ? (
                <span style={{ color: "#f44336" }}>PERMANENTLY RESOLVED</span>
              ) : localActive !== event.is_active ? (
                <span style={{ color: "#2196F3" }}>
                  ● STATUS CHANGE PENDING
                </span>
              ) : (
                <span style={{ color: "#9e9e9e" }}>CURRENT STATUS</span>
              )}
            </div>
          </li>

          {/* 2. Action Items */}
          {localActions.map((action, index) => {
            const isPermanentlyDone = event.actions?.[index]?.done;
            const isDraftChange = action.done !== !!isPermanentlyDone;

            return (
              <li
                key={index}
                className="action-item"
                style={{ marginBottom: "15px" }}
              >
                <div
                  style={{ display: "flex", alignItems: "center", gap: "10px" }}
                >
                  <input
                    type="checkbox"
                    checked={action.done}
                    disabled={isPermanentlyDone}
                    onChange={() => handleToggleLocalAction(index)}
                    style={{
                      width: "18px",
                      height: "18px",
                      cursor: isPermanentlyDone ? "not-allowed" : "pointer",
                    }}
                  />
                  <span
                    style={{
                      textDecoration: action.done ? "line-through" : "none",
                    }}
                  >
                    {action.task}
                  </span>
                </div>
                <div
                  style={{
                    marginLeft: "28px",
                    fontSize: "0.7rem",
                    fontWeight: "bold",
                  }}
                >
                  {isPermanentlyDone ? (
                    <span style={{ color: "#4CAF50" }}>✓ COMPLETED</span>
                  ) : isDraftChange ? (
                    <span style={{ color: "#2196F3" }}>● UNPUSHED CHANGE</span>
                  ) : (
                    <span style={{ color: "#9e9e9e" }}>AWAITING DEPLOYMENT</span>
                  )}
                </div>
              </li>
            );
          })}
        </ul>

        {/* BUTTON FOOTER */}
        <div
          style={{
            marginTop: "30px",
            borderTop: "1px solid #eee",
            paddingTop: "20px",
          }}
        >
          <button
            className="btn-primary"
            disabled={!hasChanges}
            onClick={handlePushUpdates}
            style={{
              padding: "12px 24px",
              fontSize: "0.9rem",
              fontWeight: "600",
              cursor: hasChanges ? "pointer" : "not-allowed",
              backgroundColor: hasChanges ? "#2196F3" : "#ccc",
              color: "white",
              border: "none",
              borderRadius: "4px",
              minWidth: "160px",
              transition: "all 0.2s ease",
            }}
          >
            Push Updates
          </button>
        </div>
      </div>
    </div>
  );
}