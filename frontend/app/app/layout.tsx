'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { api, MeResponse, setToken } from '@/lib/api';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [me, setMe] = useState<MeResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<MeResponse>('/auth/me')
      .then(setMe)
      .catch(() => router.replace('/login'))
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return <div className="app-loading">Carregando…</div>;
  }
  if (!me) return null;

  const isProprietario = me.user.role === 'proprietario';

  function logout() {
    setToken(null);
    router.replace('/login');
  }

  const navItems = [
    { href: '/app', label: 'Dashboard', icon: '▤' },
    { href: '/app/obras', label: 'Obras', icon: '▦' },
    { href: '/app/catalogo/fornecedores', label: 'Fornecedores', icon: '◫' },
    { href: '/app/catalogo/insumos', label: 'Insumos', icon: '◧' },
  ];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-mark" aria-hidden />
          <span>Construtor Total</span>
        </div>
        <nav className="sidebar-nav">
          {navItems.map((it) => (
            <Link
              key={it.href}
              href={it.href}
              className={pathname === it.href ? 'nav-item active' : 'nav-item'}
            >
              <span className="nav-icon">{it.icon}</span>
              {it.label}
            </Link>
          ))}
        </nav>
        <div className="sidebar-foot">
          <div className="user-block">
            <div className="user-nome">{me.user.nome}</div>
            <div className="user-tenant">{me.tenant_nome}</div>
            <div className="user-role">
              {isProprietario ? 'Proprietário' : 'Operacional'}
            </div>
          </div>
          <button className="btn-link" onClick={logout}>
            Sair
          </button>
        </div>
      </aside>
      <main className="app-main">{children}</main>
    </div>
  );
}
