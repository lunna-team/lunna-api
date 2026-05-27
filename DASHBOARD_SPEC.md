# Lunna Dashboard — Especificação do Repositório Frontend

> **Repositório complementar à [Lunna API](../appclinica-api).**
> Dashboard web SaaS white-label para clínicas obstétricas privadas, com portais distintos para médico(a), secretária e paciente/gestante.

---

## 1. Visão Geral do Projeto

O **Lunna Dashboard** é a interface web que consome a Lunna API. Ele expõe três portais isolados por papel (`role`), cada um com layout, navegação e permissões de recursos adequados ao perfil do usuário autenticado.

**Pilares do produto:**
- White-label por clínica — tema visual (cores, logo) carregado dinamicamente via `GET /api/v1/users/{id}/clinic`
- Controle de acesso baseado em papel (`role`) aplicado em cada rota e componente
- Mobile-first, mas responsivo para desktop (clínica usa web; paciente usa mobile)

---

## 2. Tech Stack

| Camada | Tecnologia |
|---|---|
| Framework | Next.js 15+ (App Router, React Server Components) |
| Linguagem | TypeScript (strict mode) |
| Estilização | Tailwind CSS + shadcn/ui |
| Tipografia | Fraunces + DM Sans via `next/font/google` |
| Formulários | React Hook Form + Zod |
| Fetch / Cache | TanStack Query (React Query v5) |
| Estado global | Zustand |
| Gráficos | Recharts |
| Autenticação | Própria (JWT da API) via cookies httpOnly |
| Testes | Vitest + Testing Library |
| Linting | ESLint + Prettier |

---

## 3. Integração com a API

### Variáveis de ambiente

```env
NEXT_PUBLIC_API_URL=https://<dominio-da-api>/api/v1
```

### Fluxo de autenticação

1. `POST /auth/login` → recebe `access_token` (JWT 24h) e `refresh_token` (JWT 7d)
2. `access_token` armazenado em memória (Zustand); `refresh_token` em cookie httpOnly
3. Após login, ler `role` do payload JWT e redirecionar:
   - `patient` → `/patient/dashboard`
   - `doctor` → `/doctor/dashboard`
   - `secretary` → `/secretary/dashboard`
   - `admin` → `/admin/dashboard`
4. `POST /auth/logout` chamado ao sair; tokens descartados

### Cliente HTTP

Criar wrapper tipado sobre `fetch` com interceptor que:
- Injeta `Authorization: Bearer <access_token>` em todas as requisições autenticadas
- Em resposta `401`, tenta renovar via `refresh_token`; se falhar, redireciona para `/login`

---

## 4. Estrutura de Pastas

```
src/
├── app/
│   ├── (auth)/
│   │   └── login/                    # Página pública de login
│   ├── (portal)/
│   │   ├── patient/                  # Portal da paciente
│   │   │   ├── layout.tsx            # Sidebar + header do portal
│   │   │   ├── dashboard/
│   │   │   ├── health/               # Sinais vitais
│   │   │   ├── appointments/
│   │   │   ├── exams/
│   │   │   └── profile/
│   │   ├── doctor/                   # Portal do médico
│   │   │   ├── layout.tsx
│   │   │   ├── dashboard/
│   │   │   ├── patients/
│   │   │   ├── patients/[patientId]/ # Prontuário
│   │   │   ├── schedule/
│   │   │   └── profile/
│   │   └── secretary/                # Portal da secretária
│   │       ├── layout.tsx
│   │       ├── dashboard/
│   │       ├── schedule/
│   │       ├── patients/
│   │       ├── reschedules/
│   │       └── profile/
├── components/
│   ├── ui/                           # Primitivos shadcn/ui
│   ├── charts/                       # GlucoseChart, BloodPressureChart, ContractionTimeline
│   ├── vitals/                       # Cards e formulários de sinais vitais
│   ├── appointments/                 # Cards, modais e formulários de consultas
│   └── layout/                       # Sidebar, Header, ThemeProvider
├── lib/
│   ├── api/                          # Funções de fetch tipadas por recurso
│   │   ├── auth.ts
│   │   ├── users.ts
│   │   ├── appointments.ts
│   │   ├── vitals.ts
│   │   └── exams.ts
│   └── auth/                         # Helpers JWT (decode, verificar role)
├── hooks/                            # React Query hooks (useAppointments, useVitals, etc.)
├── stores/                           # Zustand stores (auth, theme)
└── types/                            # Tipos TypeScript espelhando os schemas da API
    ├── auth.ts
    ├── user.ts
    ├── appointment.ts
    ├── vitals.ts
    └── exams.ts
```

