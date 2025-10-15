from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from .entities import Observation

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

