DROP DATABASE IF EXISTS linki_health_citas;
CREATE DATABASE linki_health_citas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE linki_health_citas;

CREATE TABLE especialidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profesionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    especialidad_id INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    matricula VARCHAR(50),
    descripcion VARCHAR(255),
    foto_url VARCHAR(255),
    activo TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_profesional_especialidad FOREIGN KEY (especialidad_id) REFERENCES especialidades(id)
);

CREATE TABLE disponibilidad_profesional (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesional_id INT NOT NULL,
    tipo_jornada ENUM('medio_tiempo','tiempo_completo','personalizada') NOT NULL,
    dias_atencion VARCHAR(80) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    duracion_cita_minutos INT NOT NULL DEFAULT 30,
    activo TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT fk_disponibilidad_profesional FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
);

CREATE TABLE horarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profesional_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    disponible TINYINT(1) NOT NULL DEFAULT 1,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_horario_profesional FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
    CONSTRAINT uq_profesional_fecha_hora UNIQUE (profesional_id, fecha, hora_inicio)
);

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    documento VARCHAR(40),
    telefono VARCHAR(40) NOT NULL,
    email VARCHAR(120) NOT NULL,
    fecha_nacimiento DATE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    profesional_id INT NOT NULL,
    horario_id INT NOT NULL,
    motivo TEXT,
    estado ENUM('confirmada','cancelada','atendida') NOT NULL DEFAULT 'confirmada',
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cita_paciente FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    CONSTRAINT fk_cita_especialidad FOREIGN KEY (especialidad_id) REFERENCES especialidades(id),
    CONSTRAINT fk_cita_profesional FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
    CONSTRAINT fk_cita_horario FOREIGN KEY (horario_id) REFERENCES horarios(id),
    CONSTRAINT uq_cita_horario UNIQUE (horario_id)
);

INSERT INTO especialidades (nombre, descripcion) VALUES
('Medicina General', 'Atención inicial, controles y orientación médica.'),
('Pediatría', 'Atención médica para niños y adolescentes.'),
('Cardiología', 'Evaluación del corazón y sistema cardiovascular.'),
('Dermatología', 'Diagnóstico y tratamiento de la piel.'),
('Ginecología', 'Atención integral de salud femenina.'),
('Traumatología', 'Evaluación de lesiones óseas y musculares.');

INSERT INTO profesionales (especialidad_id, nombre, matricula, descripcion, foto_url) VALUES
(1, 'Dra. Valeria Rojas', 'MG-1025', 'Medicina familiar y controles preventivos.', NULL),
(1, 'Dr. Mateo Quiroga', 'MG-2041', 'Atención primaria y seguimiento clínico.', NULL),
(2, 'Dra. Camila Salazar', 'PED-1180', 'Control pediátrico y vacunación.', NULL),
(2, 'Dr. Andrés Paredes', 'PED-2204', 'Pediatría general y crecimiento infantil.', NULL),
(3, 'Dr. Javier Montaño', 'CAR-3020', 'Evaluación cardiovascular y presión arterial.', NULL),
(4, 'Dra. Renata Vega', 'DER-4118', 'Acné, alergias cutáneas y lunares.', NULL),
(5, 'Dra. Mariana Flores', 'GIN-5190', 'Controles ginecológicos y salud preventiva.', NULL),
(6, 'Dr. Diego Arce', 'TRA-6222', 'Lesiones deportivas y dolor articular.', NULL);

INSERT INTO disponibilidad_profesional (profesional_id, tipo_jornada, dias_atencion, hora_inicio, hora_fin, duracion_cita_minutos) VALUES
(1, 'medio_tiempo', 'Lunes a viernes', '08:00:00', '12:00:00', 30),
(2, 'tiempo_completo', 'Lunes a viernes', '08:00:00', '16:00:00', 30),
(3, 'medio_tiempo', 'Lunes, miércoles y viernes', '08:00:00', '12:00:00', 30),
(4, 'medio_tiempo', 'Martes y jueves', '09:00:00', '13:00:00', 30),
(5, 'tiempo_completo', 'Lunes a viernes', '08:00:00', '16:00:00', 30),
(6, 'medio_tiempo', 'Lunes, miércoles y viernes', '09:00:00', '13:00:00', 30),
(7, 'medio_tiempo', 'Martes y jueves', '08:00:00', '12:00:00', 30),
(8, 'tiempo_completo', 'Lunes a viernes', '08:00:00', '16:00:00', 30);

INSERT INTO horarios (profesional_id, fecha, hora_inicio, hora_fin, disponible) VALUES
(1, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:30:00', '09:00:00', 0),
(2, DATE_ADD(CURDATE(), INTERVAL 2 DAY), '11:00:00', '11:30:00', 0),
(5, DATE_ADD(CURDATE(), INTERVAL 3 DAY), '08:30:00', '09:00:00', 0),
(8, DATE_ADD(CURDATE(), INTERVAL 4 DAY), '15:30:00', '16:00:00', 0);

INSERT INTO pacientes (nombre_completo, documento, telefono, email, fecha_nacimiento) VALUES
('Paciente Demo Uno', '1234567', '70000001', 'paciente1@demo.com', '1998-04-12'),
('Paciente Demo Dos', '7654321', '70000002', 'paciente2@demo.com', '2001-09-21');

INSERT INTO citas (paciente_id, especialidad_id, profesional_id, horario_id, motivo, estado) VALUES
(1, 1, 1, 1, 'Control general de ejemplo.', 'confirmada'),
(2, 3, 5, 3, 'Consulta cardiológica de ejemplo.', 'confirmada');
