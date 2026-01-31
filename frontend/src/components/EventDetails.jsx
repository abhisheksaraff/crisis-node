import { useEffect, useRef, useState } from "react";
import { getPlan } from "../lib/api";
import { formatTimestamp } from "../lib/time";

const fallbackPlanText =
  "Plan unavailable. Prioritize life safety, verify evacuation routes, and coordinate local response teams while awaiting a full UN-style assessment.";

const buildPlanState = (status, data, isFallback = false) => ({
  status,
  data,
  isFallback,
});

export default function EventDetails({ event }) {
  const [planState, setPlanState] = useState(buildPlanState("idle", null));
  const planCache = useRef({});

  useEffect(() => {
    if (!event) return;
    const cached = planCache.current[event.id];
    if (cached) {
      setPlanState(cached);
      return;
    }

    setPlanState(buildPlanState("loading", null));

    getPlan(event.id)
      .then((data) => {
        const next = buildPlanState("ready", data);
        setPlanState(next);
        planCache.current[event.id] = next;
      })
      .catch(() => {
        const next = buildPlanState("unavailable", fallbackPlanText, true);
        setPlanState(next);
        planCache.current[event.id] = next;
      });
  }, [event?.id]);

  if (!event) {
    return (
      <div>
        <div className="panel-title">Event Details</div>
        <div className="event-meta">Select an event to see its response plan.</div>
      </div>
    );
  }

  const plan = planState.data;
  const isPlanObject = plan && typeof plan === "object" && !Array.isArray(plan);

  return (
    <div>
      <div className="panel-title">Event Details</div>
      <h3>{event.title}</h3>
      <div className="details-grid">
        <div className="detail-card">
          <strong>{event.type}</strong>
          <div>{event.confidence}% confidence</div>
        </div>
        <div className="detail-card">
          <div>{event.source}</div>
          <div>{formatTimestamp(event.timestamp)}</div>
        </div>
        <div className="detail-card">
          <div>Lat {event.lat.toFixed(3)}</div>
          <div>Lng {event.lng.toFixed(3)}</div>
        </div>
        <div className="detail-card">
          <div>ID {event.id}</div>
          <div>{event.details || "No additional notes."}</div>
        </div>
      </div>

      <div className="plan-section">
        <div className="plan-title">Response Plan</div>
        {planState.status === "loading" && <div>Loading plan...</div>}
        {planState.isFallback && (
          <div className="plan-unavailable">Plan unavailable</div>
        )}

        {planState.status !== "loading" && (
          <>
            {isPlanObject ? (
              <>
                {plan.summary && <p>{plan.summary}</p>}
                {Array.isArray(plan.actions) && plan.actions.length > 0 && (
                  <div>
                    <strong>Actions</strong>
                    <ul className="plan-list">
                      {plan.actions.map((action, index) => (
                        <li key={`${action}-${index}`}>{action}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {Array.isArray(plan.resources) && plan.resources.length > 0 && (
                  <div>
                    <strong>Resources</strong>
                    <div className="plan-resources">
                      {plan.resources.map((resource, index) => (
                        <div className="plan-resource" key={`${resource.item}-${index}`}>
                          <span>{resource.item}</span>
                          <span>{resource.qty}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {Array.isArray(plan.risks) && plan.risks.length > 0 && (
                  <div>
                    <strong>Risks</strong>
                    <ul className="plan-list">
                      {plan.risks.map((risk, index) => (
                        <li key={`${risk}-${index}`}>{risk}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {Number.isFinite(plan.confidence) && (
                  <div>
                    <strong>Plan confidence:</strong> {plan.confidence}%
                  </div>
                )}
              </>
            ) : (
              <p>{plan || fallbackPlanText}</p>
            )}
          </>
        )}
      </div>
    </div>
  );
}
