##Tasa de Churn Por Contrato

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


##Distribucion de Antiguedad Tenure

plt.figure(figsize=(9, 5))

# Generar la curva de densidad mapeando explícitamente 0 a verde y 1 a rojo
sns.kdeplot(
    data=df,
    x='antiguedad_meses',
    hue='churn',
    fill=True,
    common_norm=False,
    palette={0: 'green', 1: 'red'},
    alpha=0.4
)

# Línea vertical de referencia para el periodo crítico de bajas (12 meses)
plt.axvline(x=12, color='darkred', linestyle='--', linewidth=1.5, label='Periodo Crítico (12 meses)')

plt.title('Densidad de Antigüedad: Clientes Activos vs Churn', fontsize=14, fontweight='bold')
plt.xlabel('Antigüedad Meses (Tenure)', fontsize=12)
plt.ylabel('Densidad de Probabilidad', fontsize=12)

# Ajustar leyenda con la línea de referencia añadida
plt.legend(['Churn (Bajas)', 'No Churn (Activos)', 'Periodo Crítico (12 meses)'], title='Estado')

plt.tight_layout()
plt.savefig('densidad_antiguedad.png', dpi=300)
plt.show()
