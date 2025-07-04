
from app.auth.application.service.auth import UserNotFoundException
from app.rbac.domain.entity.role import Role
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepository
from app.user.domain.usecase.user import UserUseCase
from core.db.transactional import Transactional


class UserService(UserUseCase):

	def __init__(self, repository : UserRepository):
		self.repository = repository

	async def get_user_list(self, limit: int, page:int) -> list[User]:
		data = await self.repository.get_user_list(limit,page)
		return data

	async def get_user_by_id(self, user_id: int) -> User | None:
		user = await self.repository.get_user_by_id(user_id)
		return user
	
	async def get_user_by_uuid(self, user_uuid: str) -> User | None:
		user = await self.repository.get_user_by_uuid(user_uuid)
		return user

	async def get_user_by_email(self) -> User | None:
		raise NotImplementedError

	async def is_active(self,user_id) -> bool:
		raise NotImplementedError

	async def is_owner(self) -> bool:
		raise NotImplementedError

	def is_admin(self) -> bool:
		raise NotImplementedError
	
	@Transactional()
	async def create_user(self, *, command: CreateUserCommand) -> User | None:
		user = User.model_validate(command)
		new_user = await self.repository.save(user=user)
		return new_user

	@Transactional()
	async def asign_role_to_user(self, user_uuid: str, role_id: int) -> User:
		user = await self.repository.get_user_by_uuid(user_uuid)
		if not user:
			raise UserNotFoundException
		user.fk_role = role_id
		user = await self.repository.save(user)
		return user
		
		



