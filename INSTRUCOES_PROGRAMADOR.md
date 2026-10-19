# Portfólio de Startups — Inatel Startups (Guia de Implementação)

Este projeto contém a seção **Portfólio de Startups** do Inatel Startups (72 startups/empresas sincronizadas com o Airtable), já publicada e pronta para ser inserida via **Embed (`<iframe>`)** ou **código-fonte direto**.

---

## 🔗 Links Oficiais do Projeto

- **URL do Frame (GitHub Pages):** [https://inatelstartups.github.io/portfolio-startups/](https://inatelstartups.github.io/portfolio-startups/)
- **Repositório GitHub:** [https://github.com/inatelstartups/portfolio-startups](https://github.com/inatelstartups/portfolio-startups)

---

## ⚡ Opção 1 (Recomendada): Inserir apenas o Código do Frame (`<iframe>`)

Para que futuras atualizações de startups, textos e logomarcas feitas no GitHub apareçam **automaticamente no site** sem precisar mexer no código da página novamente, basta colar o trecho abaixo no local onde a seção de Portfólio deve ser exibida (também disponível no arquivo `CODIGO_EMBED_IFRAME.html`):

```html
<!-- PORTFÓLIO DE STARTUPS — INATEL STARTUPS (AUTO-ATUALIZÁVEL VIA GITHUB) -->
<div id="inatel-portfolio-embed-wrapper" style="width: 100%; overflow: hidden;">
    <iframe
        id="inatel-portfolio-iframe"
        src="https://inatelstartups.github.io/portfolio-startups/"
        title="Portfólio de Startups - Inatel Startups"
        style="width: 100%; min-height: 920px; border: none; display: block; background: transparent;"
        scrolling="no"
        loading="lazy"
        allowtransparency="true"
    ></iframe>
</div>

<script>
    // Ajusta automaticamente a altura do frame ao trocar de aba ou redimensionar a tela (sem barra de rolagem interna)
    window.addEventListener('message', function (event) {
        if (event.data && event.data.type === 'inatel-portfolio-resize' && event.data.height) {
            var iframe = document.getElementById('inatel-portfolio-iframe');
            if (iframe) {
                iframe.style.height = event.data.height + 'px';
            }
        }
    });
</script>
```

> **Como funciona o redimensionamento automático:** O `portfolio.js` dentro do frame possui um `ResizeObserver` que envia via `postMessage` a altura exata da seção sempre que a página carrega, muda de tamanho (desktop/mobile) ou troca de aba (*Ideação*, *Pré-Incubação*, *Incubação*, *Graduadas*), evitando barras de rolagem internas.

---

## 🧩 Opção 2: Integração Direta no Código-Fonte (HTML + CSS + JS)

Caso prefira incorporar diretamente no código da página em vez de usar `<iframe>`:

1. **Assets (Logos):** Copie a pasta `elementos/logos/` mantendo o caminho relativo `elementos/logos/...`.
2. **HTML:** Copie a `<section id="portfolio" class="section">...</section>` do arquivo `index.html`.
3. **CSS:** Inclua os estilos da seção de portfólio presentes no `style.css` (mantendo as classes `.dark-bg`, `.cover-bg` e os `style="background-color: ..."` inline de cada `.portfolio-logo-container`).
4. **JS:** Inclua o script `portfolio.js` antes do fechamento do `</body>`.
5. **Atualizações via Git:** Para puxar novas atualizações do repositório:
   ```bash
   git pull origin main
   ```