---

## 5. Controle de Acesso (Matriz de Permissões)

> `✅ permitido` | `❌ negado` | `⚠️ apenas os próprios registros`

| Recurso / Ação | `patient` | `doctor` | `secretary` | `admin` | `superadmin` |
|---|:---:|:---:|:---:|:---:|:---:|
| Ver próprio perfil | ✅ | ✅ | ✅ | ✅ | ✅ |
| Editar próprio perfil | ✅ | ✅ | ✅ | ✅ | ✅ |
| Editar perfil de outro usuário | ❌ | ❌ | ❌ | ✅ | ✅ |
| Ver dados da clínica | ✅ | ✅ | ✅ | ✅ | ✅ |
| Listar pacientes | ⚠️ | ⚠️ | ✅ | ✅ | ✅ |
| Ver prontuário / sinais vitais | ⚠️ | ⚠️ | ❌ | ✅ | ✅ |
| Registrar sinais vitais | ✅ | ✅ | ❌ | ✅ | ✅ |
| Registrar/listar exames de USG | ⚠️ (listar) | ✅ | ❌ | ✅ | ✅ |
| Listar consultas | ⚠️ | ⚠️ | ✅ | ✅ | ✅ |
| Criar nova consulta | ❌ | ✅ | ✅ | ✅ | ✅ |
| Confirmar presença na consulta | ✅ | ❌ | ❌ | ✅ | ✅ |
| Solicitar remarcação | ✅ | ❌ | ❌ | ✅ | ✅ |
| Aprovar remarcação | ❌ | ✅ | ✅ | ✅ | ✅ |
| Cancelar consulta | ✅ | ✅ | ✅ | ✅ | ✅ |
| Gerenciar clínicas (Global) | ❌ | ❌ | ❌ | ❌ | ✅ |
| Ver métricas da plataforma | ❌ | ❌ | ❌ | ❌ | ✅ |

**Implementação:** criar um Higher-Order Component (HOC) / middleware de rota `withRole(allowedRoles)` que verifica o `role` do token no lado do servidor (middleware.ts do Next.js) e redireciona para `/403` se não autorizado. Aplicar também em nível de componente para ocultar botões de ação.

---

## 6. Design System

### 6.1 Tipografia

Carregar via `next/font/google` em `app/layout.tsx`:

```ts
import { Fraunces, DM_Sans } from 'next/font/google'

const fraunces = Fraunces({ subsets: ['latin'], variable: '--font-display' })
const dmSans   = DM_Sans({ subsets: ['latin'], variable: '--font-body' })
```

Mapear para classes Tailwind em `tailwind.config.ts`:

```ts
fontFamily: {
  display: ['var(--font-display)'],  // Fraunces — H1, H2, H3 e itálico de destaque
  body:    ['var(--font-body)'],     // DM Sans — body, labels, botões, UI em geral
}
```

**Escala tipográfica**

