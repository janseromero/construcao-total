'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { api, Obra } from '@/lib/api';

export default function Dashboard() {
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
        <h1>Dashboard</h1>
        <Link href="/app/obras/nova" className="btn btn-primary">
          Nova obra
        </Link>
      </div>

      <div className="stat-row">
        <div className="stat">
          <div className="stat-label">Obras cadastradas</div>
          <div className="stat-value">{loading ? '…' : obras.length}</div>
        </div>
        <div className="stat">
          <div className="stat-label">Obras em execução</div>
          <div className="stat-value">
            {loading ? '…' : obras.filter((o) => o.status === 'em_obra').length}
          </div>
        </div>
        <div className="stat">
          <div className="stat-label">Obras em planejamento</div>
          <div className="stat-value">
            {loading ? '…' : obras.filter((o) => o.status === 'planejamento').length}
          </div>
        </div>
      </div>

      <section className="panel">
        <h2 className="panel-title">Suas obras</h2>
        {!loading && obras.length === 0 && (
          <p className="empty">
            Você ainda não tem nenhuma obra. <Link href="/app/obras/nova">Criar a primeira</Link>.
          </p>
        )}
        <ul className="obra-list">
          {obras.map((o) => (
            <li key={o.id}>
              <Link href={`/app/obras/${o.id}`} className="obra-row">
                <span className="obra-nome">{o.nome}</span>
                <span className={`status status-${o.status}`}>{o.status.replace('_', ' ')}</span>
                <span className="obra-uf">{o.uf}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
