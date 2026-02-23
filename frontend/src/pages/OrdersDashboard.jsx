import * as React from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Chip,
  Stack,
  TextField,
  Typography,
  useMediaQuery,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { DataGrid } from "@mui/x-data-grid";

const formatBRL = (value) =>
  new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(Number(value ?? 0));

export default function OrdersDashboard() {
  const navigate = useNavigate();

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  const [rows, setRows] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [search, setSearch] = React.useState("");

  React.useEffect(() => {
    async function fetchOrders() {
      try {
        const API_BASE = import.meta.env.VITE_API_BASE_URL || "";
        const res = await fetch(`${API_BASE}/api/orders/`);
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
    console.log("VITE_API_BASE_URL =", import.meta.env.VITE_API_BASE_URL);
    fetchOrders();
  }, []);

  const filteredRows = rows.filter((row) => {
    const q = search.toLowerCase();
    return (
      row.order_id.toLowerCase().includes(q) ||
      row.store.toLowerCase().includes(q) ||
      row.status.toLowerCase().includes(q)
    );
  });

  const columns = [
    {
      field: "order_id",
      headerName: "Order ID",
      flex: 1,
      minWidth: isMobile ? 220 : 260,
    },
    {
      field: "store",
      headerName: "Loja",
      flex: 1,
      minWidth: 180,
      hide: isMobile, 
    },
    {
      field: "status",
      headerName: "Status",
      width: isMobile ? 120 : 150,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size={isMobile ? "small" : "medium"}
          color={getStatusColor(params.value)}
        />
      ),
    },
    {
      field: "total",
      headerName: "Total",
      width: isMobile ? 110 : 140,
      renderCell: (params) => formatBRL(params.row?.total ?? 0),
    },
    {
      field: "actions",
      headerName: "",
      width: isMobile ? 120 : 150,
      sortable: false,
      renderCell: (params) => (
        <Button
          variant="contained"
          size={isMobile ? "small" : "small"}
          onClick={() => navigate(`/orders/${params.row.order_id}`)}
          fullWidth={isMobile}
        >
          Detalhes
        </Button>
      ),
    },
  ];

  return (
    <Box
      sx={{
        px: { xs: 1, sm: 2 },
        pt: { xs: 1, sm: 2 },
      }}
    >
      <Stack spacing={1.5} mb={2}>
        <Typography variant={isMobile ? "h6" : "h5"} fontWeight={800}>
          Pedidos
        </Typography>

        <TextField
          label="Buscar pedido"
          size="small"
          fullWidth
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Stack>

      <Box
        sx={{
          width: "100%",
          height: { xs: "calc(100vh - 210px)", sm: 600 },
          minHeight: { xs: 420, sm: 600 },
          "& .MuiDataGrid-cell": {
            py: { xs: 0.5, sm: 1 },
          },
        }}
      >
        <DataGrid
          rows={filteredRows}
          columns={columns}
          loading={loading}
          disableRowSelectionOnClick
          pageSizeOptions={isMobile ? [5, 10] : [5, 10, 20]}
          initialState={{
            pagination: { paginationModel: { pageSize: isMobile ? 5 : 10, page: 0 } },
          }}
          sx={{
            borderRadius: 2,
            "& .MuiDataGrid-columnHeaders": {
              fontSize: { xs: 12, sm: 13 },
            },
            "& .MuiDataGrid-cell": {
              fontSize: { xs: 12.5, sm: 13 },
            },
          }}
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