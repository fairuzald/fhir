import asyncio
from sqlalchemy.orm import Session
from src.infrastructure.db.session import SessionLocal
from src.infrastructure.db.models.auth import User as UserModel
from src.infrastructure.db.models.fhir.patient import Patient as PatientModel
from src.infrastructure.db.models.fhir.encounter import Encounter as EncounterModel
from src.infrastructure.db.models.fhir.observation import Observation as ObservationModel
from src.domain.bundle.services import PasswordService

def create_seed_data():
    db = SessionLocal()

    try:
        password_service = PasswordService()

        # Create users
        users_data = [
            {
                "email": "admin@fhir.com",
                "hashed_password": password_service.get_password_hash("admin123"),
                "role": "admin"
            },
            {
                "email": "clinician@fhir.com",
                "hashed_password": password_service.get_password_hash("clinician123"),
                "role": "clinician"
            },
            {
                "email": "readonly@fhir.com",
                "hashed_password": password_service.get_password_hash("readonly123"),
                "role": "read_only"
            }
        ]

        for user_data in users_data:
            existing_user = db.query(UserModel).filter(UserModel.email == user_data["email"]).first()
            if not existing_user:
                user = UserModel(**user_data)
                db.add(user)

        db.commit()

        # Create sample patients
        patients_data = [
            {
                "identifier_value": "PAT001",
                "name_family": "Smith",
                "name_given": "John",
                "gender": "male",
                "birth_date": "1985-05-15",
                "resource": {
                    "resourceType": "Patient",
                    "identifier": [{"value": "PAT001", "system": "http://hospital.example.com/patients"}],
                    "name": [{"family": "Smith", "given": ["John"]}],
                    "gender": "male",
                    "birthDate": "1985-05-15"
                }
            },
            {
                "identifier_value": "PAT002",
                "name_family": "Johnson",
                "name_given": "Jane",
                "gender": "female",
                "birth_date": "1990-08-22",
                "resource": {
                    "resourceType": "Patient",
                    "identifier": [{"value": "PAT002", "system": "http://hospital.example.com/patients"}],
                    "name": [{"family": "Johnson", "given": ["Jane"]}],
                    "gender": "female",
                    "birthDate": "1990-08-22"
                }
            }
        ]

        created_patients = []
        for patient_data in patients_data:
            existing_patient = db.query(PatientModel).filter(PatientModel.identifier_value == patient_data["identifier_value"]).first()
            if not existing_patient:
                patient = PatientModel(**patient_data)
                db.add(patient)
                db.flush()  # Get the ID
                created_patients.append(patient)

        db.commit()

        # Create sample encounters
        encounters_data = [
            {
                "status": "finished",
                "class_code": "AMB",
                "subject_patient_id": created_patients[0].id,
                "period_start": "2024-01-15T09:00:00Z",
                "period_end": "2024-01-15T10:00:00Z",
                "reason_code": "Z00.00",
                "resource": {
                    "resourceType": "Encounter",
                    "status": "finished",
                    "class": {"code": "AMB", "display": "Ambulatory"},
                    "subject": {"reference": f"Patient/{created_patients[0].id}"},
                    "period": {
                        "start": "2024-01-15T09:00:00Z",
                        "end": "2024-01-15T10:00:00Z"
                    },
                    "reasonCode": [{"coding": [{"code": "Z00.00", "display": "Encounter for general adult medical examination"}]}]
                }
            },
            {
                "status": "in-progress",
                "class_code": "AMB",
                "subject_patient_id": created_patients[1].id,
                "period_start": "2024-01-16T14:00:00Z",
                "period_end": None,
                "reason_code": "Z00.00",
                "resource": {
                    "resourceType": "Encounter",
                    "status": "in-progress",
                    "class": {"code": "AMB", "display": "Ambulatory"},
                    "subject": {"reference": f"Patient/{created_patients[1].id}"},
                    "period": {
                        "start": "2024-01-16T14:00:00Z"
                    },
                    "reasonCode": [{"coding": [{"code": "Z00.00", "display": "Encounter for general adult medical examination"}]}]
                }
            }
        ]

        created_encounters = []
        for encounter_data in encounters_data:
            encounter = EncounterModel(**encounter_data)
            db.add(encounter)
            db.flush()  # Get the ID
            created_encounters.append(encounter)

        db.commit()

        # Create sample observations
        observations_data = [
            {
                "status": "final",
                "code_code": "8310-5",
                "subject_patient_id": created_patients[0].id,
                "encounter_id": created_encounters[0].id,
                "effective_datetime": "2024-01-15T09:30:00Z",
                "value_quantity_value": 98.6,
                "value_quantity_unit": "°F",
                "value_string": None,
                "resource": {
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {"coding": [{"code": "8310-5", "display": "Body temperature"}]},
                    "subject": {"reference": f"Patient/{created_patients[0].id}"},
                    "encounter": {"reference": f"Encounter/{created_encounters[0].id}"},
                    "effectiveDateTime": "2024-01-15T09:30:00Z",
                    "valueQuantity": {"value": 98.6, "unit": "°F", "system": "http://unitsofmeasure.org", "code": "[degF]"}
                }
            },
            {
                "status": "final",
                "code_code": "29463-7",
                "subject_patient_id": created_patients[0].id,
                "encounter_id": created_encounters[0].id,
                "effective_datetime": "2024-01-15T09:35:00Z",
                "value_quantity_value": 70,
                "value_quantity_unit": "kg",
                "value_string": None,
                "resource": {
                    "resourceType": "Observation",
                    "status": "final",
                    "code": {"coding": [{"code": "29463-7", "display": "Body weight"}]},
                    "subject": {"reference": f"Patient/{created_patients[0].id}"},
                    "encounter": {"reference": f"Encounter/{created_encounters[0].id}"},
                    "effectiveDateTime": "2024-01-15T09:35:00Z",
                    "valueQuantity": {"value": 70, "unit": "kg", "system": "http://unitsofmeasure.org", "code": "kg"}
                }
            },
            {
                "status": "preliminary",
                "code_code": "8310-5",
                "subject_patient_id": created_patients[1].id,
                "encounter_id": created_encounters[1].id,
                "effective_datetime": "2024-01-16T14:15:00Z",
                "value_quantity_value": 99.2,
                "value_quantity_unit": "°F",
                "value_string": None,
                "resource": {
                    "resourceType": "Observation",
                    "status": "preliminary",
                    "code": {"coding": [{"code": "8310-5", "display": "Body temperature"}]},
                    "subject": {"reference": f"Patient/{created_patients[1].id}"},
                    "encounter": {"reference": f"Encounter/{created_encounters[1].id}"},
                    "effectiveDateTime": "2024-01-16T14:15:00Z",
                    "valueQuantity": {"value": 99.2, "unit": "°F", "system": "http://unitsofmeasure.org", "code": "[degF]"}
                }
            }
        ]

        for observation_data in observations_data:
            observation = ObservationModel(**observation_data)
            db.add(observation)

        db.commit()
        print("Seed data created successfully!")

    except Exception as e:
        print(f"Error creating seed data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()

