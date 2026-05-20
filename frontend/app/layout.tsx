import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Construtor Total',
  description: 'Gestão de obra e custos para construção civil no Brasil.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
