class TeaService:

    def __init__(self, repository):
        self.repository = repository

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, id):
        return await self.repository.get_by_id(id)
