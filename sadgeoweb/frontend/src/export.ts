import type { Row } from "./Table";
export function toCsv(rows: Row[]): string {
  const columns = [...new Set(rows.flatMap((r) => Object.keys(r)))];
  const cell = (v: unknown) => {
    let text = String(v ?? "");
    if (/^[\s]*[=+@-]/.test(text)) text = "'" + text;
    return '"' + text.replaceAll('"', '""') + '"';
  };
  return (
    "\uFEFF" +
    [
      columns.map(cell).join(";"),
      ...rows.map((r) => columns.map((c) => cell(r[c])).join(";")),
    ].join("\r\n")
  );
}
export function downloadCsv(rows: Row[], filename: string) {
  const url = URL.createObjectURL(
    new Blob([toCsv(rows)], { type: "text/csv;charset=utf-8" }),
  );
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}
