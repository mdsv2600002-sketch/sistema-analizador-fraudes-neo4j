# Sistema Analizador de Fraudes Financieros (Primera Iteración)

Prototipo funcional desarrollado en **Python** conectado a una base de datos NoSQL orientada a grafos (**Neo4j**) para la detección de operaciones fraudulentas en tiempo real.

## Requisitos y Configuración de la Base de Datos

1. **Motor de Base de Datos:** Neo4j Desktop (v5.x) o Neo4j AuraDB (instancia gratuita en la nube).
2. **Python:** Versión 3.9 o superior.
3. **Instalación de dependencias:**
   Ejecutar en terminal: `pip install -r requirements.txt`
4. **Inicialización de la Base de Datos:**
   Ejecutar el contenido del archivo `database_setup.cypher` en Neo4j Browser/Workspace, o dejar que el script en Python lo cargue automáticamente al detectar la base vacía.
5. **Variables de Entorno y Ejecución:**
   Configurar las credenciales de conexión (`NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`) y ejecutar: `python analizador_fraudes.py`
