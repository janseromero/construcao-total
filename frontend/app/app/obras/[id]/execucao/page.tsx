'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, EAPNode, Fornecedor, NotaFiscal } from '@/lib/api';
import { brl } from '@/lib/format';

export default function ExecucaoPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [nfs, setNfs] = useState<NotaFiscal[]>([]);
  const [fornecedores, setFornecedores] = useState<Fornecedor[]>([]);
  const [eap, setEap] = useState<EAPNode[]>([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    fornecedor_id: '',
    numero: '',
    data_emissao: '',
    valor_total: '',
    descricao: '',
  });
  const [appropriating, setAppropriating] = useState<{
    nfId: string;
    itemId: string;
    valorItem: string;
  } | null>(null);
  const [apropForm, setApropForm] = useState({ eap_id: '', valor: '' });

  function reload() {
    if (!id) return;
    api.get<NotaFiscal[]>(`/notas-fiscais?obra_id=${id}`).then(setNfs);
  }

  useEffect(() => {
    reload();
    api.get<Fornecedor[]>('/fornecedores').then(setFornecedores);
    if (id) api.get<EAPNode[]>(`/obras/${id}/eap`).then(setEap);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function criarNF(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;
    await api.post('/notas-fiscais', {
      obra_id: id,
      fornecedor_id: form.fornecedor_id,
      numero: form.numero,
      data_emissao: form.data_emissao,
      valor_total: form.valor_total,
      itens: [
        {
          descricao: form.descricao || 'Item',
          unidade: 'vb',
          quantidade: '1',
          valor_unitario: form.valor_total,
          valor_total: form.valor_total,
        },
      ],
    });
    setForm({ fornecedor_id: '', numero: '', data_emissao: '', valor_total: '', descricao: '' });
    setCreating(false);
    reload();
  }

  async function apropriar(e: React.FormEvent) {
    e.preventDefault();
    if (!appropriating) return;
    try {
      await api.post('/apropriacoes', {
        obra_id: id,
        eap_id: apropForm.eap_id,
        origem_tipo: 'nota_fiscal_item',
        origem_id: appropriating.itemId,
        valor: apropForm.valor,
        data_competencia: new Date().toISOString().slice(0, 10),
      });
      setAppropriating(null);
      setApropForm({ eap_id: '', valor: '' });
      reload();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Erro');
    }
  }

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">Notas fiscais</h2>
        <button className="btn btn-primary" onClick={() => setCreating(!creating)}>
          {creating ? 'Cancelar' : 'Nova NF'}
        </button>
      </div>

      {creating && (
        <form className="form-grid panel" onSubmit={criarNF}>
          <label>
            Fornecedor
            <select
              value={form.fornecedor_id}
              onChange={(e) => setForm({ ...form, fornecedor_id: e.target.value })}
              required
            >
              <option value="">— escolher —</option>
              {fornecedores.map((f) => (
                <option key={f.id} value={f.id}>{f.nome}</option>
              ))}
            </select>
          </label>
          <label>
            Número
            <input
              value={form.numero}
              onChange={(e) => setForm({ ...form, numero: e.target.value })}
              required
            />
          </label>
          <label>
            Data emissão
            <input
              type="date"
              value={form.data_emissao}
              onChange={(e) => setForm({ ...form, data_emissao: e.target.value })}
              required
            />
          </label>
          <label>
            Valor total (R$)
            <input
              type="number"
              step="0.01"
              value={form.valor_total}
              onChange={(e) => setForm({ ...form, valor_total: e.target.value })}
              required
            />
          </label>
          <label className="span-2">
            Descrição do item (será criado 1 item único)
            <input
              value={form.descricao}
              onChange={(e) => setForm({ ...form, descricao: e.target.value })}
            />
          </label>
          <div className="span-2 form-actions">
            <button type="submit" className="btn btn-primary">Salvar NF</button>
          </div>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Número</th>
            <th>Data</th>
            <th className="num">Valor</th>
            <th>Status</th>
            <th>Itens</th>
          </tr>
        </thead>
        <tbody>
          {nfs.map((nf) => (
            <tr key={nf.id}>
              <td>{nf.numero}</td>
              <td>{nf.data_emissao}</td>
              <td className="num">{brl(nf.valor_total)}</td>
              <td>
                <span className={`status status-${nf.status}`}>{nf.status.replace(/_/g, ' ')}</span>
              </td>
              <td>
                {nf.itens.map((it) => (
                  <div key={it.id} className="nf-item">
                    <span>{it.descricao}</span>
                    <span className="num">{brl(it.valor_total)}</span>
                    <button
                      className="btn-link"
                      onClick={() =>
                        setAppropriating({
                          nfId: nf.id,
                          itemId: it.id,
                          valorItem: it.valor_total,
                        })
                      }
                    >
                      Apropriar
                    </button>
                  </div>
                ))}
              </td>
            </tr>
          ))}
          {nfs.length === 0 && (
            <tr>
              <td colSpan={5} className="empty">Nenhuma NF lançada.</td>
            </tr>
          )}
        </tbody>
      </table>

      {appropriating && (
        <div className="modal-backdrop" onClick={() => setAppropriating(null)}>
          <form className="modal" onClick={(e) => e.stopPropagation()} onSubmit={apropriar}>
            <h3>Apropriar item</h3>
            <p>Valor do item: {brl(appropriating.valorItem)}</p>
            <label>
              EAP
              <select
                value={apropForm.eap_id}
                onChange={(e) => setApropForm({ ...apropForm, eap_id: e.target.value })}
                required
              >
                <option value="">— escolher —</option>
                {eap.map((n) => (
                  <option key={n.id} value={n.id}>{n.codigo} {n.nome}</option>
                ))}
              </select>
            </label>
            <label>
              Valor a apropriar (R$)
              <input
                type="number"
                step="0.01"
                value={apropForm.valor}
                onChange={(e) => setApropForm({ ...apropForm, valor: e.target.value })}
                required
              />
            </label>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">Apropriar</button>
              <button type="button" className="btn btn-ghost" onClick={() => setAppropriating(null)}>
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
