import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configurando o estilo dos gráficos
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 12})

# Criando diretório para os gráficos se não existir
os.makedirs('resultados', exist_ok=True)

def carregar_dados():
    """Carrega os dados do arquivo CSV"""
    try:
        df = pd.read_csv('dados/medicoes.csv')
        print(f"Dados carregados com sucesso! {len(df)} registros encontrados.")
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

def visualizar_crescimento_por_tipo(df):
    """Visualiza o crescimento médio das plantas por tipo de água"""
    if df is None:
        return
    
    # Filtrando apenas dias específicos para simplificar o gráfico
    dias_selecionados = [1, 4, 7, 10, 14]
    df_filtrado = df[df['Dia'].isin(dias_selecionados)]
    
    # Calculando altura média por dia e tipo de água
    dados_agrupados = df_filtrado.groupby(['Dia', 'Tipo_Agua'])['Altura_cm'].mean().reset_index()
    
    # Criando o gráfico
    plt.figure(figsize=(12, 8))
    
    # Definindo cores para cada tipo de água
    cores = {'Torneira': 'blue', 'Mineral': 'green', 'Açucarada': 'red'}
    
    # Plotando os dados para cada tipo de água
    for tipo, cor in cores.items():
        dados_tipo = dados_agrupados[dados_agrupados['Tipo_Agua'] == tipo]
        plt.plot(dados_tipo['Dia'], dados_tipo['Altura_cm'], 
                 marker='o', linestyle='-', linewidth=2, 
                 color=cor, label=f'Água {tipo}')
    
    plt.title('Crescimento Médio das Plantas por Tipo de Água', fontweight='bold')
    plt.xlabel('Dia do Experimento')
    plt.ylabel('Altura Média (cm)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.xticks(dias_selecionados)
    
    # Salvando o gráfico
    plt.savefig('resultados/crescimento_por_tipo.png', dpi=300, bbox_inches='tight')
    print("Gráfico de crescimento salvo em 'resultados/crescimento_por_tipo.png'")
    
def visualizar_numero_folhas(df):
    """Visualiza o número médio de folhas por tipo de água"""
    if df is None:
        return
    
    # Filtrando apenas o último dia para visualizar resultado final
    ultimo_dia = df['Dia'].max()
    df_ultimo_dia = df[df['Dia'] == ultimo_dia]
    
    # Calculando número médio de folhas por tipo de água
    folhas_por_tipo = df_ultimo_dia.groupby('Tipo_Agua')['Num_Folhas'].mean()
    
    # Criando o gráfico de barras
    plt.figure(figsize=(10, 6))
    
    # Definindo cores para cada tipo de água
    cores = {'Torneira': 'blue', 'Mineral': 'green', 'Açucarada': 'red'}
    
    # Criando as barras
    barras = plt.bar(folhas_por_tipo.index, folhas_por_tipo.values, 
                     color=[cores.get(tipo, 'gray') for tipo in folhas_por_tipo.index])
    
    # Adicionando os valores nas barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + 0.1,
                f'{altura:.1f}', ha='center', va='bottom')
    
    plt.title(f'Número Médio de Folhas por Tipo de Água (Dia {ultimo_dia})', fontweight='bold')
    plt.xlabel('Tipo de Água')
    plt.ylabel('Número Médio de Folhas')
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Salvando o gráfico
    plt.savefig('resultados/folhas_por_tipo.png', dpi=300, bbox_inches='tight')
    print("Gráfico de folhas salvo em 'resultados/folhas_por_tipo.png'")

