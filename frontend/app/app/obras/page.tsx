'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { api, Obra } from '@/lib/api';

export default function ObrasList() {
  const [obras, setObras] = useState<Obra[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Obra[]>('/obras')
      .then(setObras)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Obras</h1>
        <Link href="/app/obras/nova" className="btn btn-primary">
          Nova obra
        </Link>
      </div>

      {loading ? (
        <p>Carregando…</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>UF</th>
              <th>Status</th>
              <th>Início previsto</th>
              <th>Fim previsto</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {obras.map((o) => (
              <tr key={o.id}>
                <td>{o.nome}</td>
                <td>{o.uf}</td>
                <td>
                  <span className={`status status-${o.status}`}>
                    {o.status.replace('_', ' ')}
                  </span>
                </td>
                <td>{o.data_inicio_prevista || '—'}</td>
                <td>{o.data_fim_prevista || '—'}</td>
                <td>
                  <Link href={`/app/obras/${o.id}`}>Abrir</Link>
                </td>
              </tr>
            ))}
            {obras.length === 0 && (
              <tr>
                <td colSpan={6} className="empty">
                  Nenhuma obra cadastrada.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
