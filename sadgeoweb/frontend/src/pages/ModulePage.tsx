import { useLocation } from "react-router-dom";
import { Alert } from "@mui/material";
import { screenFor } from "../navigation";
import RecordsPage from "./RecordsPage";
import ReportsPage from "./ReportsPage";
import IntegrationsPage from "./IntegrationsPage";
import HelpPage from "./HelpPage";
import WorkflowTemplatePage from "./WorkflowTemplatePage";
import BasicTablePage from "./BasicTablePage";
export default function ModulePage() {
  const route = screenFor(useLocation().pathname);
  if (!route) return <Alert severity="warning">Página não encontrada.</Alert>;
  const { screen, group } = route;
  if (screen.kind === "records")
    return <RecordsPage key={screen.context} screen={screen} group={group} />;
  if (screen.kind === "table")
    return (
      <BasicTablePage key={screen.table} table={screen.table!} group={group} />
    );
  if (screen.kind === "reports")
    return <ReportsPage key={screen.path} title={screen.label} />;
  if (screen.kind === "integrations") return <IntegrationsPage />;
  if (screen.kind === "help") return <HelpPage manual={screen.path === "/ajuda/manual"} />;
  return (
    <WorkflowTemplatePage key={screen.path} screen={screen} group={group} />
  );
}
