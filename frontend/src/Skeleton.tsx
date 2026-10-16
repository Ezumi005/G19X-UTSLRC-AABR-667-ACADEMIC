export function SkeletonCards({ n = 4, alto = 74 }: { n?: number; alto?: number }) {
  return (
    <div className="cards">
      {Array.from({ length: n }, (_, i) => (
        <div key={i} className="card skeleton-card" style={{ minHeight: alto }} />
      ))}
    </div>
  );
}

export function SkeletonRows({ n = 5, columnas = 5 }: { n?: number; columnas?: number }) {
  return (
    <table className="table">
      <thead>
        <tr>
          {Array.from({ length: columnas }, (_, i) => (
            <th key={i}>
              <span className="skeleton skeleton-line" style={{ width: "70%" }} />
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {Array.from({ length: n }, (_, i) => (
          <tr key={i}>
            {Array.from({ length: columnas }, (_, j) => (
              <td key={j}>
                <span className="skeleton skeleton-line" style={{ width: j === 0 ? "80%" : "55%" }} />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export function SkeletonBlocks({ n = 4, alto = 290 }: { n?: number; alto?: number }) {
  return (
    <div className="chart-grid">
      {Array.from({ length: n }, (_, i) => (
        <div key={i} className="chart-card" style={{ minHeight: alto }} />
      ))}
    </div>
  );
}
