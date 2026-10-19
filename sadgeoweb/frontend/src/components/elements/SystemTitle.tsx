import { Typography } from "@mui/material";
export default function SystemTitle() {
  return (
    <div>
      <Typography component="h1" variant="h4" className="login-title">
        SADGEO
      </Typography>
      <Typography className="login-subtitle">
        Sistema de acompanhamento de dados geodésicos
      </Typography>
    </div>
  );
}
