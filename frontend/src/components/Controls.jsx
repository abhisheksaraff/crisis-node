export default function Controls({
  filters,
  onFiltersChange,
  stats,
  types,
  onRefresh,
  loading,
  autoRefresh,
  onToggleAuto,
  refreshInterval,
  onIntervalChange,
}) {
  return (
    <div className="controls">
      {/* Dynamic Stat Grid */}
      <div className="stat-grid">
        <div className="stat">
          <strong>{stats.total}</strong>
          Total
        </div>
        {/* Map through dynamic type counts if provided in stats */}
        {Object.entries(stats.counts || {}).map(([type, count]) => (
          <div className="stat" key={type}>
            <strong>{count}</strong>
            {type}s
          </div>
        ))}
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
          {/* Map through the dynamic types array */}
          {types.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="control-row">
        <label htmlFor="search-filter">Search</label>
        <input
          id="search-filter"
          type="text"
          placeholder="Title, source, or location"
          value={filters.search}
          onChange={(event) =>
            onFiltersChange({ ...filters, search: event.target.value })
          }
        />
      </div>

      {/* <div className="actions-row">
        <button className="button" onClick={onRefresh} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh"}
        </button>
        <button
          className="button secondary"
          type="button"
          onClick={() =>
            onFiltersChange({ type: "All", search: "" })
          }
        >
          Clear
        </button>
      </div> */}

      {/* <div className="control-row">
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
      </div> */}
    </div>
  );
}