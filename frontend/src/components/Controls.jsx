export default function Controls({
  filters,
  onFiltersChange,
  stats,
  onRefresh,
  loading,
  autoRefresh,
  onToggleAuto,
  refreshInterval,
  onIntervalChange,
}) {
  return (
    <div className="controls">
      <div className="stat-grid">
        <div className="stat">
          <strong>{stats.total}</strong>
          Total
        </div>
        <div className="stat">
          <strong>{stats.fireCount}</strong>
          Fires
        </div>
        <div className="stat">
          <strong>{stats.floodCount}</strong>
          Floods
        </div>
      </div>

      <div className="control-row">
        <label htmlFor="type-filter">Type filter</label>
        <select
          id="type-filter"
          value={filters.type}
          onChange={(event) =>
            onFiltersChange({ ...filters, type: event.target.value })
          }
        >
          <option value="All">All</option>
          <option value="Fire">Fire</option>
          <option value="Flood">Flood</option>
        </select>
      </div>

      <div className="control-row">
        <label htmlFor="confidence-filter">
          Minimum confidence: {filters.minConfidence}%
        </label>
        <input
          id="confidence-filter"
          type="range"
          min="0"
          max="100"
          value={filters.minConfidence}
          onChange={(event) =>
            onFiltersChange({
              ...filters,
              minConfidence: Number(event.target.value),
            })
          }
        />
      </div>

      <div className="control-row">
        <label htmlFor="search-filter">Search</label>
        <input
          id="search-filter"
          type="text"
          placeholder="Title or source"
          value={filters.search}
          onChange={(event) =>
            onFiltersChange({ ...filters, search: event.target.value })
          }
        />
      </div>

      <div className="actions-row">
        <button className="button" onClick={onRefresh} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh"}
        </button>
        <button
          className="button secondary"
          type="button"
          onClick={() =>
            onFiltersChange({ type: "All", minConfidence: 0, search: "" })
          }
        >
          Clear
        </button>
      </div>

      <div className="control-row">
        <label>Auto-refresh</label>
        <div className="actions-row">
          <label className="toggle">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={onToggleAuto}
            />
            Enabled
          </label>
          <select
            value={refreshInterval}
            onChange={(event) => onIntervalChange(Number(event.target.value))}
          >
            {[5, 10, 15, 20, 30].map((seconds) => (
              <option key={seconds} value={seconds}>
                Every {seconds}s
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
