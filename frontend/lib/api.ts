/**
 * Cliente HTTP minimal para a API do Construtor Total.
 * Lê token do localStorage e injeta Authorization automaticamente.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export class ApiError extends Error {
  status: number;
  detail: unknown;
  constructor(status: number, detail: unknown, message: string) {
    super(message);
    this.status = status;
    this.detail = detail;
  }
}

function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return window.localStorage.getItem('ct_token');
}

export function setToken(token: string | null) {
  if (typeof window === 'undefined') return;
  if (token === null) window.localStorage.removeItem('ct_token');
  else window.localStorage.setItem('ct_token', token);
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    cache: 'no-store',
  });

  if (res.status === 204) return undefined as T;

  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const msg = (data && (data.detail || data.message)) || res.statusText;
    throw new ApiError(res.status, data, typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
  return data as T;
}

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
  put: <T>(path: string, body?: unknown) => request<T>('PUT', path, body),
  delete: <T = void>(path: string) => request<T>('DELETE', path),
};

// ---- Types compartilhados ----

export type Role = 'proprietario' | 'operacional';

export interface MeResponse {
  user: { id: string; tenant_id: string; email: string; nome: string; role: Role; ativo: boolean };
  tenant_nome: string;
}

export interface Obra {
  id: string;
  nome: string;
  endereco: string | null;
  uf: string;
  data_inicio_prevista: string | null;
  data_fim_prevista: string | null;
  area_total_construida: string | null;
  area_terreno: string | null;
  em_afetacao: boolean;
  status: 'planejamento' | 'em_obra' | 'concluida' | 'pausada';
}

export interface Unidade {
  id: string;
  obra_id: string;
  tipologia_id: string | null;
  identificador: string;
  andar: number | null;
  bloco: string | null;
  fracao_ideal: string;
  area_privativa_m2: string;
}

export interface Tipologia {
  id: string;
  obra_id: string;
  nome: string;
  area_privativa_m2: string;
  area_comum_proporcional_m2: string;
  descricao: string | null;
}

export interface EAPNode {
  id: string;
  obra_id: string;
  parent_id: string | null;
  codigo: string;
  nome: string;
  nivel: number;
  ordem: number;
}

export interface Fornecedor {
  id: string;
  cnpj_cpf: string | null;
  nome: string;
  tipo: 'material' | 'servico' | 'equipamento' | 'misto';
  contato: string | null;
  observacoes: string | null;
}

export interface Insumo {
  id: string;
  codigo: string;
  descricao: string;
  unidade: string;
  tipo: 'material' | 'mao_obra' | 'equipamento';
  sinapi_codigo: string | null;
  custo_unitario_referencia: string;
}

export interface NotaFiscalItem {
  id: string;
  descricao: string;
  unidade: string;
  quantidade: string;
  valor_unitario: string;
  valor_total: string;
}

export interface NotaFiscal {
  id: string;
  obra_id: string | null;
  fornecedor_id: string;
  numero: string;
  data_emissao: string;
  valor_total: string;
  status:
    | 'pendente_apropriacao'
    | 'parcialmente_apropriada'
    | 'totalmente_apropriada'
    | 'cancelada';
  itens: NotaFiscalItem[];
}

export interface CustoUnidade {
  unidade_id: string;
  identificador: string;
  area_privativa_m2: string;
  fracao_ideal: string;
  custo_acumulado: string;
  custo_por_m2: string;
}

export interface MargemUnidade {
  unidade_id: string;
  identificador: string;
  custo_acumulado: string;
  preco_venda: string | null;
  margem_valor: string | null;
  margem_percentual: string | null;
}

export interface Venda {
  id: string;
  unidade_id: string;
  comprador_id: string | null;
  preco_tabela: string;
  preco_venda_final: string | null;
  data_venda: string | null;
  status: 'disponivel' | 'reservada' | 'vendida' | 'distratada';
  observacoes: string | null;
}

export interface Orcamento {
  id: string;
  obra_id: string;
  versao: number;
  nome: string;
  status: 'rascunho' | 'aprovado' | 'superado';
  data_aprovacao: string | null;
  custo_total_calculado: string;
}

export interface ResumoExecutivo {
  vgv: number;
  custo_total: number;
  margem_total: number;
  margem_percentual: number | null;
  unidades_total: number;
  unidades_vendidas: number;
}
