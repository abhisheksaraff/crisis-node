export default function Controls({ filters, onFiltersChange, stats, types }) {
  return (
    <div className="controls">
      <div className="stat-grid">
        <div className="stat">
          <strong>{stats.total}</strong>
          Total
        </div>
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
    </div>
  );
}
