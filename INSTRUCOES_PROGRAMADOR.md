# Portfólio de Startups — Inatel Startups (Guia de Implementação)

Este pacote contém a seção completa e autônoma do **Portfólio de Startups** do Inatel Startups, pronta para integração na página principal ou uso via repositório GitHub.

---

## 🔗 Links Oficiais do Projeto

- **Repositório GitHub:** [https://github.com/inatelstartups/portfolio-startups](https://github.com/inatelstartups/portfolio-startups)
- **Preview Ao Vivo (GitHub Pages):** [https://inatelstartups.github.io/portfolio-startups/](https://inatelstartups.github.io/portfolio-startups/)

---

## 📁 Estrutura de Arquivos da Pasta

```text
Portfólio - GitHub/
├── index.html                  # Marcação HTML da seção <section id="portfolio"> (72 cards)
├── style.css                   # Folha de estilos completa (variáveis, grid, cards, responsividade)
├── portfolio.js                # Lógica de filtragem por abas, carrossel, swipe mobile e barra de progresso
├── elementos/
│   └── logos/                  # 72 logomarcas otimizadas (recorte óptico + perfil sRGB)
├── INSTRUCOES_PROGRAMADOR.md   # Este guia técnico de implementação e manutenção
└── README.md                   # Documentação do repositório GitHub
```

---

## 🚀 Como Integrar no Projeto Principal

### Opção 1: Integração Direta (HTML + CSS + JS)
1. **Assets (Logos):**
   Copie a pasta `elementos/logos/` mantendo o caminho relativo `elementos/logos/...` (ou ajuste o prefixo nas tags `<img src="elementos/logos/...">`).
2. **HTML:**
   Copie o bloco `<section id="portfolio" class="section">...</section>` do arquivo `index.html` e insira no local correspondente da Home.
3. **CSS:**
   - Caso esteja utilizando o `style.css` completo deste pacote, basta referenciá-lo no `<head>`.
   - Caso vá mesclar em uma folha de estilos já existente, certifique-se de incluir as regras da seção `/* ================= PORTFOLIO & EMPRESAS ================= */` e o bloco final `/* ================= PORTFOLIO CARD REFINEMENTS (DESIGN HARMONY & VERTICAL RHYTHM) ================= */`.
4. **JavaScript:**
   Inclua o script `portfolio.js` antes do fechamento do `</body>`:
   ```html
   <script src="portfolio.js"></script>
   ```

---

### Opção 2: Consumo via Git / Submodule (Atualização Contínua)
Este projeto está versionado no repositório oficial `https://github.com/inatelstartups/portfolio-startups.git`.
Sempre que novas startups, descrições ou logomarcas forem atualizadas pela equipe do Inatel Startups no repositório, basta executar:

```bash
git pull origin main
```

---

## ⚙️ Detalhes Técnicos Importantes

1. **Ordem e Categorias (72 Empresas):**
   Os cards estão organizados em **ordem alfabética (A–Z)** dentro de cada uma das 4 fases identificadas pela classe CSS no elemento `.portfolio-card`:
   - `ideation` (**Ideação** — 12 startups, aba amarela)
   - `pre-incubated` (**Pré-Incubação** — 18 startups, aba roxa)
   - `incubated` (**Incubação** — 10 startups, aba laranja, ativa por padrão no carregamento)
   - `graduated` (**Graduadas** — 32 empresas, aba azul)

2. **Tratamento Óptico das Logomarcas:**
   - As imagens em `elementos/logos/` já foram convertidas para `sRGB` e recortadas com margem óptica individual.
   - Alguns containers `.portfolio-logo-container` possuem classes ou estilos inline específicos (`dark-bg`, `cover-bg`, `style="background-color: #..."`) para garantir contraste perfeito com a cor de fundo original de cada marca. **Mantenha esses atributos inline e classes ao integrar.**

3. **Links Dinâmicos do Airtable:**
   O botão `"Ver lista completa no Airtable"` ao final da seção é atualizado automaticamente pelo `portfolio.js` (objeto `airtableLinks`) de acordo com a aba selecionada pelo usuário.
