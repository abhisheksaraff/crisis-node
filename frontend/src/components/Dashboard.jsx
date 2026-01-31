import { useEffect, useMemo, useState } from "react";
import Controls from "./Controls";
import EventDetails from "./EventDetails";
import EventList from "./EventList";
import MapView from "./MapView";
import { getEvents } from "../lib/api";
import mockEvents from "../lib/mockEvents";

const DEFAULT_INTERVAL = 5;

export default function Dashboard() {
  const [events, setEvents] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [filters, setFilters] = useState({
    type: "All",
    minConfidence: 0,
    search: "",
  });
  const [usingMock, setUsingMock] = useState(false);
  const [loading, setLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(DEFAULT_INTERVAL);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const data = await getEvents();
      setEvents(data);
      setUsingMock(false);
    } catch (error) {
      setEvents(mockEvents);
      setUsingMock(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  useEffect(() => {
    if (!autoRefresh) return;
    const intervalId = setInterval(fetchEvents, refreshInterval * 1000);
    return () => clearInterval(intervalId);
  }, [autoRefresh, refreshInterval]);

  const sortedEvents = useMemo(() => {
    return [...events].sort((a, b) => b.confidence - a.confidence);
  }, [events]);

  const filteredEvents = useMemo(() => {
    const search = filters.search.trim().toLowerCase();
    return sortedEvents.filter((event) => {
      const matchesType =
        filters.type === "All" || event.type === filters.type;
      const matchesConfidence = event.confidence >= filters.minConfidence;
      const matchesSearch =
        !search ||
        event.title.toLowerCase().includes(search) ||
        event.source.toLowerCase().includes(search);
      return matchesType && matchesConfidence && matchesSearch;
    });
  }, [sortedEvents, filters]);

  useEffect(() => {
    if (!filteredEvents.length) return;
    const stillSelected = filteredEvents.find((event) => event.id === selectedId);
    if (!stillSelected) {
      setSelectedId(filteredEvents[0].id);
    }
  }, [filteredEvents, selectedId]);

  useEffect(() => {
    if (!events.length) return;
    const exists = events.some((event) => event.id === selectedId);
    if (!exists) {
      setSelectedId(sortedEvents[0]?.id ?? null);
    }
  }, [events, selectedId, sortedEvents]);

  const selectedEvent = useMemo(
    () => events.find((event) => event.id === selectedId),
    [events, selectedId]
  );

  const stats = useMemo(() => {
    const fireCount = events.filter((event) => event.type === "Fire").length;
    const floodCount = events.filter((event) => event.type === "Flood").length;
    return { total: events.length, fireCount, floodCount };
  }, [events]);

  return (
    <div className="app">
      <header className="app-header">
        <div>
          <div className="app-title">CrisisNode</div>
          <div className="app-subtitle">
            Verified events and response plans, updated in real time.
          </div>
        </div>
        {usingMock && <div className="banner">Using mock data</div>}
      </header>

      <div className="app-body">
        <aside className="sidebar">
          <div className="panel">
            <div className="panel-title">Overview</div>
            <Controls
              filters={filters}
              onFiltersChange={setFilters}
              stats={stats}
              onRefresh={fetchEvents}
              loading={loading}
              autoRefresh={autoRefresh}
              onToggleAuto={() => setAutoRefresh((prev) => !prev)}
              refreshInterval={refreshInterval}
              onIntervalChange={setRefreshInterval}
            />
          </div>
          <div className="panel list-panel">
            <div className="panel-title">Verified Events</div>
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
            <EventDetails event={selectedEvent} />
          </section>
        </main>
      </div>
    </div>
  );
}
