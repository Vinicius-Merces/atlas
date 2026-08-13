import { absolute, journal, residences, site } from "./content.js";

const nav = [
  ["/residencias", "Residências"],
  ["/localizacao", "Localização"],
  ["/caderno", "Caderno"],
];

const icons = {
  arrow: `<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 10h13M11 5l5 5-5 5"/></svg>`,
  mark: `<svg viewBox="0 0 52 52" aria-hidden="true"><path d="M8 42 26 8l18 34M15 30h22"/></svg>`,
};

function header(path) {
  const links = nav.map(([href, label]) => `<a href="${href}"${path.startsWith(href) ? ' aria-current="page"' : ""}>${label}</a>`).join("");
  return `<header class="site-header"><a class="brand" href="/" aria-label="Asteria Residences — início">${icons.mark}<span>ASTERIA<small>RESIDENCES</small></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav"><span class="menu-icon"></span><span class="menu-icon"></span><span class="sr-only menu-label">Abrir menu</span></button><nav id="primary-nav" aria-label="Navegação principal">${links}<a class="nav-cta" href="/contato">Agendar visita</a></nav></header>`;
}

function footer() {
  return `<footer class="site-footer"><div><a class="brand brand--footer" href="/">${icons.mark}<span>ASTERIA<small>RESIDENCES</small></span></a><p>Doze residências autorais entre a cidade e a paisagem.</p></div><div><strong>Visitas</strong><a href="tel:+551130001212">${site.phone}</a><a href="mailto:${site.email}">${site.email}</a></div><div><strong>Informações</strong><a href="/privacidade">Privacidade</a><a href="/termos">Termos de uso</a></div><p class="footer-note">Empreendimento fictício criado para o benchmark P4 do ATLAS. Imagens ilustrativas.</p></footer>`;
}

