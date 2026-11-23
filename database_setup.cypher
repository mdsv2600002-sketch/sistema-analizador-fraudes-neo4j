// 1. Creación de Índices de Optimización
CREATE INDEX idx_cliente_id IF NOT EXISTS FOR (c:Cliente) ON (c.id);
CREATE INDEX idx_transaccion_score IF NOT EXISTS FOR (t:Transaccion) ON (t.score_fraude);
CREATE INDEX idx_ip_vpn IF NOT EXISTS FOR (ip:DireccionIP) ON (ip.es_vpn);

// 2. Creación de Nodos
CREATE (c:Cliente {id: "CLI-01", nombre: "André", nivel_riesgo: "Bajo", fecha_registro: datetime("2023-01-15T08:30:00Z")})
CREATE (cta:Cuenta {numero: "ACC-101", tipo: "Corriente", saldo: 25000.00, moneda: "MXN"})
CREATE (t:Transaccion {id: "TX-9982", monto: 125000.00, fecha_hora: datetime("2026-10-19T09:15:00Z"), score_fraude: 0.94, estado: "Bloqueada"})
CREATE (mer:Comercio {id: "MER-880", nombre: "CryptoExchange Global", categoria_mcc: "6051", nivel_riesgo_comercio: "Alto"})
CREATE (d:Dispositivo {mac: "00:1B:44:11:3a:B7", so: "Android 13", fingerprint: "fp_9f8a2b3c4d5e"})
CREATE (ip:DireccionIP {ip: "185.220.101.5", pais: "RU", es_vpn: true, proveedor: "TorExitNode"})
CREATE (alt:AlertaFraude {id: "ALT-501", tipo_regla: "Ubicacion_Improbable_VPN", severidad: "Critica", fecha_creacion: datetime("2026-10-19T09:15:01Z")})

// 3. Creación de Relaciones
CREATE (c)-[:TITULAR_DE {fecha_vinculacion: "2023-01-15"}]->(cta)
CREATE (cta)-[:ORIGEN_DE]->(t)
CREATE (t)-[:DESTINO_A]->(mer)
CREATE (t)-[:EJECUTADA_DESDE]->(d)
CREATE (d)-[:CONECTADO_A {ultima_conexion: datetime("2026-10-19T09:14:50Z")}]->(ip)
CREATE (t)-[:GENERO_ALERTA]->(alt);
