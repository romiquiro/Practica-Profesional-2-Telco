# Valores de la matriz de decisión (en dólares)
# Filas: Predicción (Intervenir / No intervenir) | Columnas: Realidad (Se iba / No se iba)
matriz_datos = np.array([
    [280, -50],    # Intervenir:    Verdadero Positivo vs Falso Positivo
    [-600, 0]      # No intervenir: Falso Negativo vs Verdadero Negativo
])

plt.figure(figsize=(7, 5))
sns.heatmap(
    matriz_datos,
    annot=True,            # muestra el valor en cada celda
    fmt='d',               # formato entero
    cmap='RdYlGn',         # rojo (pérdida) -> verde (ganancia)
    center=0,              # el 0 queda en el color neutro
    cbar=False,            # sin barra de colores
    linewidths=1,          # línea blanca entre celdas
    xticklabels=['Se iba a ir (Churn)', 'No se iba (Estable)'],
    yticklabels=['Se le ofrece Descuento', 'Sin Intervención']
)
nombres = [['Verdadero Positivo', 'Falso Positivo'],
           ['Falso Negativo', 'Verdadero Negativo']]
ax = plt.gca()
for i in range(2):
    for j in range(2):
        color_texto = 'white' if matriz_datos[i][j] < -300 else 'black'
        ax.text(j + 0.5, i + 0.25, nombres[i][j], ha='center', va='center',
                fontsize=11, color=color_texto)

plt.title('Matriz de Impacto Financiero ($ Neto)', fontsize=14, fontweight='bold')
plt.xlabel('Comportamiento Real del Cliente', fontsize=12)
plt.ylabel('Acción Comercial Tomada', fontsize=12)

plt.tight_layout()
plt.savefig('matriz_decision_financiera.png', dpi=300)
plt.show()