function layout({ path, title, description, body, schema = [], indexable = true }) {
  const canonical = indexable ? absolute(path) : null;
  const graph = [
    { "@type": "Organization", "@id": `${absolute("/")}#organization`, name: site.name, url: absolute("/"), email: site.email, telephone: site.phone },
    { "@type": "WebSite", "@id": `${absolute("/")}#website`, url: absolute("/"), name: site.name, inLanguage: "pt-BR", publisher: { "@id": `${absolute("/")}#organization` } },
    { "@type": "WebPage", "@id": `${canonical || absolute(path)}#webpage`, url: canonical || absolute(path), name: title, description, inLanguage: "pt-BR", isPartOf: { "@id": `${absolute("/")}#website` } },
    ...schema,
  ];
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f2eee5"><title>${title}</title><meta name="description" content="${description}">${canonical ? `<link rel="canonical" href="${canonical}">` : ""}<meta name="robots" content="${indexable ? "index,follow,max-image-preview:large" : "noindex,nofollow"}"><meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:title" content="${title}"><meta property="og:description" content="${description}">${canonical ? `<meta property="og:url" content="${canonical}">` : ""}<link rel="stylesheet" href="/styles.css"><script type="application/ld+json">${JSON.stringify({ "@context": "https://schema.org", "@graph": graph }).replace(/</g, "\\u003c")}</script><script src="/app.js" defer></script></head><body data-path="${path}"><a class="skip-link" href="#conteudo">Pular para o conteúdo</a>${header(path)}<main id="conteudo">${body}</main>${footer()}</body></html>`;
}

function eyebrow(text) { return `<p class="eyebrow">${text}</p>`; }
function arrowLink(href, label, cls = "text-link") { return `<a class="${cls}" href="${href}">${label}${icons.arrow}</a>`; }

function home() {
  const body = `<section class="hero"><div class="hero-copy">${eyebrow("Serra Clara · 23°31’S")}<h1>Doze casas.<br><em>Um horizonte</em><br>sem excessos.</h1><p>Asteria reúne arquitetura precisa, natureza preservada e acesso metropolitano em uma coleção residencial de apenas doze endereços.</p>${arrowLink("/residencias", "Conheça as residências", "button-link")}</div><figure class="hero-media"><img src="/assets/hero.webp" width="1440" height="900" alt="Residência Asteria em pedra clara voltada para um jardim ao entardecer" fetchpriority="high"><figcaption><span>Casa Pátio</span><span>Residência 01 / 12</span></figcaption></figure><div class="hero-index" aria-hidden="true"><span>12</span><small>residências<br>autorais</small></div></section>
  <section class="principle section-grid"><div>${eyebrow("A medida do essencial")}<h2>Privacidade não precisa significar distância.</h2></div><div><p class="lead">A 34 minutos do centro financeiro, Asteria troca o ruído por um desenho de baixa densidade: casas independentes, percursos sombreados e paisagem contínua.</p>${arrowLink("/localizacao", "Explorar a localização")}</div></section>
  <section class="residence-preview"><div class="section-heading">${eyebrow("Coleção residencial")}<h2>Três maneiras de habitar a mesma paisagem.</h2></div><div class="residence-ledger">${residences.slice(0,3).map((r) => `<a href="/residencias/${r.slug}" class="residence-row"><span>${r.number}</span><strong>${r.name}</strong><em>${r.type}</em><span>${r.area}</span>${icons.arrow}</a>`).join("")}</div></section>
  <section class="material-story"><figure><img src="/assets/interior.webp" width="1200" height="900" loading="lazy" alt="Interior Asteria com madeira natural, pedra clara e vista para o jardim"></figure><div>${eyebrow("Matéria e permanência")}<h2>Feita para ganhar caráter, não para seguir uma estação.</h2><p>Pedra local, madeira de origem rastreada, ventilação cruzada e fachadas protegidas reduzem manutenção e preservam o conforto ao longo do ano.</p><dl><div><dt>38%</dt><dd>da área total preservada como paisagem permeável</dd></div><div><dt>12</dt><dd>casas, sem repetição de planta</dd></div></dl></div></section>
  <section class="journal-preview"><div class="section-heading">${eyebrow("Caderno Asteria")}<h2>Notas sobre arquitetura, lugar e tempo.</h2></div><div class="journal-list">${journal.slice(0,2).map((a,i)=>`<a href="/caderno/${a.slug}" class="journal-item"><span>0${i+1}</span><div><small>${a.category}</small><h3>${a.title}</h3><p>${a.dek}</p></div><em>${a.read}</em></a>`).join("")}</div>${arrowLink("/caderno", "Ver todos os artigos")}</section>
  <section class="closing-cta"><div>${eyebrow("Visita individual")}<h2>Alguns lugares pedem tempo para serem compreendidos.</h2></div><div><p>Converse com nossa curadoria e agende uma visita no seu ritmo, com informações completas antes do encontro.</p>${arrowLink("/contato", "Solicitar uma conversa", "button-link button-link--light")}</div></section>`;
  return layout({ path: "/", title: "Asteria Residences | Doze casas entre cidade e paisagem", description: "Coleção fictícia de doze residências autorais em Serra Clara, com arquitetura precisa, natureza preservada e visitas individuais.", body });
}

function residencesPage() {
  const body = `<section class="page-hero page-hero--residences"><div>${eyebrow("Residências 01—12")}<h1>Uma coleção,<br><em>não uma repetição.</em></h1></div><p>Cada implantação responde à luz, ao terreno e à privacidade. Pátio, Horizonte e Bosque são três famílias arquitetônicas, cada uma reinterpretada em quatro lotes.</p></section><section class="residence-catalog">${residences.map((r,i)=>`<article class="catalog-entry"><div class="catalog-number">${r.number}<small>/ 12</small></div><div><p class="eyebrow">${r.type}</p><h2>${r.name}</h2><p>${r.summary}</p><ul><li>${r.area} privativos</li><li>${r.suites}</li><li>Terreno de ${r.lots}</li></ul>${arrowLink(`/residencias/${r.slug}`, "Ver detalhes")}</div><div class="catalog-plan" aria-hidden="true"><span class="plan-line plan-line--${(i%3)+1}"></span><small>Implantação ${r.number}</small></div></article>`).join("")}</section><section class="closing-cta closing-cta--compact"><div><h2>Disponibilidade é apresentada em conversa individual.</h2></div><div><p>Receba memorial descritivo, condições e agenda de visitas com nossa equipe.</p>${arrowLink("/contato", "Consultar uma residência", "button-link button-link--light")}</div></section>`;
  return layout({ path: "/residencias", title: "Residências | Asteria Residences", description: "Conheça as tipologias Casa Pátio, Casa Horizonte e Casa Bosque, com áreas, suítes e características factuais.", body, schema: [{ "@type": "ItemList", itemListElement: residences.map((r,i)=>({"@type":"ListItem",position:i+1,url:absolute(`/residencias/${r.slug}`),name:r.name})) }] });
}

function residenceDetail(residence) {
  const body = `<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Início</a><span>/</span><a href="/residencias">Residências</a><span>/</span><span aria-current="page">${residence.name}</span></nav><section class="detail-hero"><div class="detail-number">${residence.number}<small>/ 12</small></div><div>${eyebrow(residence.type)}<h1>${residence.name}</h1><p>${residence.summary}</p></div></section><section class="detail-facts" aria-label="Características principais"><div><strong>${residence.area}</strong><span>área privativa</span></div><div><strong>${residence.lots}</strong><span>terreno</span></div><div><strong>${residence.suites.replace(" suítes","")}</strong><span>suítes</span></div><div><strong>${residence.features.at(-1).split(" ")[0]}</strong><span>vagas cobertas</span></div></section><section class="detail-story"><figure><img src="/assets/interior.webp" width="1200" height="900" alt="Sala da ${residence.name} integrada ao jardim" fetchpriority="high"></figure><div>${eyebrow("O desenho")}<h2>Luz e percurso definem a planta.</h2><p>Os ambientes sociais formam uma sequência contínua, enquanto os espaços íntimos preservam silêncio e independência. A estrutura permite adaptações internas sem comprometer a leitura arquitetônica.</p><ul>${residence.features.map(f=>`<li>${f}</li>`).join("")}</ul></div></section><section class="closing-cta"><div>${eyebrow("Conhecer a casa")}<h2>Receba plantas, memorial e disponibilidade.</h2></div><div><p>A equipe Asteria prepara uma apresentação individual da residência, sem compromisso.</p>${arrowLink(`/contato?residencia=${residence.slug}`, "Solicitar apresentação", "button-link button-link--light")}</div></section>`;
  return layout({ path: `/residencias/${residence.slug}`, title: `${residence.name} | Asteria Residences`, description: `${residence.name}: ${residence.area}, ${residence.suites}, terreno de ${residence.lots}. Conheça o projeto e solicite uma apresentação.`, body, schema: [{"@type":"SingleFamilyResidence","@id":`${absolute(`/residencias/${residence.slug}`)}#residence`,name:residence.name,description:residence.summary,floorSize:{"@type":"QuantitativeValue",value:Number.parseInt(residence.area),unitCode:"MTK"},numberOfBedrooms:4,address:{"@type":"PostalAddress",addressLocality:"Serra Clara",addressRegion:"SP",addressCountry:"BR"}}] });
}

