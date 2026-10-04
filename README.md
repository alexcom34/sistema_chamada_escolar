# sistema_chamada_escolar
sistema pessoal meu para fazer chamadas

# 📋 Sistema de Chamada

Aplicação desktop desenvolvida em **Python + Tkinter + MySQL** para gerenciamento de turmas, alunos, disciplinas e controle detalhado de frequência.

O sistema foi desenvolvido para funcionar como uma aplicação desktop distribuível para Windows, podendo ser empacotado em `.exe` e distribuído através de um instalador.

---

## 🚀 Funcionalidades

O sistema atualmente permite:

* Cadastro de alunos
* Cadastro de turmas
* Cadastro de matrículas
* Cadastro de disciplinas
* Associação de disciplinas às turmas
* Controle de professores
* Registro de chamadas
* Controle de presença por hora-aula
* Registro de:

  * Presença
  * Falta
  * Falta justificada
* Histórico de chamadas
* Relatórios de frequência
* Relatório detalhado de presença
* Consulta por turma
* Consulta individual por aluno
* Exportação de relatórios para Excel
* Exportação de relatórios para PDF
* Configuração automática do banco de dados
* Criação automática das tabelas
* Configuração independente por computador
* Distribuição através de executável Windows

---

# 🏗️ Arquitetura

O projeto utiliza uma arquitetura separada por responsabilidades:

```text
sistema_chamada/
│
├── app.py
├── config.py
├── requirements.txt
├── instalador.iss
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── initializer.py
│
├── repositories/
│   ├── __init__.py
│   ├── aluno_repository.py
│   ├── turma_repository.py
│   ├── matricula_repository.py
│   ├── professor_repository.py
│   ├── disciplina_repository.py
│   ├── turma_disciplina_repository.py
│   ├── aula_repository.py
│   ├── presenca_repository.py
│   ├── relatorio_repository.py
│   └── relatorio_presenca_repository.py
│
├── services/
│   ├── carga_horaria_service.py
│   └── chamada_service.py
│
└── views/
    ├── __init__.py
    ├── alunos_view.py
    ├── turmas_view.py
    ├── matriculas_view.py
    ├── disciplinas_view.py
    ├── turma_disciplinas_view.py
    ├── chamada_view.py
    ├── historico_chamadas_view.py
    ├── relatorios_view.py
    ├── relatorio_presenca_view.py
    └── config_banco_view.py
```

---

# 🧩 Tecnologias

## Backend / Aplicação

* Python
* Tkinter
* MySQL
* MySQL Connector/Python

## Relatórios

* OpenPyXL
* ReportLab

## Empacotamento

* PyInstaller

## Instalador

* Inno Setup

---

# 🗄️ Banco de Dados

O sistema utiliza o banco:

```text
sistema_chamada
```

O banco é criado automaticamente na primeira configuração.

## Estrutura

### professores

Armazena os professores cadastrados.

```text
id
nome
email
ativo
```

### turmas

Armazena as turmas.

```text
id
nome
codigo
ano
semestre
professor_id
ativo
```

### alunos

Armazena os alunos.

```text
id
nome
matricula
email
ativo
```

### matriculas

Relaciona alunos e turmas.

```text
id
aluno_id
turma_id
data_matricula
ativo
```

### disciplinas

Armazena as disciplinas.

```text
id
nome
codigo
carga_horaria
minutos_hora_aula
ativo
```

### turma_disciplinas

Relaciona uma turma com uma disciplina e seu professor.

```text
id
turma_id
disciplina_id
professor_id
aulas_previstas
```

### aulas

Representa as aulas realizadas.

```text
id
turma_disciplina_id
data_aula
quantidade_horas_aula
observacao
```

### presencas

Armazena a frequência individual de cada aluno em cada hora-aula.

```text
id
aula_id
aluno_id
numero_hora_aula
status
```

O campo `status` utiliza:

```text
PRESENTE
FALTA
JUSTIFICADA
```

---

# 🔗 Relacionamentos

A estrutura principal do banco pode ser representada da seguinte forma:

