-- --------------------------------------------------------
-- ESQUEMA BASE DE DATOS: CENTRO DE SALUD
-- --------------------------------------------------------

-- Tabla central compartida
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    rut VARCHAR(12) UNIQUE NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Módulo 1: Área Clínica (Reemplaza a la antigua "Agenda")
CREATE TABLE citas_medicas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id),
    medico VARCHAR(100) NOT NULL,
    box VARCHAR(10),
    fecha_cita TIMESTAMP NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente'
);

-- Módulo 2: Área de Laboratorio
CREATE TABLE examenes_laboratorio (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER REFERENCES pacientes(id),
    tipo_examen VARCHAR(50) NOT NULL,
    resultado TEXT,
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'En Proceso'
);

-- --------------------------------------------------------
-- INSERCIÓN DE DATOS DE PRUEBA (Dummy Data)
-- --------------------------------------------------------

INSERT INTO pacientes (rut, nombre_completo) VALUES 
('11111111-1', 'Juan Perez'),
('22222222-2', 'Maria Gonzalez'),
('33333333-3', 'Pedro Soto');

INSERT INTO citas_medicas (paciente_id, medico, box, fecha_cita) VALUES 
(1, 'Dr. House', 'Box 1', '2026-06-10 10:00:00'),
(2, 'Dra. Grey', 'Box 3', '2026-06-11 15:30:00');

INSERT INTO examenes_laboratorio (paciente_id, tipo_examen) VALUES 
(1, 'Hemograma Completo'),
(3, 'Perfil Bioquímico');
