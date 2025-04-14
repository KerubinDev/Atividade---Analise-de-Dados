# Projeto de Análise de Dados: Crescimento de Plantas com Diferentes Tipos de Água

Este projeto analisa como diferentes tipos de água afetam o crescimento e desenvolvimento de plantas de feijão durante um período de 14 dias.

## Visão Geral do Experimento

Neste experimento, comparamos o crescimento de plantas de feijão utilizando três tipos diferentes de água:
- Água da torneira
- Água mineral
- Água com açúcar (5g de açúcar por 100ml de água)

Durante 14 dias, medimos o crescimento das plantas e registramos dados para posterior análise.

## Materiais Utilizados

- 30 sementes de feijão
- 30 copos plásticos
- Algodão
- Água da torneira
- Água mineral
- Açúcar
- Régua milimetrada
- Caderno para anotações
- Câmera para documentação fotográfica
- Computador com Python instalado para análise de dados

## Metodologia

1. **Preparação dos copos**: Forramos o fundo de cada copo com algodão umedecido
2. **Divisão em grupos**: Separamos 10 copos para cada tipo de água
3. **Plantio**: Colocamos uma semente de feijão em cada copo
4. **Identificação**: Etiquetamos cada grupo (A: torneira, B: mineral, C: açúcar)
5. **Hidratação**: Regamos cada grupo com seu respectivo tipo de água diariamente
6. **Registro**: Medimos e registramos a altura das plantas e contamos o número de folhas diariamente
7. **Documentação**: Fotografamos as plantas a cada 3 dias para documentação visual

## Coleta de Dados

Para cada planta, registramos:
- Altura em milímetros (do algodão até a ponta mais alta)
- Número de folhas
- Taxa de germinação (porcentagem de sementes que germinaram)
- Observações visuais (cor, aspecto, etc.)

## Análise de Dados

A análise foi realizada utilizando Python com as bibliotecas:
- Pandas: para organização dos dados
- Matplotlib: para criação de gráficos
- NumPy: para cálculos estatísticos

O código de análise está disponível no arquivo `analise/analisar_dados.py`.

## Estrutura do Repositório

```
/
├── README.md                  # Este arquivo
├── dados/                     # Pasta com dados coletados
│   └── medicoes.xlsx          # Planilha com medições diárias
├── fotos/                     # Fotos do experimento
│   ├── dia_1/                 # Fotos do primeiro dia
│   ├── dia_4/                 # Fotos do quarto dia
│   ├── dia_7/                 # Fotos do sétimo dia
│   ├── dia_10/                # Fotos do décimo dia
│   └── dia_14/                # Fotos do último dia
├── analise/                   # Código para análise de dados
│   └── analisar_dados.py      # Script Python para análise
└── resultados/                # Gráficos e resultados gerados
    ├── grafico_crescimento.png  # Gráfico de altura das plantas
    ├── grafico_folhas.png       # Gráfico de número de folhas
    └── grafico_germinacao.png   # Gráfico de taxa de germinação
```

## Principais Resultados

- **Taxa de Germinação**: A água mineral resultou na maior taxa de germinação (90%), seguida pela água da torneira (80%) e água com açúcar (60%).
- **Crescimento em Altura**: As plantas regadas com água da torneira cresceram ligeiramente mais (89mm) do que as regadas com água mineral (88mm). As plantas regadas com água com açúcar apresentaram crescimento significativamente menor (60mm).
- **Desenvolvimento de Folhas**: As plantas regadas com água mineral desenvolveram mais folhas (média de 6 folhas ao final do experimento), em comparação com a água da torneira (5 folhas) e água com açúcar (3 folhas).
- **Observações Gerais**: As plantas regadas com água com açúcar apresentaram sinais de estresse, com folhas amareladas e crescimento atrofiado.

## Conclusões

Este experimento demonstra que o tipo de água usado na irrigação afeta significativamente o desenvolvimento das plantas. A água mineral mostrou-se ideal para germinação e desenvolvimento foliar, enquanto a água da torneira foi ligeiramente melhor para o crescimento em altura. A água com açúcar prejudicou o desenvolvimento normal das plantas, demonstrando que nem sempre mais nutrientes significa melhor crescimento.

Este projeto simples demonstra como podemos aplicar técnicas de análise de dados para compreender fenômenos biológicos básicos.

## Como Executar a Análise

1. Certifique-se de ter Python instalado (versão 3.6 ou superior)
2. Instale as bibliotecas necessárias:
   ```
   pip install pandas matplotlib numpy
   ```
3. Execute o script de análise:
   ```
   python analise/analisar_dados.py
   ```
4. Os gráficos serão gerados e salvos na pasta `resultados/`
