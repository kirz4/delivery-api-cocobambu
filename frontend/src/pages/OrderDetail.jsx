import * as React from "react";
import { useParams } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Typography,
} from "@mui/material";
import { apiUrl } from "../lib/api"; // ajuste o caminho se necessário

const formatBRL = (value) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(
    Number(value ?? 0)
  );

const formatDateTime = (ms) => {
  if (!ms || Number.isNaN(Number(ms))) return "-";
  return new Date(Number(ms)).toLocaleString("pt-BR");
};

function statusColor(status) {
  switch ((status || "").toUpperCase()) {
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

// evita crash quando a resposta é HTML/404
async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    return { _raw: text };
  }
}

export default function OrderDetail() {
  const { orderId } = useParams();

  const [order, setOrder] = React.useState(null);
  const [allowedNext, setAllowedNext] = React.useState([]);

  const [loading, setLoading] = React.useState(true);
  const [nextStatus, setNextStatus] = React.useState("");
  const [origin, setOrigin] = React.useState("STORE");

  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState("");
  const [success, setSuccess] = React.useState("");

  const fetchOrder = React.useCallback(async () => {
    if (!orderId) {
      setOrder(null);
      setAllowedNext([]);
      setNextStatus("");
      setError("Order ID inválido.");
      setLoading(false);
      return;
    }

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const orderUrl = apiUrl(`/api/orders/${orderId}/`);
      const allowedUrl = apiUrl(`/api/orders/${orderId}/allowed-statuses/`);

      const [orderRes, allowedRes] = await Promise.all([
        fetch(orderUrl),
        fetch(allowedUrl),
      ]);

      const orderPayload = await safeJson(orderRes);

      if (!orderRes.ok) {
        // backend pode mandar {"detail": "..."} ou {"error": "..."}
        const msg =
          orderPayload?.detail ||
          orderPayload?.error ||
          "Pedido não encontrado.";
        setOrder(null);
        setAllowedNext([]);
        setNextStatus("");
        setError(msg);
        return;
      }

      setOrder(orderPayload);

      if (allowedRes.ok) {
        const allowedPayload = await safeJson(allowedRes);
        const allowed = Array.isArray(allowedPayload?.allowed)
          ? allowedPayload.allowed
          : [];
        setAllowedNext(allowed);
        setNextStatus(allowed[0] ?? "");
      } else {
        setAllowedNext([]);
        setNextStatus("");
      }
    } catch (e) {
      console.error(e);
      setOrder(null);
      setAllowedNext([]);
      setNextStatus("");
      setError("Falha ao carregar o pedido.");
    } finally {
      setLoading(false);
    }
  }, [orderId]);

  React.useEffect(() => {
    fetchOrder();
  }, [fetchOrder]);

  async function handleChangeStatus() {
    if (!nextStatus || !orderId) return;

    setSaving(true);
    setError("");
    setSuccess("");

    try {
      const url = apiUrl(`/api/orders/${orderId}/status/`);
      const res = await fetch(url, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: nextStatus, origin }),
      });

      const payload = await safeJson(res);

      if (!res.ok) {
        const msg =
          payload?.detail || payload?.error || "Erro ao atualizar status.";
        setError(msg);
        return;
      }

      setSuccess(`Status atualizado para ${payload?.order?.last_status_name}.`);
      await fetchOrder();
    } catch (e) {
      console.error(e);
      setError("Falha ao atualizar status.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) return <Typography sx={{ p: 2 }}>Carregando...</Typography>;
  if (!order)
    return (
      <Box sx={{ p: 2 }}>
        {error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <Typography>Pedido não encontrado.</Typography>
        )}
      </Box>
    );

  const o = order.order ?? {};
  const store = o.store ?? {};
  const customer = o.customer ?? {};
  const addr = o.delivery_address ?? {};
  const coords = addr.coordinates ?? {};
  const items = Array.isArray(o.items) ? o.items : [];
  const payments = Array.isArray(o.payments) ? o.payments : [];
  const statuses = Array.isArray(o.statuses) ? o.statuses : [];

  const currentStatus = o.last_status_name ?? "-";

  return (
    <Box sx={{ p: 1 }}>
      <Stack spacing={2}>
        <Box>
          <Typography variant="h5" fontWeight={800} ml={1}>
            Pedido {order.order_id}
          </Typography>

          <Stack direction="row" spacing={2} alignItems="center" ml={1} mt={1}>
            <Chip label={currentStatus} color={statusColor(currentStatus)} />
            <Typography variant="h6">{formatBRL(o.total_price)}</Typography>
          </Stack>

          <Typography variant="body2" sx={{ opacity: 0.8 }} ml={1} mt={0.5}>
            Criado em: {formatDateTime(o.created_at)}
          </Typography>
        </Box>

        {error ? <Alert severity="error">{error}</Alert> : null}
        {success ? <Alert severity="success">{success}</Alert> : null}

        {/* AÇÕES */}
        <Card>
          <CardContent>
            <Typography fontWeight={800} mb={1}>
              Ações
            </Typography>

            {allowedNext.length === 0 ? (
              <Alert severity="info">
                Este pedido está em um status final ({currentStatus}) e não possui
                próximas transições.
              </Alert>
            ) : (
              <Stack
                direction={{ xs: "column", sm: "row" }}
                spacing={2}
                alignItems="center"
              >
                <FormControl size="small" sx={{ minWidth: 220 }}>
                  <InputLabel id="next-status-label">Próximo status</InputLabel>
                  <Select
                    labelId="next-status-label"
                    label="Próximo status"
                    value={nextStatus}
                    onChange={(e) => setNextStatus(e.target.value)}
                  >
                    {allowedNext.map((s) => (
                      <MenuItem key={s} value={s}>
                        {s}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <FormControl size="small" sx={{ minWidth: 160 }}>
                  <InputLabel id="origin-label">Origin</InputLabel>
                  <Select
                    labelId="origin-label"
                    label="Origin"
                    value={origin}
                    onChange={(e) => setOrigin(e.target.value)}
                  >
                    <MenuItem value="STORE">STORE</MenuItem>
                    <MenuItem value="SYSTEM">SYSTEM</MenuItem>
                    <MenuItem value="CUSTOMER">CUSTOMER</MenuItem>
                  </Select>
                </FormControl>

                <Button
                  variant="contained"
                  onClick={handleChangeStatus}
                  disabled={saving || !nextStatus}
                >
                  {saving ? "Atualizando..." : "Atualizar status"}
                </Button>
              </Stack>
            )}
          </CardContent>
        </Card>

        {/* CLIENTE + LOJA */}
        <Stack direction={{ xs: "column", md: "row" }} spacing={2}>
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Typography fontWeight={800}>Cliente</Typography>
              <Typography>{customer.name ?? "-"}</Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                {customer.temporary_phone ?? "-"}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography fontWeight={800}>Loja</Typography>
              <Typography>{store.name ?? "-"}</Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                store_id: {store.id ?? "-"}
              </Typography>
            </CardContent>
          </Card>

          {/* PAGAMENTOS */}
          <Card sx={{ flex: 1 }}>
            <CardContent>
              <Typography fontWeight={800} mb={1}>
                Pagamentos
              </Typography>

              {payments.length === 0 ? (
                <Typography sx={{ opacity: 0.8 }}>
                  Nenhum pagamento informado.
                </Typography>
              ) : (
                <Stack spacing={1}>
                  {payments.map((p, idx) => (
                    <Box
                      key={idx}
                      sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: 2,
                      }}
                    >
                      <Typography>
                        {p.origin ?? "-"}{" "}
                        {p.prepaid ? "(pré-pago)" : "(pago na entrega)"}
                      </Typography>
                      <Typography fontWeight={700}>{formatBRL(p.value)}</Typography>
                    </Box>
                  ))}
                </Stack>
              )}
            </CardContent>
          </Card>
        </Stack>

        {/* ENDEREÇO */}
        <Card>
          <CardContent>
            <Typography fontWeight={800} mb={1}>
              Endereço de entrega
            </Typography>
            <Typography>
              {addr.street_name ?? "-"}, {addr.street_number ?? "-"} —{" "}
              {addr.neighborhood ?? "-"}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              {addr.city ?? "-"} / {addr.state ?? "-"} — {addr.postal_code ?? "-"} —{" "}
              {addr.country ?? "-"}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              Referência: {addr.reference ?? "-"}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.8 }}>
              Coordenadas: {coords.latitude ?? "-"}, {coords.longitude ?? "-"}
            </Typography>
          </CardContent>
        </Card>

        {/* ITENS */}
        <Card>
          <CardContent>
            <Typography fontWeight={800} mb={1}>
              Itens
            </Typography>

            {items.length === 0 ? (
              <Typography sx={{ opacity: 0.8 }}>Nenhum item informado.</Typography>
            ) : (
              <Stack spacing={1.25}>
                {items.map((it, idx) => (
                  <Box
                    key={idx}
                    sx={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: 2,
                    }}
                  >
                    <Box>
                      <Typography fontWeight={700}>
                        {it.quantity ?? 1}× {it.name ?? "-"}
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.8 }}>
                        código: {it.code ?? "-"} • obs: {it.observations ?? "—"}
                      </Typography>
                    </Box>
                    <Box sx={{ textAlign: "right" }}>
                      <Typography fontWeight={800}>
                        {formatBRL(it.total_price)}
                      </Typography>
                      {Number(it.discount ?? 0) > 0 ? (
                        <Typography variant="body2" sx={{ opacity: 0.8 }}>
                          desconto: {formatBRL(it.discount)}
                        </Typography>
                      ) : null}
                    </Box>
                  </Box>
                ))}
              </Stack>
            )}
          </CardContent>
        </Card>

        {/* TIMELINE */}
        <Card>
          <CardContent>
            <Typography fontWeight={800} mb={1}>
              Timeline
            </Typography>

            {statuses.length === 0 ? (
              <Typography sx={{ opacity: 0.8 }}>Sem histórico de status.</Typography>
            ) : (
              <Stack spacing={1}>
                {statuses
                  .slice()
                  .sort(
                    (a, b) => Number(a.created_at ?? 0) - Number(b.created_at ?? 0)
                  )
                  .map((s, idx) => (
                    <Box
                      key={idx}
                      sx={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: 2,
                      }}
                    >
                      <Box>
                        <Chip
                          size="small"
                          label={s.name ?? "-"}
                          color={statusColor(s.name)}
                          sx={{ mr: 1 }}
                        />
                        <Typography component="span" sx={{ opacity: 0.9 }}>
                          origin: {s.origin ?? "-"}
                        </Typography>
                      </Box>
                      <Typography sx={{ opacity: 0.8 }}>
                        {formatDateTime(s.created_at)}
                      </Typography>
                    </Box>
                  ))}
              </Stack>
            )}
          </CardContent>
        </Card>
      </Stack>
    </Box>
  );
}