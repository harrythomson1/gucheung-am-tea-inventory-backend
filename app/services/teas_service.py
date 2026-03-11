class TeasService:

    def __init__(self, repository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all
