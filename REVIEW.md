# Revisão de Implementação — FIAP Tech Challenge Fase 5

**Data:** 01/05/2026  
**Referência:** README principal (Datathon — Guia de Desenvolvimento Fase 05)

---

## Etapa 1 — Dados + Baseline

| Requisito | Status | Observação |
|-----------|--------|------------|
| Dados versionados com DVC | ✅ Implementado | `dvc.yaml` com 6 estágios |
| EDA Notebook exploratório | ⚠️ Parcial | Apenas `teste.ipynb` — sem análise de distribuição, correlação e insights estruturados |
| Feature Engineering | ✅ Implementado | `src/features/feature_engineering.py` com 25+ indicadores (RSI, MACD, Bollinger, ATR, OBV) |
| Schema validation (pandera) | ❌ Ausente | `test_features.py` usa apenas `assert` básico; README recomenda `DataFrameSchema` |
| Baseline Scikit-Learn | ✅ Implementado | `src/models/baseline.py` com Logistic Regression + Random Forest |
| Baseline MLP PyTorch | ❌ Ausente | README recomenda MLP PyTorch como baseline complementar |
| MLflow Tracking padronizado | ✅ Implementado | `src/models/train.py` loga params, metrics, artifacts e tags obrigatórias |
| Feature Store (Feast) | ✅ Implementado | `feast/feature_store_definitions.py` com Redis online + Parquet offline |
| Materialização incremental | ⚠️ Parcial | Feast implementado, mas estratégia de upsert incremental (vs. full-flush) não documentada |

---

## Etapa 2 — LLM + Agente

| Requisito | Status | Observação |
|-----------|--------|------------|
| LLM Serving | ✅ Implementado | LiteLLM com fallback Gemini 2.0 → 1.5 → yfinance direto |
| Agente ReAct ≥ 3 tools | ✅ Implementado | `src/agent/tools.py`: 4 tools (`get_stock_price_history`, `calculate_technical_indicators`, `predict_stock_direction`, `compare_stocks`) |
| RAG Pipeline (Vector Store) | ✅ Implementado | `src/agent/rag_pipeline.py`: ChromaDB com 9 documentos financeiros |
| API FastAPI documentada | ✅ Implementado | `src/serving/app.py`: `/health`, `/metrics`, `/predict`, `/agent`, `/drift` |
| CI/CD GitHub Actions | ⚠️ Parcial | `.github/workflows/pr_auto.yml` cobre lint + test + coverage; **faltam stages de docker build e deploy** |
| `.pre-commit-config.yaml` | ❌ Ausente | Recomendado na estrutura do README; não existe no projeto |

---

## Etapa 3 — Avaliação + Observabilidade

> Esta é a etapa com **mais gaps críticos**.

| Requisito | Status | Observação |
|-----------|--------|------------|
| Prometheus + Grafana | ✅ Implementado | `configs/prometheus.yml` + dashboard `configs/grafana/provisioning/dashboards/json/api-overview.json` |
| Métricas Prometheus customizadas | ✅ Implementado | `src/monitoring/metrics.py`: latência, throughput, LLM tokens, drift score, PII |
| Drift Detection (Evidently) | ✅ Implementado | `src/monitoring/drift.py`: DataDriftPreset com alertas por threshold |
| **Endpoint `/drift` funcional** | ❌ Mock/TODO | `src/serving/app.py` retorna dados fictícios; marcado como TODO no código |
| **Golden Set ≥ 20 pares** | ❌ Ausente | Diretório `data/golden_set/` não existe; requisito explícito da Etapa 3 |
| **RAGAS (4 métricas)** | ❌ Ausente | Sem pasta `evaluation/`; sem `ragas_eval.py`; `faithfulness`, `relevancy`, `context_precision`, `context_recall` não avaliados |
| **LLM-as-judge ≥ 3 critérios** | ❌ Ausente | Sem `llm_judge.py`; sem avaliação estruturada das respostas do agente |
| **Langfuse / TruLens (telemetria LLM)** | ❌ Ausente | README exige telemetria de qualidade LLM; projeto usa apenas Prometheus operacional |

---

## Etapa 4 — Segurança + Governança

