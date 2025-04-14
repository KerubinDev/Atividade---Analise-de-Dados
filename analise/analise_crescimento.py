import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Configurando o estilo dos gráficos
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('Set2')

# Criando diretório para resultados se não existir
os.makedirs('../resultados', exist_ok=True)

# Carregando os dados
def carregar_dados():
    """Carrega os dados do arquivo CSV"""
    df = pd.read_csv('../dados/medicoes.csv')
    print(f"Dados carregados com sucesso! {len(df)} registros encontrados.")
    return df

# Análise exploratória básica
def analise_exploratoria(df):
    """Realiza uma análise exploratória básica dos dados"""
    print("\n=== ANÁLISE EXPLORATÓRIA ===")
    print("\nInformações gerais:")
    print(df.info())
    
    print("\nEstatísticas descritivas:")
    print(df.describe())
    
    print("\nContagem por tipo de água:")
    print(df['Tipo_Agua'].value_counts())
    
    print("\nTaxa de germinação por tipo de água:")
    print(df.groupby('Tipo_Agua')['Germinada'].mean())

# Análise de crescimento
def analisar_crescimento(df):
    """Analisa o crescimento das plantas ao longo do tempo por tipo de água"""
    print("\n=== ANÁLISE DE CRESCIMENTO ===")
    
    # Criando um DataFrame com a média de altura por dia e tipo de água
    altura_media = df.groupby(['Dia', 'Tipo_Agua'])['Altura_cm'].mean().reset_index()
    
    # Plotando o gráfico de crescimento
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=altura_media, x='Dia', y='Altura_cm', hue='Tipo_Agua', marker='o')
    plt.title('Crescimento médio das plantas por tipo de água')
    plt.xlabel('Dia do experimento')
    plt.ylabel('Altura média (cm)')
    plt.grid(True)
    plt.savefig('../resultados/crescimento_medio.png')
    print("Gráfico de crescimento salvo em '../resultados/crescimento_medio.png'")
    
    # Calculando a taxa de crescimento diário
    print("\nTaxa de crescimento diário:")
    for tipo in df['Tipo_Agua'].unique():
        dados_tipo = altura_media[altura_media['Tipo_Agua'] == tipo]
        crescimento_diario = dados_tipo['Altura_cm'].diff() / dados_tipo['Altura_cm'].shift(1)
        crescimento_diario = crescimento_diario.fillna(0)
        print(f"{tipo}: {crescimento_diario.mean()*100:.2f}% ao dia em média")

# Análise de número de folhas
def analisar_folhas(df):
    """Analisa o desenvolvimento de folhas por tipo de água"""
    print("\n=== ANÁLISE DE FOLHAS ===")
    
    # Criando um DataFrame com a média de folhas por dia e tipo de água
    folhas_media = df.groupby(['Dia', 'Tipo_Agua'])['Num_Folhas'].mean().reset_index()
    
    # Plotando o gráfico de desenvolvimento de folhas
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=folhas_media, x='Dia', y='Num_Folhas', hue='Tipo_Agua', marker='o')
    plt.title('Desenvolvimento médio de folhas por tipo de água')
    plt.xlabel('Dia do experimento')
    plt.ylabel('Número médio de folhas')
    plt.grid(True)
    plt.savefig('../resultados/folhas_media.png')
    print("Gráfico de desenvolvimento de folhas salvo em '../resultados/folhas_media.png'")

