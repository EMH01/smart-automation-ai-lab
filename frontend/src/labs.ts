export type LabStatus = "IMPLEMENTED" | "EXPERIMENTAL" | "STUDIO_ONLY" | "PLANNED";
export type LabGroup = "Document AI" | "Search & GenAI" | "Machine Learning" | "Multimodal" | "Cloud & Operations";
export interface Lab { id: string; name: string; group: LabGroup; description: string; status: LabStatus; detail: string; }
/** Catalog reflects previous validated experiments. No live Azure status is fetched. */
export const labs: Lab[] = [
  {id:"DOC-DI",name:"Document Intelligence",group:"Document AI",description:"OCR, layout, tablas y extracción estructurada.",status:"EXPERIMENTAL",detail:"Se ejecutó prebuilt-layout en un PDF local. No alimenta el índice RAG."},
  {id:"DOC-CU",name:"Content Understanding",group:"Document AI",description:"Analizadores y extracción semántica multimodal.",status:"STUDIO_ONLY",detail:"Analizador supplier_analyzer probado en Studio; no integrado en la API."},
  {id:"SEARCH",name:"Azure AI Search",group:"Search & GenAI",description:"Búsqueda keyword, vectorial y recuperación híbrida.",status:"IMPLEMENTED",detail:"Índice RAG consultable desde FastAPI. La última auditoría encontró 8 títulos y 68 fragmentos."},
  {id:"GENAI",name:"Microsoft Foundry",group:"Search & GenAI",description:"Modelos, respuestas estructuradas y evaluaciones.",status:"EXPERIMENTAL",detail:"Chat y embeddings utilizados en experimentos; evaluación ampliada pendiente."},
  {id:"AGENTS",name:"Foundry Agents",group:"Search & GenAI",description:"Agentes con herramientas, permisos y trazas.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"ML",name:"Azure Machine Learning",group:"Machine Learning",description:"Experimentos, AutoML, registro y MLOps.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"DL",name:"Deep Learning",group:"Machine Learning",description:"Transfer learning y entrenamiento reproducible.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"NLP",name:"Language & Translator",group:"Multimodal",description:"NER, PII, traducción y análisis de texto.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"VISION",name:"Azure AI Vision",group:"Multimodal",description:"Análisis visual y comparación de OCR.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"SPEECH",name:"Azure AI Speech",group:"Multimodal",description:"Transcripción, síntesis y evaluación de voz.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"SAFETY",name:"AI Safety",group:"Cloud & Operations",description:"Evaluaciones de seguridad y groundedness.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"DATA",name:"Data & Storage",group:"Cloud & Operations",description:"Blob, SQL, Cosmos DB y trazabilidad.",status:"EXPERIMENTAL",detail:"Blob Storage utilizado; SQL y Cosmos DB pendientes."},
  {id:"EVENTS",name:"Events & Messaging",group:"Cloud & Operations",description:"Event Grid, Service Bus y Event Hubs.",status:"PLANNED",detail:"Pendiente de implementar."},
  {id:"RUNTIME",name:"Serverless & Containers",group:"Cloud & Operations",description:"Functions, Container Apps y despliegue.",status:"PLANNED",detail:"FastAPI existe en local, pero no está desplegada en este portal."},
  {id:"OPS",name:"Security & Operations",group:"Cloud & Operations",description:"Key Vault, identidades, monitorización y IaC.",status:"EXPERIMENTAL",detail:"La autenticación local con Azure existe; observabilidad y despliegues pendientes."},
];
