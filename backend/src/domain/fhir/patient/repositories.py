from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import Patient

class PatientRepository(ABC):
    @abstractmethod
    def get_by_id(self, patient_id: UUID) -> Optional[Patient]:
        pass

    @abstractmethod
    def create(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    def update(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    def delete(self, patient_id: UUID) -> bool:
        pass

    @abstractmethod
    def search(self, name: Optional[str] = None, identifier: Optional[str] = None) -> List[Patient]:
        pass
