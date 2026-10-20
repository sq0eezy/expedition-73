/* Descriptive, paired differences of recorded policy series. No inference. */
export const contrasts = [
  { id: "land_minus_unmasked", left: "land", right: "unmasked", label: "Kara − maskesiz" },
  { id: "land_ice_minus_land", left: "land_and_ice", right: "land", label: "Kara + kara buzu − kara" },
];

export function summarizePolicyDifferences(series) {
  if (!Array.isArray(series) || series.length !== 12) throw Error("Expected twelve monthly policy records");
  const year = typeof series[0]?.date === "string" ? series[0].date.slice(0, 4) : "";
  if (!/^\d{4}$/.test(year) || !series.every((row, i) => row?.date === `${year}-${String(i + 1).padStart(2, "0")}` &&
      ["unmasked", "land", "land_and_ice"].every((key) => row[key] === null || typeof row[key] === "number" && Number.isFinite(row[key])))) throw Error("Invalid monthly policy series");
  return contrasts.map((contrast) => {
    const values = series.map((row) => ({ date: row.date,
      delta: row[contrast.left] === null || row[contrast.right] === null ? null : row[contrast.left] - row[contrast.right] }));
    if (values.some((row) => row.delta !== null && !Number.isFinite(row.delta))) throw Error("Non-finite policy difference");
    const valid = values.filter((row) => row.delta !== null);
    const maximum = valid.length ? Math.max(...valid.map((row) => Math.abs(row.delta))) : null;
    return { ...contrast, values, valid_months: valid.length,
      max_abs_delta_degC: maximum,
      max_abs_dates: valid.filter((row) => Math.abs(row.delta) === maximum).map((row) => row.date) };
  });
}
