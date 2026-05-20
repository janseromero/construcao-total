'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, Orcamento } from '@/lib/api';
import { brl } from '@/lib/format';

export default function OrcamentoPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [orcamentos, setOrcamentos] = useState<Orcamento[]>([]);
  const [creating, setCreating] = useState(false);
  const [nome, setNome] = useState('');

  function reload() {
    if (!id) return;
    api.get<Orcamento[]>(`/obras/${id}/orcamentos`).then(setOrcamentos);
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function novo(e: React.FormEvent) {
    e.preventDefault();
    await api.post<Orcamento>(`/obras/${id}/orcamentos`, { nome });
    setNome('');
    setCreating(false);
    reload();
  }

  async function aprovar(oid: string) {
    if (!confirm('Aprovar este orçamento? Versão anterior aprovada será marcada como superada.'))
      return;
    await api.post(`/obras/${id}/orcamentos/${oid}/aprovar`);
    reload();
  }

  async function remover(oid: string) {
    if (!confirm('Remover orçamento?')) return;
    try {
      await api.delete(`/obras/${id}/orcamentos/${oid}`);
      reload();
    } catch (err: unknown) {
      alert(err instanceof Error ? err.message : 'Erro');
    }
  }

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">Orçamentos</h2>
        <button className="btn btn-primary" onClick={() => setCreating(!creating)}>
          {creating ? 'Cancelar' : 'Novo orçamento'}
        </button>
      </div>

      {creating && (
        <form className="form-grid panel" onSubmit={novo}>
          <label className="span-2">
            Nome (ex.: Orçamento base, Revisão 1 — pós-fundação)
            <input value={nome} onChange={(e) => setNome(e.target.value)} required />
          </label>
          <div className="form-actions span-2">
            <button type="submit" className="btn btn-primary">Criar</button>
          </div>
        </form>
      )}

      <table className="data-table">
        <thead>
          <tr>
            <th>Versão</th>
            <th>Nome</th>
            <th>Status</th>
            <th className="num">Custo total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {orcamentos.map((o) => (
            <tr key={o.id}>
              <td>v{o.versao}</td>
              <td>{o.nome}</td>
              <td>
                <span className={`status status-${o.status}`}>{o.status}</span>
              </td>
              <td className="num">{brl(o.custo_total_calculado)}</td>
              <td>
                {o.status === 'rascunho' && (
                  <>
                    <a href={`/app/obras/${id}/orcamento/${o.id}`}>Editar itens</a>
                    {' · '}
                    <button className="btn-link" onClick={() => aprovar(o.id)}>
                      Aprovar
                    </button>
                    {' · '}
                    <button className="btn-link danger" onClick={() => remover(o.id)}>
                      Remover
                    </button>
                  </>
                )}
                {o.status !== 'rascunho' && (
                  <a href={`/app/obras/${id}/orcamento/${o.id}`}>Ver</a>
                )}
              </td>
            </tr>
          ))}
          {orcamentos.length === 0 && (
            <tr>
              <td colSpan={5} className="empty">Nenhum orçamento criado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
