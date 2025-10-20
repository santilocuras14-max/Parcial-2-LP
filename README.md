# Parcial 2 - Lenguajes de Programación (Repositorio en Python)

**Contenido**: Este repo contiene soluciones en Python para los puntos del parcial:
1. Gramática de un lenguaje simple para operaciones CRUD (archivo `src/grammar_crud.txt`).
2. Implementaciones en Python de transformaciones LL(1), cálculo de Conjuntos FIRST/FOLLOW, y un parser predictivo basado en tabla (stack-driven).
3. Implementación de un parser ascendente (stack-driven / predictivo) para la gramática aritmética dada.
4. Implementación del algoritmo CYK (Cocke-Younger-Kasami) y un script de benchmarking que compara tiempos con el parser predictivo.
5. Implementación de un parser descendente recursivo (recursive_descent.py) y un pequeño *algoritmo de emparejamiento* para ayudar al parser.

## Estructura del repositorio
- `src/` : código fuente (parsers, utilidades)
- `tests/` : casos de prueba y entradas de ejemplo
- `benchmarks/` : scripts para comparar rendimiento entre parsers
- `README.md` : este archivo

## Requisitos
- Python 3.8+ (solo librerías estándar)

## Ejecutar pruebas rápidas
1. Ejecutar el parser predictivo sobre ejemplos:
```bash
python3 src/predictive_parser.py
```
2. Ejecutar el parser recursivo descendente:
```bash
python3 src/recursive_descent.py
```
3. Ejecutar el CYK:
```bash
python3 src/cyk.py
```
4. Ejecutar benchmark comparativo:
```bash
python3 benchmarks/compare_parsers.py
```

## Notas
- Los scripts proveen ejemplos y una breve explicación en sus comentarios.
- El archivo `src/grammar_crud.txt` contiene una propuesta de gramática para operaciones CRUD
