import { Box, Typography } from "@mui/material";
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
      <Typography variant="caption" className="footer-version">
        {config ? `Versão ${config.version}` : "Versão indisponível"}
      </Typography>
    </Box>
  );
}
