import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";


import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

import getTheme from "./customizations";
import DashboardLayout from "./components/dashboard/DashboardLayout.jsx";

import OrdersDashboard from "./pages/OrdersDashboard.jsx";
import OrderDetail from "./pages/OrderDetail.jsx";

const theme = createTheme(getTheme("dark"));

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route element={<DashboardLayout />}>
            <Route path="/" element={<OrdersDashboard />} />
            <Route path="/orders/:orderId" element={<OrderDetail />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  </React.StrictMode>
);