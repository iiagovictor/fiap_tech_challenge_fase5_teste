# 🚀 Instalação Rápida

## Problema: `resolution-too-deep`

Se você encontrou o erro `resolution-too-deep` do pip, é porque o projeto tem muitas dependências complexas (TensorFlow, Feast, LangChain, ChromaDB).

## ✅ Solução: Instalação Modular

As dependências foram divididas em **grupos opcionais**. Escolha o que você precisa:

### 1️⃣ **Instalação CORE** (Recomendado para começar)
Apenas ML básico + API (sem LLM, sem Feast):

```bash
make install
# ou: pip install -e .
```

**Inclui:**
- ✅ Pandas, NumPy, Scikit-learn
- ✅ TensorFlow + MLflow (modelo LSTM)
- ✅ FastAPI + Uvicorn (API)
- ✅ YFinance (dados)
- ✅ Storage básico (S3/local via fsspec)

**NÃO inclui:**
- ❌ LLM/RAG (LiteLLM, ChromaDB)
- ❌ Feature Store (Feast)
- ❌ Drift detection (Evidently)
- ❌ PII detection (Presidio)

---

### 2️⃣ **Adicionar LLM/RAG** (Agente ReAct)
Se você precisa do agente LLM:

```bash
make install-llm
# ou: pip install -e ".[llm]"
```

**Adiciona:**
- LiteLLM (abstração cloud-agnostic)
- LangChain + LangChain Community
- ChromaDB (vector store)
- Sentence Transformers (embeddings)

---

### 3️⃣ **Adicionar Feature Store** (Feast)
Se você precisa de features online com Redis:

```bash
make install-feast
# ou: pip install -e ".[feast-support]"
```

**Adiciona:**
- Feast[redis]

---

### 4️⃣ **Instalação COMPLETA** (Tudo de uma vez)
Se você tem tempo e quer instalar tudo:

```bash
make install-full
# ou: pip install -e ".[llm,feast-support,monitoring,security,pipeline,cloud]"
```

**Adiciona tudo:**
- LLM/RAG
- Feast
- Evidently (drift)
- Presidio (PII)
- DVC (pipeline versioning)
- GCS/Azure backends

⚠️ **ATENÇÃO**: Esta instalação pode demorar 10-15 minutos e ainda pode falhar com `resolution-too-deep` em alguns ambientes.

---

## 🧪 Testando a Instalação

Após `make install`:

```bash
# Verificar importações core
python -c "import pandas, numpy, sklearn, tensorflow, mlflow, fastapi; print('✅ Core OK')"

# Verificar se API funciona
python -c "from src.serving.app import app; print('✅ API OK')"

# Verificar se modelo pode ser treinado
python -c "from src.models.train import build_lstm_model; print('✅ Model OK')"
```

---

## 📦 Dependências Opcionais

| Grupo | Comando | Casos de Uso |
|-------|---------|--------------|
| `[llm]` | `make install-llm` | Agente ReAct, RAG, ChromaDB |
| `[feast-support]` | `make install-feast` | Feature Store online (Redis) |
| `[monitoring]` | `pip install -e ".[monitoring]"` | Evidently drift detection |
| `[security]` | `pip install -e ".[security]"` | Presidio PII detection (LGPD) |
| `[pipeline]` | `pip install -e ".[pipeline]"` | DVC para versionamento |
| `[cloud]` | `pip install -e ".[cloud]"` | GCS/Azure backends |

---

## 🔧 Modo de Desenvolvimento

```bash
make dev-install
# Inclui: pytest, ruff, mypy, pre-commit
```

---

## 💡 Dica: Instalação Sem Erros

Se `make install-full` falhar, instale em etapas:

```bash
# 1. Core primeiro
make install

# 2. Adicione o que você precisa
make install-llm
make install-feast

# 3. Resto opcional
pip install -e ".[monitoring,security]"
```

---

## 🐛 Troubleshooting

**Erro: `resolution-too-deep`**
→ Use instalação modular (não `install-full`)

**Erro: `No module named 'litellm'`**
→ Rode `make install-llm`

**Erro: `No module named 'feast'`**
→ Rode `make install-feast`

**Erro: `No module named 'evidently'`**
→ Rode `pip install -e ".[monitoring]"`

---

## 📊 Fluxo de Trabalho Recomendado

```bash
# 1. Instalar core
make install

# 2. Testar modelo LSTM básico (sem Feast, sem LLM)
make data-download
python -m src.features.feature_engineering
python -m src.models.train

# 3. Se funcionar, adicionar resto
make install-llm      # Para agente
make install-feast    # Para feature store
```
