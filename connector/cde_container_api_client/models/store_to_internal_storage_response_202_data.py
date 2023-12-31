from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StoreToInternalStorageResponse202Data")


@attr.s(auto_attribs=True)
class StoreToInternalStorageResponse202Data:
    """
    Example:
        {'id': '8d90b766-16af-4683-9bfd-1d4757dfb58e'}

    Attributes:
        id (Union[Unset, str]):  Example: 8d90b766-16af-4683-9bfd-1d4757dfb58e.
    """

    id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        store_to_internal_storage_response_202_data = cls(
            id=id,
        )

        store_to_internal_storage_response_202_data.additional_properties = d
        return store_to_internal_storage_response_202_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
