import { describe, expect, it, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import EventDetails from "../EventDetails";
import { getPlan } from "../../lib/api";

vi.mock("../../lib/api", () => ({
  getPlan: vi.fn(),
}));

const baseEvent = {
  id: "evt-100",
  type: "Fire",
  confidence: 92,
  lat: 34.0522,
  lng: -118.2437,
  title: "Wildfire near canyon",
  source: "Feed A",
  timestamp: "2026-01-30T18:45:00Z",
  details: "",
};

describe("EventDetails", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders placeholder when no event selected", () => {
    render(<EventDetails event={null} />);

    expect(screen.getByText("Event Details")).toBeInTheDocument();
    expect(
      screen.getByText(/Select an event to see its response plan/i)
    ).toBeInTheDocument();
  });

  it("renders event details and a structured plan object", async () => {
    getPlan.mockResolvedValueOnce({
      summary: "Contain the fire and protect nearby settlements.",
      actions: ["Deploy aerial units", "Set evacuation zones"],
      resources: [
        { item: "Food Packs", qty: 500 },
        { item: "Water Tankers", qty: 12 },
      ],
      risks: ["Wind shift", "Limited visibility"],
      confidence: 88,
    });

    render(<EventDetails event={baseEvent} />);

    expect(await screen.findByText(baseEvent.title)).toBeInTheDocument();
    expect(screen.getByText(`${baseEvent.confidence}% confidence`)).toBeInTheDocument();
    expect(screen.getByText(baseEvent.type)).toBeInTheDocument();
    expect(screen.getByText("Lat 34.052")).toBeInTheDocument();
    expect(screen.getByText("Lng -118.244")).toBeInTheDocument();
    expect(screen.getByText("No additional notes.")).toBeInTheDocument();

    expect(
      screen.getByText("Contain the fire and protect nearby settlements.")
    ).toBeInTheDocument();
    expect(screen.getByText("Deploy aerial units")).toBeInTheDocument();
    expect(screen.getByText("Set evacuation zones")).toBeInTheDocument();
    expect(screen.getByText("Food Packs")).toBeInTheDocument();
    expect(screen.getByText("500")).toBeInTheDocument();
    expect(screen.getByText("Water Tankers")).toBeInTheDocument();
    expect(screen.getByText("12")).toBeInTheDocument();
    expect(screen.getByText("Wind shift")).toBeInTheDocument();
    expect(screen.getByText("Limited visibility")).toBeInTheDocument();
    expect(screen.getByText("Plan confidence:")).toBeInTheDocument();
    expect(screen.getByText("88%")).toBeInTheDocument();
    expect(getPlan).toHaveBeenCalledWith(baseEvent.id);
  });

  it("renders a plain text plan response", async () => {
    getPlan.mockResolvedValueOnce("Plain text plan response.");

    render(<EventDetails event={baseEvent} />);

    expect(await screen.findByText("Plain text plan response.")).toBeInTheDocument();
    expect(screen.queryByText(/Plan unavailable/i)).not.toBeInTheDocument();
  });

  it("shows plan unavailable when plan request fails", async () => {
    getPlan.mockRejectedValueOnce(new Error("Plan unavailable"));

    render(<EventDetails event={baseEvent} />);

    expect(await screen.findByText(/Plan unavailable/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Prioritize life safety/i)
    ).toBeInTheDocument();
  });
});
