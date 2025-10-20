# Parcial 2 - Lenguajes de Programación (Repositorio en Python)

**Contenido**: Este repo contiene soluciones en Python para los puntos del parcial. A continuación se **explica punto por punto** qué se pide en el PDF y qué archivo(s) del repositorio implementan cada punto, además de cómo ejecutar y comprobar cada entrega.

---

## Resumen rápido de lo que incluye
- Gramática CRUD: `src/grammar_crud.txt`
- Gramática ANTLR: `src/grammar_crud.g4`
- Transformación a LL(1): `src/transform_ll1.py`
- Cálculo FIRST/FOLLOW: `src/first_follow.py`
- Tabla de predicción / LL(1): `src/compute_prediction.py`
- Parser predictivo (ascendente, stack-driven): `src/predictive_parser.py`
- Parser recursivo descendente y función de emparejamiento: `src/recursive_descent.py`
- Parser CYK: `src/cyk.py`
- Benchmarks comparativos: `benchmarks/compare_parsers.py`
- Tokenizador: `src/tokenizer.py`
- Casos de prueba: `tests/readme_tests.txt`
- Documento que mapea entregables: `report/Deliverables.md`

---

## Explicación punto por punto (según el PDF)

### Punto 1 — Diseñe una gramática de un lenguaje de programación que permita hacer las operaciones de CRUD en una base de datos.
**Qué pide:** Diseñar la gramática (símbolos terminales/no terminales, reglas de producción) que permita expresar `SELECT`, `INSERT`, `UPDATE` y `DELETE` (operaciones CRUD) en una forma sencilla.
**Qué entrego en el repositorio:** `src/grammar_crud.txt` (versión en texto con notación BNF) y `src/grammar_crud.g4` (versión en formato ANTLR).
**Qué debes revisar / probar:** Abrir `src/grammar_crud.txt` para ver la gramática en BNF. La gramática incluye sentencias completas terminadas en `;`, listas de campos, valores, cláusula opcional `WHERE`, etc.
**Sugerencias de prueba:** Usa `tests/readme_tests.txt` y construye oraciones del tipo:
```
SELECT name, age FROM users WHERE id = 10;
INSERT INTO users (name, age) VALUES ('Ana', 25);
UPDATE users SET name = 'Luis' WHERE id = 2;
DELETE FROM users WHERE id = 3;
```

---

