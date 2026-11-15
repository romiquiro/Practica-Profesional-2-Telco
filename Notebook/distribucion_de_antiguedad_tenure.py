plt.figure(figsize=(9, 5))

#generar la curva de densidad separada por la variable churn
sns.kdeplot(
    data=df,
    x='antiguedad_meses',
    hue='churn',
    fill=True,
    common_norm=False,
    palette=['green', 'red'],
    alpha=0.4)

plt.title('Densidad de Antiguedad: Clientes Activos vs Churn', fontsize=14, fontweight='bold')
plt.xlabel('Antiguedad Meses (Tenure)', fontsize=12)
plt.ylabel('Densidad de Probabilidad', fontsize=12)
plt.legend(['No Churn (Activos)', 'Churn (Bajas)'], title='Estado')

plt.tight_layout()
plt.savefig('densidad_antiguedad.png', dpi=300)
plt.show() 
