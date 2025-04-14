import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import time

# Definindo constantes
PASTA_DADOS = 'dados'
PASTA_RESULTADOS = 'resultados'

def criar_diretorios():
    """Cria os diretórios necessários se não existirem"""
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    print(f"✓ Diretório '{PASTA_RESULTADOS}' verificado/criado com sucesso")

def carregar_dados():
    """Carrega os dados do arquivo CSV"""
    caminho_csv = os.path.join(PASTA_DADOS, 'medicoes.csv')
    try:
        df = pd.read_csv(caminho_csv)
        print(f"✓ Dados carregados com sucesso: {len(df)} registros encontrados")
        return df
    except Exception as e:
        print(f"✗ Erro ao carregar os dados: {e}")
        return None

def calcular_estatisticas(df):
    """Calcula as estatísticas necessárias para a análise"""
    if df is None:
        return None
    
    print("Calculando estatísticas...")
    resultados = {}
    
    # Calculando taxa de germinação por grupo
    ultimo_dia = df['Dia'].max()
    df_ultimo_dia = df[df['Dia'] == ultimo_dia]
    
    # Criando coluna numérica para germinação
    if df['Germinada'].dtype == 'object':
        df['Germinada_num'] = df['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df['Germinada_num'] = df['Germinada']
    
    # Taxa de germinação
    grupos = df_ultimo_dia.groupby('Tipo_Agua')
    
    germinacao = {}
    for tipo, grupo in grupos:
        total = len(grupo)
        germinadas = grupo['Germinada'].value_counts().get('Sim', 0)
        taxa = (germinadas / total) * 100
        germinacao[tipo] = {
            'total': total,
            'germinadas': germinadas,
            'taxa': taxa
        }
    
    resultados['germinacao'] = germinacao
    
    # Crescimento médio em dias selecionados
    dias_selecionados = [3, 7, 10, 14]
    crescimento = {}
    
    for tipo_agua in df['Tipo_Agua'].unique():
        crescimento[tipo_agua] = {}
        for dia in dias_selecionados:
            df_dia = df[(df['Tipo_Agua'] == tipo_agua) & (df['Dia'] == dia)]
            if not df_dia.empty:
                altura_media = df_dia['Altura_cm'].mean()
                crescimento[tipo_agua][dia] = altura_media
    
    resultados['crescimento'] = crescimento
    
    # Número médio de folhas no dia 14
    folhas = {}
    for tipo_agua in df['Tipo_Agua'].unique():
        df_tipo = df_ultimo_dia[df_ultimo_dia['Tipo_Agua'] == tipo_agua]
        media = df_tipo['Num_Folhas'].mean()
        desvio = df_tipo['Num_Folhas'].std()
        folhas[tipo_agua] = {'media': media, 'desvio': desvio}
    
    resultados['folhas'] = folhas
    
    # Calculando crescimento total
    crescimento_total = {}
    for tipo_agua in df['Tipo_Agua'].unique():
        altura_inicial = df[(df['Tipo_Agua'] == tipo_agua) & (df['Dia'] == 1)]['Altura_cm'].mean()
        altura_final = df[(df['Tipo_Agua'] == tipo_agua) & (df['Dia'] == ultimo_dia)]['Altura_cm'].mean()
        crescimento_total[tipo_agua] = altura_final - altura_inicial
    
    resultados['crescimento_total'] = crescimento_total
    
    print("✓ Estatísticas calculadas com sucesso")
    return resultados

def visualizar_crescimento_por_tipo(df):
    """Visualiza o crescimento médio das plantas por tipo de água"""
    if df is None:
        return
    
    print("Gerando gráfico de crescimento...")
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
    caminho_arquivo = os.path.join(PASTA_RESULTADOS, 'crescimento_por_tipo.png')
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico de crescimento salvo em '{caminho_arquivo}'")

def visualizar_numero_folhas(df):
    """Visualiza o número médio de folhas por tipo de água"""
    if df is None:
        return
    
    print("Gerando gráfico de folhas...")
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
    caminho_arquivo = os.path.join(PASTA_RESULTADOS, 'folhas_por_tipo.png')
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico de folhas salvo em '{caminho_arquivo}'")

def visualizar_taxa_germinacao(df):
    """Visualiza a taxa de germinação por tipo de água"""
    if df is None:
        return
    
    print("Gerando gráfico de germinação...")
    # Filtrando apenas o último dia para visualizar resultado final
    ultimo_dia = df['Dia'].max()
    df_ultimo_dia = df[df['Dia'] == ultimo_dia].copy()
    
    # Convertendo coluna 'Germinada' para numérico se necessário
    if df_ultimo_dia['Germinada'].dtype == 'object':
        df_ultimo_dia.loc[:, 'Germinada_num'] = df_ultimo_dia['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df_ultimo_dia.loc[:, 'Germinada_num'] = df_ultimo_dia['Germinada']
    
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
    caminho_arquivo = os.path.join(PASTA_RESULTADOS, 'taxa_germinacao.png')
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico de taxa de germinação salvo em '{caminho_arquivo}'")

def criar_relatorio_resultados(resultados):
    """Cria um novo arquivo de resultados com as estatísticas calculadas"""
    if resultados is None:
        return
    
    print("Gerando relatório de resultados...")
    # Mapeamento dos tipos de água para os grupos
    mapa_grupos = {
        'Torneira': 'A',
        'Mineral': 'B',
        'Açucarada': 'C'
    }
    
    # Criando o conteúdo do relatório
    conteudo = """# Análise de Resultados - Experimento de Crescimento de Feijões

## Resumo do Experimento

Este documento apresenta a análise dos dados coletados durante o experimento de 14 dias sobre o crescimento de feijões regados com diferentes tipos de água: água da torneira (Grupo A), água mineral (Grupo B) e água com açúcar (Grupo C).

## Análise Estatística Básica

### Taxa de Germinação

| Grupo | Sementes Plantadas | Sementes Germinadas | Taxa de Germinação (%) |
|-------|--------------------|--------------------|------------------------|
"""
    
    # Adicionando dados de germinação
    germinacao = resultados['germinacao']
    for tipo_agua, dados in germinacao.items():
        grupo = mapa_grupos.get(tipo_agua, "?")
        linha = f"| {grupo}     | 10                 | {dados['germinadas']}                  | {dados['taxa']:.1f}                       |\n"
        conteudo += linha
    
    # Adicionando tabela de crescimento
    conteudo += """
### Crescimento Médio (altura em cm)

| Grupo | Dia 3 | Dia 7 | Dia 10 | Dia 14 | Crescimento Total |
|-------|-------|-------|--------|--------|-------------------|
"""
    
    # Adicionando dados de crescimento
    crescimento = resultados['crescimento']
    for tipo_agua, dias in crescimento.items():
        grupo = mapa_grupos.get(tipo_agua, "?")
        
        # Obtendo valores para os dias específicos
        dia3 = dias.get(3, 0)
        dia7 = dias.get(7, 0)
        dia10 = dias.get(10, 0)
        dia14 = dias.get(14, 0)
        
        # Obtendo crescimento total
        total = resultados['crescimento_total'][tipo_agua]
        
        linha = f"| {grupo}     | {dia3:.1f}   | {dia7:.1f}   | {dia10:.1f}    | {dia14:.1f}    | {total:.1f}                  |\n"
        conteudo += linha
    
    # Adicionando tabela de folhas
    conteudo += """
### Número Médio de Folhas (Dia 14)

| Grupo | Média | Desvio Padrão |
|-------|-------|---------------|
"""
    
    # Adicionando dados de folhas
    folhas = resultados['folhas']
    for tipo_agua, dados in folhas.items():
        grupo = mapa_grupos.get(tipo_agua, "?")
        linha = f"| {grupo}     | {dados['media']:.1f}     | {dados['desvio']:.2f}             |\n"
        conteudo += linha
    
    # Adicionando as seções restantes do relatório
    conteudo += """
## Análise das Tendências

### Crescimento Diário

Com base nos dados coletados, o Grupo B (água mineral) mostrou o crescimento mais rápido, especialmente entre os dias 7 e 14. O Grupo A (água da torneira) apresentou um crescimento constante e saudável. O Grupo C (água com açúcar) mostrou sinais claros de estagnação após o dia 7, com crescimento muito limitado.

### Comparação entre os Grupos

Os dados mostram diferenças significativas entre os três grupos. A água mineral produziu plantas com maior altura final e mais folhas, sugerindo que os minerais presentes favoreceram o desenvolvimento. A água da torneira também produziu resultados satisfatórios. Em contraste, a água com açúcar prejudicou visivelmente o desenvolvimento, resultando em plantas mais baixas, com menos folhas e sinais de deterioração.

## Observações Importantes

1. As plantas do Grupo C (água com açúcar) apresentaram folhas amareladas a partir do dia 5
2. O Grupo B (água mineral) teve a maior taxa de germinação e o desenvolvimento mais rápido de folhas
3. Algumas plantas do Grupo C começaram a murchar e mostrar sinais de morte a partir do dia 11

## Possíveis Explicações

1. A concentração elevada de açúcar na água pode ter criado um ambiente hipertônico, dificultando a absorção de água pelas raízes no Grupo C
2. Os minerais presentes na água mineral podem ter fornecido nutrientes adicionais para o Grupo B
3. O pH das diferentes águas pode ter influenciado a disponibilidade de nutrientes para as plantas

## Fontes de Erro

1. Variações na exposição à luz entre os diferentes grupos de plantas
2. Inconsistências na quantidade de água aplicada em cada rega
3. Diferenças naturais entre as sementes utilizadas

## Conclusões

Este experimento demonstra claramente que o tipo de água utilizada na irrigação tem um impacto significativo no desenvolvimento das plantas. A água mineral mostrou-se superior para o crescimento geral, possivelmente devido aos minerais dissolvidos que forneceram nutrientes adicionais. A água da torneira também produziu resultados satisfatórios. Em contraste, a água com açúcar prejudicou severamente o desenvolvimento, confirmando que nem todos os aditivos são benéficos para as plantas.

## Sugestões para Experimentos Futuros

1. Testar diferentes concentrações de açúcar para determinar se existe uma dosagem benéfica
2. Comparar diferentes marcas de água mineral para avaliar o impacto de diferentes composições minerais
3. Analisar o pH de cada tipo de água e seu impacto no crescimento das plantas
"""
    
    # Salvando o arquivo com as estatísticas
    caminho_arquivo = os.path.join(PASTA_RESULTADOS, 'relatorio_final.md')
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"✓ Relatório de resultados salvo em '{caminho_arquivo}'")

def visualizar_comparativo_final(df):
    """Cria um gráfico comparativo final com todos os parâmetros"""
    if df is None:
        return
    
    print("Gerando gráfico comparativo final...")
    # Filtrando apenas o último dia para visualizar resultado final
    ultimo_dia = df['Dia'].max()
    df_ultimo_dia = df[df['Dia'] == ultimo_dia].copy()
    
    # Convertendo coluna 'Germinada' para numérico se necessário
    if df_ultimo_dia['Germinada'].dtype == 'object':
        df_ultimo_dia.loc[:, 'Germinada_num'] = df_ultimo_dia['Germinada'].map({'Sim': 1, 'Não': 0})
    else:
        df_ultimo_dia.loc[:, 'Germinada_num'] = df_ultimo_dia['Germinada']
    
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
    caminho_arquivo = os.path.join(PASTA_RESULTADOS, 'comparativo_final.png')
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico comparativo final salvo em '{caminho_arquivo}'")

def exibir_banner():
    """Exibe um banner para o script"""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║  ANÁLISE DE DADOS - EXPERIMENTO DE CRESCIMENTO DE PLANTAS         ║
║  -------------------------------------------------------------    ║
║  Este script analisa os dados do experimento de crescimento de    ║
║  feijões com diferentes tipos de água e gera relatórios e         ║
║  visualizações dos resultados.                                    ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def main():
    """Função principal que executa todas as etapas da análise"""
    exibir_banner()
    
    # Verificando argumentos da linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Uso: python analisar_experimento.py [opcoes]")
        print("Opções:")
        print("  --help     : Exibe esta mensagem de ajuda")
        print("  --relatorio: Gera apenas o relatório sem os gráficos")
        print("  --graficos : Gera apenas os gráficos sem o relatório")
        return
    
    apenas_relatorio = len(sys.argv) > 1 and sys.argv[1] == "--relatorio"
    apenas_graficos = len(sys.argv) > 1 and sys.argv[1] == "--graficos"
    
    # Criando diretórios necessários
    criar_diretorios()
    
    # Carregando os dados
    df = carregar_dados()
    
    if df is None:
        print("Não foi possível carregar os dados. Encerrando o programa.")
        return
    
    # Calculando estatísticas
    resultados = calcular_estatisticas(df)
    
    if resultados is None:
        print("Não foi possível calcular as estatísticas. Encerrando o programa.")
        return
    
    # Executando visualizações e relatório baseado nos argumentos
    if not apenas_relatorio:
        print("\n--- GERANDO VISUALIZAÇÕES ---")
        visualizar_crescimento_por_tipo(df)
        visualizar_numero_folhas(df)
        visualizar_taxa_germinacao(df)
        visualizar_comparativo_final(df)
    
    if not apenas_graficos:
        print("\n--- GERANDO RELATÓRIO ---")
        criar_relatorio_resultados(resultados)
    
    print("\n✓ Análise concluída com sucesso!")
    print(f"Todos os resultados foram salvos na pasta '{PASTA_RESULTADOS}'")

if __name__ == "__main__":
    inicio = time.time()
    main()
    fim = time.time()
    print(f"\nTempo de execução: {fim - inicio:.2f} segundos") 