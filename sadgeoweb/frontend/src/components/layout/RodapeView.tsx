import { Box, Typography } from "@mui/material";
export default function RodapeView({ demo = false }: { demo?: boolean }) {
  return (
    <Box component="footer" className="portal-footer">
      <Typography variant="caption">
        © {new Date().getFullYear()} IBGE – DGC/CGED
      </Typography>
      <Typography variant="caption">
        {demo ? "Demonstração • dados fictícios" : "Ambiente institucional"}
      </Typography>
      <Typography variant="caption">SADGEO 0.1.0</Typography>
    </Box>
  );
}
