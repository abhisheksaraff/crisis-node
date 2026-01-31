import { useEffect } from "react";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import { formatTimestamp } from "../lib/time";

const createMarkerIcon = (type, isSelected) => {
  const typeClass = type.toLowerCase();
  const pulseClass = isSelected ? "pulse" : "";
  return L.divIcon({
    className: "event-marker-wrapper",
    html: `<span class="event-marker ${typeClass} ${pulseClass}"></span>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
    popupAnchor: [0, -12],
  });
};

const MapFocus = ({ event }) => {
  const map = useMap();

  useEffect(() => {
    if (!event) return;
    map.flyTo([event.lat, event.lng], 6, {
      duration: 1.2,
    });
  }, [event, map]);

  return null;
};

export default function MapView({ events, selectedEvent, onSelect }) {
  const fallbackCenter = [20, 0];
  const center = selectedEvent ? [selectedEvent.lat, selectedEvent.lng] : fallbackCenter;
  const zoom = selectedEvent ? 6 : 2;

  return (
    <MapContainer center={center} zoom={zoom} scrollWheelZoom className="map-container">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {events.map((event) => (
        <Marker
          key={event.id}
          position={[event.lat, event.lng]}
          icon={createMarkerIcon(event.type, selectedEvent?.id === event.id)}
          eventHandlers={{
            click: () => onSelect(event.id),
          }}
        >
          <Popup>
            <strong>{event.title}</strong>
            <div>{event.source}</div>
            <div>{formatTimestamp(event.timestamp)}</div>
            <div>
              {event.type} • {event.confidence}% confidence
            </div>
          </Popup>
        </Marker>
      ))}

      <MapFocus event={selectedEvent} />
    </MapContainer>
  );
}