# Análise de germinação
def analisar_germinacao(df):
    """Analisa a taxa de germinação por tipo de água ao longo do tempo"""
    print("\n=== ANÁLISE DE GERMINAÇÃO ===")
    
    # Convertendo a coluna 'Germinada' para valor numérico se for texto
    if df['Germinada'].dtype == 'object':
        df['Germinada_num'] = df['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df['Germinada_num'] = df['Germinada']
    
    # Calculando a taxa de germinação por dia e tipo de água
    taxa_germinacao = df.groupby(['Dia', 'Tipo_Agua'])['Germinada_num'].mean().reset_index()
    
    # Plotando o gráfico de taxa de germinação
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=taxa_germinacao, x='Dia', y='Germinada_num', hue='Tipo_Agua', marker='o')
    plt.title('Taxa de germinação por tipo de água')
    plt.xlabel('Dia do experimento')
    plt.ylabel('Taxa de germinação (%)')
    plt.ylim(0, 1.1)
    plt.grid(True)
    plt.savefig('../resultados/taxa_germinacao.png')
    print("Gráfico de taxa de germinação salvo em '../resultados/taxa_germinacao.png'")
    
    # Dia médio de germinação
    plantas_germinadas = df[df['Germinada_num'] == 1]
    dia_germinacao = plantas_germinadas.groupby(['ID_Planta', 'Tipo_Agua'])['Dia'].min().reset_index()
    media_dias = dia_germinacao.groupby('Tipo_Agua')['Dia'].mean()
    
    print("\nDia médio de germinação por tipo de água:")
    print(media_dias)
    
    # Plotando o boxplot do dia de germinação
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=dia_germinacao, x='Tipo_Agua', y='Dia')
    plt.title('Distribuição do dia de germinação por tipo de água')
    plt.xlabel('Tipo de água')
    plt.ylabel('Dia de germinação')
    plt.grid(True)
    plt.savefig('../resultados/dia_germinacao_boxplot.png')
    print("Boxplot de dia de germinação salvo em '../resultados/dia_germinacao_boxplot.png'")

# Análise comparativa final
def analise_comparativa(df):
    """Realiza uma análise comparativa final entre os diferentes tipos de água"""
    print("\n=== ANÁLISE COMPARATIVA FINAL ===")
    
    # Obtendo o último dia do experimento
    ultimo_dia = df['Dia'].max()
    
    # Selecionando apenas os dados do último dia
    df_ultimo_dia = df[df['Dia'] == ultimo_dia]
    
    # Calculando estatísticas por tipo de água
    estatisticas = df_ultimo_dia.groupby('Tipo_Agua').agg({
        'Altura_cm': ['mean', 'std', 'min', 'max'],
        'Num_Folhas': ['mean', 'std', 'min', 'max'],
        'Germinada_num': 'mean'
    })
    
    print(f"\nEstatísticas no último dia (Dia {ultimo_dia}):")
    print(estatisticas)
    
    # Criando gráficos comparativos
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Altura final
    sns.barplot(data=df_ultimo_dia, x='Tipo_Agua', y='Altura_cm', ax=axes[0])
    axes[0].set_title('Altura final por tipo de água')
    axes[0].set_ylabel('Altura (cm)')
    axes[0].set_xlabel('Tipo de água')
    
    # Número de folhas final
    sns.barplot(data=df_ultimo_dia, x='Tipo_Agua', y='Num_Folhas', ax=axes[1])
    axes[1].set_title('Número de folhas final por tipo de água')
    axes[1].set_ylabel('Número de folhas')
    axes[1].set_xlabel('Tipo de água')
    
    # Taxa de germinação final
    taxa_germinacao = df_ultimo_dia.groupby('Tipo_Agua')['Germinada_num'].mean()
    taxa_germinacao.plot(kind='bar', ax=axes[2])
    axes[2].set_title('Taxa de germinação final por tipo de água')
    axes[2].set_ylabel('Taxa de germinação (%)')
    axes[2].set_xlabel('Tipo de água')
    axes[2].set_ylim(0, 1.1)
    
    plt.tight_layout()
    plt.savefig('../resultados/comparativo_final.png')
    print("Gráfico comparativo final salvo em '../resultados/comparativo_final.png'")

# Função principal
def main():
    """Função principal que executa todas as análises"""
    print("=== ANÁLISE DE DADOS DO EXPERIMENTO DE CRESCIMENTO DE FEIJÕES ===")
    
    # Carregando os dados
    df = carregar_dados()
    
    # Verificando se a coluna 'Germinada' é numérica, se não for, converte
    if df['Germinada'].dtype == 'object':
        df['Germinada_num'] = df['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df['Germinada_num'] = df['Germinada']
    
    # Executando as análises
    analise_exploratoria(df)
    analisar_crescimento(df)
    analisar_folhas(df)
    analisar_germinacao(df)
    analise_comparativa(df)
    
    print("\nAnálise concluída com sucesso! Todos os resultados foram salvos na pasta 'resultados'.")

if __name__ == "__main__":
    main() 