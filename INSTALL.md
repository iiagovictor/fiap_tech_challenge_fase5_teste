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

**Configuração adicional:**
```bash
# Edite .env e configure o LLM
nano .env

# Para Google Gemini (recomendado):
LLM_MODEL=gemini/gemini-2.0-flash-exp
GOOGLE_API_KEY=sua-chave-aqui

# Para OpenAI:
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...

# Para Ollama local (requer instalação):
LLM_MODEL=ollama/llama3
```

**Popular base de conhecimento:**
```bash
# Popula ChromaDB com conhecimento de análise técnica
make seed-rag
```

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

**Erro: `make: uvicorn: command not found`**
→ O Makefile foi corrigido para usar `$(CURDIR)/.venv/bin/python` (caminho absoluto)
→ Se ainda ocorrer, rode diretamente:
```bash
cd /Users/seu-usuario/path/to/fiap_tech_challenge_fase5
.venv/bin/python -m uvicorn src.serving.app:app --host 0.0.0.0 --port 8000 --reload
```

**Erro: ChromaDB `np.float_` removed in NumPy 2.0**
→ ChromaDB 0.4.24 requer NumPy < 2.0
→ O pyproject.toml já especifica `numpy>=1.26.4,<2.0.0`
→ Se necessário: `.venv/bin/pip install 'numpy>=1.26.4,<2.0.0'`

**Erro: ChromaDB `no such column: collections.topic`**
→ Schema incompatível após mudança de versão
→ Solução: Limpar database e popular novamente
```bash
mv ./data/chromadb ./data/chromadb.old
mkdir -p ./data/chromadb
docker-compose restart chromadb
make seed-rag
```

**Erro: ChromaDB `404 Not Found` no endpoint `/api/v2/auth/identity`**
→ Incompatibilidade entre client Python (0.5.x) e servidor Docker (0.4.24)
→ Verifique versões: `.venv/bin/pip show chromadb` (deve ser 0.4.24)
→ Solução: `.venv/bin/pip install --force-reinstall chromadb==0.4.24`

**Erro: `cannot import name 'service' from 'google.protobuf'`**
→ MLflow requer protobuf < 5.0, mas versão mais nova foi instalada
→ Solução:
```bash
.venv/bin/pip install 'protobuf>=4.24.0,<5.0.0'
.venv/bin/pip install 'importlib-metadata>=3.7.0,<8' 'packaging<25' 'tenacity>=7,<9'
```
→ Se persistir, reinstale o ambiente:
```bash
.venv/bin/pip install -e . -e '.[llm]'
```

**Erro: Google API Key invalid (400)**
→ Verifique se a chave está correta no `.env`
→ Teste: `curl "https://generativelanguage.googleapis.com/v1beta/models?key=SUA_CHAVE"`
→ Obtenha chave em: https://makersuite.google.com/app/apikey

**Erro: Gemini 503 (high demand)**
→ O sistema tem fallback automático para `gemini-1.5-flash`
→ Se persistir, o endpoint retorna dados diretos do yfinance

**Aviso: RAG pipeline unavailable (404)**
→ Collection vazia - rode `make seed-rag` para popular
→ O sistema funciona sem RAG (opcional)

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
