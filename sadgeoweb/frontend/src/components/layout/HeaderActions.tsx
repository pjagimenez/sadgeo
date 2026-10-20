import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Typography,
} from "@mui/material";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import MenuBookIcon from "@mui/icons-material/MenuBook";
import { screenFor } from "../../navigation";
import HelpIcon from "@mui/icons-material/Help";
import PersonIcon from "@mui/icons-material/Person";
import { useAuth } from "../../auth/AuthContext";
export default function HeaderActions() {
  const { user, logout } = useAuth();
  const { pathname } = useLocation();
  const route = screenFor(pathname);
  const title =
    pathname === "/index"
      ? "Painel de Controle"
      : (route?.screen.label ?? "SADGEO");
  const context =
    pathname === "/index"
      ? "Dashboard público. Use os filtros independentes de ano, campanha e projeto. Os fatos são consultados por página. Janeiro a março iniciam no ano anterior; abril a dezembro, no ano corrente."
      : (route?.screen.note ??
        (route?.screen.kind === "records"
          ? "Pesquise registros e abra os detalhes. A campanha da análise é fixa; esta consulta não libera nem retém registros."
          : route?.screen.kind === "table"
            ? "Cadastro de referência. A manutenção exige login autorizado e chave confirmada; na demonstração, as alterações são apenas em memória."
            : route?.screen.milestone
              ? `Tela preparada para evolução no milestone ${route.screen.milestone}; os comandos definitivos estão desabilitados.`
              : "Consulte o Manual para orientação sobre esta tela."));
  const [help, setHelp] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function exit() {
    setBusy(true);
    try {
      await logout();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <Box className="header-actions">
      {error && <Alert severity="error">{error}</Alert>}
      <Box className="header-account">
        <Box className="header-documentation">
          <Button
            component={NavLink}
            to="/ajuda/manual"
            startIcon={<MenuBookIcon />}
          >
            Manual
          </Button>
          <Button startIcon={<HelpIcon />} onClick={() => setHelp(true)}>
            Ajuda desta tela
          </Button>
        </Box>
        <Box className="portal-user" aria-label="Identificação do usuário">
          <PersonIcon />
          <Box sx={{ minWidth: 0 }}>
            <Typography fontWeight={700}>
              {user?.nome ?? "Visitante"}
            </Typography>
            {user && (
              <Typography variant="caption" component="div">
                Identificador: {user.login}
              </Typography>
            )}
            {user?.description && (
              <Typography variant="caption" component="div">
                Descrição: {user.description}
              </Typography>
            )}
            <Typography variant="caption" component="div">
              Perfil: {user?.perfil ?? "Não autenticado"}
            </Typography>
          </Box>
        </Box>
        {user ? (
          <Button startIcon={<LogoutIcon />} disabled={busy} onClick={exit}>
            Sair
          </Button>
        ) : (
          <Button component={NavLink} to="/login" startIcon={<LoginIcon />}>
            Fazer login
          </Button>
        )}
      </Box>
      <Dialog open={help} onClose={() => setHelp(false)}>
        <DialogTitle>Ajuda — {title}</DialogTitle>
        <DialogContent>{context}</DialogContent>
        <DialogActions>
          <Button
            component={NavLink}
            to="/ajuda/manual"
            onClick={() => setHelp(false)}
          >
            Manual completo
          </Button>
          <Button onClick={() => setHelp(false)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
