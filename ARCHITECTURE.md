# Football Transfer Intelligence API — Documento de Arquitetura (Fase 0)

Este documento registra as decisões de planejamento e modelagem tomadas antes do início da implementação. O objetivo é documentar não só **o que** foi decidido, mas **por que** — para servir como referência durante o desenvolvimento e como material de apresentação do projeto.

---

## 1. Problema e Público-Alvo

A API resolve o problema de consulta e análise de dados de jogadores, clubes e transferências de futebol, com foco especial em um **sistema de recomendação de jogadores** baseado em atributos informados pelo usuário (posição, idade, orçamento, etc.).

**Público-alvo principal:** diretores esportivos, analistas de dados esportivos e olheiros (scouts), que precisam identificar jogadores compatíveis com necessidades específicas de um clube.

**Diferencial do projeto:** o Recommendation Engine (motor de recomendação baseado em regras e pesos), combinado com a possibilidade de associar vídeos de destaque a cada jogador.

---

## 2. Escopo do MVP

### Incluído no MVP
- CRUD completo de `Player`, `Club`, `Transfer`
- Armazenamento de estatísticas por jogador/temporada (`PlayerStats`)
- Recommendation Engine baseado em regras/pesos definidos manualmente
- Campo de vídeo de destaque do jogador (`video_url`), cadastrado **manualmente**

### Adiado para versões futuras (v2)
- **Busca automática de vídeos** via YouTube Data API — identificado como problema de infraestrutura (integração externa, matching de resultados), não apenas modelagem de dados. Decisão: manter cadastro manual de link no MVP.
- **Prós e contras automáticos do jogador** — identificado como uma extensão natural do Recommendation Engine (mesma lógica de regras/pesos, aplicada de forma diferente). Não é uma feature isolada, mas depende do motor de recomendação já estar maduro.

### Limitações conhecidas (assumidas conscientemente no MVP)
- **Empréstimos de jogadores** não são modelados — um jogador pertence a apenas um clube por vez (o clube "dono"). O caso de cessão temporária fica como melhoria futura.
- **Trocas de jogadores** em uma mesma negociação são representadas como **duas transferências separadas**, não como uma transferência N:N entre múltiplos jogadores — simplificação deliberada para manter o modelo simples, cobrindo a grande maioria dos casos reais.

---

## 3. Entidades

| Entidade | O que armazena |
|---|---|
| `Player` | Dados do jogador: nome, idade, posição, nacionalidade, valor de mercado, clube atual (opcional), `video_url` (opcional) |
| `Club` | Dados do clube: nome, país, etc. |
| `League` | Dados da liga/competição |
| `Season` | Ano/temporada (ex: "2023/2024") |
| `Transfer` | Movimentação de **um** jogador entre clubes: jogador, clube de origem (opcional), clube de destino (opcional), data, temporada, valor |
| `PlayerStats` | Estatísticas de **um** jogador em **uma** temporada: partidas, minutos, gols, assistências, cartões |
| `LeagueParticipation` | Participação de **um** clube em **uma** liga em **uma** temporada: pontos, vitórias, empates, derrotas |

### Dados derivados (não armazenados — calculados via endpoint)
Estas informações **não** viram tabelas/campos no banco, pois são calculadas a partir de dados já existentes:
- Estatísticas de carreira de um jogador (soma de `PlayerStats` por jogador)
- Artilheiro / melhor jogador de uma liga em uma temporada
- Saldo de transferências de um clube (compras − vendas)
- Recomendações de jogadores para um clube (Recommendation Engine)
- Classificação de uma liga em uma temporada (a partir de `LeagueParticipation`)

**Princípio aplicado:** dado derivado não deve ser armazenado como se fosse dado original, para evitar risco de inconsistência quando os dados-fonte mudam.

---

## 4. Relacionamentos

- **`Player` → `Club`**: 1:N, **opcional**. Um clube tem vários jogadores; cada jogador tem no máximo um clube atual (jogador pode estar sem clube — agente livre, base, etc.).
- **`Transfer` → `Player`**: 1:N. Cada transferência refere-se a um único jogador.
- **`Transfer` → `Club`**: duas Foreign Keys separadas — `from_club` (origem) e `to_club` (destino), **ambas opcionais** (NULL representa "sem clube": jogador vindo da base/agente livre, ou jogador se aposentando).
  - **Trade-off avaliado:** duas FKs separadas (`from_club`/`to_club`) vs. uma FK única + campo de direção (`club` + `direction`). Optado por duas FKs separadas por simplificar diretamente as consultas de entrada/saída de um clube (`WHERE from_club = X` / `WHERE to_club = X`), sem necessidade de combinar múltiplas queries.
