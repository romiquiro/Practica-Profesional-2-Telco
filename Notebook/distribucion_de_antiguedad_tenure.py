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
