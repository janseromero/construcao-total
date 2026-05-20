'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, setToken } from '@/lib/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { access_token } = await api.post<{ access_token: string }>('/auth/login', {
        email,
        password,
      });
      setToken(access_token);
      router.replace('/app');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Erro ao entrar');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-shell">
      <form className="auth-card" onSubmit={submit}>
        <div className="brand" style={{ marginBottom: 24 }}>
          <span className="brand-mark" aria-hidden />
          <span className="brand-name">Construtor Total</span>
        </div>
        <h1 className="auth-title">Entrar</h1>
        <label>
          E-mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Senha
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {error && <div className="form-error">{error}</div>}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Entrando…' : 'Entrar'}
        </button>
        <p className="auth-footer">
          Ainda não tem conta? <Link href="/signup">Criar conta</Link>
        </p>
      </form>
    </main>
  );
}
