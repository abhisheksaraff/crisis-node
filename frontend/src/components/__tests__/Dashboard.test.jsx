import { describe, expect, it, beforeEach, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Dashboard from "../Dashboard";
import mockEvents from "../../lib/mockEvents";
import { getEvents, getPlan } from "../../lib/api";

vi.mock("../MapView", () => ({
  default: () => <div data-testid="map" />,
}));

vi.mock("../../lib/api", () => ({
  getEvents: vi.fn(),
  getPlan: vi.fn(),
}));

const demoEvents = [
  {
    id: "evt-10",
    type: "Fire",
    confidence: 90,
    lat: 10,
    lng: 20,
    title: "Fire A",
    source: "Feed A",
    timestamp: "2026-01-30T10:00:00Z",
    details: "",
  },
  {
    id: "evt-20",
    type: "Flood",
    confidence: 80,
    lat: 30,
    lng: 40,
    title: "Flood B",
    source: "Feed B",
    timestamp: "2026-01-30T11:00:00Z",
    details: "",
  },
  {
    id: "evt-30",
    type: "Fire",
    confidence: 40,
    lat: 50,
    lng: 60,
    title: "Fire C",
    source: "Other Source",
    timestamp: "2026-01-30T12:00:00Z",
    details: "",
  },
];

describe("Dashboard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    getPlan.mockResolvedValue({ summary: "Plan summary" });
  });

  it("shows mock banner and renders events when API fails", async () => {
    getEvents.mockRejectedValueOnce(new Error("API down"));

    render(<Dashboard />);

    expect(await screen.findByText(/Using mock data/i)).toBeInTheDocument();
    expect(screen.getByText(mockEvents[0].title)).toBeInTheDocument();
  });

  it("filters by type, confidence, and search", async () => {
    const user = userEvent.setup();
    getEvents.mockResolvedValueOnce(demoEvents);
    render(<Dashboard />);

    await screen.findByText("Fire A");

    const typeSelect = screen.getByLabelText(/Type filter/i);
    await user.selectOptions(typeSelect, "Flood");
    expect(screen.getByText("Flood B")).toBeInTheDocument();
    expect(screen.queryByText("Fire A")).not.toBeInTheDocument();

    await user.selectOptions(typeSelect, "All");

    const confidenceSlider = screen.getByLabelText(/Minimum confidence/i);
    fireEvent.change(confidenceSlider, { target: { value: "85" } });
    await waitFor(() => {
      expect(screen.getByText("Fire A")).toBeInTheDocument();
      expect(screen.queryByText("Flood B")).not.toBeInTheDocument();
    });

    const searchInput = screen.getByLabelText(/Search/i);
    fireEvent.change(confidenceSlider, { target: { value: "0" } });
    await user.clear(searchInput);
    await user.type(searchInput, "Other");
    expect(screen.getByText("Fire C")).toBeInTheDocument();
    expect(screen.queryByText("Fire A")).not.toBeInTheDocument();
  });

  it("updates details when selecting an event", async () => {
    const user = userEvent.setup();
    getEvents.mockResolvedValueOnce(demoEvents);
    render(<Dashboard />);

    const floodItem = await screen.findByText("Flood B");
    await user.click(floodItem);

    expect(screen.getByRole("heading", { name: "Flood B" })).toBeInTheDocument();
    expect(screen.getByText("80% confidence")).toBeInTheDocument();
    expect(screen.getByText("Flood")).toBeInTheDocument();
  });
});
