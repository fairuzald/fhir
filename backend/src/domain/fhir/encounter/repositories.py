from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import Encounter

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