### Punto 2 — Implemente la gramática del punto 1 en BISON o ANTLR y realice pruebas sobre el lenguaje.
**Qué pide:** Implementar la gramática en un generador de parsers (BISON o ANTLR) y ejecutar pruebas reales para mostrar que el parser reconoce sentencias válidas y rechaza inválidas.
**Qué entrego en el repositorio:** `src/grammar_crud.g4` (archivo ANTLR).
**Instrucciones para probar con ANTLR (no incluyo el runtime generado en este repo):**
1. Instala ANTLR4 y su runtime para Python (sigue la guía en https://www.antlr.org/).
2. Genera lexer/parser en Python (desde la raíz del repo):
   ```bash
   antlr4 -Dlanguage=Python3 src/grammar_crud.g4 -o generated
   ```
3. Crea un driver Python (ej: `generated/run_crud.py`) que use `CRUDParser` y `CRUDLexer` para parsear entradas. En `report/Deliverables.md` doy una guía breve sobre esto.
4. Ejecuta el driver con ejemplos de `tests/readme_tests.txt` y verifica salidas (parse tree o mensajes de error).

---

### Punto 3 — Para la gramática aritmética (E → E + T | T ; T → T * F | F ; F → ( E ) | id): implementes en Python un analizador sintáctico ascendente. 
**Qué pide (desglose):**
- Transformar la gramática para que sea LL(1) (eliminar recursión izquierda y aplicar left-factoring si fuera necesario).
- Calcular conjuntos FIRST, FOLLOW y tabla de predicción (prediction table).
- Diseñar un algoritmo ascendente basado en pila (stack-driven) e implementarlo.
- Realizar pruebas del analizador ascendente.
**Qué entrego en el repositorio:**
- `src/transform_ll1.py` — transformación manual que elimina la recursión izquierda: produce las producciones E → T E' ; E' → + T E' ; etc.
- `src/first_follow.py` — algoritmo para calcular conjuntos FIRST y FOLLOW para una gramática representada como diccionario.
- `src/compute_prediction.py` — produce la tabla de predicción LL(1) (prediction table) usando FIRST/FOLLOW.
- `src/predictive_parser.py` — implementación de un parser predictivo (tabla-driven) que simula un parser ascendente/stack-driven para la gramática transformada.
**Cómo ejecutar y qué esperar:**
- Ejecuta `python3 src/compute_prediction.py` para ver FIRST, FOLLOW y la tabla de predicción mostrados en consola.
- Ejecuta `python3 src/predictive_parser.py` para probar la aceptación/rechazo de expresiones de prueba (`id + id * id`, `( id + id ) * id`, etc.).
- El parser predictivo simula la conducta de un parser ascendente basado en stack: se construye una pila, se consultan entradas en la tabla y se aplican producciones. Observa los mensajes de aceptación o errores por desajuste.

---

### Punto 4 — Implementar un parser usando el algoritmo CYK y comparar rendimiento con un parser predictivo.
**Qué pide:** Implementar CYK (requiere gramática en Forma Normal de Chomsky — CNF), ejecutar pruebas y comparar rendimiento con el parser predictivo (tiempos de ejecución, escalabilidad con la longitud de la entrada).
**Qué entrego en el repositorio:**
- `src/cyk.py` — implementación CYK (ejemplo de CNF adaptada para las expresiones de prueba).
- `benchmarks/compare_parsers.py` — script que ejecuta micro-benchmarks para cadenas de distinto tamaño y compara tiempos entre el parser predictivo y CYK.
**Cómo ejecutar y qué esperar:**
- Ejecuta `python3 src/cyk.py` para probar ejemplos. Verás `True/False` según si la cadena se reconoce.
- Ejecuta `python3 benchmarks/compare_parsers.py` para un benchmark simple: se imprimirán tiempos de ejecución para entradas de distintos tamaños.
**Notas sobre la comparación:** CYK tiene complejidad O(n^3) en la longitud de la cadena (n), mientras que un parser LL(1) típico opera en tiempo lineal O(n). El script de benchmark ilustra esta diferencia con entradas crecientes.

---

### Punto 5 — Diseñe e implemente un algoritmo de emparejamiento para el algoritmo descendente recursivo.
**Qué pide:** Diseñar un algoritmo/helper que facilite el emparejamiento de tokens esperados por las funciones recursivas (p. ej. `match` o `expect`) y lo implemente en el parser descendente recursivo.
**Qué entrego en el repositorio:**
- `src/recursive_descent.py` — parser recursivo descendente para la gramática transformada; incluye la función `match(expected_type / expected_val)` que realiza el emparejamiento y lanza errores en caso de discrepancia.
**Cómo ejecutar y qué esperar:**
- Ejecuta `python3 src/recursive_descent.py` para ver el parser en acción sobre ejemplos. El parser imprime si la entrada fue aceptada o muestra un error de sintaxis con la posición del token inesperado.
- Lee los comentarios en el archivo para entender cómo funciona `match` y las decisiones de diseño (peek, consumo de tokens, manejo de tokens terminales y literales).

---

## Ejecución paso a paso (sugerida para evaluar todo el parcial)
1. Desde la raíz del repo, ejecutar las herramientas de prueba que están en `src/`:
   ```bash
   python3 src/compute_prediction.py
   python3 src/predictive_parser.py
   python3 src/recursive_descent.py
   python3 src/cyk.py
   python3 benchmarks/compare_parsers.py
   ```
2. Si deseas probar la gramática CRUD en ANTLR, genera los archivos con ANTLR y crea un driver Python que invoque el parser (instrucciones resumidas en `report/Deliverables.md`).

---