| Nível | Família | Peso | Tamanho | Uso |
|---|---|---|---|---|
| H1 | Fraunces | 400 | 36–42px | Hero headlines, títulos de seção |
| H2 | Fraunces | 400 | 24–30px | Subtítulos de seção |
| H3 | Fraunces | 600 | 18–22px | Títulos de card |
| Body Large | DM Sans | 400 | 16–18px | Parágrafos principais, descrições |
| Body | DM Sans | 400 | 14–16px | Texto corrido de interface |
| Small | DM Sans | 300 | 12–13px | Metadados, informações secundárias |
| Label | DM Sans | 500 | 10–11px | Tags, badges, CTAs pequenos — UPPERCASE |
| Micro | DM Sans | 400 | 8–9px | Captions, timestamps, rodapés |

O itálico da Fraunces é reservado para palavras-chave de destaque isoladas (ex.: *experiência*, *cuidado*); nunca aplicar em parágrafos inteiros.

---

### 6.2 Paleta de Cores

**Cores primárias**

| Token CSS | Nome | Hex | RGB | Papel |
|---|---|---|---|---|
| `--color-plum` | Plum | `#301B28` | 48, 27, 40 | Principal — âncora da marca |
| `--color-sage` | Sage | `#8DAA91` | 141, 170, 145 | Suporte — naturalidade e saúde |
| `--color-coral` | Coral | `#E5987D` | 229, 152, 125 | Destaque — calor e ação |

**Tons e fundos**

| Token CSS | Nome | Hex | RGB | Papel |
|---|---|---|---|---|
| `--color-sage-light` | Sage Light | `#C5D5C8` | 197, 213, 200 | Fundo de cards, separadores |
| `--color-sage-dark` | Sage Dark | `#5E7E63` | 94, 126, 99 | Ênfase em ícones e bordas ativas |
| `--color-coral-light` | Coral Light | `#F7CFC3` | 247, 207, 195 | Fundo suave de badges e alertas de ação |
| `--color-bg` | Background | `#F4F6F4` | 244, 246, 244 | Fundo geral de páginas e seções claras |

**Texto**

| Token CSS | Nome | Hex | RGB | Papel |
|---|---|---|---|---|
| `--color-text-dark` | Dark | `#2D312E` | 45, 49, 46 | Texto principal, títulos em fundo claro |
| `--color-text-mid` | Mid | `#6B7471` | 107, 116, 113 | Texto secundário, metadados, placeholders |
| `--color-text-white` | White | `#FFFFFF` | 255, 255, 255 | Texto sobre fundos escuros (Plum, Sage Dark) |

---

### 6.3 Aplicação por Elemento de UI

| Elemento | Cor aplicada |
|---|---|
| Sidebar e header | Plum `#301B28` · texto White `#FFFFFF` |
| Botão primário | Plum `#301B28` · texto White · hover escurece 10% |
| Botão CTA / ação principal | Coral `#E5987D` · texto White |
| Links e ações inline | Coral `#E5987D` |
| Fundo geral de página | Background `#F4F6F4` |
| Cards | White `#FFFFFF` · borda Sage Light `#C5D5C8` |
| Badges e tags secundárias | Sage Light `#C5D5C8` · texto Dark `#2D312E` |
| Badges de alerta / ação pendente | Coral Light `#F7CFC3` · texto Coral `#E5987D` |
| Ícones de suporte e bordas | Sage `#8DAA91` |
| Ícones ativos / selecionados | Sage Dark `#5E7E63` |
| Texto principal de body | Dark `#2D312E` |
| Texto secundário, labels, placeholders | Mid `#6B7471` |
| Gráfico — linha primária (glicose, sistólica) | Coral `#E5987D` |
| Gráfico — linha secundária (diastólica) | Sage `#8DAA91` |
| Gráfico — faixa de normalidade | Sage Light `#C5D5C8` com opacidade 40% |
| Indicador de risco alto | Coral `#E5987D` |
| Indicador de risco médio | Sage `#8DAA91` |
| Indicador de risco baixo | Sage Dark `#5E7E63` |

---

### 6.4 White-label por Clínica

