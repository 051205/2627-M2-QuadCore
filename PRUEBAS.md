# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- nivel válido y nivel inexistente;
- nivel con filas de distinta longitud;
- paleta en ambos límites de la pantalla;
- rebote contra pared, paleta y cada tipo de bloque;
- pérdida de una vida y reinicio de la bola;
- victoria al eliminar el último bloque y derrota al agotar vidas;
- salida limpia con Escape y al cerrar la ventana.

Una mejora opcional no debe romper ninguno de estos casos.

## Pruebas realizadas por QuadCore

| Prueba realizada | Resultado esperado | Resultado obtenido |
|---|---|---|
| Pulsar A y D | La paleta se mueve a izquierda y derecha | Correcto |
| Pulsar las flechas | La paleta se mueve a izquierda y derecha | Correcto |
| Mover la paleta hasta los bordes | La paleta no sale de la pantalla | Correcto |
| Bola contra paredes, paleta y bloques | La bola rebota | Correcto |
| Bola contra un bloque | El bloque desaparece y aumenta la puntuación | Correcto |
| Dejar caer la bola | Se pierde una vida | Correcto |
| Agotar las tres vidas | Aparece Game Over y termina la partida | Correcto |
| Pulsar Escape o la X | El juego se cierra | Correcto |
| Cargar un archivo inexistente | Se detecta el error | Correcto |
| Cargar un nivel con filas desiguales | Se detecta el error | Correcto |
| Eliminar el último bloque | Se detecta la victoria | Correcto |


