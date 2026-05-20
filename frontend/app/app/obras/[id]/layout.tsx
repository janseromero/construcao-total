'use client';

import Link from 'next/link';
import { usePathname, useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { api, MeResponse, Obra } from '@/lib/api';

export default function ObraLayout({ children }: { children: React.ReactNode }) {
  const params = useParams<{ id: string }>();
  const pathname = usePathname();
  const [obra, setObra] = useState<Obra | null>(null);
  const [me, setMe] = useState<MeResponse | null>(null);

  useEffect(() => {
    if (!params?.id) return;
    api.get<Obra>(`/obras/${params.id}`).then(setObra).catch(() => setObra(null));
    api.get<MeResponse>('/auth/me').then(setMe);
  }, [params?.id]);

  if (!obra) return <div className="page"><p>Carregando obra…</p></div>;

  const isProp = me?.user.role === 'proprietario';
  const base = `/app/obras/${obra.id}`;
  const tabs = [
    { href: base, label: 'Visão geral' },
    { href: `${base}/unidades`, label: 'Unidades' },
    { href: `${base}/eap`, label: 'EAP' },
    { href: `${base}/orcamento`, label: 'Orçamento' },
    { href: `${base}/execucao`, label: 'Execução' },
    { href: `${base}/analise`, label: 'Análise' },
    ...(isProp ? [{ href: `${base}/vendas`, label: 'Vendas' }] : []),
  ];

  return (
    <div className="obra-shell">
      <div className="obra-header">
        <div>
          <div className="obra-eyebrow">Obra</div>
          <h1 className="obra-title">{obra.nome}</h1>
          <div className="obra-meta">
            <span>{obra.uf}</span>
            <span className={`status status-${obra.status}`}>
              {obra.status.replace('_', ' ')}
            </span>
            {obra.em_afetacao && <span className="badge">Em afetação</span>}
          </div>
        </div>
      </div>
      <nav className="tabs">
        {tabs.map((t) => (
          <Link
            key={t.href}
            href={t.href}
            className={pathname === t.href ? 'tab active' : 'tab'}
          >
            {t.label}
          </Link>
        ))}
      </nav>
      <div className="obra-body">{children}</div>
    </div>
  );
}
