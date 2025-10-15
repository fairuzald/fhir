CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE SCHEMA IF NOT EXISTS fhir;

-- Users
CREATE TABLE auth_user (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  hashed_password TEXT NOT NULL,
  role TEXT CHECK (role IN ('admin','clinician','read_only')),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Patient
CREATE TABLE fhir.patient (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  identifier_value TEXT,
  name_family TEXT,
  name_given TEXT,
  gender TEXT CHECK (gender IN ('male','female','other','unknown')),
  birth_date DATE,
  resource JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Encounter
CREATE TABLE fhir.encounter (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status TEXT,
  class_code TEXT,
  subject_patient_id UUID REFERENCES fhir.patient(id),
  period_start TIMESTAMPTZ,
  period_end TIMESTAMPTZ,
  reason_code TEXT,
  resource JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Observation
CREATE TABLE fhir.observation (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  status TEXT,
  code_code TEXT,
  subject_patient_id UUID REFERENCES fhir.patient(id),
  encounter_id UUID REFERENCES fhir.encounter(id),
  effective_datetime TIMESTAMPTZ,
  value_quantity_value NUMERIC,
  value_quantity_unit TEXT,
  value_string TEXT,
  resource JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better search performance
CREATE INDEX idx_patient_identifier ON fhir.patient(identifier_value);
CREATE INDEX idx_patient_name_family ON fhir.patient(name_family);
CREATE INDEX idx_patient_name_given ON fhir.patient(name_given);
CREATE INDEX idx_encounter_status ON fhir.encounter(status);
CREATE INDEX idx_encounter_subject ON fhir.encounter(subject_patient_id);
CREATE INDEX idx_encounter_period_start ON fhir.encounter(period_start);
CREATE INDEX idx_observation_code ON fhir.observation(code_code);
CREATE INDEX idx_observation_subject ON fhir.observation(subject_patient_id);
CREATE INDEX idx_observation_effective ON fhir.observation(effective_datetime);

