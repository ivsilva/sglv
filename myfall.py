import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import os
import plotly.express as px



#   Proxima etapa: 
#   Fazer uma lista da descrição para padronizar os serviços + 
#   verificar se os arquivos estão passando no codigo sem problema


Comissão = 0.30

#   Localizando onde o arquivo está
pasta_atual = Path(__file__).parent.parent / 'pasta'
df_vendas = pd.read_csv(pasta_atual / '1vendas.csv', decimal=',', parse_dates=['DATA'], dayfirst=True)
df_servi = pd.read_csv (pasta_atual / 'Serviços.csv', decimal= ',' )
df_lava = pd.read_csv (pasta_atual / 'Lavadores.csv', decimal= ',' )

df_servi = df_servi.rename(columns = {'SERVIÇOS': 'SERVIÇO'}) 
#   df_vendas = df_vendas.reset_index() reseta o valor do index
df_vendas = pd.merge(left=df_vendas, right=df_servi[['SERVIÇO', 'PREÇO']]
                    ,on='SERVIÇO',
                    how='left')
df_vendas['COMISSÃO'] = df_vendas ['PREÇO'] * Comissão

#   Nome do arquivo CSV
csv_file = 'Lavajato.csv'
#   Verifica se o arquivo CSV já existe
if os.path.exists(csv_file):
#   Se existir, carrega os dados existentes
    cadastros = pd.read_csv(csv_file).to_dict('records')
else:
    # Se não existir, inicializa a lista de cadastros vazia
    cadastros = []
#   listas constantes
lista_nomes = ['Diogo', 'Klisman', 'Dede', 'Outro']
forms_pagamento = ['Pix', 'Espécie', 'Credito', 'Debito' ]
# Função para adicionar um novo cadastro e salvar no arquivo CSV
def adicionar_cadastro(Nome, Veiculo, Preço, Obs):
    data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cadastros.append({'Nome': nome_cliente, 'Veiculo': Veiculo, 'Valor': Preço, 'Data de Cadastro': data_cadastro, 'Descrição':Obs, 'Lavador': nome_selecionado})
    
#   Salva os dados no arquivo CSV
    df = pd.DataFrame(cadastros)
    df.to_csv(csv_file, index=False)

st.sidebar.title('FlashPrime⚡️')
#   Menu
page = st.sidebar.radio('Navegação', ['Boas Vindas', 'Adicionar Lavagem', 'Resumo de Vendas', 'Análise Dinâmica', 'Gráficos', 'Relatórios'])
if page == 'Boas Vindas':
    st.title('Bem Vindo ')
    st.write('Sistema de Gestão - Flashprime')
    st.markdown('''
    Tenha Acesso a:
    - Faturamento
    - Resumo de Vendas
    - Relatórios
    ''')


#   Forma centralizada do GPT:
#   import streamlit as st

# Criar duas colunas com proporção 1:3:1
#col1, col2, col3 = st.columns([1, 3, 1])

#with col2:
#    st.title('Bem Vindo')
#    st.write('Sistema de Gestão - Flashprime')
#    st.write('Tenha Acesso a:')
#    st.write('- Faturamento')
#    st.write('- Resumo de Vendas')
#    st.write('- Relatório')
# 
# 
# 
#     
if page == 'Adicionar Lavagem':
    st.title('Adicionar Lavagem')
#   Entrada de dados
    nome_selecionado = st.selectbox("Selecione o Lavador:", lista_nomes)
    nome_cliente = st.text_input('Nome do Cliente:')
    Veiculo = st.text_input('Carro/Moto:')
    Vlr_serv = st.text_input('Valor do Serviço:')
    Obs = st.text_input('Descrição:')
    pagamento = st.selectbox('Selecione a Forma de Pagamento', forms_pagamento)
#   Botão para adicionar a nova compra
    if st.button('Adicionar nova Lavagem'):
        adicionar_cadastro(nome_cliente, Veiculo, Vlr_serv, Obs)
        st.success('Lavagem registrada com sucesso!')
