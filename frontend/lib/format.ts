export function brl(value: string | number | null | undefined): string {
  if (value === null || value === undefined) return '—';
  const n = typeof value === 'string' ? parseFloat(value) : value;
  if (Number.isNaN(n)) return '—';
  return n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

export function num(value: string | number | null | undefined, fractionDigits = 2): string {
  if (value === null || value === undefined) return '—';
  const n = typeof value === 'string' ? parseFloat(value) : value;
  if (Number.isNaN(n)) return '—';
  return n.toLocaleString('pt-BR', {
    minimumFractionDigits: fractionDigits,
    maximumFractionDigits: fractionDigits,
  });
}

export function pct(value: string | number | null | undefined): string {
  if (value === null || value === undefined) return '—';
  const n = typeof value === 'string' ? parseFloat(value) : value;
  if (Number.isNaN(n)) return '—';
  return `${n.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}%`;
}
