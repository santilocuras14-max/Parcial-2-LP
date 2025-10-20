# Entrega - Mapeo de requerimientos del PDF a archivos del repositorio

A continuación se indica cómo cada punto del PDF entregado está resuelto en este repositorio.

1) Diseñe una gramática de un lenguaje de programación que permita hacer las operaciones de CRUD en una base de datos.
   - Archivo: `src/grammar_crud.txt`
   - También se añadió una gramática ANTLR: `src/grammar_crud.g4`

2) Implemente la gramática del punto 1 en BISON o ANTLR y realice pruebas sobre el lenguaje.
   - Implementación ANTLR: `src/grammar_crud.g4`
   - Pruebas: usar ANTLR (no se incluyen binarios). Para probar:
     - Instalar ANTLR4 (https://www.antlr.org/)
     - Generar lexer/parser: `antlr4 -Dlanguage=Python3 src/grammar_crud.g4`
     - Crear un driver Python que use el parser generado para parsear sentencias en `tests/readme_tests.txt`.

3) Para la gramática aritmética (E -> E + T | T ...):
   - Implementación de transformación a LL(1): `src/transform_ll1.py`
   - Cálculo de FIRST/FOLLOW y tabla de predicción: `src/first_follow.py` y `src/compute_prediction.py`
   - Parser ascendente (stack-driven/predictivo) y pruebas: `src/predictive_parser.py`

4) Implemente un parser usando el algoritmo CYK. Pruebas y comparación de rendimiento:
   - Implementación CYK: `src/cyk.py`
   - Script de benchmark comparativo: `benchmarks/compare_parsers.py`

5) Diseñe e implemente un algoritmo de emparejamiento para el algoritmo descendente recursivo.
   - Implementación en: `src/recursive_descent.py`
   - El método `match` realiza el emparejamiento de tokens esperado por el parser (ver comentarios).

## Cómo ejecutar y comprobar
- Abrir un terminal y situarse en la carpeta del repo.
- Ejecutar los scripts en el orden y con las instrucciones descritas en `README.md`.