#   Mostra os cadastros em uma tabela
    if len(cadastros) > 0:
        df = pd.DataFrame(cadastros)
        st.write('Lavagens Registradas:')
        st.dataframe(df, height=300)
        
elif page == 'Resumo de Vendas':
    st.title('Resumo de Vendas')
#   Entrada de dados
    st.sidebar.title('Selecione as Datas para Analise')
    date_default = df_vendas['DATA'].max()
    data_inicio = st.sidebar.date_input('Data Inicio', date_default - timedelta(days=100))
    data_fim = st.sidebar.date_input('Data Final', date_default)
    mask = (df_vendas['DATA'] >= pd.to_datetime(data_inicio)) & (df_vendas['DATA'] <= pd.to_datetime(data_fim))
    df_vendas_filtradas = df_vendas[mask]


    st.markdown('Valor Total')
    col10, col20 = st.columns(2)
    valor_vendas1 = df_vendas_filtradas['PREÇO'].sum()
    valor_vendas1 = f"R$ {valor_vendas1:.2f}"
    col10.metric('Valor de Lavagens no Periodo: ', valor_vendas1)
    col20.metric('Quantidade Lavagens no Periodo: ', df_vendas_filtradas['PREÇO'].count())

    st.divider()

    melhor_lavagem = df_vendas_filtradas['SERVIÇO'].value_counts().index[0]
    col30, col40 = st.columns(2)
    valor_vendas2 = df_vendas_filtradas[df_vendas_filtradas['SERVIÇO'] == melhor_lavagem]['PREÇO'].sum()
    valor_vendas2 = f"R$ {valor_vendas2:.2f}"
    quantidade_vendas = df_vendas_filtradas[df_vendas_filtradas['SERVIÇO'] == melhor_lavagem]['PREÇO'].count()
    col30.metric('Serviço mais Pedido: ', melhor_lavagem)
    col40.metric('Quantidade: ', quantidade_vendas)

    st.divider()

    melhor_lavador = df_vendas_filtradas['LAVADOR'].value_counts().index[0]
    col50, col60 = st.columns(2)
    valor_vendas3 = df_vendas_filtradas[df_vendas_filtradas['LAVADOR'] == melhor_lavador]['PREÇO'].sum()
    valor_comissao = df_vendas_filtradas[df_vendas_filtradas['LAVADOR'] == melhor_lavador]['COMISSÃO'].sum()
    valor_comissao = f"R$ {valor_comissao:.2f}"
    col50.metric('Principal Lavador: ', melhor_lavador)
    col60.metric('Quantidade de Comissão no Periodo: ', valor_comissao)

    st.dataframe(df_vendas_filtradas)
    st.divider()
    
elif page == 'Análise Dinâmica':
    st.title('Análise Dinâmica')
    colunas_analises = ['SERVIÇO', 'LAVADOR', 'CLIENTE', 'FORMA/PAGAMENTO']
    colunas_numericas = ['PREÇO', 'COMISSÃO']
    funcoes_agg = {'Soma': 'sum', 'Contagem': 'count'}
    selecao_analise1 = st.sidebar.multiselect('Selecione os Indices: ', colunas_analises)
    colunas_filtro = [c for c in colunas_analises if not c in selecao_analise1]
    selecao_analise2 = st.sidebar.multiselect('Selecione as Colunas: ', colunas_numericas)
    valor_analise = st.sidebar.selectbox('Selecione o valor de Analise:',colunas_numericas)
    metrica_analise = st.sidebar.selectbox('Selecione a Métrica:',
                                     list(funcoes_agg.keys()))

    if len(selecao_analise1) > 0 and len(selecao_analise2) > 0:
        metrica = funcoes_agg[metrica_analise]
        vendas_dinamica = pd.pivot_table(df_vendas, index=selecao_analise1,
                                     columns=selecao_analise2, 
                                     values=valor_analise,
                                     aggfunc=metrica)
        vendas_dinamica['TOTAL GERAL'] = vendas_dinamica.sum(axis=1) #adcionando uma coluna
        vendas_dinamica.loc['TOTAL GERAL'] = vendas_dinamica.sum(axis=0).to_list() #adcionando uma linha
        st.dataframe(vendas_dinamica)

    st.subheader('Dados Gerais')
    st.dataframe(df_vendas)

