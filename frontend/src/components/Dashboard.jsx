import { useEffect, useMemo, useState } from "react";
import Controls from "./Controls";
import EventDetails from "./EventDetails";
import EventList from "./EventList";
import MapView from "./MapView";
import {
  checkHealth,
  getEvents,
  updateTaskStatus,
  resolveAlert,
} from "../lib/api";
import mockEvents from "../lib/mockEvents";

const DEFAULT_INTERVAL = 5;

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [filters, setFilters] = useState({
    type: "All",
    search: "",
  });
  const [usingMock, setUsingMock] = useState(false);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(DEFAULT_INTERVAL);
  
  const fetchEvents = async () => {
    setLoading(true);
    try {
      // 1. Verify connection first
      const isHealthy = await checkHealth();

      if (!isHealthy) {
        // If health check fails, throw to the catch block immediately
        throw new Error("Backend unreachable");
      }

      // 2. Fetch live data
      const data = await getEvents();
      setEvents(data);
      setUsingMock(false);
    } catch (error) {
      // 3. Fallback to mock data on any failure
      console.warn("Switching to offline mode:", error.message);
      setEvents(mockEvents);
      setUsingMock(true);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateEvent = async (eventId, updatedData) => {
    if (usingMock) {
      setEvents((prev) =>
        prev.map((ev) => (ev.id === eventId ? { ...ev, ...updatedData } : ev)),
      );
      console.log("Mock data updated locally.");
      return;
    }

    try {
      const originalEvent = events.find((e) => e.id === eventId);

      const taskPromises = updatedData.actions
        .map((action, index) => {
          if (action.done !== originalEvent.actions[index]?.done) {
            return updateTaskStatus(eventId, index, action.done);
          }
          return null;
        })
        .filter(Boolean);

      if (originalEvent.is_active && !updatedData.is_active) {
        taskPromises.push(resolveAlert(eventId));
      }

      await Promise.all(taskPromises);

      await fetchEvents();
    } catch (error) {
      console.error("Sync failed:", error);
    }
  };

  const uniqueTypes = useMemo(() => {
    const types = events.map((event) => event.type);
    return ["All", ...new Set(types)].sort();
  }, [events]);

  useEffect(() => {
    fetchEvents();
  }, []);

  useEffect(() => {
    if (!autoRefresh) return;
    const intervalId = setInterval(fetchEvents, refreshInterval * 1000);
    return () => clearInterval(intervalId);
  }, [autoRefresh, refreshInterval]);

  const sortedEvents = useMemo(() => [...events], [events]);

  const filteredEvents = useMemo(() => {
    const search = filters.search.trim().toLowerCase();
    return sortedEvents.filter((event) => {
      const matchesType = filters.type === "All" || event.type === filters.type;

      // Check title
      const matchesTitle = event.title.toLowerCase().includes(search);

      // Check ALL source names in the array
      const matchesAnySource = event.source?.some((src) =>
        src.name?.toLowerCase().includes(search),
      );

      // Check location name if applicable
      const matchesLocation = event.name?.toLowerCase().includes(search);

      return (
        matchesType && (matchesTitle || matchesAnySource || matchesLocation)
      );
    });
  }, [sortedEvents, filters]);

  useEffect(() => {
    if (!filteredEvents.length) return;
    const stillSelected = filteredEvents.find((e) => e.id === selectedId);
    if (!stillSelected) setSelectedId(filteredEvents[0].id);
  }, [filteredEvents, selectedId]);

  const selectedEvent = useMemo(
    () => events.find((event) => event.id === selectedId),
    [events, selectedId],
  );

  const stats = useMemo(() => {
    const fireCount = events.filter((e) => e.type === "Fire").length;
    const floodCount = events.filter((e) => e.type === "Flood").length;
    return { total: events.length, fireCount, floodCount };
  }, [events]);

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="app-title">CrisisNode</div>
          <div className="app-subtitle">
            Verified events updated in real time.
          </div>
        </div>
        {/* Status Indicators */}
        <div style={{ display: "flex", gap: "10px" }}>
          {usingMock ? (
            <div
              className="banner mock-mode"
              style={{
                backgroundColor: "#cf9236",
                color: "white",
                padding: "4px 12px",
                borderRadius: "4px",
                fontSize: "0.8rem",
                fontWeight: "bold",
              }}
            >
              USING MOCK DATA
            </div>
          ) : (
            <div
              className="banner live-mode"
              style={{
                backgroundColor: "#4CAF50",
                color: "white",
                padding: "4px 12px",
                borderRadius: "4px",
                fontSize: "0.8rem",
                fontWeight: "bold",
              }}
            >
              ● SYSTEM LIVE
            </div>
          )}
        </div>
      </header>

      <div className="app-body">
        <aside className="sidebar">
          <div className="panel">
            <div className="panel-title">Overview</div>
            <Controls
              filters={filters}
              onFiltersChange={setFilters}
              stats={stats}
              types={uniqueTypes}
              onRefresh={fetchEvents}
              loading={loading}
              autoRefresh={autoRefresh}
              onToggleAuto={() => setAutoRefresh((p) => !p)}
              refreshInterval={refreshInterval}
              onIntervalChange={setRefreshInterval}
            />
          </div>
          <div className="panel list-panel">
            <div className="panel-title">Events</div>
            <EventList
              events={filteredEvents}
              selectedId={selectedId}
              onSelect={setSelectedId}
            />
          </div>
        </aside>

        <main className="main">
          <section className="panel map-panel">
            <MapView
              events={filteredEvents}
              selectedEvent={selectedEvent}
              onSelect={setSelectedId}
            />
          </section>
          <section className="panel details-panel">
            <EventDetails
              event={selectedEvent}
              onUpdateEvent={handleUpdateEvent}
            />
          </section>
        </main>
      </div>
    </div>
  );
}
