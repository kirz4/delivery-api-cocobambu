import React from "react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import OrdersDashboard from "../OrdersDashboard.jsx";

function mockFetchOnce(data) {
  global.fetch = vi.fn(async () => ({
    ok: true,
    json: async () => data,
  }));
}

describe("OrdersDashboard", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renderiza e lista pedidos vindos da API", async () => {
    mockFetchOnce([
      {
        order_id: "order-1",
        order: {
          store: { name: "Coco Bambu" },
          last_status_name: "CONFIRMED",
          total_price: 89.9,
        },
      },
    ]);

    render(
      <MemoryRouter
        initialEntries={["/"]}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      >
        <OrdersDashboard />
      </MemoryRouter>
    );

    expect(screen.getByText(/Pedidos/i)).toBeInTheDocument();

    expect(await screen.findByText("order-1")).toBeInTheDocument();
    expect(await screen.findByText("Coco Bambu")).toBeInTheDocument();
    expect(await screen.findByText("CONFIRMED")).toBeInTheDocument();
    expect(await screen.findByText(/R\$\s*89,90/)).toBeInTheDocument();
  });
});