import { Box, Typography, IconButton } from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import type { Config } from "../../auth/AuthContext";
export default function RodapeView({ config }: { config?: Config }) {
  return (
    <Box
      component="footer"
      className="portal-footer"
      aria-label="Informações do ambiente"
    >
      <Typography variant="caption" className="footer-copyright">
        © {new Date().getFullYear()} IBGE-DGC/CGED/GSD
      </Typography>
      <Typography variant="caption" className="footer-environment">
        {config
          ? `${config.profileLabel} (${config.profile}) • ${config.hostname}`
          : "Ambiente indisponível"}
      </Typography>
      <Box className="footer-version">
        <Typography variant="caption">
          {config ? `Versão ${config.version}` : "Versão indisponível"}
        </Typography>
        <IconButton
          component="a"
          href="/ajuda/guia"
          size="small"
          title="Guia de Uso e Evolução"
          aria-label="Guia de Uso e Evolução"
        >
          <InfoOutlinedIcon fontSize="inherit" />
        </IconButton>
      </Box>
    </Box>
  );
}
