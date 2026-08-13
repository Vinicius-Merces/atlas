export const site = {
  name: "Asteria Residences",
  origin: process.env.PUBLIC_ORIGIN || "http://localhost:4173",
  phone: "+55 11 3000-1212",
  email: "visitas@asteriaresidences.example",
  address: "Alameda do Horizonte, 120 — Serra Clara, SP",
};

const residenceTypes = [
  {
    slug: "casa-patio",
    number: "01",
    name: "Casa Pátio",
    type: "Jardim central",
    area: "384 m²",
    suites: "4 suítes",
    lots: "612 m²",
    summary: "A casa se organiza ao redor de um pátio vivo, com circulação protegida e luz natural em todas as áreas sociais.",
    features: ["Pátio de 86 m²", "Piscina orientada ao poente", "Elevador privativo", "3 vagas cobertas"],
  },
  {
    slug: "casa-horizonte",
    number: "02",
    name: "Casa Horizonte",
    type: "Vista longa",
    area: "421 m²",
    suites: "4 suítes",
    lots: "680 m²",
    summary: "Um plano contínuo enquadra a paisagem e separa com precisão os ritmos de receber, trabalhar e descansar.",
    features: ["Terraço de 42 m", "Biblioteca", "Piscina com raia de 15 m", "4 vagas cobertas"],
  },
  {
    slug: "casa-bosque",
    number: "03",
    name: "Casa Bosque",
    type: "Sombra e textura",
    area: "398 m²",
    suites: "4 suítes",
    lots: "645 m²",
    summary: "A implantação preserva árvores maduras e cria ambientes frescos, silenciosos e conectados ao jardim.",
    features: ["Bosque privativo", "Adega climatizada", "Ateliê independente", "3 vagas cobertas"],
  },
];

const variations = [
  { suffix: "", area: 0, lot: 0 },
  { suffix: "-ii", area: 12, lot: 18 },
  { suffix: "-iii", area: -8, lot: 24 },
  { suffix: "-iv", area: 18, lot: 36 },
];

export const residences = Array.from({ length: 12 }, (_, index) => {
  const type = residenceTypes[index % residenceTypes.length];
  const edition = Math.floor(index / residenceTypes.length);
  const variation = variations[edition];
  const roman = ["", " II", " III", " IV"][edition];
  return {
    ...type,
    slug: `${type.slug}${variation.suffix}`,
    number: String(index + 1).padStart(2, "0"),
    name: `${type.name}${roman}`,
    area: `${Number.parseInt(type.area) + variation.area} m²`,
    lots: `${Number.parseInt(type.lots) + variation.lot} m²`,
  };
});

export const journal = [
  {
    slug: "viver-entre-cidade-e-paisagem",
    category: "Guia de localização",
    title: "Viver entre a cidade e a paisagem",
    dek: "Como Serra Clara combina acesso metropolitano, serviços essenciais e uma rotina mais silenciosa.",
    date: "2026-08-08",
    read: "6 min",
    sections: [
      ["Começar pela distância certa", "Asteria nasce de uma pergunta prática: como permanecer conectado à cidade sem carregar seu ritmo para dentro de casa? Em Serra Clara, a resposta aparece numa borda metropolitana já servida por escola, hospital e comércio cotidiano."],
      ["Percursos que cabem na rotina", "Os tempos informados neste guia são estimativas, não promessas. Mais importante que um número isolado é a existência de rotas alternativas e de serviços essenciais próximos."],
      ["Paisagem como infraestrutura", "O corredor verde preservado não é cenário. Ele ajuda a drenar águas de chuva, protege a cota baixa do terreno e cria continuidade para a vegetação."],
    ],
  },
  {
    slug: "arquitetura-que-envelhece-bem",
    category: "Arquitetura",
    title: "Materiais que ganham caráter com o tempo",
    dek: "Pedra, madeira e metal escolhidos por desempenho, manutenção e beleza durável.",
    date: "2026-07-24",
    read: "4 min",
    sections: [
      ["Uma escolha de longo prazo", "Materiais residenciais precisam responder simultaneamente ao uso, ao clima e à manutenção. Em Asteria, cada acabamento foi avaliado por esse conjunto."],
      ["Origem e desempenho", "Madeiras de origem rastreada, pedra local e metais com acabamento reparável compõem uma paleta curta. Menos variações simplificam manutenção sem tornar as casas idênticas."],
      ["O tempo como parte do projeto", "Superfícies naturais mudam de tom e textura. O detalhamento considera essa transformação para que o envelhecimento seja caráter, não defeito prematuro."],
    ],
  },
  {
    slug: "doze-casas-uma-paisagem",
    category: "Projeto",
    title: "Doze casas, uma paisagem compartilhada",
    dek: "A lógica de implantação que preserva privacidade sem transformar vizinhança em isolamento.",
    date: "2026-07-05",
    read: "5 min",
    sections: [
      ["Vizinhança sem exposição", "As doze casas alternam acessos, pátios e planos de fachada para evitar visadas diretas. A proximidade existe no percurso comum, enquanto cada jardim mantém sua própria escala."],
      ["Três tipologias, doze respostas", "Pátio, Horizonte e Bosque são famílias de projeto, não plantas repetidas. Cada uma aparece quatro vezes com ajustes de área, lote, orientação solar e relação com as árvores existentes."],
      ["O chão compartilhado", "O paisagismo conecta drenagem, sombra e caminhada. A infraestrutura coletiva ocupa menos espaço e deixa a paisagem conduzir a experiência."],
    ],
  },
];

export function absolute(path = "/") {
  return new URL(path, site.origin).toString();
}
