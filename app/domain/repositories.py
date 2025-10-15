from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities import User, Patient, Encounter, Observation

class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

class PatientRepository(ABC):
    @abstractmethod
    async def get_by_id(self, patient_id: UUID) -> Optional[Patient]:
        pass

    @abstractmethod
    async def create(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    async def update(self, patient: Patient) -> Patient:
        pass

    @abstractmethod
    async def delete(self, patient_id: UUID) -> bool:
        pass

    @abstractmethod
    async def search(self, name: Optional[str] = None, identifier: Optional[str] = None) -> List[Patient]:
        pass

class EncounterRepository(ABC):
    @abstractmethod
    async def get_by_id(self, encounter_id: UUID) -> Optional[Encounter]:
        pass

    @abstractmethod
    async def create(self, encounter: Encounter) -> Encounter:
        pass

    @abstractmethod
    async def update(self, encounter: Encounter) -> Encounter:
        pass

    @abstractmethod
    async def delete(self, encounter_id: UUID) -> bool:
        pass

    @abstractmethod
    async def search(self, status: Optional[str] = None, subject: Optional[UUID] = None, date: Optional[str] = None) -> List[Encounter]:
        pass

class ObservationRepository(ABC):
    @abstractmethod
    async def get_by_id(self, observation_id: UUID) -> Optional[Observation]:
        pass

    @abstractmethod
    async def create(self, observation: Observation) -> Observation:
        pass

    @abstractmethod
    async def update(self, observation: Observation) -> Observation:
        pass

    @abstractmethod
    async def delete(self, observation_id: UUID) -> bool:
        pass

    @abstractmethod
    async def search(self, code: Optional[str] = None, date: Optional[str] = None, subject: Optional[UUID] = None) -> List[Observation]:
        pass