function locationPage() {
  const body = `<section class="page-hero page-hero--location"><div>${eyebrow("Serra Clara, SP")}<h1>Perto do que importa.<br><em>Longe do excesso.</em></h1></div><p>Uma localização fictícia desenhada para equilibrar acesso metropolitano, serviços cotidianos e a presença constante da paisagem.</p></section><section class="location-map" aria-label="Tempos estimados a partir de Asteria"><div class="map-art" aria-hidden="true"><span class="route route--one"></span><span class="route route--two"></span><i class="map-pin">A</i></div><div><p class="eyebrow">Tempos estimados</p><dl><div><dt>08 min</dt><dd>Colégio Serra Clara</dd></div><div><dt>12 min</dt><dd>Hospital São Bento</dd></div><div><dt>18 min</dt><dd>Clube de Campo</dd></div><div><dt>34 min</dt><dd>Centro financeiro</dd></div></dl><small>Estimativas em condições normais de tráfego; os tempos podem variar.</small></div></section><section class="place-sequence"><article><span>01</span><h2>Manhã a pé</h2><p>Trilhas sombreadas e comércio de bairro formam um percurso cotidiano de baixa velocidade.</p></article><article><span>02</span><h2>Cidade ao alcance</h2><p>Duas conexões rodoviárias distribuem o trajeto sem atravessar o centro histórico.</p></article><article><span>03</span><h2>Paisagem preservada</h2><p>A cota mais baixa do terreno mantém o corredor verde e protege as vistas principais.</p></article></section><section class="journal-callout">${eyebrow("Guia de localização")}<h2>Um dia possível entre Serra Clara e a cidade.</h2><p>Nosso caderno reúne percursos, serviços e escolhas de implantação que explicam o lugar para além de um ponto no mapa.</p>${arrowLink("/caderno/viver-entre-cidade-e-paisagem", "Ler o guia completo")}</section>`;
  return layout({ path: "/localizacao", title: "Localização e estilo de vida | Asteria Residences", description: "Conheça o contexto fictício de Serra Clara, os tempos estimados de deslocamento e a relação entre Asteria e a paisagem.", body });
}

