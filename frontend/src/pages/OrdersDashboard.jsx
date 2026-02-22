import * as React from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Chip,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
const formatBRL = (value) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(value ?? 0));
export default function OrdersDashboard() {
  const navigate = useNavigate();
  const [rows, setRows] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [search, setSearch] = React.useState("");

  React.useEffect(() => {
    async function fetchOrders() {
      try {
        const res = await fetch("/api/orders/");
        const data = await res.json();

        const mapped = (Array.isArray(data) ? data : []).map((o) => ({
          id: o?.order_id ?? crypto.randomUUID(),
          order_id: o?.order_id ?? "-",
          store: o?.order?.store?.name ?? "-",
          status: o?.order?.last_status_name ?? "-",
          total: Number(o?.order?.total_price ?? 0),
        }));

        setRows(mapped);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchOrders();
  }, []);

  const filteredRows = rows.filter((row) =>
    row.order_id.toLowerCase().includes(search.toLowerCase()) ||
    row.store.toLowerCase().includes(search.toLowerCase()) ||
    row.status.toLowerCase().includes(search.toLowerCase())
  );

  const columns = [
    { field: "order_id", headerName: "Order ID", flex: 1, minWidth: 260 },
    { field: "store", headerName: "Loja", flex: 1 },
    {
      field: "status",
      headerName: "Status",
      width: 150,
      renderCell: (params) => (
        <Chip label={params.value} color={getStatusColor(params.value)} />
      ),
    },
    {
      field: "total",
      headerName: "Total",
      width: 140,
      renderCell: (params) => formatBRL(params.row?.total ?? 0),
    },
    {
      field: "actions",
      headerName: "",
      width: 150,
      sortable: false,
      renderCell: (params) => (
        <Button
          variant="contained"
          size="small"
          onClick={() => navigate(`/orders/${params.row.order_id}`)}
        >
          Detalhes
        </Button>
      ),
    },
  ];

  return (
    <Box>
      <Stack spacing={2} mb={2} ml={1} mt={1}>
        <Typography variant="h5" fontWeight={800}>
          Pedidos
        </Typography>

        <TextField
          label="Buscar pedido"
          size="small"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Stack>

      <Box sx={{ height: 600 }}>
        <DataGrid
          rows={filteredRows}
          columns={columns}
          loading={loading}
          pageSizeOptions={[5, 10, 20]}
          initialState={{
            pagination: { paginationModel: { pageSize: 10, page: 0 } },
          }}
          disableRowSelectionOnClick
        />
      </Box>
    </Box>
  );
}

function getStatusColor(status) {
  switch (status) {
    case "RECEIVED":
      return "default";
    case "CONFIRMED":
      return "info";
    case "DISPATCHED":
      return "warning";
    case "DELIVERED":
      return "success";
    case "CANCELED":
      return "error";
    default:
      return "default";
  }
}