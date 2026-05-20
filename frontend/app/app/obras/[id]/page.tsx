'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api, Obra, Unidade, EAPNode, ResumoExecutivo } from '@/lib/api';
import { brl, pct } from '@/lib/format';

export default function ObraOverview() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [obra, setObra] = useState<Obra | null>(null);
  const [unidades, setUnidades] = useState<Unidade[]>([]);
  const [eap, setEap] = useState<EAPNode[]>([]);
  const [resumo, setResumo] = useState<ResumoExecutivo | null>(null);
  const [resumoForbidden, setResumoForbidden] = useState(false);

  useEffect(() => {
    if (!id) return;
    api.get<Obra>(`/obras/${id}`).then(setObra);
    api.get<Unidade[]>(`/obras/${id}/unidades`).then(setUnidades);
    api.get<EAPNode[]>(`/obras/${id}/eap`).then(setEap);
    api
      .get<ResumoExecutivo>(`/obras/${id}/analise/resumo`)
      .then(setResumo)
      .catch((err) => {
        if (err?.status === 403) setResumoForbidden(true);
      });
  }, [id]);

  if (!obra) return <p>Carregando…</p>;

  const somaFracao = unidades.reduce((s, u) => s + parseFloat(u.fracao_ideal || '0'), 0);
  const somaArea = unidades.reduce((s, u) => s + parseFloat(u.area_privativa_m2 || '0'), 0);

  return (
    <div className="overview">
      <div className="stat-row">
        <div className="stat">
          <div className="stat-label">Unidades</div>
          <div className="stat-value">{unidades.length}</div>
        </div>
        <div className="stat">
          <div className="stat-label">Etapas EAP</div>
          <div className="stat-value">{eap.length}</div>
        </div>
        <div className="stat">
          <div className="stat-label">Soma fração ideal</div>
          <div className="stat-value">
            {somaFracao.toLocaleString('pt-BR', { maximumFractionDigits: 4 })}
            {Math.abs(somaFracao - 1) > 0.0001 && (
              <span className="stat-warn"> ⚠ ≠ 1,0000</span>
            )}
          </div>
        </div>
        <div className="stat">
          <div className="stat-label">Área privativa total (m²)</div>
          <div className="stat-value">
            {somaArea.toLocaleString('pt-BR', { maximumFractionDigits: 2 })}
          </div>
        </div>
      </div>

      <section className="panel">
        <h2 className="panel-title">Resumo financeiro</h2>
        {resumoForbidden ? (
          <p className="empty">
            Resumo financeiro disponível apenas para o perfil Proprietário.
          </p>
        ) : !resumo ? (
          <p>Carregando…</p>
        ) : (
          <div className="stat-row">
            <div className="stat">
              <div className="stat-label">VGV</div>
              <div className="stat-value">{brl(resumo.vgv)}</div>
            </div>
            <div className="stat">
              <div className="stat-label">Custo total</div>
              <div className="stat-value">{brl(resumo.custo_total)}</div>
            </div>
            <div className="stat">
              <div className="stat-label">Margem</div>
              <div className="stat-value">{brl(resumo.margem_total)}</div>
            </div>
            <div className="stat">
              <div className="stat-label">Margem %</div>
              <div className="stat-value">{pct(resumo.margem_percentual)}</div>
            </div>
            <div className="stat">
              <div className="stat-label">Vendidas</div>
              <div className="stat-value">
                {resumo.unidades_vendidas} / {resumo.unidades_total}
              </div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