function journalPage() {
  const body = `<section class="page-hero page-hero--journal"><div>${eyebrow("Caderno Asteria")}<h1>Arquitetura se entende<br><em>também pela conversa.</em></h1></div><p>Ensaios e guias sobre o desenho das casas, a paisagem de Serra Clara e escolhas que permanecem relevantes depois da entrega das chaves.</p></section><section class="journal-index">${journal.map((a,i)=>`<article><a href="/caderno/${a.slug}"><span>0${i+1}</span><div><p class="eyebrow">${a.category} · <time datetime="${a.date}">${new Date(`${a.date}T12:00:00Z`).toLocaleDateString("pt-BR",{day:"2-digit",month:"short",year:"numeric",timeZone:"UTC"})}</time></p><h2>${a.title}</h2><p>${a.dek}</p></div><em>${a.read}</em>${icons.arrow}</a></article>`).join("")}</section>`;
  return layout({ path: "/caderno", title: "Caderno | Asteria Residences", description: "Artigos fictícios sobre arquitetura residencial, materiais, localização e o projeto paisagístico de Asteria.", body, schema:[{"@type":"CollectionPage",name:"Caderno Asteria",hasPart:journal.map(a=>({"@type":"Article",headline:a.title,url:absolute(`/caderno/${a.slug}`),datePublished:a.date}))}] });
}

function articlePage(article) {
  const body = `<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Início</a><span>/</span><a href="/caderno">Caderno</a><span>/</span><span aria-current="page">${article.title}</span></nav><article class="article"><header><p class="eyebrow">${article.category}</p><h1>${article.title}</h1><p class="article-dek">${article.dek}</p><div><time datetime="${article.date}">${new Date(`${article.date}T12:00:00Z`).toLocaleDateString("pt-BR",{day:"2-digit",month:"long",year:"numeric",timeZone:"UTC"})}</time><span>${article.read} de leitura</span></div></header><figure><img src="/assets/interior.webp" width="1200" height="900" alt="Interior Asteria aberto para a paisagem"></figure><div class="article-body"><p class="article-intro">Habitar bem depende menos de acumular conveniências e mais de organizar relações: entre dentro e fora, silêncio e acesso, permanência e transformação.</p>${article.sections.map(([h,p])=>`<section><h2>${h}</h2><p>${p}</p></section>`).join("")}<aside><p>Quer conhecer o lugar com contexto?</p>${arrowLink("/contato", "Agendar uma visita guiada")}</aside></div></article>`;
  return layout({ path:`/caderno/${article.slug}`, title:`${article.title} | Caderno Asteria`, description:article.dek, body, schema:[{"@type":"Article","@id":`${absolute(`/caderno/${article.slug}`)}#article`,headline:article.title,description:article.dek,datePublished:article.date,dateModified:article.date,inLanguage:"pt-BR",author:{"@id":`${absolute("/")}#organization`},publisher:{"@id":`${absolute("/")}#organization`},mainEntityOfPage:{"@id":`${absolute(`/caderno/${article.slug}`)}#webpage`}}] });
}

function contactPage(query) {
  const selected = query.get("residencia") || "";
  const body = `<section class="contact-layout"><div class="contact-intro">${eyebrow("Conversa individual")}<h1>Uma visita começa com as informações certas.</h1><p>Conte o que você procura. Nossa equipe responde em até um dia útil com disponibilidade, materiais e opções de agenda.</p><dl><div><dt>Telefone</dt><dd><a href="tel:+551130001212">${site.phone}</a></dd></div><div><dt>E-mail</dt><dd><a href="mailto:${site.email}">${site.email}</a></dd></div><div><dt>Endereço</dt><dd>${site.address}</dd></div></dl></div><form id="visit-form" novalidate><div class="form-status" id="form-status" role="status" aria-live="polite"></div><div class="field-row"><div class="field"><label for="name">Nome completo</label><input id="name" name="name" autocomplete="name" required minlength="3"><span class="field-error" id="name-error"></span></div><div class="field"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required><span class="field-error" id="email-error"></span></div></div><div class="field-row"><div class="field"><label for="phone">Telefone</label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="(11) 99999-9999"><span class="field-error" id="phone-error"></span></div><div class="field"><label for="interest">Residência de interesse</label><select id="interest" name="interest" required><option value="">Selecione</option>${residences.map(r=>`<option value="${r.slug}"${selected===r.slug?" selected":""}>${r.name} — ${r.area}</option>`).join("")}<option value="a-definir">Ainda estou comparando</option></select><span class="field-error" id="interest-error"></span></div></div><fieldset><legend>Faixa de investimento</legend><div class="choice-row">${[["ate-5m","Até R$ 5 mi"],["5m-7m","R$ 5—7 mi"],["acima-7m","Acima de R$ 7 mi"]].map(([v,l])=>`<label><input type="radio" name="budget" value="${v}" required><span>${l}</span></label>`).join("")}</div><span class="field-error" id="budget-error"></span></fieldset><div class="field"><label for="visitDate">Data preferida <small>(opcional)</small></label><input id="visitDate" name="visitDate" type="date"><span class="field-error" id="visitDate-error"></span></div><div class="field field--hidden" aria-hidden="true"><label for="company">Empresa</label><input id="company" name="company" tabindex="-1" autocomplete="off"></div><label class="consent"><input type="checkbox" name="consent" required><span>Autorizo o contato da equipe Asteria sobre esta solicitação e li a <a href="/privacidade">política de privacidade</a>.</span></label><span class="field-error" id="consent-error"></span><button class="submit-button" type="submit"><span>Solicitar conversa</span>${icons.arrow}</button><p class="form-note">Seus dados não serão usados para comunicações não relacionadas a esta solicitação.</p></form></section>`;
  return layout({ path:"/contato", title:"Agendar visita | Asteria Residences", description:"Solicite uma conversa e uma visita individual às residências Asteria. Resposta em até um dia útil.", body });
}

