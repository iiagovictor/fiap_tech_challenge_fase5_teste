# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [1.1.0] - 2026-05-01

### Adicionado
- **Google Gemini como LLM padrão**: Configurado `gemini/gemini-2.0-flash-exp` como modelo padrão
- **Ferramenta de predição para o agente**: `predict_stock_direction` - agente agora pode usar o modelo LSTM para prever valorizações
- **Fallback automático de LLM**: Se Gemini retornar 503 (alta demanda), tenta `gemini-1.5-flash` automaticamente
- **Fallback inteligente no endpoint /agent**: Detecta tipo de pergunta e retorna resposta apropriada:
  - Lista de tickers disponíveis
  - Comparação de ações
  - Análise técnica específica
  - **Predição de valorização usando modelo LSTM**
- **Comando `make seed-rag`**: Popula ChromaDB com conhecimento de análise técnica
- **Script `src/agent/seed_rag.py`**: Seed automático da base de conhecimento RAG
- **API keys no settings**: Suporte para `GOOGLE_API_KEY` e `OPENAI_API_KEY` no `.env`

### Corrigido
- **Makefile**: Corrigidos todos os comandos para usar `$(CURDIR)/.venv/bin/python` (caminho absoluto)
- **Protobuf**: Fixado em 4.25.9 (<5.0) para compatibilidade com MLflow 2.14.3
- **ChromaDB fixado em 0.4.24**: Versão estável compatível com NumPy < 2.0
- **NumPy fixado em 1.26.4**: Mantido em < 2.0 para compatibilidade com ChromaDB 0.4.24
- **RAG pipeline**: Tratamento de erro 404 mais silencioso (collection vazia é esperada)
- **API keys**: Export correto de `GOOGLE_API_KEY` e `GEMINI_API_KEY` para ambiente antes de importar LiteLLM
- **Logs mais limpos**: Reduzidos warnings desnecessários para RAG collection vazia
- **Schema ChromaDB**: Limpeza automática de dados antigos se houver incompatibilidade de schema

### Melhorado
- **Endpoint /agent**:
  - Extrai ticker automaticamente da query usando regex
  - Suporta perguntas em português natural
  - Fallback de 3 camadas (Gemini 2.0 → Gemini 1.5 → yfinance direto)
  - **Sources agora mostra exatamente quais ferramentas foram usadas**
  - **Warning se agente não usar ferramentas (possível alucinação)**
- **System Prompt do ReactAgent**:
  - **Regras CRÍTICAS explícitas** para forçar uso de ferramentas
  - **Exemplos concretos** de uso correto (few-shot learning)
  - **Instruções OBRIGATÓRIAS** para não inventar números
  - Formato de resposta mais claro e específico
- **Logs do ReactAgent**:
  - Emojis informativos (🔄 🔧 ✅ ⚠️ 📝)
  - Debug detalhado de cada iteração
  - Contagem de ferramentas usadas
  - Warning quando resposta pode ser "alucinada"
- **Documentação**: 
  - README.md atualizado com configuração do Gemini
  - QUICKSTART.md com passo-a-passo detalhado
  - INSTALL.md com troubleshooting expandido
  - SYSTEM_CARD.md com nova arquitetura de fallbacks
  - **DEBUGGING_AGENT.md** com guia completo de debug
- **Logs informativos**: Mostram quando API key é exportada e qual modelo está sendo usado

### Alterado
- **LLM padrão**: Ollama → Google Gemini (mais acessível, sem instalação local)
- **ChromaDB**: Fixado em 0.4.24 (compatível com NumPy < 2.0)
- **NumPy**: Mantido em 1.26.4 (< 2.0) conforme pyproject.toml
- **Porta MLflow**: 5000 → 5001 (para evitar conflitos no macOS)

## [1.0.0] - 2026-04-26

### Adicionado
- Release inicial do projeto
- Pipeline completo de MLOps com LSTM
- Feature Store com Feast
- LLM Agent com ReAct pattern
- Monitoramento com Prometheus e Grafana
- Deploy AWS com Terraform
- Documentação completa (Model Card, System Card, OWASP, LGPD)

---

**Formato baseado em [Keep a Changelog](https://keepachangelog.com/)**
