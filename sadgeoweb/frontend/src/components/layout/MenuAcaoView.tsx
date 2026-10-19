// Adaptado do template em sadgeo-react-web.7z; sessão e ações integradas à API 0.1.
import { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";
import LoginIcon from "@mui/icons-material/Login";
import LogoutIcon from "@mui/icons-material/Logout";
import HelpIcon from "@mui/icons-material/Help";
import PersonIcon from "@mui/icons-material/Person";
import { useAuth } from "../../auth/AuthContext";
export default function MenuAcaoView({
  tema,
  setTema,
  temas,
}: {
  tema: string;
  setTema: (s: string) => void;
  temas: string[];
}) {
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
      <nav aria-label="Navegação principal">
        <NavLink to="/index">Painel resumo</NavLink>
        <NavLink to="/registros">Registros</NavLink>
      </nav>
      <FormControl fullWidth size="small">
        <InputLabel id="tema-label">Tema / projeto</InputLabel>
        <Select
          labelId="tema-label"
          label="Tema / projeto"
          value={tema}
          onChange={(e) => setTema(e.target.value)}
        >
          <MenuItem value="">Todos</MenuItem>
          {temas.map((t) => (
            <MenuItem key={t} value={t}>
              {t}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Typography variant="caption">
        O tema filtra a grade de registros. O painel resumo apresenta os totais
        gerais.
      </Typography>
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
          Consulte os indicadores no Painel resumo. Em Registros, selecione um
          tema, busque campanha, município ou UF e clique numa linha para
          consultar seus detalhes. A versão 0.1 é de consulta; não altera dados
          do Oracle.
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setHelp(false)}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