function legalPage(kind) {
  const privacy = kind === "privacidade";
  const title = privacy ? "Política de privacidade" : "Termos de uso";
  const sections = privacy ? [
    ["Dados coletados", "Ao solicitar contato, coletamos nome, e-mail, telefone, residência de interesse, faixa de investimento e, quando informada, data preferida de visita."],
    ["Finalidade e retenção", "Usamos os dados exclusivamente para responder à solicitação e organizar a conversa comercial. Neste benchmark fictício, os registros são mantidos no servidor da demonstração e podem ser removidos ao encerrar o ambiente."],
    ["Seus direitos", `Para consultar, corrigir ou solicitar a exclusão dos dados, escreva para ${site.email}.`],
  ] : [
    ["Natureza da experiência", "Asteria Residences é um empreendimento fictício criado para avaliação técnica. Conteúdo, endereço, disponibilidade e valores não constituem oferta imobiliária real."],
    ["Imagens e medidas", "Imagens são ilustrativas. Medidas e características apresentadas integram o cenário canônico do benchmark e não representam imóvel comercializado."],
    ["Uso do site", "O site pode ser navegado e avaliado sem cadastro. Não é permitido automatizar envios abusivos ao formulário ou tentar acessar dados do servidor."],
  ];
  const body = `<article class="legal"><p class="eyebrow">Informações legais</p><h1>${title}</h1><p class="legal-updated">Atualizado em 13 de agosto de 2026</p>${sections.map(([h,p])=>`<section><h2>${h}</h2><p>${p}</p></section>`).join("")}<p>${arrowLink("/contato", "Falar com a equipe")}</p></article>`;
  return layout({ path:`/${kind}`, title:`${title} | Asteria Residences`, description:`${title} do site fictício Asteria Residences.`, body });
}

function notFound() {
  return { status:404, html:layout({path:"/404",title:"Página não encontrada | Asteria",description:"A página solicitada não existe.",indexable:false,body:`<section class="not-found"><span>404</span><h1>Este caminho não leva a uma residência.</h1><p>Volte ao início ou explore a coleção Asteria.</p>${arrowLink("/", "Voltar ao início", "button-link")}</section>`}) };
}

export function renderPage(url) {
  const path = url.pathname.replace(/\/$/, "") || "/";
  if (path === "/") return { status:200, html:home() };
  if (path === "/residencias") return { status:200, html:residencesPage() };
  if (path.startsWith("/residencias/")) { const r=residences.find(x=>`/residencias/${x.slug}`===path); return r?{status:200,html:residenceDetail(r)}:notFound(); }
  if (path === "/localizacao") return { status:200, html:locationPage() };
  if (path === "/caderno") return { status:200, html:journalPage() };
  if (path.startsWith("/caderno/")) { const a=journal.find(x=>`/caderno/${x.slug}`===path); return a?{status:200,html:articlePage(a)}:notFound(); }
  if (path === "/contato") return { status:200, html:contactPage(url.searchParams) };
  if (path === "/privacidade") return { status:200, html:legalPage("privacidade") };
  if (path === "/termos") return { status:200, html:legalPage("termos") };
  return notFound();
}
