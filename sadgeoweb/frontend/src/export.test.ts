import { expect, it } from "vitest";
import { toCsv } from "./export";
it("quotes CSV values and neutralizes spreadsheet formulas without losing precision", () => {
  const csv = toCsv([
    {
      descricao: 'a;"b"\nc',
      formula: ' =HYPERLINK("x")',
      precisao: "12345678901234567890123456789012345678",
    },
  ]);
  expect(csv.startsWith("\uFEFF")).toBe(true);
  expect(csv).toContain('"a;""b""\nc"');
  expect(csv).toContain('"\' =HYPERLINK(""x"")"');
  expect(csv).toContain("12345678901234567890123456789012345678");
});