| Requisito | Status | Observação |
|-----------|--------|------------|
| Guardrails Input + Output | ✅ Implementado | `src/security/guardrails.py`: prompt injection, tokens, PII, toxic content |
| PII Detection (Presidio) | ✅ Implementado | `src/security/pii_detection.py`: suporte pt + en |
| OWASP LLM Top 10 ≥ 5 ameaças | ✅ Implementado | `docs/OWASP_MAPPING.md`: 7/10 mapeadas |
| Red Teaming ≥ 5 cenários | ✅ Implementado | `docs/RED_TEAM_REPORT.md`: RT-01 a RT-05 |
| LGPD Plan | ✅ Implementado | `docs/LGPD_PLAN.md` com matriz de riscos e medidas de conformidade |
| Model Card | ✅ Implementado | `docs/MODEL_CARD.md` com métricas, limitações e uso pretendido |
| System Card | ✅ Implementado | `docs/SYSTEM_CARD.md` com arquitetura e comportamentos do sistema |
| Fairness + Explicabilidade | ⚠️ Parcial | Mencionado no Model Card, mas sem implementação técnica (ex: SHAP, LIME) |
| Champion-Challenger | ⚠️ Parcial | Descrito no System Card; lógica de promoção não implementada em `src/models/train.py` |

---

## Qualidade de Código + Testes

| Critério | Status | Observação |
|----------|--------|------------|
| `pyproject.toml` + hatchling | ✅ OK | Dependências segregadas: core, llm, feast, monitoring, security |
| Type hints | ✅ OK | Presente em todos os módulos |
| Logging estruturado (não `print`) | ✅ OK | `logging.getLogger(__name__)` em todos os módulos |
| pytest + cobertura ≥ 60% | ✅ Configurado | `--cov-fail-under=60` no CI; 14 testes (3 arquivos) |
| `test_guardrails.py` | ❌ Ausente | Recomendado no README; cobertura do módulo security comprometida |
| `test_agent.py` | ❌ Ausente | Sem testes do agente ReAct; cobertura da Etapa 2 comprometida |
| Schema validation com pandera | ❌ Ausente | README exemplifica `DataFrameSchema`; não usado em `test_features.py` |
| Cloud-agnostic (fsspec + LiteLLM) | ✅ Implementado | `src/config/storage.py` + `src/config/settings.py` |

---

## Resumo — Gaps por Prioridade

### 🔴 Críticos (requisito explícito ausente)

1. **Avaliação RAG inexistente** — sem golden set, sem RAGAS, sem LLM-as-judge. A Etapa 3 é o núcleo do Datathon.
2. **`/drift` endpoint é mock** — retorna dados fictícios; precisa chamar `drift_monitoring_pipeline()` real.
3. **Langfuse/TruLens ausente** — telemetria de qualidade LLM é requisito explícito da Etapa 3.

### 🟡 Importantes (requisito parcialmente atendido)

4. **CI/CD incompleto** — faltam stages `docker build`, `docker push` e deploy.
5. **`test_agent.py` e `test_guardrails.py` ausentes** — cobertura real de 60% pode não ser atingida.
6. **EDA desorganizada** — `teste.ipynb` não substitui análise exploratória estruturada.
7. **Baseline sem MLP PyTorch** — recomendado no README; apenas LogReg + RF implementados.
8. **Champion-challenger** não implementado em código, apenas documentado.

### 🟢 Bem implementado

- Arquitetura cloud-agnostic com `fsspec` + `LiteLLM`
- Feature Store Feast com 25 features técnicas
- Segurança completa: OWASP mapping, Red Team report, PII detection, guardrails
- Documentação de governança: Model Card, System Card, LGPD
- MLflow tracking padronizado com tags obrigatórias
- Docker Compose com 9 serviços para ambiente local completo
- Agente ReAct com 4 tools e fallback robusto

---

## Ações Recomendadas

| Prioridade | Ação |
|------------|------|
| 🔴 Alta | Criar `data/golden_set/` com ≥ 20 pares (query, expected, contexts) |
| 🔴 Alta | Implementar `evaluation/ragas_eval.py` com as 4 métricas RAGAS |
| 🔴 Alta | Implementar `evaluation/llm_judge.py` com ≥ 3 critérios de avaliação |
| 🔴 Alta | Conectar endpoint `/drift` ao `drift_monitoring_pipeline()` real |
| 🟡 Média | Adicionar stages `docker build` e `deploy` no GitHub Actions |
| 🟡 Média | Criar `tests/test_agent.py` e `tests/test_guardrails.py` |
| 🟡 Média | Adicionar `evaluation/` com Langfuse ou TruLens para telemetria LLM |
| 🟢 Baixa | Criar EDA notebook estruturada com análise de distribuição e correlação |
| 🟢 Baixa | Adicionar baseline MLP PyTorch em `src/models/baseline.py` |
| 🟢 Baixa | Implementar lógica champion-challenger em `src/models/train.py` |