A paleta acima define os tokens padrão da marca Lunna. Para clínicas white-label, os campos `primary_color`, `secondary_color` e `accent_color` retornados por `GET /users/{id}/clinic` sobrescrevem os três tokens primários via `style` inline no elemento `<html>`. Os demais tokens (tons, fundos, texto) permanecem fixos.

```css
/* globals.css — defaults da marca Lunna */
:root {
  --color-plum:        #301B28;
  --color-sage:        #8DAA91;
  --color-coral:       #E5987D;

  --color-sage-light:  #C5D5C8;
  --color-sage-dark:   #5E7E63;
  --color-coral-light: #F7CFC3;
  --color-bg:          #F4F6F4;

  --color-text-dark:   #2D312E;
  --color-text-mid:    #6B7471;
  --color-text-white:  #FFFFFF;
}
```

```ts
// stores/theme.ts — sobrescreve tokens primários ao autenticar
interface ThemeStore {
  clinicName:     string
  logoUrl:        string
  primaryColor:   string  // → --color-plum
  secondaryColor: string  // → --color-sage
  accentColor:    string  // → --color-coral
}
```

---

### 6.5 Regras e Proibições da Marca

**Obrigatório**
- Usar sempre os hex codes exatos da paleta oficial — sem aproximações.
- Manter contraste mínimo de **4.5:1** em texto sobre fundo (WCAG 2.1 AA, exigido pelo brand guide).
- Usar itálico da Fraunces apenas em palavras-chave isoladas, nunca em blocos ou parágrafos.

**Proibido**
- Coral (`#E5987D`) como cor de fundo em áreas amplas — reservado para destaques e CTAs pontuais.
- Sage (`#8DAA91`) ou Sage Light (`#C5D5C8`) como cor de texto em fundo claro — contraste insuficiente.
- Substituir Fraunces ou DM Sans por fontes genéricas (Arial, Roboto, Helvetica, etc.).
- Aplicar sombra, gradiente, brilho ou efeito 3D em elementos da identidade visual.
- Usar Dark (`#2D312E`) em fundos — é exclusivo de texto; o equivalente escuro para fundos é o Plum.
- Usar Mid (`#6B7471`) em títulos ou botões CTA — peso visual insuficiente para posições de destaque.

---

## 7. Portais por Perfil

### 7.1 Portal da Paciente / Gestante

**Foco:** automonitoramento e acompanhamento da gestação.

| Página | Rota | Recursos da API |
|---|---|---|
| Dashboard | `/patient/dashboard` | Próxima consulta, semana gestacional, alertas de vitais fora do range |
| Minha Saúde — Glicose | `/patient/health/glucose` | `GET/POST /patients/{id}/glucose-readings`, `/stats`, `/chart` |
| Minha Saúde — Pressão | `/patient/health/blood-pressure` | `GET/POST /patients/{id}/blood-pressure`, `/stats`, `/chart` |
| Minha Saúde — Contrações | `/patient/health/contractions` | `GET/POST /patients/{id}/contractions`, `/stats`, `DELETE .../session` |
| Consultas | `/patient/appointments` | `GET /patients/{id}/appointments`, `PATCH .../confirm`, `POST .../reschedule-request`, `DELETE /appointments/{id}` |
| Detalhe da Consulta | `/patient/appointments/[id]` | `GET /appointments/{id}` |
| Exames | `/patient/exams` | `GET /patients/{id}/ultrasounds` |
| Meu Perfil | `/patient/profile` | `GET/PUT /users/{id}` |

**Componentes-chave:**
- `GestationalWeekBadge` — exibe semana atual e barra de progresso
- `VitalCard` — card com valor atual, classificação (Normal / Atenção / Alto) e badge colorido
- `GlucoseChart` / `BloodPressureChart` — gráficos de linha com limites clínicos
- `ContractionTimer` — cronômetro interativo para registrar duração e intervalo
- `AppointmentCard` — card com status, botões contextuais (confirmar / remarcar / cancelar)

