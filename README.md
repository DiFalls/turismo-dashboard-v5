# 🌊 Turismo Nordeste Dashboard v4.0

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://turismo-dashboard-v4-seuusuario.streamlit.app)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

Dashboard estratégico para análise de desempenho do setor de turismo no Nordeste brasileiro.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Dashboard+Preview)

## 📊 Sobre o Dashboard
Este dashboard foi desenvolvido para apoiar a análise de desempenho de empreendimentos do setor de turismo (hotéis, pousadas e agências) nos estados do Ceará (CE), Pernambuco (PE), Piauí (PI) e Rio Grande do Norte (RN).

### Funcionalidades
- **KPIs Estratégicos**: Receita Total, Clientes, Ocupação Média, Avaliação, Ticket Médio
- **Filtros Interativos**: Tipo de empreendimento, período (janela deslizante), estado e cidade
- **Gráficos Dinâmicos**: 
  - Evolução da Receita Mensal
  - Mix por Tipo (Donut)
  - Matriz Estratégica (Ocupação × Satisfação)
  - Ranking de Cidades
  - Heatmap de Sazonalidade
  - Perfil Competitivo (Radar)
- **Insights Automáticos**: Análise baseada nos dados filtrados
- **Tabela Gerencial**: Sumário por Estado e Tipo

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Baixe os arquivos
Baixe todos os arquivos do projeto para uma pasta no seu computador.

### Passo 2: Crie um ambiente virtual (recomendado)

**Windows:**
python -m venv .venv
.venv\Scripts\activate

**Mac/Linux:**
python3 -m venv .venv
source .venv/bin/activate

### Passo 3: Instale as dependências
pip install -r requirements.txt

### Passo 4: Verifique o arquivo de dados
Certifique-se de que o arquivo `base_case_turismo.xlsx` está na mesma pasta do `streamlit_app.py`.

### Passo 5: Execute o dashboard
streamlit run streamlit_app.py

O dashboard será aberto automaticamente no seu navegador em `http://localhost:8501`

## 📦 Dependências

|   Pacote   |  Versão  |              Descrição              |
|------------|----------|-------------------------------------|
|  streamlit | >=1.32.0 | Framework para criação do dashboard |
|   plotly   | >=5.19.0 |   Criação de gráficos interativos   |
|   pandas   | >=2.0.0  |    Manipulação e análise de dados   |
|    numpy   | >=1.24.0 |         Operações matemáticas       |
|  openpyxl  | >=3.1.0  |      Leitura de arquivos Excel      |
---------------------------------------------------------------

## 🎯 Como Usar o Dashboard

### Filtros na Sidebar
1. **Tipo de Empreendimento**: Selecione Hotel, Pousada e/ou Agência
2. **Período de Análise**: Defina o tamanho da janela (quantos meses) e ajuste a posição inicial
3. **Localização**: Selecione estados e expanda para escolher cidades específicas

### Navegação
O dashboard possui três abas:
- **Dashboard**: Visualização principal com todos os gráficos e KPIs
- **Como Interpretar os Gráficos**: Guia explicativo de cada visualização
- **Como Usar os Filtros**: Tutorial e dicas para uso dos filtros

### Exportação
- Clique no botão 🖨️ Imprimir / PDF para gerar um PDF do dashboard
- Passe o mouse sobre qualquer gráfico e clique na câmera para exportar como PNG

## 📁 Estrutura do Projeto
turismo-dashboard-v4/
├── streamlit_app.py # Código principal do dashboard
├── base_case_turismo.xlsx # Base de dados (432 registros)
├── requirements.txt # Dependências do projeto
├── LICENSE # Licença de uso
└── README.md # Este arquivo

## 🔧 Solução de Problemas
**Erro: "Arquivo base_case_turismo.xlsx não encontrado"**
Solução: Verifique se o arquivo está na mesma pasta do streamlit_app.py.

**Erro: "Module not found"**
Solução: Instale as dependências novamente: pip install -r requirements.txt --upgrade

**Erro: "Porta 8501 já está em uso"**
Solução: Use uma porta diferente: streamlit run streamlit_app.py --server.port 8502


## 📊 Dados da Base

- **Período**: 12 meses (Janeiro a Dezembro)
- **Estados**: CE, PE, PI, RN
- **Cidades**: 12 cidades
- **Tipos**: Hotel, Pousada, Agência
- **Registros**: 432 (12 meses × 12 cidades × 3 tipos)

## 🛠️ Tecnologias Utilizadas

- Streamlit - Framework Python para dashboards
- Plotly - Biblioteca de gráficos interativos
- Pandas - Manipulação de dados
- NumPy - Computação numérica

## 📝 Licença

Este projeto está licenciado sob a **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License**.

- ✅ Você pode compartilhar este código (copiar e redistribuir)
- ✅ Você deve dar crédito ao autor original
- ❌ Você NÃO pode usar para fins comerciais
- ❌ Você NÃO pode modificar e distribuir versões alteradas

Para mais informações: https://creativecommons.org/licenses/by-nc-nd/4.0/

## 👤 Autor
**Pedro Victor S.**
- GitHub: @Difalls

## 🙏 Agradecimentos
Dados fictícios criados para fins de demonstração e aprendizado.

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
