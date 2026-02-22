import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import OrderDetail from "../OrderDetail.jsx";

describe("OrderDetail", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("carrega e exibe detalhes do pedido", async () => {
    global.fetch = vi.fn(async (url) => {
      if (String(url).includes("/allowed-statuses/")) {
        return { ok: true, json: async () => ({ allowed: ["DISPATCHED"] }) };
      }
      return {
        ok: true,
        json: async () => ({
          order_id: "order-1",
          order: {
            last_status_name: "CONFIRMED",
            total_price: 89.9,
            created_at: 1770842000000,
            store: { name: "Coco Bambu", id: "store-1" },
            customer: { name: "Ana", temporary_phone: "+55..." },
            delivery_address: { street_name: "Rua X", street_number: "10" },
            items: [],
            payments: [],
            statuses: [],
          },
        }),
      };
    });

    render(
      <MemoryRouter
        initialEntries={["/orders/order-1"]}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <Routes>
          <Route path="/orders/:orderId" element={<OrderDetail />} />
        </Routes>
      </MemoryRouter>
    );

    // findBy* já espera automaticamente o render assíncrono
    expect(await screen.findByText(/Pedido order-1/i)).toBeInTheDocument();
    expect(await screen.findByText("CONFIRMED")).toBeInTheDocument();
    expect(await screen.findByText(/R\$\s*89,90/)).toBeInTheDocument();
    expect(await screen.findByText("Coco Bambu")).toBeInTheDocument();
    expect(await screen.findByText("Ana")).toBeInTheDocument();
  });
});