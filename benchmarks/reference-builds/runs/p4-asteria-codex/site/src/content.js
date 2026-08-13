export const site = {
  name: "Asteria Residences",
  origin: process.env.PUBLIC_ORIGIN || "http://localhost:4173",
  phone: "+55 11 3000-1212",
  email: "visitas@asteriaresidences.example",
  address: "Alameda do Horizonte, 120 — Serra Clara, SP",
};

export const residences = [
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

export const journal = [
  {
    slug: "viver-entre-cidade-e-paisagem",
    category: "Guia de localização",
    title: "Viver entre a cidade e a paisagem",
    dek: "Como Serra Clara combina acesso metropolitano, serviços essenciais e uma rotina mais silenciosa.",
    date: "2026-08-08",
    read: "6 min",
  },
  {
    slug: "arquitetura-que-envelhece-bem",
    category: "Arquitetura",
    title: "Materiais que ganham caráter com o tempo",
    dek: "Pedra, madeira e metal escolhidos por desempenho, manutenção e beleza durável.",
    date: "2026-07-24",
    read: "4 min",
  },
  {
    slug: "doze-casas-uma-paisagem",
    category: "Projeto",
    title: "Doze casas, uma paisagem compartilhada",
    dek: "A lógica de implantação que preserva privacidade sem transformar vizinhança em isolamento.",
    date: "2026-07-05",
    read: "5 min",
  },
];

export function absolute(path = "/") {
  return new URL(path, site.origin).toString();
}
