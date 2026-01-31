import { describe, expect, it } from "vitest";
import { normalizeEvents } from "../normalizeEvents";

describe("normalizeEvents", () => {
  it("normalizes mixed schemas and filters invalid coordinates", () => {
    const rawEvents = [
      {
        id: "a1",
        type: "wildfire",
        confidence: 0.86,
        lat: 34.5,
        lng: -120.2,
        title: "Wildfire near ridge",
        source: "Feed A",
      },
      {
        event_id: "b2",
        event_type: "flooding",
        score: 78.4,
        latitude: "40.7",
        longitude: "-74.0",
        headline: "Flooding reported",
        source: "Feed B",
      },
      {
        id: "c3",
        type: "fire",
        confidence: 0.2,
        latitude: null,
        longitude: 10,
      },
      {
        id: "d4",
        type: "FLOOD",
        score: 150,
        lat: 0,
        lng: 0,
        title: null,
        source: null,
      },
    ];

    const normalized = normalizeEvents(rawEvents);

    expect(normalized).toHaveLength(3);
    expect(normalized[0]).toMatchObject({
      id: "a1",
      type: "Fire",
      confidence: 86,
      title: "Wildfire near ridge",
      source: "Feed A",
    });
    expect(normalized[1]).toMatchObject({
      id: "b2",
      type: "Flood",
      confidence: 78,
      title: "Flooding reported",
      source: "Feed B",
    });
    expect(normalized[2]).toMatchObject({
      id: "d4",
      type: "Flood",
      confidence: 100,
      title: "Untitled event",
      source: "Unknown source",
    });
  });

  it("accepts wrapper objects with events array", () => {
    const wrapped = {
      events: [
        {
          event_id: "x1",
          event_type: "fire",
          score: 0.55,
          latitude: 11,
          longitude: 22,
        },
      ],
    };

    const normalized = normalizeEvents(wrapped);

    expect(normalized).toEqual([
      expect.objectContaining({
        id: "x1",
        type: "Fire",
        confidence: 55,
      }),
    ]);
  });
});
