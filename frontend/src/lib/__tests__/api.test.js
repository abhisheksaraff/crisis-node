import { afterEach, describe, expect, it, vi } from "vitest";
import { getEvents } from "../api";

const makeResponse = (data, { ok = true, status = 200 } = {}) => ({
  ok,
  status,
  json: vi.fn().mockResolvedValue(data),
});

describe("api", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("returns normalized events when API responds with array", async () => {
    const raw = [
      {
        id: "evt-1",
        type: "fire",
        confidence: 0.9,
        lat: 10,
        lng: 20,
      },
    ];
    const fetchMock = vi.fn().mockResolvedValue(makeResponse(raw));
    vi.stubGlobal("fetch", fetchMock);

    const result = await getEvents();

    expect(fetchMock).toHaveBeenCalledOnce();
    expect(result).toEqual([
      expect.objectContaining({
        id: "evt-1",
        type: "Fire",
        confidence: 90,
      }),
    ]);
  });

  it("returns normalized events when API responds with wrapper", async () => {
    const raw = {
      events: [
        {
          event_id: "evt-2",
          event_type: "flood",
          score: 72,
          latitude: 1,
          longitude: 2,
        },
      ],
    };
    const fetchMock = vi.fn().mockResolvedValue(makeResponse(raw));
    vi.stubGlobal("fetch", fetchMock);

    const result = await getEvents();

    expect(result).toEqual([
      expect.objectContaining({
        id: "evt-2",
        type: "Flood",
        confidence: 72,
      }),
    ]);
  });

  it("throws on non-200 responses", async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue(makeResponse({ message: "bad" }, { ok: false, status: 500 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(getEvents()).rejects.toThrow("Events request failed: 500");
  });

  it("throws on network errors", async () => {
    const fetchMock = vi.fn().mockRejectedValue(new Error("network down"));
    vi.stubGlobal("fetch", fetchMock);

    await expect(getEvents()).rejects.toThrow("network down");
  });
});