- **`PlayerStats` → `Player` + `Season`**: 1:N em cada. Constraint de unicidade composta: a combinação (`player`, `season`) não pode se repetir.
- **`Club` ↔ `League`**: relação N:N, implementada via tabela associativa `LeagueParticipation`, que também referencia `Season` (um clube participa de uma liga em uma temporada específica). Constraint de unicidade composta: (`club`, `league`, `season`).

---

## 5. Decisões sobre campos opcionais (NULL) vs. obrigatórios

| Campo | Obrigatório? | Justificativa |
|---|---|---|
| `Player.club` | Opcional | Jogador pode estar sem clube (agente livre) |
| `Transfer.from_club` | Opcional | Jogador pode vir da base ou estar sem clube antes da transferência |
| `Transfer.to_club` | Opcional | Jogador pode se aposentar (sem clube de destino) |
| `PlayerStats.season` | **Obrigatório** | Toda estatística, por definição, está sempre associada a uma temporada específica — não há cenário de estatística "sem temporada" |
| `PlayerStats.player` | **Obrigatório** | Toda estatística pertence a um jogador específico |

**Decisão rejeitada:** criar clubes "sentinela" fictícios (ex: "Passes Livres", "Aposentados") para representar ausência de clube. Rejeitado porque poluiria estatísticas agregadas de clubes reais (ex: rankings de compra/venda) e complicaria constraints de unicidade em `Club.name`. Optado por usar NULL nos campos apropriados.

---

## 6. Convenções de API (REST)

### Padrão de verbos HTTP
| Verbo | Uso |
|---|---|
| `GET` | Leitura/consulta |
| `POST` | Criação |
| `PUT` | Atualização |
| `DELETE` | Exclusão |

### Regra para nested resources vs. query parameters
- **Nested resource** (`/api/clubs/{id}/players/`): usado para relações de **pertencimento direto** (ex: jogadores de um clube).
- **Query parameter** (`/api/clubs/?country=brazil`): usado para **filtros** que podem ser combinados entre si (ex: país, liga, posição, idade).

Identificadores em URLs e filtros usam sempre o `id` numérico (chave primária gerada automaticamente pelo banco), nunca nomes — para evitar ambiguidade (nomes podem se repetir ou mudar).

---

## 7. Endpoints planejados

### Player
```
GET    /api/players/
GET    /api/players/{id}/
POST   /api/players/
PUT    /api/players/{id}/
DELETE /api/players/{id}/
GET    /api/players/?position=ATA
GET    /api/players/?age_max=21
GET    /api/players/?nationality=brazilian
GET    /api/players/?position=ATA&age_max=21&nationality=brazilian   (filtros combinados)
```

### Club
```
GET    /api/clubs/
GET    /api/clubs/{id}/
POST   /api/clubs/
PUT    /api/clubs/{id}/
DELETE /api/clubs/{id}/
GET    /api/clubs/?league_id=3
GET    /api/clubs/?country=brazil
GET    /api/clubs/{id}/players/                (nested — relação de posse)
```

### League
```
GET    /api/leagues/
GET    /api/leagues/{id}/
POST   /api/leagues/
PUT    /api/leagues/{id}/
DELETE /api/leagues/{id}/
GET    /api/leagues/{id}/standings/?season=2024      (nested — classificação pertence à liga)
GET    /api/leagues/{id}/top_scorers/?season=2024    (nested — artilheiros pertencem à liga)
```

### Transfer
```
GET    /api/transfers/
GET    /api/transfers/{id}/
POST   /api/transfers/
PUT    /api/transfers/{id}/
DELETE /api/transfers/{id}/
GET    /api/transfers/?player={id}          (histórico de um jogador)
GET    /api/transfers/?to_club={id}         (entradas de um clube)
GET    /api/transfers/?from_club={id}       (saídas de um clube)
GET    /api/transfers/?season=2026          (por temporada)
GET    /api/transfers/?ordering=-value      (maiores transferências)
```

---

## 8. Próximos passos (Fase 1 em diante)

- Configuração do ambiente (Python venv, Django, DRF, PostgreSQL, Git)
- Estrutura de pastas do projeto
- Implementação dos Models a partir do modelo conceitual acima
- Implementação da API REST (serializers, views, URLs)
- Filtros, paginação e ordenação (Fase 4)
- Recommendation Engine (Fase 6)
- Autenticação, testes, Docker, documentação Swagger, CI/CD (Fases 7–11)
