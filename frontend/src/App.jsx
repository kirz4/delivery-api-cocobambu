import { Routes, Route, Link } from "react-router-dom";
import OrdersList from "./pages/OrdersList.jsx";
import OrderDetail from "./pages/OrderDetail.jsx";

export default function App() {
  return (
    <div style={{ fontFamily: "system-ui", padding: 16, maxWidth: 1100, margin: "0 auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <Link to="/" style={{ textDecoration: "none", color: "black" }}>
          <h2 style={{ margin: 0 }}>Delivery App</h2>
          <div style={{ color: "#666", fontSize: 12 }}>Coco Bambu — UI</div>
        </Link>
        <a href="/api/orders/" target="_blank" rel="noreferrer" style={{ fontSize: 12 }}>
          Ver API JSON
        </a>
      </header>

      <Routes>
        <Route path="/" element={<OrdersList />} />
        <Route path="/orders/:orderId" element={<OrderDetail />} />
      </Routes>
    </div>
  );
}