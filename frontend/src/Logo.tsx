export default function Logo({ size = 26 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" aria-hidden="true">
      <defs>
        <linearGradient id="logo-grad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#d9a44b" />
          <stop offset="1" stopColor="#b4703f" />
        </linearGradient>
      </defs>
      <rect width="64" height="64" rx="14" fill="url(#logo-grad)" />
      <rect x="13" y="32" width="8" height="19" rx="3" fill="#fff8ec" opacity="0.85" />
      <rect x="28" y="20" width="8" height="31" rx="3" fill="#fff8ec" />
      <rect x="43" y="13" width="8" height="38" rx="3" fill="#fff8ec" opacity="0.85" />
    </svg>
  );
}