elif page == 'Gráficos':
    st.title('Gráficos')
#   Seleção    
    colunas_analises = ['SERVIÇO', 'LAVADOR', 'CLIENTE', 'FORMA/PAGAMENTO']
    st.sidebar.title('Selecione as Datas para Analise')
    date_default = df_vendas['DATA'].max()
    data_inicio = st.sidebar.date_input('Data Inicio', date_default - timedelta(days=100))
    data_fim = st.sidebar.date_input('Data Final', date_default)
    mask = (df_vendas['DATA'] >= pd.to_datetime(data_inicio)) & (df_vendas['DATA'] <= pd.to_datetime(data_fim))
    df_vendas_filtradas = df_vendas[mask]
    valor_vendas4 = df_vendas_filtradas['PREÇO'].sum() #calculando o valor de vendas de um periodo
    qtd_vendas = df_vendas_filtradas['PREÇO'].count()
    valor_vendas4 = f"R$ {valor_vendas4:.2f}"

#   Colunas    
    col41, col42, col43 = st.columns([0.5, 0.40, 0.60]) #Proporsão das colunas
    col41.markdown('Números Gerais ➡️')
    col42.metric('Valor de Lavagens no Periodo: ', valor_vendas4)
    col43.metric('Quantidade de Lavagens no Periodo: ', qtd_vendas)

    st.divider()    

#   Colunas gráficos    
    col44, col45 = st.columns(2)
    df_vendas_filtradas['DIA_VENDA'] = df_vendas_filtradas['DATA'].dt.date
    fig = px.line(df_vendas_filtradas, x='DIA_VENDA', y='PREÇO', title='Vendas por Dia')
    col44.plotly_chart(fig)
    analise_sel = st.sidebar.selectbox('Analisar: ',  colunas_analises)
    fig = px.pie(df_vendas_filtradas, values='PREÇO', names=analise_sel, title='Vendas por Dia')
    col45.plotly_chart(fig)
    st.divider()        

elif page == 'Relatórios':
    st.title('Relatórios')
    colunas = list(df_vendas.columns) #Lendo minhas colunas e printando posteriormente
    colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas', colunas, colunas) #Adcionando minha caixa de opções na sidebar, ou so com multiselect para por no meio
#minha variavel vai receber e printar o mque vier da variavel colunas
#usei o segundo colunas ali para logo de cara mostrar todas minhas seleções e depois eu retirar se eu quiser.

# FILTROS EM COLUNAS
    coluna1, coluna2 = st.sidebar.columns(2) #Adcionando colunas
    coluna_filtro = coluna1.selectbox('Selecione a coluna', colunas) #[c for c in colunas if c not in ['DATA']]) se eu quisesse excluir algum elemento no meu filtro
# selecionando apenas os valores de alguna coluna. col filtro é quem recebe o valor das colunas
    valor_filtro = coluna2.selectbox('Selecione um valor',  list(df_vendas[coluna_filtro].unique())) 
# Linkando uma coluna com a outra. unique retorna todos os valores unicos de uma coluna
# o col2 já que ja se já sei os valores da coluna agora quero que a pessoa possa selecionar, desses valores unicos quais ela quer filtrar

# CRIANDO BOTÕES
    status_filtrar = coluna1.button("Filtrar")
    status_limpar = coluna2.button("Limpar")

# Dizendo o que os botões vão fazer se eu clicar ou não
    if status_filtrar: 
        st.dataframe(df_vendas.loc[df_vendas[coluna_filtro] == valor_filtro, colunas_selecionadas], height=400)
#aqui eu vou mostrar a minha lista de colunas e filtrar qual coluna quero e ela será linkada ao valor da coluna(linha)

    elif status_limpar:
        st.dataframe(df_vendas [colunas_selecionadas], height=400)
    else: 
        st.dataframe(df_vendas [colunas_selecionadas], height=400)
    
#st.dataframe(df_vendas[colunas_selecionadas]) #Print com esse primt estava saindo 2 prints
    