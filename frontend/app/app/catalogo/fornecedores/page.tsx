'use client';

import { useEffect, useState } from 'react';
import { api, Fornecedor } from '@/lib/api';

export default function FornecedoresPage() {
  const [list, setList] = useState<Fornecedor[]>([]);
  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    nome: '',
    cnpj_cpf: '',
    tipo: 'material' as Fornecedor['tipo'],
    contato: '',
  });

  function reload() {
    api.get<Fornecedor[]>('/fornecedores').then(setList);
  }

  useEffect(reload, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    await api.post<Fornecedor>('/fornecedores', {
      nome: form.nome,
      cnpj_cpf: form.cnpj_cpf || null,
      tipo: form.tipo,
      contato: form.contato || null,
    });
    setForm({ nome: '', cnpj_cpf: '', tipo: 'material', contato: '' });
    setCreating(false);
    reload();
  }

  async function remover(fid: string) {
    if (!confirm('Remover fornecedor?')) return;
    await api.delete(`/fornecedores/${fid}`);
    reload();
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Fornecedores</h1>
        <button className="btn btn-primary" onClick={() => setCreating(!creating)}>
          {creating ? 'Cancelar' : 'Novo fornecedor'}
        </button>
      </div>

      {creating && (
        <form className="form-grid panel" onSubmit={submit}>
          <label className="span-2">
            Nome
            <input
              value={form.nome}
              onChange={(e) => setForm({ ...form, nome: e.target.value })}
              required
            />
          </label>
          <label>
            CNPJ/CPF
            <input
              value={form.cnpj_cpf}
              onChange={(e) => setForm({ ...form, cnpj_cpf: e.target.value })}
            />
          </label>
          <label>
            Tipo
            <select
              value={form.tipo}
              onChange={(e) =>
                setForm({ ...form, tipo: e.target.value as Fornecedor['tipo'] })
              }
            >
              <option value="material">Material</option>
              <option value="servico">Serviço</option>
              <option value="equipamento">Equipamento</option>
              <option value="misto">Misto</option>
            </select>
          </label>
          <label className="span-2">
            Contato
            <input
              value={form.contato}
              onChange={(e) => setForm({ ...form, contato: e.target.value })}
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
            <th>Nome</th>
            <th>CNPJ/CPF</th>
            <th>Tipo</th>
            <th>Contato</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {list.map((f) => (
            <tr key={f.id}>
              <td>{f.nome}</td>
              <td>{f.cnpj_cpf || '—'}</td>
              <td>{f.tipo}</td>
              <td>{f.contato || '—'}</td>
              <td>
                <button className="btn-link danger" onClick={() => remover(f.id)}>
                  Remover
                </button>
              </td>
            </tr>
          ))}
          {list.length === 0 && (
            <tr>
              <td colSpan={5} className="empty">Nenhum fornecedor cadastrado.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
