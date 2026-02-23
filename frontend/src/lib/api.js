export function getApiBase() {
  const raw = import.meta.env.VITE_API_BASE_URL;
  const base =
    raw && raw !== "VITE_API_BASE_URL" ? raw.replace(/\/$/, "") : "";
  return base; 
}

export function apiUrl(path) {
  const base = getApiBase();
  return base ? `${base}${path}` : path;
}