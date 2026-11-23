import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


class AnalizadorFraudes:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def cerrar(self):
        self.driver.close()

    def inicializar_datos(self):
        """Carga el esquema y datos iniciales si la base de datos está vacía."""
        with self.driver.session() as session:
            conteo = session.run("MATCH (n) RETURN count(n) AS total").single()["total"]
            if conteo == 0:
                print("[INFO] Base de datos vacía. Cargando nodos y relaciones...")
                with open("database_setup.cypher", "r", encoding="utf-8") as f:
                    script = f.read()
                for sentencia in script.split(";"):
                    if sentencia.strip():
                        session.run(sentencia.strip())
                print("[OK] Grafo inicializado correctamente.\n")

    def detectar_transacciones_vpn(self):
        """Consulta 1: Transacciones de alto riesgo desde redes anónimas (VPN)."""
        query = """
        MATCH (c:Cliente)-[:TITULAR_DE]->(cta:Cuenta)-[:ORIGEN_DE]->(t:Transaccion)
              -[:EJECUTADA_DESDE]->(d:Dispositivo)-[:CONECTADO_A]->(ip:DireccionIP)
        WHERE ip.es_vpn = true AND t.score_fraude > 0.80
        RETURN c.nombre AS Cliente, cta.numero AS Cuenta, t.id AS Transaccion,
               t.monto AS Monto, t.score_fraude AS Riesgo, ip.ip AS IP_Origen
        """
        with self.driver.session() as session:
            return [record.data() for record in session.run(query)]

    def auditar_comercios_criticos(self):
        """Consulta 2: Comercios receptores con alertas críticas."""
        query = """
        MATCH (alt:AlertaFraude)<-[:GENERO_ALERTA]-(t:Transaccion)-[:DESTINO_A]->(mer:Comercio)
        WHERE alt.severidad IN ['Alta', 'Critica']
        RETURN DISTINCT t.id AS Transaccion, t.monto AS Monto_Bloqueado,
               mer.nombre AS Comercio_Destino, mer.categoria_mcc AS MCC,
               alt.tipo_regla AS Motivo_Alerta
        """
        with self.driver.session() as session:
            return [record.data() for record in session.run(query)]

    def analizar_dispositivos_reincidentes(self):
        """Consulta 3: Consolidación de alertas por dispositivo móvil."""
        query = """
        MATCH (d:Dispositivo)<-[:EJECUTADA_DESDE]-(t:Transaccion)-[:GENERO_ALERTA]->(alt:AlertaFraude)
        RETURN d.mac AS Dispositivo_MAC, d.so AS Sistema_Operativo,
               COUNT(alt) AS Total_Alertas_Generadas,
               MAX(t.score_fraude) AS Maximo_Score_Detectado
        """
        with self.driver.session() as session:
            return [record.data() for record in session.run(query)]


if __name__ == "__main__":
    print("=== SISTEMA ANALIZADOR DE FRAUDES FINANCIEROS (NEO4J) ===\n")
    try:
        app = AnalizadorFraudes(URI, USER, PASSWORD)
        app.inicializar_datos()

        print("1. Transacciones de Alto Riesgo desde VPN:")
        for fila in app.detectar_transacciones_vpn():
            print("  ->", fila)

        print("\n2. Auditoría de Comercios Receptores con Alertas Críticas:")
        for fila in app.auditar_comercios_criticos():
            print("  ->", fila)

        print("\n3. Consolidación de Infraestructura Reincidente:")
        for fila in app.analizar_dispositivos_reincidentes():
            print("  ->", fila)

        app.cerrar()
    except Exception as e:
        print(f"[AVISO] No se detectó conexión activa a Neo4j ({e}).")
        print("Asegúrate de configurar las variables NEO4J_URI, NEO4J_USER y NEO4J_PASSWORD.")
