from mongoengine import Q
from bson import ObjectId
from beanie import PydanticObjectId
from src.infrastructure.document.account import Account as AccountDocument
from src.domain.user.account.entities import Account as AccountEntity
from src.domain.user.account.input_account import InputCreateAccount, InputUpdateAccount

class AccountRepository(object):
    def __init__(
            self,
            account_document: AccountDocument
    ):
        self.__account_document = account_document
    
    async def get_by_id(self, id: str) -> AccountEntity| None:
        document = await self.__account_document.find_one({"_id": ObjectId(id)})
        if not document:
            return None
        return self.__to_domain_object(document)
    
    async def get_by_email(self, email: str) -> AccountEntity| None:
        document = await self.__account_document.find_one({"email": email})
        if not document:
            return None
        return self.__to_domain_object(document)
    
    async def create(self, input_create_account: InputCreateAccount) -> AccountEntity:
        document = AccountDocument(**input_create_account.to_input_dict())
        await document.insert()
        return self.__to_domain_object(document)
    
    async def list(self) -> list[AccountEntity]:
        docs = await self.__account_document.find_all().to_list()
        return [self.__to_domain_object(doc) for doc in docs]
    
    async def update(self, id: str, input_update: InputUpdateAccount) -> AccountDocument | None:
        document = await self.__account_document.get(PydanticObjectId(id))
        if not document:
            return None

        await document.set(input_update.model_dump(exclude_unset=True))

        return await self.get_by_id(document.id)

    def __to_domain_object(self, document: AccountDocument) -> AccountEntity:
        return AccountEntity(
            id=str(document.id),
            username = str(document.username),
            email = str(document.email),
            mobile_number = str(document.mobile_number),
            password_hash = str(document.password_hash),
            status = str(document.status.value),
            role = str(document.role.value),
            created_at = str(document.created_at),
            updated_at = str(document.updated_at),
            deleted_at = str(document.deleted_at),
        )