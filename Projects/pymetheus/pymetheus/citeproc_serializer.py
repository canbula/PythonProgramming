from typing import TypeAlias

from .models_pymetheus import Item
from .zotero_csl_interop import CslFieldName, get_field_type, FieldType, \
    zotero_item_type_to, FIELD_ZOTERO_CSL, CREATOR_ZOTERO_CSL

CslDateFieldValue: TypeAlias = list[list[int]]


def split_date_field(field_value: str, /) -> CslDateFieldValue:
    """Split a date field value into CSL-JSON format."""
    if "/" not in field_value:
        return [list(map(int, field_value.split("-")))]
    else:
        return [
            list(map(int, date_str.split("-")))
            for date_str in field_value.split("/")
        ]


def serialize_item(item: Item, /) -> dict:
    """Serialize a pymetheus item to CSL-JSON."""

    text_fields: dict[CslFieldName, str] = {}
    date_fields: dict[CslFieldName, dict[str, CslDateFieldValue]] = {}
    name_fields: dict[CslFieldName, list[dict[str, str]]] = {}

    for zotero_field_name, field_value in item.field_data.items():
        field_type = get_field_type(zotero_field_name)
        csl_field_name = FIELD_ZOTERO_CSL[zotero_field_name]
        if field_type == FieldType.STANDARD:
            text_fields[csl_field_name] = field_value
        elif field_type == FieldType.DATE:
            date_fields[csl_field_name] = {
                "date-parts": split_date_field(field_value)
            }
        elif field_type == FieldType.NAME:
            raise ValueError(f"Unexpected name field: {csl_field_name}")
        else:
            raise ValueError(f"Field name with unknown type: {csl_field_name}")

    for zotero_creator_type, name_data_list in item.creators.items():
        csl_field_name = CREATOR_ZOTERO_CSL[zotero_creator_type]
        name_fields[csl_field_name] = [
            name_data.as_dict() for name_data in name_data_list
        ]

    return {
        "type": zotero_item_type_to(item.type.name, "csl"),
        **text_fields,
        **date_fields,
        **name_fields,
    }
