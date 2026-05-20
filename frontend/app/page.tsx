export default function Home() {
  return (
    <main className="container">
      <header className="header">
        <div className="brand">
          <span className="brand-mark" aria-hidden />
          <span className="brand-name">Construtor Total</span>
        </div>
        <span className="badge">pré-MVP</span>
      </header>

      <section className="hero">
        <h1>Gestão de obra e custos para construção civil.</h1>
        <p>
          Antes, durante e depois da obra. Orçamento, apropriação de custos, rateio por unidade
          e margem real por apartamento — sem planilha paralela.
        </p>
      </section>

      <section className="grid">
        <article className="card">
          <h2>Pré-obra</h2>
          <p>Orçamento versionado vinculado à EAP, catálogo de insumos e composições.</p>
        </article>
        <article className="card">
          <h2>Durante a obra</h2>
          <p>Notas fiscais, apontamentos de mão de obra e medições apropriados à EAP.</p>
        </article>
        <article className="card">
          <h2>Pós-obra</h2>
          <p>Custo rateado por unidade e margem contra o preço vendido.</p>
        </article>
      </section>

      <footer className="footer">
        <span>v0.1.0 — esqueleto do repositório</span>
      </footer>
    </main>
  );
}