---

### 7.2 Portal do Médico

**Foco:** acompanhamento clínico das pacientes e gestão da agenda.

| Página | Rota | Recursos da API |
|---|---|---|
| Dashboard | `/doctor/dashboard` | Consultas do dia, pacientes com risco alto, solicitações de remarcação pendentes |
| Lista de Pacientes | `/doctor/patients` | Listagem das pacientes vinculadas ao médico |
| Prontuário da Paciente | `/doctor/patients/[patientId]` | `GET /users/{id}`, todos os vitals e exames da paciente |
| Agenda | `/doctor/schedule` | `GET /patients/{id}/appointments`, `POST /doctors/{id}/appointments` |
| Detalhe da Consulta | `/doctor/schedule/[appointmentId]` | `GET/PATCH/DELETE /appointments/{id}`, aprovar remarcação |
| Registrar USG | `/doctor/patients/[id]/exams/new` | `POST /patients/{id}/ultrasounds` |
| Meu Perfil | `/doctor/profile` | `GET/PUT /users/{id}` |

**Componentes-chave:**
- `PatientRiskBadge` — badge com nível de risco (`low` / `medium` / `high`)
- `ProntuarioView` — layout em abas (Vitals / Exames / Consultas) do prontuário
- `AppointmentCalendar` — calendário mensal/semanal com slots de agenda
- `NewAppointmentModal` — formulário de criação de consulta (paciente, data, tipo, local)
- `RescheduleApprovalCard` — card com motivo da solicitação e campos para nova data/hora

---

### 7.3 Portal da Secretária

**Foco:** operação logística — agendamentos e gestão de cadastros.

| Página | Rota | Recursos da API |
|---|---|---|
| Dashboard | `/secretary/dashboard` | Consultas do dia por médico, pendências de confirmação, fila de remarcação |
| Agenda Geral | `/secretary/schedule` | `GET /patients/{id}/appointments` (todos), `POST /doctors/{id}/appointments`, `PATCH .../reschedule/approve`, `DELETE /appointments/{id}` |
| Detalhe da Consulta | `/secretary/schedule/[appointmentId]` | `GET/PATCH/DELETE /appointments/{id}` |
| Fila de Remarcações | `/secretary/reschedules` | Filtro de consultas com `patient_status = reschedule_requested`, `PATCH .../reschedule/approve` |
| Pacientes | `/secretary/patients` | Listagem de todas as pacientes da clínica |
| Meu Perfil | `/secretary/profile` | `GET/PUT /users/{id}` |

**Componentes-chave:**
- `DailyAgendaTable` — tabela do dia com todos os médicos e seus slots
- `RescheduleQueue` — lista de solicitações pendentes com aprovação rápida inline
- `AppointmentStatusPill` — badge visual para cada status (`pending` / `confirmed` / `reschedule_requested` / `cancelled`)

---

### 7.4 Portal do Superadmin (Lunna HQ)

**Foco:** gestão global do ecossistema e métricas da plataforma.

| Página | Rota | Recursos da API |
|---|---|---|
| Dashboard | `/superadmin/dashboard` | `GET /superadmin/metrics/overview`, `GET /superadmin/metrics/growth` |
| Gestão de Clínicas | `/superadmin/clinics` | `GET /superadmin/clinics`, `POST /superadmin/clinics` |
| Detalhe da Clínica | `/superadmin/clinics/[id]` | `GET /superadmin/clinics/[id]`, `PUT /superadmin/clinics/[id]` |
| Meu Perfil | `/superadmin/profile` | `GET/PUT /users/{id}` |

**Componentes-chave:**
- `PlatformKPICards` — exibe totais de clínicas, pacientes, médicos e consultas.
- `GrowthAreaChart` — gráfico de área (Recharts) comparando novos pacientes vs novas consultas nos últimos 30 dias.
- `ClinicStatusTable` — tabela com listagem de todas as clínicas, data de cadastro e administrador vinculado.
- `NewClinicForm` — wizard para cadastro de clínica e definição imediata do administrador inicial.

