# Sistema Tutor Inteligente de Lógica Proposicional

**Equivalências Lógicas** - Um sistema inteligente para ensino personalizado de lógica proposicional

## Sobre o Projeto

Este projeto implementa um **Sistema Tutor Inteligente (STI)** para o ensino e avaliação de equivalências lógicas em lógica proposicional. O sistema utiliza uma arquitetura clássica baseada em conhecimento, proporcionando uma experiência de aprendizado personalizada e adaptativa.

### Características Principais

- **Ensino Personalizado**: Adapta-se ao ritmo e nível de cada estudante
- **Avaliação Inteligente**: Sistema de feedback automatizado e detalhado
- **Resolução Automática**: Motor de inferência para validação de equivalências
- **Acompanhamento de Progresso**: Análise visual do desempenho do aluno
- **Integração com IA**: Suporte a APIs de modelos de linguagem (Gemini, OpenRouter)

## Arquitetura do Sistema

O sistema segue a arquitetura clássica de Sistemas Tutores Inteligentes com os seguintes componentes:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Modelo         │    │  Modelo         │    │  Modelo do      │
│  Especialista   │    │  Pedagógico     │    │  Estudante      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Controlador/   │
                    │  Mediação       │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Interface      │
                    │  do Estudante   │
                    └─────────────────┘
```

## Estrutura do Projeto

```
Tutor-de-equivalencia-logica/
│
├── questoes/                    # Banco de questões por nível
├── dados/                       # Dados de progresso dos alunos
│   └── perfis/                  # Perfis individuais dos estudantes
├── src/
│   ├── main.py                  # Ponto de entrada da aplicação
│   ├── screens/                 # Interface gráfica do usuário
│   ├── especialista/            # Modelo Especialista e Base de Regras
│   ├── pedagogico/              # Modelo Pedagógico
│   ├── perfil/                  # Modelagem do Estudante
│   ├── llm_interface/           # Integração com APIs de IA
│   └── utils.py, config.py      # Utilitários e configuração
├── requirements.txt             # Dependências do projeto
├── .env                         # Chaves de API (não versionado)
└── README.md                    # Este arquivo
```

### Componentes Principais

| Componente | Localização | Função |
|------------|-------------|---------|
| **Modelo Especialista** | `src/especialista/` | Resolve problemas, avalia soluções e aplica regras lógicas |
| **Modelo Pedagógico** | `src/pedagogico/` | Define estratégias de ensino e controla progressão |
| **Modelo do Estudante** | `src/perfil/` | Monitora e analisa o desempenho do aluno |
| **Controlador** | `src/screens/` | Interface entre estudante e sistema |
| **Base de Conhecimento** | `questoes/` | Curriculum estruturado por níveis |

## Como Começar

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/tutor-de-equivalencia-logica.git
   cd tutor-de-equivalencia-logica
   ```

2. **Crie um ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure as chaves de API:**
   
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   GEMINI_API_KEY="sua-chave-gemini"
   OPENROUTER_API_KEY="sua-chave-openrouter"
   ```

6. **Execute o sistema:**
   ```bash
   python main.py
   ```

## Funcionalidades

### Para Estudantes
- Interface intuitiva e amigável
- Exercícios graduais de equivalências lógicas
- Feedback imediato e detalhado
- Acompanhamento visual do progresso
- Sistema de níveis adaptativos

### Para Educadores
- Monitoramento do progresso dos alunos
- Relatórios detalhados de performance
- Personalização de conteúdo
- Análise de padrões de aprendizado

## Tecnologias Utilizadas

- **Python 3.10+**: Linguagem principal
- **Tkinter**: Interface gráfica
- **JSON**: Armazenamento de dados
- **APIs de IA**: Gemini, OpenRouter
- **Matplotlib**: Visualização de dados

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Autores

- **Alison Bruno Martires Soares** - 
- **Jean Felipe Duarte Tenório** -
- **Rian Américo Brito da Silva** - 
- **Davi Silva de Melo Lins** - 