```text
PROFESSORES
     │
     ├───────────────┐
     │               │
     ▼               ▼
  TURMAS       TURMA_DISCIPLINAS
     │               │
     │               ▼
     │          DISCIPLINAS
     │
     ▼
 MATRÍCULAS
     │
     ▼
  ALUNOS


TURMA_DISCIPLINAS
        │
        ▼
      AULAS
        │
        ▼
    PRESENCAS
        │
        ▼
      ALUNOS
```

---

# 📊 Modelo de frequência

O sistema trabalha com frequência por **hora-aula**.

Por exemplo, uma aula com três horas-aula pode produzir:

| Aluno  | Hora 1 | Hora 2 | Hora 3 |
| ------ | ------ | ------ | ------ |
| João   | P      | P      | F      |
| Maria  | P      | F      | F      |
| Carlos | P      | P      | P      |

Onde:

```text
P = Presente
F = Falta
J = Falta Justificada
- = Sem aula/sem registro
```

Essa abordagem permite identificar faltas parciais dentro de uma mesma aula.

---

# 🔄 Fluxo do sistema

O fluxo principal da aplicação é:

```text
Configuração do banco
        ↓
Cadastro de disciplinas
        ↓
Cadastro de turmas
        ↓
Cadastro de alunos
        ↓
Matrícula dos alunos
        ↓
Vinculação das disciplinas às turmas
        ↓
Registro das aulas
        ↓
Registro das presenças
        ↓
Histórico
        ↓
Relatórios
        ↓
Exportação Excel/PDF
```

---

# ⚙️ Configuração do banco

Uma das principais características do projeto é que a configuração do MySQL **não fica fixa no código**.

Na primeira execução, o sistema verifica se existe uma configuração salva.

Caso não exista, abre:

```text
Configuração do MySQL
```

O usuário informa:

```text
Servidor
Porta
Usuário
Senha
```

O sistema testa a conexão e, caso seja válida:

1. Cria o banco `sistema_chamada`, se necessário;
2. Cria as tabelas;
3. Salva a configuração;
4. Inicia o sistema.

---

# 🔐 Configuração por computador

A configuração é armazenada no diretório de dados do usuário do Windows:

```text
%APPDATA%\SistemaChamada\config_banco.json
```

Isso permite que computadores diferentes utilizem configurações diferentes.

Por exemplo:

```text
Computador A
    MySQL → senha A

Computador B
    MySQL → senha B
```

O mesmo executável pode ser utilizado nos dois computadores.

A senha do banco não é incorporada ao executável durante a compilação.

> **Importante:** o arquivo de configuração contém credenciais do banco e não deve ser versionado no Git.

---

# 🖥️ Execução em desenvolvimento

## 1. Criar ambiente virtual

```bash
python -m venv venv
```

Ativar no Windows:

```bash
venv\Scripts\activate
```

---

## 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 3. Executar

```bash
python app.py
```

Na primeira execução, será solicitada a configuração do MySQL.

---

# 📦 Dependências

O arquivo `requirements.txt` contém:

```text
mysql-connector-python
openpyxl
reportlab
```

Para instalar:

```bash
pip install -r requirements.txt
```

---

# 🏭 Gerando o executável

O projeto utiliza o **PyInstaller**.

Instalação:

```bash
pip install pyinstaller
```

Para gerar o executável:

```bash
pyinstaller --noconfirm --clean --onefile --windowed --name SistemaChamada app.py
```

O executável será criado em:

```text
dist/
└── SistemaChamada.exe
```

---

# 🧹 Build limpo

Para gerar uma compilação completamente limpa, remova os diretórios anteriores.

No PowerShell:

```powershell
Remove-Item -Recurse -Force build
Remove-Item -Recurse -Force dist
```

Depois execute novamente:

```powershell
pyinstaller --noconfirm --clean --onefile --windowed --name SistemaChamada app.py
```

---

# 📥 Criando o instalador

O projeto utiliza o **Inno Setup** para gerar o instalador do Windows.

O arquivo:

```text
instalador.iss
```

define:

* Nome da aplicação;
* Versão;
* Diretório de instalação;
* Atalhos;
* Executável que será instalado;
* Execução automática após a instalação.

