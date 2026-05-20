'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, EAPNode, Orcamento } from '@/lib/api';
import { brl, num } from '@/lib/format';

interface OrcItem {
  id: string;
  eap_id: string;
  composicao_id: string | null;
  descricao: string;
  unidade: string;
  quantidade: string;
  custo_unitario: string;
  custo_total: string;
}

export default function OrcamentoEditor() {
  const params = useParams<{ id: string; orcId: string }>();
  const obraId = params?.id;
  const orcId = params?.orcId;
  const [orc, setOrc] = useState<Orcamento | null>(null);
  const [itens, setItens] = useState<OrcItem[]>([]);
  const [eap, setEap] = useState<EAPNode[]>([]);
  const [form, setForm] = useState({
    eap_id: '',
    descricao: '',
    unidade: 'un',
    quantidade: '',
    custo_unitario: '',
  });

  function reload() {
    if (!obraId || !orcId) return;
    api.get<Orcamento[]>(`/obras/${obraId}/orcamentos`).then((os) => {
      setOrc(os.find((o) => o.id === orcId) || null);
    });
    api.get<OrcItem[]>(`/obras/${obraId}/orcamentos/${orcId}/itens`).then(setItens);
    api.get<EAPNode[]>(`/obras/${obraId}/eap`).then(setEap);
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [obraId, orcId]);

  async function addItem(e: React.FormEvent) {
    e.preventDefault();
    await api.post(`/obras/${obraId}/orcamentos/${orcId}/itens`, {
      eap_id: form.eap_id,
      descricao: form.descricao,
      unidade: form.unidade,
      quantidade: form.quantidade,
      custo_unitario: form.custo_unitario,
    });
    setForm({ eap_id: form.eap_id, descricao: '', unidade: 'un', quantidade: '', custo_unitario: '' });
    reload();
  }

  async function removeItem(iid: string) {
    if (!confirm('Remover item?')) return;
    await api.delete(`/obras/${obraId}/orcamentos/${orcId}/itens/${iid}`);
    reload();
  }

  if (!orc) return <p>Carregando…</p>;
  const isDraft = orc.status === 'rascunho';

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">
          Orçamento v{orc.versao} — {orc.nome}{' '}
          <span className={`status status-${orc.status}`}>{orc.status}</span>
        </h2>
        <div className="stat">
          <div className="stat-label">Custo total</div>
          <div className="stat-value">{brl(orc.custo_total_calculado)}</div>
        </div>
      </div>

      {isDraft && (
        <form className="form-grid panel" onSubmit={addItem}>
          <label>
            EAP
            <select
              value={form.eap_id}
              onChange={(e) => setForm({ ...form, eap_id: e.target.value })}
              required
            >
              <option value="">— escolher —</option>
              {eap.map((n) => (
                <option key={n.id} value={n.id}>
                  {n.codigo} {n.nome}
                </option>
              ))}
            </select>
          </label>
          <label>
            Unidade
            <input
              value={form.unidade}
              onChange={(e) => setForm({ ...form, unidade: e.target.value })}
              required
            />
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
            Quantidade
            <input
              type="number"
              step="0.000001"
              value={form.quantidade}
              onChange={(e) => setForm({ ...form, quantidade: e.target.value })}
              required
            />
          </label>
          <label>
            Custo unitário (R$)
            <input
              type="number"
              step="0.01"
              value={form.custo_unitario}
              onChange={(e) => setForm({ ...form, custo_unitario: e.target.value })}
              required
            />
          </label>
          <div className="span-2 form-actions">
            <button className="btn btn-primary" type="submit">
              Adicionar item
            </button>
          </div>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>EAP</th>
            <th>Descrição</th>
            <th>Un.</th>
            <th className="num">Qtd</th>
            <th className="num">Custo unit.</th>
            <th className="num">Custo total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {itens.map((it) => {
            const e = eap.find((n) => n.id === it.eap_id);
            return (
              <tr key={it.id}>
                <td>{e ? `${e.codigo}` : '—'}</td>
                <td>{it.descricao}</td>
                <td>{it.unidade}</td>
                <td className="num">{num(it.quantidade, 4)}</td>
                <td className="num">{brl(it.custo_unitario)}</td>
                <td className="num">{brl(it.custo_total)}</td>
                <td>
                  {isDraft && (
                    <button className="btn-link danger" onClick={() => removeItem(it.id)}>
                      Remover
                    </button>
                  )}
                </td>
              </tr>
            );
          })}
          {itens.length === 0 && (
            <tr>
              <td colSpan={7} className="empty">Sem itens.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
