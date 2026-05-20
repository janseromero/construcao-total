'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { api, Obra } from '@/lib/api';

const UFS = [
  'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE',
  'PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO',
];

export default function NovaObra() {
  const router = useRouter();
  const [form, setForm] = useState({
    nome: '',
    endereco: '',
    uf: 'SP',
    data_inicio_prevista: '',
    data_fim_prevista: '',
    area_total_construida: '',
    area_terreno: '',
    em_afetacao: false,
    status: 'planejamento' as const,
  });
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setSaving(true);
    try {
      const payload = {
        ...form,
        data_inicio_prevista: form.data_inicio_prevista || null,
        data_fim_prevista: form.data_fim_prevista || null,
        area_total_construida: form.area_total_construida || null,
        area_terreno: form.area_terreno || null,
        endereco: form.endereco || null,
      };
      const obra = await api.post<Obra>('/obras', payload);
      router.replace(`/app/obras/${obra.id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Erro ao criar');
      setSaving(false);
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1>Nova obra</h1>
      </div>

      <form className="form-grid" onSubmit={submit}>
        <label className="span-2">
          Nome
          <input
            value={form.nome}
            onChange={(e) => setForm({ ...form, nome: e.target.value })}
            required
          />
        </label>
        <label className="span-2">
          Endereço
          <input
            value={form.endereco}
            onChange={(e) => setForm({ ...form, endereco: e.target.value })}
          />
        </label>
        <label>
          UF
          <select value={form.uf} onChange={(e) => setForm({ ...form, uf: e.target.value })}>
            {UFS.map((uf) => (
              <option key={uf}>{uf}</option>
            ))}
          </select>
        </label>
        <label>
          Status
          <select
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value as 'planejamento' })}
          >
            <option value="planejamento">Planejamento</option>
            <option value="em_obra">Em obra</option>
            <option value="pausada">Pausada</option>
            <option value="concluida">Concluída</option>
          </select>
        </label>
        <label>
          Início previsto
          <input
            type="date"
            value={form.data_inicio_prevista}
            onChange={(e) => setForm({ ...form, data_inicio_prevista: e.target.value })}
          />
        </label>
        <label>
          Fim previsto
          <input
            type="date"
            value={form.data_fim_prevista}
            onChange={(e) => setForm({ ...form, data_fim_prevista: e.target.value })}
          />
        </label>
        <label>
          Área construída (m²)
          <input
            type="number"
            step="0.01"
            value={form.area_total_construida}
            onChange={(e) => setForm({ ...form, area_total_construida: e.target.value })}
          />
        </label>
        <label>
          Área terreno (m²)
          <input
            type="number"
            step="0.01"
            value={form.area_terreno}
            onChange={(e) => setForm({ ...form, area_terreno: e.target.value })}
          />
        </label>

        {error && <div className="form-error span-2">{error}</div>}

        <div className="span-2 form-actions">
          <button type="submit" className="btn btn-primary" disabled={saving}>
            {saving ? 'Salvando…' : 'Criar obra'}
          </button>
          <button type="button" className="btn btn-ghost" onClick={() => router.back()}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
}