O instalador utiliza:

```text
dist\SistemaChamada.exe
```

como fonte.

Após compilar o projeto com PyInstaller, o instalador deve ser recompilado no Inno Setup para incorporar a nova versão do executável.

O resultado será:

```text
instalador/
└── SistemaChamada-Setup.exe
```

---

# 📁 Distribuição

O arquivo que deve ser enviado ao usuário final é:

```text
SistemaChamada-Setup.exe
```

O usuário não precisa receber:

```text
app.py
venv/
build/
repositories/
services/
views/
database/
```

O instalador contém o executável necessário para utilização da aplicação.

---

# 🔧 Primeira execução em um computador novo

O fluxo é:

```text
SistemaChamada-Setup.exe
        ↓
Instalação
        ↓
SistemaChamada.exe
        ↓
Verifica configuração
        ↓
Configuração inexistente
        ↓
Tela de configuração MySQL
        ↓
Teste de conexão
        ↓
Criação do banco
        ↓
Criação das tabelas
        ↓
Sistema iniciado
```

Nas execuções seguintes:

```text
SistemaChamada.exe
        ↓
Carrega configuração
        ↓
Conecta ao MySQL
        ↓
Sistema iniciado
```

---

# 🔄 Atualização

Uma nova versão pode ser distribuída através de um novo instalador.

A configuração do banco fica fora do diretório de instalação:

```text
%APPDATA%\SistemaChamada\
```

Por isso, atualizar o executável não precisa apagar a configuração existente.

Os dados continuam armazenados no MySQL.

---

# 📑 Relatórios

O projeto possui dois fluxos principais de relatório.

## Relatório de frequência

Utilizado para consultar informações consolidadas de frequência.

## Relatório detalhado de presença

Permite visualizar a frequência detalhada por:

* Turma;
* Aluno;
* Data;
* Hora-aula.

Também permite exportação para:

```text
.xlsx
.pdf
```

---

# 📤 Exportação Excel

A exportação utiliza:

```text
openpyxl
```

O arquivo gerado pode ser aberto pelo Microsoft Excel e outros softwares compatíveis com `.xlsx`.

---

# 📄 Exportação PDF

A exportação utiliza:

```text
reportlab
```

Os relatórios são gerados em PDF, permitindo impressão e compartilhamento.

---

# 🧱 Organização do código

## `app.py`

Ponto de entrada da aplicação.

Responsável por:

* Criar a janela principal;
* Inicializar a aplicação;
* Verificar o banco;
* Abrir as diferentes telas.

---

## `config.py`

Responsável pela configuração do banco.

Funções principais:

```python
carregar_config()
salvar_config()
caminho_config()
```

---

## `database/`

Responsável pela comunicação e inicialização do banco.

### `connection.py`

Cria conexões com o MySQL utilizando a configuração salva.

### `initializer.py`

Responsável por:

* Testar conexão;
* Criar banco;
* Criar tabelas.

---

## `repositories/`

Camada responsável pelo acesso aos dados.

Cada repository concentra operações relacionadas a uma entidade.

Exemplos:

```text
aluno_repository.py
turma_repository.py
disciplina_repository.py
presenca_repository.py
```

Isso evita concentrar toda a lógica SQL em uma única parte da aplicação.

---

## `services/`

Contém regras de negócio da aplicação.

Exemplos:

```text
carga_horaria_service.py
chamada_service.py
```

Essa camada é utilizada para regras que vão além do simples CRUD.

---

## `views/`

Contém as interfaces gráficas do sistema.

Cada tela possui sua própria implementação.

Exemplos:

```text
alunos_view.py
turmas_view.py
chamada_view.py
relatorios_view.py
```

---

# 🔒 Segurança e Git

O arquivo abaixo contém informações sensíveis:

```text
config_banco.json
```

Ele **não deve ser enviado para o GitHub**.

Como ele fica no `%APPDATA%`, normalmente não está dentro do diretório do projeto.

Também não devem ser publicados:

```text
senhas
tokens
credenciais
arquivos .env contendo segredos
backups reais do banco
```

