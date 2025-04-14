import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para carregar os dados (simulados neste código)
def carregar_dados():
    # Em um experimento real, você carregaria os dados de um arquivo Excel
    # Por exemplo: df = pd.read_excel('../dados/medicoes.xlsx')
    
    # Simulando dados para demonstração
    dias = range(1, 15)  # 14 dias de experimento
    
    # Simulando alturas médias para cada grupo (em mm)
    altura_grupo_a = [0, 5, 12, 20, 28, 35, 43, 50, 58, 65, 72, 78, 84, 89]  # Água da torneira
    altura_grupo_b = [0, 4, 10, 18, 25, 32, 40, 48, 56, 64, 71, 77, 83, 88]  # Água mineral
    altura_grupo_c = [0, 3, 8, 15, 21, 26, 32, 37, 42, 46, 50, 54, 57, 60]   # Água com açúcar
    
    # Simulando número médio de folhas para cada grupo
    folhas_grupo_a = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
    folhas_grupo_b = [0, 0, 0, 0, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
    folhas_grupo_c = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]
    
    # Simulando taxas de germinação para cada grupo (%)
    germinacao_a = 80  # 8 de 10 sementes germinaram
    germinacao_b = 90  # 9 de 10 sementes germinaram
    germinacao_c = 60  # 6 de 10 sementes germinaram
    
    return {
        'dias': dias,
        'altura': {
            'Água da Torneira': altura_grupo_a,
            'Água Mineral': altura_grupo_b,
            'Água com Açúcar': altura_grupo_c
        },
        'folhas': {
            'Água da Torneira': folhas_grupo_a,
            'Água Mineral': folhas_grupo_b, 
            'Água com Açúcar': folhas_grupo_c
        },
        'germinacao': {
            'Água da Torneira': germinacao_a,
            'Água Mineral': germinacao_b,
            'Água com Açúcar': germinacao_c
        }
    }

# Função para analisar crescimento
def analisar_crescimento(dados):
    # Calculando estatísticas de crescimento
    for tipo_agua, alturas in dados['altura'].items():
        print(f"\nEstatísticas de crescimento para {tipo_agua}:")
        print(f"Altura final média: {alturas[-1]} mm")
        print(f"Taxa de crescimento diário médio: {alturas[-1]/14:.2f} mm/dia")
        
        # Calculando quando a planta atingiu metade da altura final
        metade_altura = alturas[-1] / 2
        for i, altura in enumerate(alturas):
            if altura >= metade_altura:
                print(f"Atingiu metade da altura final no dia {i+1}")
                break

# Função para criar gráfico de crescimento
def criar_grafico_crescimento(dados):
    plt.figure(figsize=(10, 6))
    
    for tipo_agua, alturas in dados['altura'].items():
        plt.plot(dados['dias'], alturas, marker='o', linestyle='-', label=tipo_agua)
    
    plt.xlabel('Dias')
    plt.ylabel('Altura Média (mm)')
    plt.title('Crescimento das Plantas por Tipo de Água')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    # Salvar o gráfico
    plt.savefig('grafico_crescimento.png')
    print("\nGráfico de crescimento salvo como 'grafico_crescimento.png'")
    
    # Em um ambiente interativo, você pode mostrar o gráfico com:
    # plt.show()

# Função para criar gráfico de barras da germinação
def criar_grafico_germinacao(dados):
    plt.figure(figsize=(8, 5))
    
    tipos_agua = list(dados['germinacao'].keys())
    taxas = list(dados['germinacao'].values())
    
    barras = plt.bar(tipos_agua, taxas)
    
    # Adicionar rótulos no topo das barras
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + 1,
                f'{altura}%', ha='center', va='bottom')
    
    plt.xlabel('Tipo de Água')
    plt.ylabel('Taxa de Germinação (%)')
    plt.title('Taxa de Germinação por Tipo de Água')
    plt.ylim(0, 100)  # Fixando o limite do eixo y em 100%
    plt.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Salvar o gráfico
    plt.savefig('grafico_germinacao.png')
    print("Gráfico de germinação salvo como 'grafico_germinacao.png'")
    
    # Em um ambiente interativo, você pode mostrar o gráfico com:
    # plt.show()

# Função para criar gráfico das folhas
def criar_grafico_folhas(dados):
    plt.figure(figsize=(10, 6))
    
    for tipo_agua, num_folhas in dados['folhas'].items():
        plt.plot(dados['dias'], num_folhas, marker='s', linestyle='-', label=tipo_agua)
    
    plt.xlabel('Dias')
    plt.ylabel('Número Médio de Folhas')
    plt.title('Desenvolvimento de Folhas por Tipo de Água')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    # Salvar o gráfico
    plt.savefig('grafico_folhas.png')
    print("Gráfico de desenvolvimento de folhas salvo como 'grafico_folhas.png'")
    
    # Em um ambiente interativo, você pode mostrar o gráfico com:
    # plt.show()

# Função principal
def main():
    print("Análise de Dados: Crescimento de Plantas com Diferentes Tipos de Água")
    print("=" * 70)
    
    # Carregar dados
    dados = carregar_dados()
    
    # Analisar crescimento
    analisar_crescimento(dados)
    
    # Criar gráficos
    criar_grafico_crescimento(dados)
    criar_grafico_germinacao(dados)
    criar_grafico_folhas(dados)
    
    print("\nAnálise concluída com sucesso!")

# Executar o programa
if __name__ == "__main__":
    main() 