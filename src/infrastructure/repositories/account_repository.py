from mongoengine import Q
from bson import ObjectId
from datetime import datetime
from beanie import PydanticObjectId
from src.infrastructure.document.account import Account as AccountDocument, AccountStatus
from src.domain.user.account.entities import Account as AccountEntity, Localization
from src.domain.user.account.enum import Lang, TimeFormat, DateFormat, Currency, NumberFormat
from src.domain.user.authentication.authentication import AccountAuthentication
from src.domain.user.account.input_account import InputCreateAccount, InputUpdateAccount, InputUpdateLocalozation

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
    
    async def update(self, authentication: AccountAuthentication, input_update: InputUpdateAccount) -> AccountDocument | None:
        document = await self.__define_document(authentication)

        if not document:
            return None
        
        for key, value in input_update.model_dump(exclude_unset=True).items():
            setattr(document, key, value)

        await document.save()

        return await self.get_by_id(document.id)
    
    async def delete(self, authentication: AccountAuthentication, id: str) -> None:
        document = await self.__define_document(authentication)
        if not document:
            return None

        document.status = AccountStatus.DELETED
        document.deleted_at = int(datetime.now().timestamp() * 1000)
        await document.save()

        return None
    
    async def update_localization(self, authentication: AccountAuthentication, data: InputUpdateLocalozation) -> AccountEntity:
        document = await self.__define_document(authentication)
        if not document:
            return None
        
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(document.localization, key, value)

        await document.save()

        return await self.get_by_id(document.id)
    
    async def __define_document(self, authentication: AccountAuthentication) -> AccountDocument:
        return await self.__account_document.get(PydanticObjectId(authentication.id))

    def __to_domain_object(self, document: AccountDocument) -> AccountEntity:
        return AccountEntity(
            id=str(document.id),
            username = str(document.username),
            email = str(document.email),
            mobile_number = str(document.mobile_number),
            password_hash = str(document.password_hash),
            status = str(document.status.value),
            role = str(document.role.value),
            localization = Localization(
                lang= getattr(document.localization, "lang", Lang.ID),
                date_format= getattr(document.localization, "date_format", DateFormat.DDMMYY),
                time_format= getattr(document.localization, "time_format", TimeFormat._24H),
                number_format= getattr(document.localization, "number_format", NumberFormat.TITIK),
                currency= getattr(document.localization, "currency", Currency.IDR)
            ),
            created_at = str(document.created_at),
            updated_at = str(document.updated_at),
            deleted_at = str(document.deleted_at),
        )