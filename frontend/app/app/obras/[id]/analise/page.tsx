'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, CustoUnidade, MargemUnidade } from '@/lib/api';
import { brl, num, pct } from '@/lib/format';

interface OrcadoReal {
  eap_id: string;
  codigo: string;
  nome: string;
  orcado: string;
  realizado: string;
  delta: string;
  percentual: string | null;
}

export default function AnalisePage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [custo, setCusto] = useState<CustoUnidade[]>([]);
  const [margem, setMargem] = useState<MargemUnidade[] | null>(null);
  const [margemForbidden, setMargemForbidden] = useState(false);
  const [orcReal, setOrcReal] = useState<OrcadoReal[]>([]);
  const [recalculando, setRecalculando] = useState(false);

  function reload() {
    if (!id) return;
    api.get<CustoUnidade[]>(`/obras/${id}/analise/custo-por-unidade`).then(setCusto);
    api
      .get<MargemUnidade[]>(`/obras/${id}/analise/margem-por-unidade`)
      .then(setMargem)
      .catch((err) => {
        if (err?.status === 403) setMargemForbidden(true);
      });
    api.get<OrcadoReal[]>(`/obras/${id}/analise/orcado-vs-realizado`).then(setOrcReal);
  }

  useEffect(() => {
    reload();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  async function recalc() {
    setRecalculando(true);
    try {
      await api.post(`/obras/${id}/rateio/recalcular`);
      reload();
    } finally {
      setRecalculando(false);
    }
  }

  return (
    <div className="overview">
      <div className="panel-header">
        <h2 className="panel-title">Análise</h2>
        <button className="btn btn-ghost" onClick={recalc} disabled={recalculando}>
          {recalculando ? 'Recalculando…' : 'Recalcular rateio'}
        </button>
      </div>

      <section className="panel">
        <h3 className="subpanel-title">Custo por unidade</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Unidade</th>
              <th className="num">Área (m²)</th>
              <th className="num">Fração ideal</th>
              <th className="num">Custo acumulado</th>
              <th className="num">Custo / m²</th>
            </tr>
          </thead>
          <tbody>
            {custo.map((c) => (
              <tr key={c.unidade_id}>
                <td>{c.identificador}</td>
                <td className="num">{num(c.area_privativa_m2)}</td>
                <td className="num">{num(c.fracao_ideal, 6)}</td>
                <td className="num">{brl(c.custo_acumulado)}</td>
                <td className="num">{brl(c.custo_por_m2)}</td>
              </tr>
            ))}
            {custo.length === 0 && (
              <tr>
                <td colSpan={5} className="empty">Sem dados.</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      <section className="panel">
        <h3 className="subpanel-title">Margem por unidade</h3>
        {margemForbidden ? (
          <p className="empty">Visível apenas para o perfil Proprietário.</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Unidade</th>
                <th className="num">Custo</th>
                <th className="num">Preço venda</th>
                <th className="num">Margem (R$)</th>
                <th className="num">Margem (%)</th>
              </tr>
            </thead>
            <tbody>
              {(margem || []).map((m) => (
                <tr key={m.unidade_id}>
                  <td>{m.identificador}</td>
                  <td className="num">{brl(m.custo_acumulado)}</td>
                  <td className="num">{brl(m.preco_venda)}</td>
                  <td className="num">{brl(m.margem_valor)}</td>
                  <td className="num">{pct(m.margem_percentual)}</td>
                </tr>
              ))}
              {margem && margem.length === 0 && (
                <tr>
                  <td colSpan={5} className="empty">Sem dados.</td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </section>

      <section className="panel">
        <h3 className="subpanel-title">Orçado × Realizado (por etapa raiz da EAP)</h3>
        <table className="data-table">
          <thead>
            <tr>
              <th>Etapa</th>
              <th className="num">Orçado</th>
              <th className="num">Realizado</th>
              <th className="num">Δ</th>
              <th className="num">%</th>
            </tr>
          </thead>
          <tbody>
            {orcReal.map((r) => (
              <tr key={r.eap_id}>
                <td>{r.codigo} — {r.nome}</td>
                <td className="num">{brl(r.orcado)}</td>
                <td className="num">{brl(r.realizado)}</td>
                <td className={`num ${parseFloat(r.delta) > 0 ? 'warn' : ''}`}>
                  {brl(r.delta)}
                </td>
                <td className="num">{pct(r.percentual)}</td>
              </tr>
            ))}
            {orcReal.length === 0 && (
              <tr>
                <td colSpan={5} className="empty">Sem orçamento aprovado.</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </div>
  );
}
