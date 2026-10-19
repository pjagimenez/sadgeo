import { lazy, Suspense } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import { AuthProvider } from "./auth/AuthContext";
import LoginPage from "./pages/LoginPage";
const PrincipalPage = lazy(() => import("./pages/PrincipalPage"));
const RegistrosPage = lazy(() =>
  import("./pages/PrincipalPage").then((m) => ({ default: m.RegistrosPage })),
);
const DashboardPage = lazy(() => import("./pages/DashboardPage"));
const theme = createTheme({
  palette: {
    primary: { main: "#4a568c" },
    secondary: { main: "#b66e29" },
    background: { default: "#f3f5f8" },
  },
  typography: { fontFamily: '"Segoe UI", Arial, sans-serif' },
  shape: { borderRadius: 8 },
});
export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <BrowserRouter>
          <Suspense fallback={<p role="status">Carregando tela…</p>}>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route element={<PrincipalPage />}>
                <Route path="/index" element={<DashboardPage />} />
                <Route path="/registros" element={<RegistrosPage />} />
              </Route>
              <Route path="*" element={<Navigate to="/index" replace />} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}
