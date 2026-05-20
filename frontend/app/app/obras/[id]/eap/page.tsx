'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, EAPNode } from '@/lib/api';

export default function EAPPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [nodes, setNodes] = useState<EAPNode[]>([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({ parent_id: '', codigo: '', nome: '', ordem: '0' });

  function reload() {
    if (!id) return;
    api.get<EAPNode[]>(`/obras/${id}/eap`).then(setNodes);
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;
    await api.post(`/obras/${id}/eap`, {
      parent_id: form.parent_id || null,
      codigo: form.codigo,
      nome: form.nome,
      ordem: parseInt(form.ordem || '0', 10),
    });
    setForm({ parent_id: '', codigo: '', nome: '', ordem: '0' });
    setCreating(false);
    reload();
  }

  async function remover(eid: string) {
    if (!confirm('Remover esta etapa e todas as filhas?')) return;
    await api.delete(`/obras/${id}/eap/${eid}`);
    reload();
  }

  // Renderiza árvore
  const byParent: Record<string, EAPNode[]> = {};
  for (const n of nodes) {
    const k = n.parent_id || 'root';
    byParent[k] = byParent[k] || [];
    byParent[k].push(n);
  }
  for (const k of Object.keys(byParent)) {
    byParent[k].sort((a, b) => a.ordem - b.ordem || a.codigo.localeCompare(b.codigo));
  }

  function renderTree(parentId: string, depth = 0): React.ReactNode {
    const list = byParent[parentId] || [];
    return list.map((n) => (
      <div key={n.id}>
        <div className="eap-row" style={{ paddingLeft: depth * 24 + 12 }}>
          <span className="eap-codigo">{n.codigo}</span>
          <span className="eap-nome">{n.nome}</span>
          <button className="btn-link danger" onClick={() => remover(n.id)}>
            Remover
          </button>
        </div>
        {renderTree(n.id, depth + 1)}
      </div>
    ));
  }

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">Estrutura Analítica do Projeto (EAP)</h2>
        <button className="btn btn-primary" onClick={() => setCreating(!creating)}>
          {creating ? 'Cancelar' : 'Nova etapa'}
        </button>
      </div>

      {creating && (
        <form className="form-grid panel" onSubmit={submit}>
          <label>
            Etapa pai
            <select
              value={form.parent_id}
              onChange={(e) => setForm({ ...form, parent_id: e.target.value })}
            >
              <option value="">— Raiz —</option>
              {nodes.map((n) => (
                <option key={n.id} value={n.id}>
                  {n.codigo} {n.nome}
                </option>
              ))}
            </select>
          </label>
          <label>
            Código
            <input
              value={form.codigo}
              onChange={(e) => setForm({ ...form, codigo: e.target.value })}
              required
            />
          </label>
          <label className="span-2">
            Nome
            <input
              value={form.nome}
              onChange={(e) => setForm({ ...form, nome: e.target.value })}
              required
            />
          </label>
          <label>
            Ordem
            <input
              type="number"
              value={form.ordem}
              onChange={(e) => setForm({ ...form, ordem: e.target.value })}
            />
          </label>
          <div className="span-2 form-actions">
            <button type="submit" className="btn btn-primary">Salvar</button>
          </div>
        </form>
      )}

      <div className="panel eap-tree">
        {nodes.length === 0 && <p className="empty">Nenhuma etapa cadastrada.</p>}
        {renderTree('root')}
      </div>
    </div>
  );
}
