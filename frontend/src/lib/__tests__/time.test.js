import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { formatTimestamp } from "../time";

describe("formatTimestamp", () => {
  const baseTime = new Date("2026-01-31T00:00:00Z");

  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(baseTime);
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("returns just now for very recent times", () => {
    const value = new Date(baseTime.getTime() - 5000).toISOString();
    expect(formatTimestamp(value)).toBe("just now");
  });

  it("returns seconds ago for short deltas", () => {
    const value = new Date(baseTime.getTime() - 10000).toISOString();
    expect(formatTimestamp(value)).toBe("10s ago");
  });

  it("returns minutes ago for minute deltas", () => {
    const value = new Date(baseTime.getTime() - 3 * 60 * 1000).toISOString();
    expect(formatTimestamp(value)).toBe("3m ago");
  });

  it("returns Unknown time for invalid values", () => {
    expect(formatTimestamp("not-a-date")).toBe("Unknown time");
  });
});
