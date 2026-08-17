# Mapa de CARs e Relatório Climático de Talhões

Aplicação web que permite visualizar CARs (Cadastro Ambiental Rural) e seus talhões num mapa interativo, e gerar relatórios climáticos em PDF por talhão — com climatologia histórica, comparativo do ano atual, croqui de satélite e insights gerados por IA.

## Stack

- **Backend**: Python 3.13, FastAPI, geopandas, matplotlib, WeasyPrint, Jinja2
- **Frontend**: Next.js (TypeScript), React-Leaflet
- **Dados climáticos**: NASA POWER API
- **Imagem de satélite**: Esri World Imagery (via contextily)
- **Insights por IA**: OpenAI (gpt-4o-mini)

## Como rodar

Pré-requisitos: Docker e Docker Compose instalados.

1. Crie um arquivo `.env` na raiz do projeto:

OPENAI_API_KEY=sua-chave-aqui

2. Suba os containers:
```bash
   docker compose up
```

3. Acesse:
   - Frontend: http://localhost:3000
   - Backend (docs interativas): http://localhost:8000/docs

## Como usar

1. O mapa carrega automaticamente todos os CARs do município de Jataí/GO
2. Clique em um CAR para ver seus talhões
3. Os talhões vêm todos selecionados por padrão — desmarque os que não quiser incluir no relatório, tanto pela lista lateral quanto clicando neles no mapa
4. Clique em "Gerar Relatório PDF" — o download inicia automaticamente ao terminar

## Arquitetura

### Backend

```
backend/app/
├── api/ # rotas HTTP (FastAPI)
├── services/ # lógica de negócio
│ ├── geo_service.py # leitura e processamento geoespacial (geopandas)
│ ├── climate_service.py # integração com NASA POWER
│ ├── charts_service.py # geração dos 4 gráficos climáticos
│ ├── satellite_service.py # croqui sobre imagem de satélite
│ ├── ai_insights_service.py # geração de insights via OpenAI
│ └── report_service.py # orquestração: monta o PDF final
├── helpers/ # utilitários compartilhados (conversão de imagem)
├── templates/ # template HTML/Jinja2 do relatório
└── data/ # GeoJSON de CARs e talhões
```

Os dados são carregados em memória no startup (`geo_service.load_data()`), sem banco de dados — adequado ao volume de dados do desafio. Para produção com datasets maiores, a evolução natural seria migrar para PostGIS.

### Frontend

```
frontend/src/components/
├── MapView.tsx # mapa principal, estado central da aplicação
├── FitBoundsToTalhoes.tsx # ajusta zoom/posição ao carregar talhões
└── TalhoesSidebar.tsx # lista de seleção + botão de gerar relatório
```

## Decisões técnicas e trade-offs

- **Fonte de dados climáticos**: inicialmente implementado com Open-Meteo, mas o tier gratuito impõe um limite de "peso" (localizações × dias × variáveis) que inviabiliza buscar 30 anos de histórico para CARs com muitos talhões. Migrado para NASA POWER, que não tem essa limitação para o volume usado aqui.

- **Climatologia de 30 anos**: obtida buscando o histórico diário completo em uma única chamada por talhão e agregando localmente com pandas — mais eficiente do que múltiplas chamadas por período.

- **Resiliência da IA**: cada chamada de insight é isolada em try/except; se falhar (rate limit, instabilidade do provedor), o relatório é gerado normalmente com uma mensagem de fallback naquele talhão, em vez de falhar o processo inteiro.

- **Processamento paralelo**: a geração do relatório busca clima e insights de IA em paralelo (ThreadPoolExecutor) para múltiplos talhões, já que são operações de rede (I/O-bound). A geração de gráficos/croqui permanece sequencial, pois matplotlib não é thread-safe.

- **Simplificação de geometria**: os polígonos enviados ao frontend passam por `.simplify()` antes de virar GeoJSON, reduzindo o volume de dados transferido e melhorando a performance de renderização no mapa, sem impacto visual perceptível na escala em que são exibidos.

- **Seleção de talhões no relatório**: implementado o requisito opcional do desafio — o usuário pode escolher, via lista lateral ou clique direto no mapa, quais talhões entram no PDF final.

## Limitações conhecidas

- O croqui de satélite usa zoom fixo (não automático) para garantir disponibilidade de tiles em áreas rurais, o que resulta em resolução moderada, não a máxima disponível.
- Relatórios de CARs com muitos talhões (50+) podem levar alguns minutos para gerar, devido ao volume de chamadas externas (clima + IA) por talhão.
- Não há testes automatizados (fora do escopo dado o prazo do desafio).

## Próximos passos (se o projeto continuasse)

- Migrar armazenamento de dados para PostGIS
- Cache de dados climáticos (mesma coordenada/período não deveria ser buscado repetidamente)
- Testes automatizados (unitários nos services, integração nas rotas)
- Autenticação/autorização, caso a aplicação vá a produção com múltiplos usuários
