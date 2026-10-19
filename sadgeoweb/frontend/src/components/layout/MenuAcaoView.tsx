// Adaptado do template em sadgeo-react-web.7z; sessão e ações integradas à API 0.1.
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
import HelpIcon from "@mui/icons-material/Help";
import PersonIcon from "@mui/icons-material/Person";
import { menus } from "../../navigation";
import { useAuth } from "../../auth/AuthContext";
export default function MenuAcaoView() {
  const { pathname } = useLocation();
  const { user, logout } = useAuth();
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
    <Box component="aside" className="portal-menu">
      <nav aria-label="Navegação principal" className="menu-navigation">
        <NavLink to="/index">Painel de Controle</NavLink>
        {menus.map((group) => (
          <details
            className="menu-group"
            key={group.label}
            open={group.items.some((item) => item.path === pathname)}
          >
            <summary>{group.label}</summary>
            <div>
              {group.items.map((item) => (
                <NavLink key={item.path} to={item.path}>
                  {item.label}
                  {item.campanha && (
                    <span className="campaign-code"> ({item.campanha})</span>
                  )}
                </NavLink>
              ))}
            </div>
          </details>
        ))}
      </nav>
      {error && <Alert severity="error">{error}</Alert>}
      <Box className="portal-account">
        <Button startIcon={<HelpIcon />} onClick={() => setHelp(true)}>
          Ajuda
        </Button>
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
        <DialogTitle>Ajuda do SADGEO</DialogTitle>
        <DialogContent>
          O Painel de Controle apresenta os indicadores. Crítica de Dados e
          Análise compartilham o template de consulta, com campanha definida
          pelo menu. Tabelas básicas e Campanha têm manutenção para usuários
          autorizados. Em demonstração, as alterações existem apenas em memória.
        </DialogContent>
        <DialogActions>
          <Button
            component={NavLink}
            to="/ajuda/guia"
            onClick={() => setHelp(false)}
          >
            Guia completo
          </Button>
          <Button onClick={() => setHelp(false)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
