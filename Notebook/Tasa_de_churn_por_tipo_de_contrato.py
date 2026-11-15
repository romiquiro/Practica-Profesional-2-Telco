import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#configuracion estetica global de los gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (8, 5)

#cargar el dataset
df = pd.read_csv('telco_limpio.csv')

# Calcular la tasa de churn por tipo de contrato
churn_contrato = df.groupby('tipo_contrato')['churn'].apply(lambda x: (x == 1).mean()* 100).reset_index()
churn_contrato.columns = ['tipo_contrato', 'tasa_churn']

# Crear el gráfico de barras
plt.figure(figsize=(8, 5))
ax = sns.barplot(x='tipo_contrato', y='tasa_churn', data=churn_contrato, palette='Blues_d')

#personalizar titulos y etiquetas
plt.title('Tasa de Abandono (Churn) por Tipo de Contrato', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Contrato', fontsize=12)
plt.ylabel('Tasa de Churn (%)', fontsize=12)
plt.ylim(0,50)

#añadir las etiquetas de texto sobre cada barra
for p in ax.patches:
    ax.annotate(f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0,5),
                textcoords='offset points')
plt.tight_layout()
plt.savefig('churn_por_contrato.png', dpi=300) #guardar
plt.show()