def visualizar_taxa_germinacao(df):
    """Visualiza a taxa de germinação por tipo de água"""
    if df is None:
        return
    
    # Filtrando apenas o último dia para visualizar resultado final
    ultimo_dia = df['Dia'].max()
    df_ultimo_dia = df[df['Dia'] == ultimo_dia]
    
    # Convertendo coluna 'Germinada' para numérico se necessário
    if df_ultimo_dia['Germinada'].dtype == 'object':
        df_ultimo_dia['Germinada_num'] = df_ultimo_dia['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df_ultimo_dia['Germinada_num'] = df_ultimo_dia['Germinada']
    
    # Calculando taxa de germinação por tipo de água
    taxa_germinacao = df_ultimo_dia.groupby('Tipo_Agua')['Germinada_num'].mean() * 100
    
    # Criando o gráfico de barras
    plt.figure(figsize=(10, 6))
    
    # Definindo cores para cada tipo de água
    cores = {'Torneira': 'blue', 'Mineral': 'green', 'Açucarada': 'red'}
    
    # Criando as barras
    barras = plt.bar(taxa_germinacao.index, taxa_germinacao.values, 
                     color=[cores.get(tipo, 'gray') for tipo in taxa_germinacao.index])
    
    # Adicionando os valores nas barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + 2,
                f'{altura:.1f}%', ha='center', va='bottom')
    
    plt.title('Taxa de Germinação por Tipo de Água', fontweight='bold')
    plt.xlabel('Tipo de Água')
    plt.ylabel('Taxa de Germinação (%)')
    plt.ylim(0, 105)  # Fixando o limite do eixo y em 105%
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Salvando o gráfico
    plt.savefig('resultados/taxa_germinacao.png', dpi=300, bbox_inches='tight')
    print("Gráfico de taxa de germinação salvo em 'resultados/taxa_germinacao.png'")

def visualizar_comparativo_final(df):
    """Cria um gráfico comparativo final com todos os parâmetros"""
    if df is None:
        return
    
    # Filtrando apenas o último dia para visualizar resultado final
    ultimo_dia = df['Dia'].max()
    df_ultimo_dia = df[df['Dia'] == ultimo_dia]
    
    # Convertendo coluna 'Germinada' para numérico se necessário
    if df_ultimo_dia['Germinada'].dtype == 'object':
        df_ultimo_dia['Germinada_num'] = df_ultimo_dia['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df_ultimo_dia['Germinada_num'] = df_ultimo_dia['Germinada']
    
    # Criando o gráfico com 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Definindo cores para cada tipo de água
    cores = {'Torneira': 'blue', 'Mineral': 'green', 'Açucarada': 'red'}
    
    # Altura média
    altura_media = df_ultimo_dia.groupby('Tipo_Agua')['Altura_cm'].mean()
    axes[0].bar(altura_media.index, altura_media.values, 
               color=[cores.get(tipo, 'gray') for tipo in altura_media.index])
    axes[0].set_title('Altura Média (cm)', fontweight='bold')
    axes[0].set_xlabel('Tipo de Água')
    axes[0].set_ylabel('Altura (cm)')
    axes[0].grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Número médio de folhas
    folhas_media = df_ultimo_dia.groupby('Tipo_Agua')['Num_Folhas'].mean()
    axes[1].bar(folhas_media.index, folhas_media.values, 
               color=[cores.get(tipo, 'gray') for tipo in folhas_media.index])
    axes[1].set_title('Número Médio de Folhas', fontweight='bold')
    axes[1].set_xlabel('Tipo de Água')
    axes[1].set_ylabel('Número de Folhas')
    axes[1].grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Taxa de germinação
    taxa_germinacao = df_ultimo_dia.groupby('Tipo_Agua')['Germinada_num'].mean() * 100
    axes[2].bar(taxa_germinacao.index, taxa_germinacao.values, 
               color=[cores.get(tipo, 'gray') for tipo in taxa_germinacao.index])
    axes[2].set_title('Taxa de Germinação (%)', fontweight='bold')
    axes[2].set_xlabel('Tipo de Água')
    axes[2].set_ylabel('Taxa (%)')
    axes[2].set_ylim(0, 105)
    axes[2].grid(True, linestyle='--', alpha=0.7, axis='y')
    
    plt.tight_layout()
    
    # Salvando o gráfico
    plt.savefig('resultados/comparativo_final.png', dpi=300, bbox_inches='tight')
    print("Gráfico comparativo final salvo em 'resultados/comparativo_final.png'")

def main():
    """Função principal que executa todas as visualizações"""
    print("=== VISUALIZAÇÃO DOS DADOS DO EXPERIMENTO DE CRESCIMENTO DE PLANTAS ===")
    
    # Carregando os dados
    df = carregar_dados()
    
    # Gerando as visualizações
    visualizar_crescimento_por_tipo(df)
    visualizar_numero_folhas(df)
    visualizar_taxa_germinacao(df)
    visualizar_comparativo_final(df)
    
    print("\nVisualização concluída com sucesso! Todos os gráficos foram salvos na pasta 'resultados'.")

if __name__ == "__main__":
    main() 