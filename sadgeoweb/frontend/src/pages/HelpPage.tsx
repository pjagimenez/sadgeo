import { Box, Button } from "@mui/material";
import guide from "../content/guia.md?raw";
import manualText from "../content/manual.md?raw";
// Small safe Markdown subset: headings, bullet lists and paragraphs; no raw HTML.
export default function HelpPage({ manual = false }: { manual?: boolean }) {
  const lines = (manual ? manualText : guide).split("\n");
  return (
    <Box component="main" className="portal-content documentation">
      {lines.map((line, index) =>
        line.startsWith("# ") ? (
          <h1 key={index}>{line.slice(2)}</h1>
        ) : line.startsWith("## ") ? (
          <h2 key={index}>{line.slice(3)}</h2>
        ) : line.startsWith("- ") ? (
          <ul key={index}>
            <li>{line.slice(2)}</li>
          </ul>
        ) : line.trim() ? (
          <p key={index}>{line}</p>
        ) : null,
      )}
      {!manual && (
        <Button
          component="a"
          href="https://github.com/pjagimenez/sadgeo/blob/main/TODO.md"
          target="_blank"
          rel="noopener noreferrer"
        >
          TODO e milestones no GitHub
        </Button>
      )}
    </Box>
  );
}
