'use client';

import { useEffect, useState } from 'react';
import { api, Insumo } from '@/lib/api';
import { brl } from '@/lib/format';

export default function InsumosPage() {
  const [list, setList] = useState<Insumo[]>([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    codigo: '',
    descricao: '',
    unidade: 'un',
    tipo: 'material' as Insumo['tipo'],
    sinapi_codigo: '',
    custo_unitario_referencia: '0',
  });

  function reload() {
    api.get<Insumo[]>('/insumos').then(setList);
  }

  useEffect(reload, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    await api.post<Insumo>('/insumos', {
      codigo: form.codigo,
      descricao: form.descricao,
      unidade: form.unidade,
      tipo: form.tipo,
      sinapi_codigo: form.sinapi_codigo || null,
      custo_unitario_referencia: form.custo_unitario_referencia || '0',
    });
    setForm({
      codigo: '',
      descricao: '',
      unidade: 'un',
      tipo: 'material',
      sinapi_codigo: '',
      custo_unitario_referencia: '0',
    });
    setCreating(false);
    reload();
  }

  async function remover(iid: string) {
    if (!confirm('Remover insumo?')) return;
    try {
      await api.delete(`/insumos/${iid}`);
      reload();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Erro (insumo pode estar em uso)');
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Insumos</h1>
        <button className="btn btn-primary" onClick={() => setCreating(!creating)}>
          {creating ? 'Cancelar' : 'Novo insumo'}
        </button>
      </div>

      {creating && (
        <form className="form-grid panel" onSubmit={submit}>
          <label>
            Código
            <input
              value={form.codigo}
              onChange={(e) => setForm({ ...form, codigo: e.target.value })}
              required
            />
          </label>
          <label>
            Tipo
            <select
              value={form.tipo}
              onChange={(e) => setForm({ ...form, tipo: e.target.value as Insumo['tipo'] })}
            >
              <option value="material">Material</option>
              <option value="mao_obra">Mão de obra</option>
              <option value="equipamento">Equipamento</option>
            </select>
          </label>
          <label className="span-2">
            Descrição
            <input
              value={form.descricao}
              onChange={(e) => setForm({ ...form, descricao: e.target.value })}
              required
            />
          </label>
          <label>
            Unidade
            <input
              value={form.unidade}
              onChange={(e) => setForm({ ...form, unidade: e.target.value })}
              required
            />
          </label>
          <label>
            Código SINAPI (opcional)
            <input
              value={form.sinapi_codigo}
              onChange={(e) => setForm({ ...form, sinapi_codigo: e.target.value })}
            />
          </label>
          <label>
            Custo unitário ref. (R$)
            <input
              type="number"
              step="0.01"
              value={form.custo_unitario_referencia}
              onChange={(e) =>
                setForm({ ...form, custo_unitario_referencia: e.target.value })
              }
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
            <th>Código</th>
            <th>Descrição</th>
            <th>Un.</th>
            <th>Tipo</th>
            <th>SINAPI</th>
            <th className="num">Custo ref.</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map((i) => (
            <tr key={i.id}>
              <td>{i.codigo}</td>
              <td>{i.descricao}</td>
              <td>{i.unidade}</td>
              <td>{i.tipo}</td>
              <td>{i.sinapi_codigo || '—'}</td>
              <td className="num">{brl(i.custo_unitario_referencia)}</td>
              <td>
                <button className="btn-link danger" onClick={() => remover(i.id)}>
                  Remover
                </button>
              </td>
            </tr>
          ))}
          {list.length === 0 && (
            <tr>
              <td colSpan={7} className="empty">Nenhum insumo cadastrado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
