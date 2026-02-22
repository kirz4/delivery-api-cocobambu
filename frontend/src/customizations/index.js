export default function getTheme(mode = "dark") {
  return {
    palette: {
      mode,
      primary: { main: "#d6a23a" },   // dourado
      secondary: { main: "#2b1711" }, // marrom
      background: {
        default: mode === "dark" ? "#0b0b0c" : "#f7f7f7",
        paper: mode === "dark" ? "#121214" : "#ffffff",
      },
    },
    shape: { borderRadius: 12 },
    typography: {
      fontFamily:
        'system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif',
    },
    components: {},
  };
}