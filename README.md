# Portfólio de Startups — Inatel Startups

Componente interativo do **Portfólio de Startups** (Ideação, Pré-Incubação, Incubação e Graduadas) integrado às views oficiais do Airtable do Inatel Startups.

## 🔗 Link Público (GitHub Pages)
- **URL de Produção:** `https://inatelstartups.github.io/portfolio-startups/`

---

## 🛠️ Como Integrar na Página Principal (Instruções para o Desenvolvedor)

### Opção 1: Incorporação via `<iframe>` (Recomendado — Atualização Automática)
Ao incorporar via `<iframe>`, qualquer atualização de startups ou logos feita neste repositório reflete automaticamente no site em produção sem necessidade de novo deploy da página principal:

```html
<iframe 
    src="https://inatelstartups.github.io/portfolio-startups/" 
    width="100%" 
    height="780" 
    style="border: none; overflow: hidden; background: transparent;" 
    loading="lazy"
    title="Portfólio de Startups - Inatel Startups">
</iframe>
```

### Opção 2: Integração Nativa (HTML + CSS + JS)
Caso prefira embutir diretamente no código-fonte da página:
1. Copie a pasta `elementos/logos/` para o diretório de assets do projeto.
2. Copie a seção `<section id="portfolio" class="section">...</section>` do arquivo `index.html`.
3. Inclua os estilos de `.portfolio-*` e `.slider-arrow` presentes em `style.css` e o script `portfolio.js`.
4. Para receber atualizações futuras, basta executar `git pull origin main` neste repositório.

---

## 📊 Fontes de Dados (Airtable Views)
- **Ideação:** `https://airtable.com/app9mAZl7zLu7zeZb/shr6lGlyWE9395CtX/tblAEZQFetlB1ThTe`
- **Pré-Incubação:** `https://airtable.com/app9mAZl7zLu7zeZb/shrQMcUOOgtk19ydG/tblAEZQFetlB1ThTe`
- **Incubação:** `https://airtable.com/app9mAZl7zLu7zeZb/shrd6rAzCsgZv2elr/tblAEZQFetlB1ThTe`
- **Graduadas:** `https://airtable.com/app45MMiNeduNXvUx/shrHu5Ku1Q5Phv7WP/tblAEZQFetlB1ThTe`