---

# 📝 `.gitignore`

Recomenda-se utilizar um `.gitignore` semelhante a:

```gitignore
# Ambiente virtual
venv/
.venv/

# PyInstaller
build/
dist/
*.spec

# Configurações locais
config_banco.json
*.env

# Configuração local
__pycache__/
*.py[cod]

# IDE
.vscode/
.idea/

# Sistema operacional
.DS_Store
Thumbs.db
```

> O `*.spec` pode ser removido do `.gitignore` caso o projeto passe a manter o arquivo `.spec` versionado propositalmente.

---

# 🧪 Testes recomendados

Antes de distribuir uma nova versão:

### Teste 1 — Python

```bash
python app.py
```

### Teste 2 — Primeira configuração

Verificar se a tela do MySQL aparece quando não existe configuração.

### Teste 3 — Conexão

Verificar se o sistema consegue conectar ao MySQL.

### Teste 4 — Criação do banco

Verificar se:

```text
sistema_chamada
```

é criado corretamente.

### Teste 5 — Cadastro

Cadastrar:

* Aluno;
* Turma;
* Disciplina;
* Matrícula.

### Teste 6 — Chamada

Criar uma aula e registrar:

```text
P
F
J
```

### Teste 7 — Relatórios

Gerar os relatórios e verificar os dados.

### Teste 8 — Exportação

Testar:

```text
Excel
PDF
```

### Teste 9 — Executável

Gerar:

```text
SistemaChamada.exe
```

e executar sem Python.

### Teste 10 — Instalação

Gerar:

```text
SistemaChamada-Setup.exe
```

e instalar em um computador de teste.

---

# 📌 Estrutura final do projeto

```text
sistema_chamada/
│
├── app.py
├── config.py
├── requirements.txt
├── instalador.iss
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── initializer.py
│
├── repositories/
│   ├── __init__.py
│   ├── aluno_repository.py
│   ├── turma_repository.py
│   ├── matricula_repository.py
│   ├── professor_repository.py
│   ├── disciplina_repository.py
│   ├── turma_disciplina_repository.py
│   ├── aula_repository.py
│   ├── presenca_repository.py
│   ├── relatorio_repository.py
│   └── relatorio_presenca_repository.py
│
├── services/
│   ├── carga_horaria_service.py
│   └── chamada_service.py
│
└── views/
    ├── __init__.py
    ├── alunos_view.py
    ├── turmas_view.py
    ├── matriculas_view.py
    ├── disciplinas_view.py
    ├── turma_disciplinas_view.py
    ├── chamada_view.py
    ├── historico_chamadas_view.py
    ├── relatorios_view.py
    ├── relatorio_presenca_view.py
    └── config_banco_view.py
```

---

# 🚀 Roadmap

Possíveis evoluções futuras:

* [ ] Cadastro completo de professores
* [ ] Sistema de login e permissões
* [ ] Dashboard de frequência
* [ ] Indicadores de alunos com baixa frequência
* [ ] Filtros avançados nos relatórios
* [ ] Backup automático do banco
* [ ] Restauração de backup
* [ ] Controle de usuários
* [ ] Melhorias de interface
* [ ] Sistema de atualização automática
* [ ] Suporte a banco MySQL remoto
* [ ] Logs de operação
* [ ] Controle de versões das alterações

---

# 👨‍💻 Desenvolvimento

Projeto desenvolvido como uma aplicação desktop para gerenciamento de frequência acadêmica, com foco em:

* Organização de dados;
* Separação de responsabilidades;
* Persistência relacional;
* Automação da configuração do ambiente;
* Geração de relatórios;
* Distribuição simplificada para usuários Windows.

---

# 📄 Licença

Defina aqui a licença do projeto de acordo com a forma como deseja disponibilizá-lo.

Exemplo:

```text
Copyright © 2026 Alexandre Gaspari.

Todos os direitos reservados.
```

Caso o projeto seja disponibilizado como código aberto, recomenda-se escolher uma licença apropriada, como MIT, Apache-2.0 ou GPL-3.0.
