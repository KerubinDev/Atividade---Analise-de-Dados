import os
import re
import pandas as pd

def extrair_medicoes_markdown(arquivo_md):
    """
    Extrai os dados de medições do arquivo markdown e retorna um DataFrame
    """
    # Lendo o arquivo markdown
    with open(arquivo_md, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Expressão regular para capturar a tabela de dados
    # Procurando por linhas que começam com um dia (número)
    pattern = r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
    
    # Encontrando todas as correspondências
    matches = re.findall(pattern, conteudo)
    
    # Criando listas para armazenar os dados
    dados = []
    
    # Para cada correspondência, extrair os dados
    for match in matches:
        dia = int(match[0])
        
        # Para cada grupo (A, B, C)
        for grupo_idx, grupo_nome in enumerate(['A', 'B', 'C']):
            # Extraindo os valores da tabela
            altura = match[1].strip().split(',')[grupo_idx].strip()
            germinada = match[2].strip().split(',')[grupo_idx].strip()
            num_folhas = match[3].strip().split(',')[grupo_idx].strip()
            cor_folhas = match[4].strip().split(',')[grupo_idx].strip()
            observacoes = match[5].strip().split(',')[grupo_idx].strip() if len(match[5].strip().split(',')) > grupo_idx else ""
            
            # Convertendo valores para o formato correto
            try:
                altura = float(altura.replace('cm', '').strip()) if altura and 'cm' in altura else 0.0
            except:
                altura = 0.0
                
            germinada = 'Sim' if germinada.lower() in ['sim', 's', 'yes', 'y', 'true', 't'] else 'Não'
            
            try:
                num_folhas = int(num_folhas) if num_folhas and num_folhas.isdigit() else 0
            except:
                num_folhas = 0
            
            # Adicionando à lista de dados
            tipo_agua = {'A': 'Água da Torneira', 'B': 'Água Mineral', 'C': 'Água com Açúcar'}[grupo_nome]
            
            dados.append({
                'ID_Planta': f'{grupo_nome}{dia}',
                'Grupo': grupo_nome,
                'Tipo_Agua': tipo_agua,
                'Dia': dia,
                'Altura_cm': altura,
                'Germinada': germinada,
                'Num_Folhas': num_folhas,
                'Cor_Folhas': cor_folhas,
                'Observacoes': observacoes
            })
    
    # Criando o DataFrame
    df = pd.DataFrame(dados)
    
    return df

def main():
    """
    Função principal para converter os dados do markdown para CSV
    """
    # Diretório dos dados
    diretorio_dados = os.path.join('..', 'dados')
    
    # Arquivo markdown de entrada
    arquivo_md = os.path.join(diretorio_dados, 'medicoes.md')
    
    # Arquivo CSV de saída
    arquivo_csv = os.path.join(diretorio_dados, 'medicoes.csv')
    
    # Verificando se o arquivo markdown existe
    if not os.path.exists(arquivo_md):
        print(f"Erro: O arquivo {arquivo_md} não foi encontrado.")
        return
    
    # Extraindo os dados do markdown
    print(f"Extraindo dados do arquivo {arquivo_md}...")
    df = extrair_medicoes_markdown(arquivo_md)
    
    # Salvando o DataFrame como CSV
    print(f"Salvando dados no arquivo {arquivo_csv}...")
    df.to_csv(arquivo_csv, index=False)
    
    print(f"Conversão concluída! {len(df)} registros foram extraídos e salvos.")
    print(f"Dados convertidos com sucesso! Arquivo CSV salvo em: {arquivo_csv}")

if __name__ == "__main__":
    main() 