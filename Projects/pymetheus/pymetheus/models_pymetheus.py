from dataclasses import dataclass
from typing import Self

from .models_zotero import ItemType, ITEM_TYPES
from .zotero_csl_interop import ZoteroFieldName, ZoteroCreatorTypeName, \
    is_field_date


@dataclass(frozen=True)
class NameData:
    family: str | None = None
    given: str | None = None
    suffix: str | None = None
    dropping_particle: str | None = None
    non_dropping_particle: str | None = None
    literal: str | None = None

    _casefolded_family: str | None = None
    _casefolded_given: str | None = None
    _casefolded_suffix: str | None = None
    _casefolded_dropping_particle: str | None = None
    _casefolded_non_dropping_particle: str | None = None
    _casefolded_literal: str | None = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
            object.__setattr__(
                self,
                f"_casefolded_{key}",
                value.casefold() if value is not None else None
            )

    def __str__(self):
        if self.literal:
            return self.literal
        parts = []
        if self.dropping_particle:
            parts.append(self.dropping_particle)
        if self.given:
            parts.append(self.given)
        if self.non_dropping_particle:
            parts.append(self.non_dropping_particle)
        if self.family:
            parts.append(self.family)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)

    def as_dict(self) -> dict:
        new_obj = {}

        if self.family is not None:
            new_obj['family'] = self.family
        if self.given is not None:
            new_obj['given'] = self.given
        if self.suffix is not None:
            new_obj['suffix'] = self.suffix
        if self.dropping_particle is not None:
            new_obj['dropping-particle'] = self.dropping_particle
        if self.non_dropping_particle is not None:
            new_obj['non-dropping-particle'] = self.non_dropping_particle
        if self.literal is not None:
            new_obj['literal'] = self.literal

        return new_obj

    @classmethod
    def from_dict(cls, d: dict, /) -> Self:
        args = {}

        if "family" in d:
            args["family"] = d["family"]
        if "given" in d:
            args["given"] = d["given"]
        if "suffix" in d:
            args["suffix"] = d["suffix"]
        if "dropping-particle" in d:
            args["dropping_particle"] = d["dropping-particle"]
        if "non-dropping-particle" in d:
            args["non_dropping_particle"] = d["non-dropping-particle"]
        if "literal" in d:
            args["literal"] = d["literal"]

        return cls(**args)

    def search(self, query: str, casefolded: bool = False) -> bool:
        if not casefolded:
            return (
                query in str(self)
                or (self.family is not None and query in self.family)
                or (self.given is not None and query in self.given)
                or (self.suffix is not None and query in self.suffix)
                or (
                        self.dropping_particle is not None
                        and query in self.dropping_particle
                )
                or (
                        self.non_dropping_particle is not None
                        and query in self.non_dropping_particle
                )
                or (
                        self.literal is not None
                        and query in self.literal
                )
            )

        # Assume query is casefolded and search in casefolded fields instead
        return (
            query in str(self).casefold()
            or (
                    self._casefolded_family is not None
                    and query in self._casefolded_family
            )
            or (
                    self._casefolded_given is not None
                    and query in self._casefolded_given
            )
            or (
                    self._casefolded_suffix is not None
                    and query in self._casefolded_suffix
            )
            or (
                    self._casefolded_dropping_particle is not None
                    and query in self._casefolded_dropping_particle
            )
            or (
                    self._casefolded_non_dropping_particle is not None
                    and query in self._casefolded_non_dropping_particle
            )
            or (
                    self._casefolded_literal is not None
                    and query in self._casefolded_literal
            )
        )

    def empty(self) -> bool:
        return all(
            value is None
            for value in (
                self.family,
                self.given,
                self.suffix,
                self.dropping_particle,
                self.non_dropping_particle,
                self.literal,
            )
        )


@dataclass
class Item:
    type: ItemType
    field_data: dict[ZoteroFieldName, str]
    creators: dict[ZoteroCreatorTypeName, list[NameData]]

    _casefolded_field_data: dict[ZoteroFieldName, str] = None

    def as_dict(self) -> dict:
        return {
            "type": self.type.name,
            "field_data": self.field_data,
            "creators": {
                c_type: [nd.as_dict() for nd in nd_list]
                for c_type, nd_list in self.creators.items()
            }
        }

    @classmethod
    def from_dict(cls, d: dict, /) -> Self:
        return cls(
            type=ITEM_TYPES[d["type"]],
            field_data=d["field_data"],
            creators={
                ZoteroCreatorTypeName(creator_type): [
                    NameData.from_dict(name_data)
                    for name_data in name_data_list
                ]
                for creator_type, name_data_list in d["creators"].items()
            }
        )

    @classmethod
    def from_triplet(
            cls, *, item_type: str, field_data: dict, creators: dict
    ) -> Self:
        return cls.from_dict({
            "type": item_type,
            "field_data": field_data,
            "creators": creators,
        })

    def get_main_creator_type(self) -> ZoteroCreatorTypeName | None:
        if not self.type.creator_types:
            return None
        return self.type.creator_types[0]

    def get_main_creator(self) -> NameData | None:
        main_creator_type = self.get_main_creator_type()
        if main_creator_type is None:
            return None
        if main_creator_type not in self.creators:
            return None
        if not self.creators[main_creator_type]:
            return None
        return self.creators[main_creator_type][0]

    def _ensure_casefold_cache(self) -> None:
        if self._casefolded_field_data is not None:
            return

        self._casefolded_field_data = {
            key: value.casefold()
            for key, value in self.field_data.items()
        }

    def search(self, query: str, casefolded: bool = False) -> bool:
        if not casefolded:
            data = self.field_data
        else:
            self._ensure_casefold_cache()
            data = self._casefolded_field_data

        for field_value in data.values():
            if query in field_value:
                return True
        for name_data_list in self.creators.values():
            for name_data in name_data_list:
                if name_data.search(query, casefolded=casefolded):
                    return True
        return False

    def try_to_generate_id(self) -> str | None:
        parts = []
        main_creator = self.get_main_creator()
        if main_creator is not None:
            parts.append(main_creator.family)
        date_fields = [
            x
            for x in self.type.fields
            if is_field_date(x.base_field)
        ]
        for field in date_fields:
            if field in self.field_data:
                parts.append(self.field_data[field])
        if parts:
            return "_".join(parts)
        return None
