'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, Unidade } from '@/lib/api';
import { num } from '@/lib/format';

export default function UnidadesPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [unidades, setUnidades] = useState<Unidade[]>([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    identificador: '',
    andar: '',
    bloco: '',
    fracao_ideal: '',
    area_privativa_m2: '',
  });

  function reload() {
    if (!id) return;
    api.get<Unidade[]>(`/obras/${id}/unidades`).then(setUnidades);
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;
    await api.post<Unidade>(`/obras/${id}/unidades`, {
      identificador: form.identificador,
      andar: form.andar ? parseInt(form.andar, 10) : null,
      bloco: form.bloco || null,
      fracao_ideal: form.fracao_ideal || '0',
      area_privativa_m2: form.area_privativa_m2 || '0',
    });
    setForm({ identificador: '', andar: '', bloco: '', fracao_ideal: '', area_privativa_m2: '' });
    setCreating(false);
    reload();
  }

  async function remover(uid: string) {
    if (!confirm('Remover esta unidade?')) return;
    await api.delete(`/obras/${id}/unidades/${uid}`);
    reload();
  }

  const somaFracao = unidades.reduce((s, u) => s + parseFloat(u.fracao_ideal || '0'), 0);

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">Unidades ({unidades.length})</h2>
        <button className="btn btn-primary" onClick={() => setCreating(!creating)}>
          {creating ? 'Cancelar' : 'Nova unidade'}
        </button>
      </div>

      {creating && (
        <form className="form-grid panel" onSubmit={submit}>
          <label>
            Identificador
            <input
              value={form.identificador}
              onChange={(e) => setForm({ ...form, identificador: e.target.value })}
              required
            />
          </label>
          <label>
            Andar
            <input
              type="number"
              value={form.andar}
              onChange={(e) => setForm({ ...form, andar: e.target.value })}
            />
          </label>
          <label>
            Bloco
            <input
              value={form.bloco}
              onChange={(e) => setForm({ ...form, bloco: e.target.value })}
            />
          </label>
          <label>
            Fração ideal (0–1)
            <input
              type="number"
              step="0.00000001"
              value={form.fracao_ideal}
              onChange={(e) => setForm({ ...form, fracao_ideal: e.target.value })}
              required
            />
          </label>
          <label>
            Área privativa (m²)
            <input
              type="number"
              step="0.01"
              value={form.area_privativa_m2}
              onChange={(e) => setForm({ ...form, area_privativa_m2: e.target.value })}
              required
            />
          </label>
          <div className="span-2 form-actions">
            <button type="submit" className="btn btn-primary">Salvar</button>
          </div>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Identificador</th>
            <th>Andar</th>
            <th>Bloco</th>
            <th className="num">Fração ideal</th>
            <th className="num">Área (m²)</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {unidades.map((u) => (
            <tr key={u.id}>
              <td>{u.identificador}</td>
              <td>{u.andar ?? '—'}</td>
              <td>{u.bloco ?? '—'}</td>
              <td className="num">{num(u.fracao_ideal, 6)}</td>
              <td className="num">{num(u.area_privativa_m2)}</td>
              <td>
                <button className="btn-link danger" onClick={() => remover(u.id)}>
                  Remover
                </button>
              </td>
            </tr>
          ))}
          {unidades.length > 0 && (
            <tr className="row-total">
              <td colSpan={3}>
                <strong>Total</strong>
              </td>
              <td className="num">
                <strong>{num(somaFracao, 6)}</strong>
                {Math.abs(somaFracao - 1) > 0.0001 && (
                  <span className="warn"> ⚠</span>
                )}
              </td>
              <td className="num"></td>
              <td></td>
            </tr>
          )}
          {unidades.length === 0 && (
            <tr>
              <td colSpan={6} className="empty">Nenhuma unidade cadastrada.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
