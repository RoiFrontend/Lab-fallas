import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("docs/graficos", exist_ok=True)

# 1. Gráfico: Round Robin vs Least Connections
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

categorias = ['Réplica Rápida 1', 'Réplica Rápida 2', 'Réplica Lenta (2s)']
round_robin_reqs = [8, 8, 8]
least_conn_reqs = [12, 11, 1]

colores = ['#4C7DFF', '#2EC4B6', '#FF5C6C']

# Subplot 1: Round Robin
bars1 = ax1.bar(categorias, round_robin_reqs, color=colores, width=0.55, edgecolor='black', linewidth=1)
ax1.set_title("Round Robin (A ciegas por turno)\nPeticiones repartidas por igual (33.3% c/u)", fontsize=11, fontweight='bold', pad=12)
ax1.set_ylabel("Peticiones Atendidas", fontsize=10)
ax1.set_ylim(0, 15)
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval} reqs\n({yval/24*100:.1f}%)", ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Subplot 2: Least Connections / Least Outstanding Requests
bars2 = ax2.bar(categorias, least_conn_reqs, color=colores, width=0.55, edgecolor='black', linewidth=1)
ax2.set_title("Least Connections / Least Outstanding\nAislamiento automático de réplica lenta", fontsize=11, fontweight='bold', pad=12)
ax2.set_ylabel("Peticiones Atendidas", fontsize=10)
ax2.set_ylim(0, 15)
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.3, f"{yval} reqs\n({yval/24*100:.1f}%)", ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
fig.savefig("docs/graficos/comparativa_algoritmos.png", dpi=300)
plt.close(fig)

# 2. Gráfico: Ley de Little y Saturación de CPU en 1 Tarea vs 4 Tareas
fig2, ax = plt.subplots(figsize=(8, 4))
clientes = [5, 10, 20]
p50_1tarea = [3, 22, 35]
p95_1tarea = [36, 55, 72]
p50_4tareas = [2, 3, 3]

ax.plot(clientes, p50_1tarea, marker='o', linewidth=2.5, color='#FF5C6C', label='1 Tarea Fargate (p50 latencia)')
ax.plot(clientes, p95_1tarea, marker='s', linewidth=2, linestyle='--', color='#E0A030', label='1 Tarea Fargate (p95 latencia)')
ax.plot(clientes, p50_4tareas, marker='^', linewidth=2.5, color='#139A5E', label='4 Tareas Fargate escaladas (p50)')

ax.set_title("Ley de Little en Fargate: Clientes Simultáneos vs. Latencia (ms)", fontsize=11, fontweight='bold', pad=12)
ax.set_xlabel("Clientes Concurrentes en Vuelo", fontsize=10)
ax.set_ylabel("Tiempo de Respuesta (ms)", fontsize=10)
ax.set_xticks(clientes)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(frameon=True, facecolor='white', framealpha=0.9)

plt.tight_layout()
fig2.savefig("docs/graficos/ley_de_little_escalabilidad.png", dpi=300)
plt.close(fig2)

print("Gráficos generados correctamente en docs/graficos/")
