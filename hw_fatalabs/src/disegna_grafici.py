from matplotlib import pyplot as plt
import numpy as np

# Dati dei due pin I2C (sostituisci con i tuoi dati)
tempo = np.array(list(range(0, 16 + 1)))
livello_pin2 = np.array([1] + [1, 0] * 8)
livello_pin1 = np.array([1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
livello_pin2 += 2

# Creazione del grafico
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(tempo, livello_pin1, label='Data', color='blue', marker='o', linestyle='-')
ax.plot(tempo, livello_pin2, label='Busy', color='red', marker='x', linestyle='--')
ax.set_xlabel('Tempo')
#ax.set_ylabel('Livello')
ax.set_title('Grafico dei segnali I2C dei Pin 1 e 2')
ax.grid(True)
ax.legend()

# Rimuovi i valori dell'asse y mostrati a lato
ax.set_yticks([])

plt.savefig('grafico_i2c.png', dpi=300)
plt.show()