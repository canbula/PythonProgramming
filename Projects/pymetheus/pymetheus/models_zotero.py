from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias, Protocol, TypedDict, NotRequired, Literal, \
    NamedTuple

from .zotero_csl_interop import ZoteroItemTypeName, ZoteroFieldName, \
    ZoteroCreatorTypeName, ZoteroName


class Field(NamedTuple):
    name: ZoteroFieldName
    base_field: ZoteroFieldName


@dataclass(slots=True, frozen=True)
class ItemType:
    name: ZoteroItemTypeName
    fields: list[Field]
    creator_types: list[ZoteroCreatorTypeName]


class SchemaField(TypedDict):
    field: str
    baseField: NotRequired[str]


class SchemaCreatorType(TypedDict):
    creatorType: str
    primary: NotRequired[Literal[True]]


class SchemaItemType(TypedDict):
    itemType: str
    fields: list[SchemaField]
    creatorTypes: list[SchemaCreatorType]


SCHEMA_ITEM_TYPES: list[SchemaItemType] = [
    {
        "itemType": "annotation",
        "fields": [],
        "creatorTypes": []
    },
    {
        "itemType": "artwork",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "artworkMedium",
                "baseField": "medium"
            },
            {
                "field": "artworkSize"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "artist",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "attachment",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "url"
            }
        ],
        "creatorTypes": []
    },
    {
        "itemType": "audioRecording",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "audioRecordingFormat",
                "baseField": "medium"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "volume"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "place"
            },
            {
                "field": "label",
                "baseField": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "runningTime"
            },
            {
                "field": "language"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "performer",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "composer"
            },
            {
                "creatorType": "wordsBy"
            }
        ]
    },
    {
        "itemType": "bill",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "billNumber",
                "baseField": "number"
            },
            {
                "field": "code"
            },
            {
                "field": "codeVolume",
                "baseField": "volume"
            },
            {
                "field": "section"
            },
            {
                "field": "codePages",
                "baseField": "pages"
            },
            {
                "field": "legislativeBody",
                "baseField": "authority"
            },
            {
                "field": "session"
            },
            {
                "field": "history"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "sponsor",
                "primary": True
            },
            {
                "creatorType": "cosponsor"
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "blogPost",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "blogTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "websiteType",
                "baseField": "type"
            },
            {
                "field": "date"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "commenter"
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "book",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "series"
            },
            {
                "field": "seriesNumber"
            },
            {
                "field": "volume"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "edition"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "numPages"
            },
            {
                "field": "language"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "bookSection",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "bookTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "series"
            },
            {
                "field": "seriesNumber"
            },
            {
                "field": "volume"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "edition"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "pages"
            },
            {
                "field": "language"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "bookAuthor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "case",
        "fields": [
            {
                "field": "caseName",
                "baseField": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "court",
                "baseField": "authority"
            },
            {
                "field": "dateDecided",
                "baseField": "date"
            },
            {
                "field": "docketNumber",
                "baseField": "number"
            },
            {
                "field": "reporter"
            },
            {
                "field": "reporterVolume",
                "baseField": "volume"
            },
            {
                "field": "firstPage",
                "baseField": "pages"
            },
            {
                "field": "history"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "counsel"
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "computerProgram",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "versionNumber"
            },
            {
                "field": "date"
            },
            {
                "field": "system"
            },
            {
                "field": "place"
            },
            {
                "field": "company",
                "baseField": "publisher"
            },
            {
                "field": "programmingLanguage"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "rights"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "programmer",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "conferencePaper",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "date"
            },
            {
                "field": "proceedingsTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "conferenceName"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "volume"
            },
            {
                "field": "pages"
            },
            {
                "field": "series"
            },
            {
                "field": "language"
            },
            {
                "field": "DOI"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "dataset",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "identifier",
                "baseField": "number"
            },
            {
                "field": "type"
            },
            {
                "field": "versionNumber"
            },
            {
                "field": "date"
            },
            {
                "field": "repository",
                "baseField": "publisher"
            },
            {
                "field": "repositoryLocation",
                "baseField": "place"
            },
            {
                "field": "format",
                "baseField": "medium"
            },
            {
                "field": "DOI"
            },
            {
                "field": "citationKey"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "language"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "dictionaryEntry",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "dictionaryTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "series"
            },
            {
                "field": "seriesNumber"
            },
            {
                "field": "volume"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "edition"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "pages"
            },
            {
                "field": "language"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "document",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "reviewedAuthor"
            }
        ]
    },
    {
        "itemType": "email",
        "fields": [
            {
                "field": "subject",
                "baseField": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "date"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "language"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "recipient"
            }
        ]
    },
    {
        "itemType": "encyclopediaArticle",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "encyclopediaTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "series"
            },
            {
                "field": "seriesNumber"
            },
            {
                "field": "volume"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "edition"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "pages"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "language"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "film",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "distributor",
                "baseField": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "genre",
                "baseField": "type"
            },
            {
                "field": "videoRecordingFormat",
                "baseField": "medium"
            },
            {
                "field": "runningTime"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "director",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "scriptwriter"
            },
            {
                "creatorType": "producer"
            }
        ]
    },
    {
        "itemType": "forumPost",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "forumTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "postType",
                "baseField": "type"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "hearing",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "committee"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "documentNumber",
                "baseField": "number"
            },
            {
                "field": "pages"
            },
            {
                "field": "legislativeBody",
                "baseField": "authority"
            },
            {
                "field": "session"
            },
            {
                "field": "history"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "contributor",
                "primary": True
            }
        ]
    },
    {
        "itemType": "instantMessage",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "recipient"
            }
        ]
    },
    {
        "itemType": "interview",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "date"
            },
            {
                "field": "interviewMedium",
                "baseField": "medium"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "interviewee",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "interviewer"
            },
            {
                "creatorType": "translator"
            }
        ]
    },
    {
        "itemType": "journalArticle",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "publicationTitle"
            },
            {
                "field": "volume"
            },
            {
                "field": "issue"
            },
            {
                "field": "pages"
            },
            {
                "field": "date"
            },
            {
                "field": "series"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "seriesText"
            },
            {
                "field": "journalAbbreviation"
            },
            {
                "field": "language"
            },
            {
                "field": "DOI"
            },
            {
                "field": "ISSN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "reviewedAuthor"
            }
        ]
    },
    {
        "itemType": "letter",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "letterType",
                "baseField": "type"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "recipient"
            }
        ]
    },
    {
        "itemType": "magazineArticle",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "publicationTitle"
            },
            {
                "field": "volume"
            },
            {
                "field": "issue"
            },
            {
                "field": "date"
            },
            {
                "field": "pages"
            },
            {
                "field": "language"
            },
            {
                "field": "ISSN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "reviewedAuthor"
            }
        ]
    },
    {
        "itemType": "manuscript",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "manuscriptType",
                "baseField": "type"
            },
            {
                "field": "place"
            },
            {
                "field": "date"
            },
            {
                "field": "numPages"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "translator"
            }
        ]
    },
    {
        "itemType": "map",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "mapType",
                "baseField": "type"
            },
            {
                "field": "scale"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "edition"
            },
            {
                "field": "place"
            },
            {
                "field": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "language"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "cartographer",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "newspaperArticle",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "publicationTitle"
            },
            {
                "field": "place"
            },
            {
                "field": "edition"
            },
            {
                "field": "date"
            },
            {
                "field": "section"
            },
            {
                "field": "pages"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "ISSN"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "reviewedAuthor"
            }
        ]
    },
    {
        "itemType": "note",
        "fields": [],
        "creatorTypes": []
    },
    {
        "itemType": "patent",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "place"
            },
            {
                "field": "country"
            },
            {
                "field": "assignee"
            },
            {
                "field": "issuingAuthority",
                "baseField": "authority"
            },
            {
                "field": "patentNumber",
                "baseField": "number"
            },
            {
                "field": "filingDate"
            },
            {
                "field": "pages"
            },
            {
                "field": "applicationNumber"
            },
            {
                "field": "priorityNumbers"
            },
            {
                "field": "issueDate",
                "baseField": "date"
            },
            {
                "field": "references"
            },
            {
                "field": "legalStatus",
                "baseField": "status"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "inventor",
                "primary": True
            },
            {
                "creatorType": "attorneyAgent"
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "podcast",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "episodeNumber",
                "baseField": "number"
            },
            {
                "field": "audioFileType",
                "baseField": "medium"
            },
            {
                "field": "runningTime"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "podcaster",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "guest"
            }
        ]
    },
    {
        "itemType": "preprint",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "genre",
                "baseField": "type"
            },
            {
                "field": "repository",
                "baseField": "publisher"
            },
            {
                "field": "archiveID",
                "baseField": "number"
            },
            {
                "field": "place"
            },
            {
                "field": "date"
            },
            {
                "field": "series"
            },
            {
                "field": "seriesNumber"
            },
            {
                "field": "DOI"
            },
            {
                "field": "citationKey"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "language"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "editor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "reviewedAuthor"
            }
        ]
    },
    {
        "itemType": "presentation",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "presentationType",
                "baseField": "type"
            },
            {
                "field": "date"
            },
            {
                "field": "place"
            },
            {
                "field": "meetingName"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "presenter",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "radioBroadcast",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "programTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "episodeNumber",
                "baseField": "number"
            },
            {
                "field": "audioRecordingFormat",
                "baseField": "medium"
            },
            {
                "field": "place"
            },
            {
                "field": "network",
                "baseField": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "runningTime"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "director",
                "primary": True
            },
            {
                "creatorType": "scriptwriter"
            },
            {
                "creatorType": "producer"
            },
            {
                "creatorType": "castMember"
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "guest"
            }
        ]
    },
    {
        "itemType": "report",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "reportNumber",
                "baseField": "number"
            },
            {
                "field": "reportType",
                "baseField": "type"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "place"
            },
            {
                "field": "institution",
                "baseField": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "pages"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "translator"
            },
            {
                "creatorType": "seriesEditor"
            }
        ]
    },
    {
        "itemType": "standard",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "organization",
                "baseField": "authority"
            },
            {
                "field": "committee"
            },
            {
                "field": "type"
            },
            {
                "field": "number"
            },
            {
                "field": "versionNumber"
            },
            {
                "field": "status"
            },
            {
                "field": "date"
            },
            {
                "field": "publisher"
            },
            {
                "field": "place"
            },
            {
                "field": "DOI"
            },
            {
                "field": "citationKey"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "numPages"
            },
            {
                "field": "language"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "statute",
        "fields": [
            {
                "field": "nameOfAct",
                "baseField": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "code"
            },
            {
                "field": "codeNumber"
            },
            {
                "field": "publicLawNumber",
                "baseField": "number"
            },
            {
                "field": "dateEnacted",
                "baseField": "date"
            },
            {
                "field": "pages"
            },
            {
                "field": "section"
            },
            {
                "field": "session"
            },
            {
                "field": "history"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "thesis",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "thesisType",
                "baseField": "type"
            },
            {
                "field": "university",
                "baseField": "publisher"
            },
            {
                "field": "place"
            },
            {
                "field": "date"
            },
            {
                "field": "numPages"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "tvBroadcast",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "programTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "episodeNumber",
                "baseField": "number"
            },
            {
                "field": "videoRecordingFormat",
                "baseField": "medium"
            },
            {
                "field": "place"
            },
            {
                "field": "network",
                "baseField": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "runningTime"
            },
            {
                "field": "language"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "director",
                "primary": True
            },
            {
                "creatorType": "scriptwriter"
            },
            {
                "creatorType": "producer"
            },
            {
                "creatorType": "castMember"
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "guest"
            }
        ]
    },
    {
        "itemType": "videoRecording",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "videoRecordingFormat",
                "baseField": "medium"
            },
            {
                "field": "seriesTitle"
            },
            {
                "field": "volume"
            },
            {
                "field": "numberOfVolumes"
            },
            {
                "field": "place"
            },
            {
                "field": "studio",
                "baseField": "publisher"
            },
            {
                "field": "date"
            },
            {
                "field": "runningTime"
            },
            {
                "field": "language"
            },
            {
                "field": "ISBN"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "archive"
            },
            {
                "field": "archiveLocation"
            },
            {
                "field": "libraryCatalog"
            },
            {
                "field": "callNumber"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "director",
                "primary": True
            },
            {
                "creatorType": "scriptwriter"
            },
            {
                "creatorType": "producer"
            },
            {
                "creatorType": "castMember"
            },
            {
                "creatorType": "contributor"
            }
        ]
    },
    {
        "itemType": "webpage",
        "fields": [
            {
                "field": "title"
            },
            {
                "field": "abstractNote"
            },
            {
                "field": "websiteTitle",
                "baseField": "publicationTitle"
            },
            {
                "field": "websiteType",
                "baseField": "type"
            },
            {
                "field": "date"
            },
            {
                "field": "shortTitle"
            },
            {
                "field": "url"
            },
            {
                "field": "accessDate"
            },
            {
                "field": "language"
            },
            {
                "field": "rights"
            },
            {
                "field": "extra"
            }
        ],
        "creatorTypes": [
            {
                "creatorType": "author",
                "primary": True
            },
            {
                "creatorType": "contributor"
            },
            {
                "creatorType": "translator"
            }
        ]
    }
]


ITEM_TYPES: dict[ZoteroItemTypeName, ItemType] = {}
for sch_item_type in SCHEMA_ITEM_TYPES:
    name = ZoteroItemTypeName(sch_item_type["itemType"])

    fields = [
        Field(
            name=ZoteroFieldName(sch_field["field"]),
            base_field=ZoteroFieldName(
                sch_field.get("baseField", sch_field["field"])
            )
        )
        for sch_field in sch_item_type["fields"]
    ]

    creator_types = [
        ZoteroCreatorTypeName(sch_creator_type["creatorType"])
        for sch_creator_type in sch_item_type["creatorTypes"]
    ]

    ITEM_TYPES[name] = ItemType(name, fields, creator_types)
