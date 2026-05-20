'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, Unidade, Venda } from '@/lib/api';
import { brl } from '@/lib/format';

interface Comprador {
  id: string;
  nome: string;
  cpf_cnpj: string | null;
}

export default function VendasPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [unidades, setUnidades] = useState<Unidade[]>([]);
  const [vendas, setVendas] = useState<Venda[]>([]);
  const [compradores, setCompradores] = useState<Comprador[]>([]);
  const [editing, setEditing] = useState<Unidade | null>(null);
  const [form, setForm] = useState({
    comprador_id: '',
    preco_tabela: '',
    preco_venda_final: '',
    data_venda: '',
    status: 'vendida' as Venda['status'],
    observacoes: '',
  });
  const [newComprador, setNewComprador] = useState('');

  function reload() {
    if (!id) return;
    api.get<Unidade[]>(`/obras/${id}/unidades`).then(setUnidades);
    api.get<Venda[]>(`/vendas?obra_id=${id}`).then(setVendas);
    api.get<Comprador[]>('/compradores').then(setCompradores);
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function criarComprador() {
    if (!newComprador.trim()) return;
    const c = await api.post<Comprador>('/compradores', { nome: newComprador });
    setNewComprador('');
    setCompradores((s) => [...s, c]);
    setForm({ ...form, comprador_id: c.id });
  }

  async function salvar(e: React.FormEvent) {
    e.preventDefault();
    if (!editing) return;
    await api.post<Venda>('/vendas', {
      unidade_id: editing.id,
      comprador_id: form.comprador_id || null,
      preco_tabela: form.preco_tabela,
      preco_venda_final: form.preco_venda_final || null,
      data_venda: form.data_venda || null,
      status: form.status,
      observacoes: form.observacoes || null,
    });
    setEditing(null);
    reload();
  }

  function vendaDaUnidade(uid: string): Venda | undefined {
    return vendas
      .filter((v) => v.unidade_id === uid)
      .sort((a, b) => (a.id < b.id ? 1 : -1))[0];
  }

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">Vendas</h2>
      </div>

      <table className="data-table">
        <thead>
          <tr>
            <th>Unidade</th>
            <th>Status</th>
            <th className="num">Preço tabela</th>
            <th className="num">Preço final</th>
            <th>Data</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {unidades.map((u) => {
            const v = vendaDaUnidade(u.id);
            return (
              <tr key={u.id}>
                <td>{u.identificador}</td>
                <td>
                  <span className={`status status-${v?.status || 'disponivel'}`}>
                    {v?.status || 'disponivel'}
                  </span>
                </td>
                <td className="num">{brl(v?.preco_tabela)}</td>
                <td className="num">{brl(v?.preco_venda_final)}</td>
                <td>{v?.data_venda || '—'}</td>
                <td>
                  <button
                    className="btn-link"
                    onClick={() => {
                      setEditing(u);
                      setForm({
                        comprador_id: v?.comprador_id || '',
                        preco_tabela: v?.preco_tabela || '',
                        preco_venda_final: v?.preco_venda_final || '',
                        data_venda: v?.data_venda || '',
                        status: v?.status || 'vendida',
                        observacoes: v?.observacoes || '',
                      });
                    }}
                  >
                    {v ? 'Atualizar' : 'Registrar venda'}
                  </button>
                </td>
              </tr>
            );
          })}
          {unidades.length === 0 && (
            <tr>
              <td colSpan={6} className="empty">
                Cadastre unidades primeiro.
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {editing && (
        <div className="modal-backdrop" onClick={() => setEditing(null)}>
          <form className="modal" onClick={(e) => e.stopPropagation()} onSubmit={salvar}>
            <h3>Venda — Unidade {editing.identificador}</h3>
            <label>
              Comprador
              <select
                value={form.comprador_id}
                onChange={(e) => setForm({ ...form, comprador_id: e.target.value })}
              >
                <option value="">— sem comprador —</option>
                {compradores.map((c) => (
                  <option key={c.id} value={c.id}>{c.nome}</option>
                ))}
              </select>
            </label>
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                placeholder="Novo comprador"
                value={newComprador}
                onChange={(e) => setNewComprador(e.target.value)}
              />
              <button type="button" className="btn btn-ghost" onClick={criarComprador}>
                Criar
              </button>
            </div>
            <label>
              Preço tabela
              <input
                type="number"
                step="0.01"
                value={form.preco_tabela}
                onChange={(e) => setForm({ ...form, preco_tabela: e.target.value })}
                required
              />
            </label>
            <label>
              Preço final
              <input
                type="number"
                step="0.01"
                value={form.preco_venda_final}
                onChange={(e) => setForm({ ...form, preco_venda_final: e.target.value })}
              />
            </label>
            <label>
              Data
              <input
                type="date"
                value={form.data_venda}
                onChange={(e) => setForm({ ...form, data_venda: e.target.value })}
              />
            </label>
            <label>
              Status
              <select
                value={form.status}
                onChange={(e) =>
                  setForm({ ...form, status: e.target.value as Venda['status'] })
                }
              >
                <option value="disponivel">Disponível</option>
                <option value="reservada">Reservada</option>
                <option value="vendida">Vendida</option>
                <option value="distratada">Distratada</option>
              </select>
            </label>
            <label>
              Observações
              <textarea
                value={form.observacoes}
                onChange={(e) => setForm({ ...form, observacoes: e.target.value })}
              />
            </label>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">Salvar</button>
              <button type="button" className="btn btn-ghost" onClick={() => setEditing(null)}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
