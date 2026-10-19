import { Link } from "react-router-dom";
import { Alert, Box, Button, Paper, Typography } from "@mui/material";
export default function HelpPage() {
  return (
    <Box component="main" className="portal-content">
      <Typography className="eyebrow">Ajuda e Manuais</Typography>
      <Typography component="h1" variant="h4">
        Guia de Uso e Evolução
      </Typography>
      <Alert severity="info" sx={{ my: 2 }}>
        Versão 0.2: consultas, cadastros e telas preparadas para evolução.
        Operações de crítica, gravação de estação e carga BDG permanecem nos
        milestones.
      </Alert>
      {[
        [
          "Painel de Controle",
          "Consulte os indicadores gerais e gráficos. As permissões detalhadas por unidade/tema ainda precisam de implementação.",
          "/index",
        ],
        [
          "Crítica de Dados e Análise",
          "Pesquise e abra detalhes por abas. A campanha da análise é fixa; consulta não libera nem retém registros.",
          "/campo/critica",
        ],
        [
          "Cadastros",
          "Campanha e tabelas básicas permitem manutenção no demo. No Oracle, a manutenção exige login autorizado e chave confirmada.",
          "/tabelas/localizacao",
        ],
        [
          "Relatórios",
          "Filtre a produção por campanha e ano e exporte as linhas da consulta em CSV.",
          "/qualidade/producao",
        ],
        [
          "Integrações",
          "Confira a saúde geral e o estado de configuração sem expor credenciais.",
          "/administracao/integracoes",
        ],
      ].map(([title, text, path]) => (
        <Paper variant="outlined" sx={{ p: 2, my: 2 }} key={title}>
          <Typography variant="h6">{title}</Typography>
          <Typography sx={{ my: 1 }}>{text}</Typography>
          <Button component={Link} to={path}>
            Abrir
          </Button>
        </Paper>
      ))}
      <Button
        component="a"
        href="https://github.com/pjagimenez/sadgeo/blob/main/TODO.md"
        target="_blank"
        rel="noopener noreferrer"
      >
        TODO e milestones no GitHub
      </Button>
    </Box>
  );
}