---

## 8. Páginas Compartilhadas

| Página | Rota | Descrição |
|---|---|---|
| Login | `/login` | Formulário de email/senha; aplica tema da clínica se URL contiver slug da clínica |
| Não Autorizado | `/403` | Exibida quando role não tem permissão na rota acessada |
| Não Encontrado | `/404` | Recurso não existente |

---

## 9. Tratamento de Estados de Dados

Usar TanStack Query com as seguintes convenções:

```ts
// Nomeação das query keys
["appointments", patientId, { status, limit, offset }]
["vitals", "glucose", patientId]
["vitals", "blood-pressure", patientId]
["user", userId]
["clinic", userId]
```

- **Loading:** skeleton screens (não spinner global)
- **Erro 401:** interceptor redireciona para `/login`
- **Erro 403:** redireciona para `/403`
- **Erro 404:** exibe estado vazio contextual
- **Erro 429 (rate limit):** toast com mensagem de "muitas tentativas, aguarde"

---

## 10. Endpoints da API por Módulo

### Autenticação
| Método | Endpoint | Uso |
|---|---|---|
| POST | `/auth/login` | Login |
| POST | `/auth/logout` | Logout |

### Usuários
| Método | Endpoint | Uso |
|---|---|---|
| GET | `/users/{id}` | Carregar perfil |
| PUT | `/users/{id}` | Atualizar perfil |
| GET | `/users/{id}/clinic` | Dados white-label da clínica |

### Consultas / Agendamentos
| Método | Endpoint | Roles |
|---|---|---|
| GET | `/patients/{id}/appointments` | Todos |
| GET | `/appointments/{id}` | Todos |
| POST | `/doctors/{id}/appointments` | doctor, secretary, admin |
| PATCH | `/appointments/{id}/confirm` | patient |
| POST | `/appointments/{id}/reschedule-request` | patient |
| PATCH | `/appointments/{id}/reschedule/approve` | doctor, secretary, admin |
| DELETE | `/appointments/{id}` | Todos |

### Sinais Vitais
| Método | Endpoint | Roles |
|---|---|---|
| POST/GET | `/patients/{id}/contractions` | patient, doctor |
| GET | `/patients/{id}/contractions/stats` | patient, doctor |
| DELETE | `/patients/{id}/contractions/session` | patient |
| POST/GET | `/patients/{id}/glucose-readings` | patient, doctor |
| GET | `/patients/{id}/glucose-readings/stats` | patient, doctor |
| GET | `/patients/{id}/glucose-readings/chart` | patient, doctor |
| POST/GET | `/patients/{id}/blood-pressure` | patient, doctor |
| GET | `/patients/{id}/blood-pressure/stats` | patient, doctor |
| GET | `/patients/{id}/blood-pressure/chart` | patient, doctor |

### Exames
| Método | Endpoint | Roles |
|---|---|---|
| POST | `/patients/{id}/ultrasounds` | doctor, admin |
| GET | `/patients/{id}/ultrasounds` | patient, doctor, admin |

---

## 11. Requisitos Não-Funcionais

- **Acessibilidade:** WCAG 2.1 AA — foco visível, `aria-label`, contraste mínimo 4.5:1 (exigido também pelo brand guide; combinações proibidas: Sage/Sage Light como texto em fundo claro)
- **Responsividade:** breakpoints `sm` (640px), `md` (768px), `lg` (1024px)
- **Performance:** Server Components para páginas estáticas; Client Components apenas onde há interatividade; imagens com `next/image`
- **Segurança:** nunca expor JWT em `localStorage`; validar `role` no middleware do Next.js antes de renderizar cada portal
- **i18n:** estrutura preparada para `pt-BR` como locale padrão; textos em arquivos de dicionário (`/messages/pt-BR.json`)
