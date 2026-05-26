# importei as bibliotecas de uso
import pandas as pd
import numpy as np

print(df.shape)
print(df.head())

# transformei a coluna date para datetime 
df['date'] = pd.to_datetime(df['date'])


# filtrei o df original para pegar apenas os investimentos maiores que 0 e realizei uma cópia do df para calcular o ROI
# ROI = Retorno sobre o Investimento
df_roi = df[df['investimento'] > 0].copy()
df_roi['roi'] = (df_roi['receita_faturada'] - df_roi['investimento']) / df_roi['investimento']

# utilizei o groupby para calcular o ROI médio por canal, ordenei os canais por ordem crescente e removi a coluna index
roi_canal = df_roi.groupby('canal')['roi'].mean().reset_index()
roi_canal.columns = ['canal', 'roi_medio']
roi_canal = roi_canal.sort_values('roi_medio').reset_index(drop=True)

# printei o resultado
print(roi_canal)

print("\nCanal com ROI mais baixo:")
print(roi_canal.head(1))

print("\nCanal com ROI mais alto:")
print(roi_canal.iloc[-1])

# criei uma nova coluna para o mês
df['mes'] = df['date'].dt.to_period('M')

# agrupei por mes pra ver o faturamento total
fat_mes = df.groupby('mes')['receita_faturada'].sum().reset_index()
fat_mes.columns = ['mes', 'receita']

# calculei a media mensal 
media_mensal = fat_mes['receita'].mean()
print(f"\nmedia mensal: {media_mensal:.2f}")

# filtrei meses os que ficaram abaixo
mes_abaixo = fat_mes[fat_mes['receita'] < media_mensal].sort_values('receita')
print(mes_abaixo)

# realizei o agrupamento por dia e calculei o faturamento por dia
vendas_dia = df.groupby('date')['receita_faturada'].sum().reset_index()

# calculei a media e o desvio padrao das vendas por dia
media_dia = vendas_dia['receita_faturada'].mean()
desvio = vendas_dia['receita_faturada'].std()

# calculei os picos de vendas
picos = vendas_dia[vendas_dia['receita_faturada'] > media_dia + 3 * desvio]
print("\npico isolado:")
print(picos.sort_values('receita_faturada', ascending=False).head(1))
