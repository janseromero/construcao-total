'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api, setToken } from '@/lib/api';

export default function SignupPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    construtora_nome: '',
    cnpj: '',
    user_nome: '',
    email: '',
    password: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  function up<K extends keyof typeof form>(k: K, v: string) {
    setForm((s) => ({ ...s, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const { access_token } = await api.post<{ access_token: string }>('/auth/signup', form);
      setToken(access_token);
      router.replace('/app');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Erro ao criar conta');
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
        <h1 className="auth-title">Criar conta</h1>
        <label>
          Nome da construtora
          <input
            value={form.construtora_nome}
            onChange={(e) => up('construtora_nome', e.target.value)}
            required
            minLength={2}
          />
        </label>
        <label>
          CNPJ
          <input value={form.cnpj} onChange={(e) => up('cnpj', e.target.value)} required />
        </label>
        <label>
          Seu nome
          <input
            value={form.user_nome}
            onChange={(e) => up('user_nome', e.target.value)}
            required
            minLength={2}
          />
        </label>
        <label>
          E-mail
          <input
            type="email"
            value={form.email}
            onChange={(e) => up('email', e.target.value)}
            required
          />
        </label>
        <label>
          Senha (mínimo 8 caracteres)
          <input
            type="password"
            value={form.password}
            onChange={(e) => up('password', e.target.value)}
            required
            minLength={8}
          />
        </label>
        {error && <div className="form-error">{error}</div>}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Criando…' : 'Criar conta'}
        </button>
        <p className="auth-footer">
          Já tem conta? <Link href="/login">Entrar</Link>
        </p>
      </form>
    </main>
  );
}
