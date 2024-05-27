from enum import Enum
from typing import NewType, Literal, TypeAlias, Union

CslName = NewType("CslName", str)
ZoteroName = NewType("ZoteroName", str)
HumanName = NewType("HumanName", str)

CslFieldName = NewType("CslFieldName", Union[CslName, str])
ZoteroFieldName = NewType("ZoteroFieldName", Union[ZoteroName, str])
HumanFieldName = NewType("HumanFieldName", Union[HumanName, str])

CslItemTypeName = NewType("CslItemTypeName", Union[CslName, str])
ZoteroItemTypeName = NewType("ZoteroItemTypeName", Union[ZoteroName, str])
HumanItemTypeName = NewType("HumanItemTypeName", Union[HumanName, str])

CslCreatorTypeName = NewType("CslCreatorTypeName", Union[CslName, str])
ZoteroCreatorTypeName = NewType("ZoteroCreatorTypeName", Union[ZoteroName, str])
HumanCreatorTypeName = NewType("HumanCreatorTypeName", Union[HumanName, str])

# region Translation maps between Zotero, CSL and human-readable names
ITEM_TYPE_CSL_ZOTERO: dict[CslItemTypeName, list[ZoteroItemTypeName]] = {
    "article": [
        "preprint"
    ],
    "article-journal": [
        "journalArticle"
    ],
    "article-magazine": [
        "magazineArticle"
    ],
    "article-newspaper": [
        "newspaperArticle"
    ],
    "bill": [
        "bill"
    ],
    "book": [
        "book"
    ],
    "broadcast": [
        "podcast",
        "tvBroadcast",
        "radioBroadcast"
    ],
    "chapter": [
        "bookSection"
    ],
    "dataset": [
        "dataset"
    ],
    "document": [
        "document",
        "attachment",
        "note"
    ],
    "entry-dictionary": [
        "dictionaryEntry"
    ],
    "entry-encyclopedia": [
        "encyclopediaArticle"
    ],
    "graphic": [
        "artwork"
    ],
    "hearing": [
        "hearing"
    ],
    "interview": [
        "interview"
    ],
    "legal_case": [
        "case"
    ],
    "legislation": [
        "statute"
    ],
    "manuscript": [
        "manuscript"
    ],
    "map": [
        "map"
    ],
    "motion_picture": [
        "film",
        "videoRecording"
    ],
    "paper-conference": [
        "conferencePaper"
    ],
    "patent": [
        "patent"
    ],
    "personal_communication": [
        "letter",
        "email",
        "instantMessage"
    ],
    "post": [
        "forumPost"
    ],
    "post-weblog": [
        "blogPost"
    ],
    "report": [
        "report"
    ],
    "software": [
        "computerProgram"
    ],
    "song": [
        "audioRecording"
    ],
    "speech": [
        "presentation"
    ],
    "standard": [
        "standard"
    ],
    "thesis": [
        "thesis"
    ],
    "webpage": [
        "webpage"
    ]
}

ITEM_TYPE_ZOTERO_CSL: dict[ZoteroItemTypeName, CslItemTypeName] = {}
for csl_name, zotero_names in ITEM_TYPE_CSL_ZOTERO.items():
    for zotero_name in zotero_names:
        ITEM_TYPE_ZOTERO_CSL[zotero_name] = csl_name

ITEM_TYPE_NAMES: dict[ZoteroItemTypeName, HumanItemTypeName] = {
    "annotation": "Annotation",
    "artwork": "Artwork",
    "attachment": "Attachment",
    "audioRecording": "Audio Recording",
    "bill": "Bill",
    "blogPost": "Blog Post",
    "book": "Book",
    "bookSection": "Book Section",
    "case": "Case",
    "computerProgram": "Software",
    "conferencePaper": "Conference Paper",
    "dataset": "Dataset",
    "dictionaryEntry": "Dictionary Entry",
    "document": "Document",
    "email": "E-mail",
    "encyclopediaArticle": "Encyclopedia Article",
    "film": "Film",
    "forumPost": "Forum Post",
    "hearing": "Hearing",
    "instantMessage": "Instant Message",
    "interview": "Interview",
    "journalArticle": "Journal Article",
    "letter": "Letter",
    "magazineArticle": "Magazine Article",
    "manuscript": "Manuscript",
    "map": "Map",
    "newspaperArticle": "Newspaper Article",
    "note": "Note",
    "patent": "Patent",
    "podcast": "Podcast",
    "preprint": "Preprint",
    "presentation": "Presentation",
    "radioBroadcast": "Radio Broadcast",
    "report": "Report",
    "standard": "Standard",
    "statute": "Statute",
    "thesis": "Thesis",
    "tvBroadcast": "TV Broadcast",
    "videoRecording": "Video Recording",
    "webpage": "Web Page",
}

FIELD_CSL_ZOTERO: dict[CslFieldName, list[ZoteroFieldName]] = {
    "abstract": [
        "abstractNote"
    ],
    "archive": [
        "archive"
    ],
    "archive_location": [
        "archiveLocation"
    ],
    "authority": [
        "authority"
    ],
    "call-number": [
        "callNumber",
        "applicationNumber"
    ],
    "chapter-number": [
        "session"
    ],
    "collection-number": [
        "seriesNumber"
    ],
    "collection-title": [
        "seriesTitle",
        "series"
    ],
    "container-title": [
        "publicationTitle",
        "reporter",
        "code"
    ],
    "dimensions": [
        "artworkSize",
        "runningTime"
    ],
    "DOI": [
        "DOI"
    ],
    "edition": [
        "edition"
    ],
    "event-place": [
        "place"
    ],
    "event-title": [
        "meetingName",
        "conferenceName"
    ],
    "genre": [
        "type",
        "programmingLanguage"
    ],
    "ISBN": [
        "ISBN"
    ],
    "ISSN": [
        "ISSN"
    ],
    "issue": [
        "issue",
        "priorityNumbers"
    ],
    "journalAbbreviation": [
        "journalAbbreviation"
    ],
    "language": [
        "language"
    ],
    "license": [
        "rights"
    ],
    "medium": [
        "medium",
        "system"
    ],
    "note": [
        "extra"
    ],
    "number": [
        "number"
    ],
    "number-of-pages": [
        "numPages"
    ],
    "number-of-volumes": [
        "numberOfVolumes"
    ],
    "page": [
        "pages"
    ],
    "publisher": [
        "publisher"
    ],
    "publisher-place": [
        "place"
    ],
    "references": [
        "history",
        "references"
    ],
    "scale": [
        "scale"
    ],
    "section": [
        "section",
        "committee"
    ],
    "shortTitle": [
        "shortTitle"
    ],
    "source": [
        "libraryCatalog"
    ],
    "status": [
        "status"
    ],
    "title": [
        "title"
    ],
    "title-short": [
        "shortTitle"
    ],
    "URL": [
        "url"
    ],
    "version": [
        "versionNumber"
    ],
    "volume": [
        "volume",
        "codeNumber"
    ],
    "accessed": ["accessDate"],
    "issued": ["date"],
    "submitted": ["filingDate"],
}

FIELD_ZOTERO_CSL: dict[ZoteroFieldName, CslFieldName] = {}
for csl_name, zotero_names in FIELD_CSL_ZOTERO.items():
    for zotero_name in zotero_names:
        FIELD_ZOTERO_CSL[zotero_name] = csl_name

FIELD_NAMES: dict[ZoteroFieldName, HumanFieldName] = {
    "abstractNote": "Abstract",
    "accessDate": "Accessed",
    "applicationNumber": "Application Number",
    "archive": "Archive",
    "archiveID": "Archive ID",
    "archiveLocation": "Loc. in Archive",
    "artworkMedium": "Medium",
    "artworkSize": "Artwork Size",
    "assignee": "Assignee",
    "audioFileType": "File Type",
    "audioRecordingFormat": "Format",
    "authority": "Authority",
    "billNumber": "Bill Number",
    "blogTitle": "Blog Title",
    "bookTitle": "Book Title",
    "callNumber": "Call Number",
    "caseName": "Case Name",
    "citationKey": "Citation Key",
    "code": "Code",
    "codeNumber": "Code Number",
    "codePages": "Code Pages",
    "codeVolume": "Code Volume",
    "committee": "Committee",
    "company": "Company",
    "conferenceName": "Conference Name",
    "country": "Country",
    "court": "Court",
    "date": "Date",
    "dateAdded": "Date Added",
    "dateDecided": "Date Decided",
    "dateEnacted": "Date Enacted",
    "dateModified": "Modified",
    "dictionaryTitle": "Dictionary Title",
    "distributor": "Distributor",
    "docketNumber": "Docket Number",
    "documentNumber": "Document Number",
    "DOI": "DOI",
    "edition": "Edition",
    "encyclopediaTitle": "Encyclopedia Title",
    "episodeNumber": "Episode Number",
    "extra": "Extra",
    "filingDate": "Filing Date",
    "firstPage": "First Page",
    "format": "Format",
    "forumTitle": "Forum/Listserv Title",
    "genre": "Genre",
    "history": "History",
    "identifier": "Identifier",
    "institution": "Institution",
    "interviewMedium": "Medium",
    "ISBN": "ISBN",
    "ISSN": "ISSN",
    "issue": "Issue",
    "issueDate": "Issue Date",
    "issuingAuthority": "Issuing Authority",
    "itemType": "Item Type",
    "journalAbbreviation": "Journal Abbr",
    "label": "Label",
    "language": "Language",
    "legalStatus": "Legal Status",
    "legislativeBody": "Legislative Body",
    "letterType": "Type",
    "libraryCatalog": "Library Catalogue",
    "manuscriptType": "Type",
    "mapType": "Type",
    "medium": "Medium",
    "meetingName": "Meeting Name",
    "nameOfAct": "Name of Act",
    "network": "Network",
    "number": "Number",
    "numberOfVolumes": "# of Volumes",
    "numPages": "# of Pages",
    "organization": "Organization",
    "pages": "Pages",
    "patentNumber": "Patent Number",
    "place": "Place",
    "postType": "Post Type",
    "presentationType": "Type",
    "priorityNumbers": "Priority Numbers",
    "proceedingsTitle": "Proceedings Title",
    "programmingLanguage": "Prog. Language",
    "programTitle": "Program Title",
    "publicationTitle": "Publication",
    "publicLawNumber": "Public Law Number",
    "publisher": "Publisher",
    "references": "References",
    "reporter": "Reporter",
    "reporterVolume": "Reporter Volume",
    "reportNumber": "Report Number",
    "reportType": "Report Type",
    "repository": "Repository",
    "repositoryLocation": "Repo. Location",
    "rights": "Rights",
    "runningTime": "Running Time",
    "scale": "Scale",
    "section": "Section",
    "series": "Series",
    "seriesNumber": "Series Number",
    "seriesText": "Series Text",
    "seriesTitle": "Series Title",
    "session": "Session",
    "shortTitle": "Short Title",
    "status": "Status",
    "studio": "Studio",
    "subject": "Subject",
    "system": "System",
    "thesisType": "Type",
    "title": "Title",
    "type": "Type",
    "university": "University",
    "url": "URL",
    "versionNumber": "Version",
    "videoRecordingFormat": "Format",
    "volume": "Volume",
    "websiteTitle": "Website Title",
    "websiteType": "Website Type"
}

CREATOR_CSL_ZOTERO: dict[CslCreatorTypeName, ZoteroCreatorTypeName] = {
    "author": "author",
    "bookAuthor": "container-author",
    "castMember": "performer",
    "composer": "composer",
    "contributor": "contributor",
    "director": "director",
    "editor": "editor",
    "guest": "guest",
    "interviewer": "interviewer",
    "producer": "producer",
    "recipient": "recipient",
    "reviewedAuthor": "reviewed-author",
    "seriesEditor": "collection-editor",
    "scriptwriter": "script-writer",
    "translator": "translator"
}

CREATOR_ZOTERO_CSL: dict[ZoteroCreatorTypeName, CslCreatorTypeName] = {
    v: k for k, v in CREATOR_CSL_ZOTERO.items()
}

CREATOR_TYPE_NAMES: dict[ZoteroCreatorTypeName, HumanCreatorTypeName] = {
    "artist": "Artist",
    "attorneyAgent": "Attorney/Agent",
    "author": "Author",
    "bookAuthor": "Book Author",
    "cartographer": "Cartographer",
    "castMember": "Cast Member",
    "commenter": "Commenter",
    "composer": "Composer",
    "contributor": "Contributor",
    "cosponsor": "Cosponsor",
    "counsel": "Counsel",
    "director": "Director",
    "editor": "Editor",
    "guest": "Guest",
    "interviewee": "Interview With",
    "interviewer": "Interviewer",
    "inventor": "Inventor",
    "performer": "Performer",
    "podcaster": "Podcaster",
    "presenter": "Presenter",
    "producer": "Producer",
    "programmer": "Programmer",
    "recipient": "Recipient",
    "reviewedAuthor": "Reviewed Author",
    "scriptwriter": "Scriptwriter",
    "seriesEditor": "Series Editor",
    "sponsor": "Sponsor",
    "translator": "Translator",
    "wordsBy": "Words By"
}
# endregion


DataFormat: TypeAlias = Literal["csl", "zotero", "human"]
DataType: TypeAlias = Literal["item_type", "field", "creator_type"]


def zotero_item_type_to(name: ZoteroItemTypeName, to: DataFormat) -> str:
    if to == "csl":
        return ITEM_TYPE_ZOTERO_CSL[name]
    elif to == "human":
        return ITEM_TYPE_NAMES[name]


def zotero_field_to(name: ZoteroFieldName, to: DataFormat) -> str:
    if to == "csl":
        return FIELD_ZOTERO_CSL[name]
    elif to == "human":
        return FIELD_NAMES[name]


def zotero_creator_type_to(name: ZoteroCreatorTypeName, to: DataFormat) -> str:
    if to == "csl":
        return CREATOR_ZOTERO_CSL[name]
    elif to == "human":
        return CREATOR_TYPE_NAMES[name]


def is_field_date(name: ZoteroFieldName) -> bool:
    if name not in FIELD_ZOTERO_CSL:
        return False
    return FIELD_ZOTERO_CSL[name] in [
        "accessed",
        "issued",
        "submitted",
    ]


def is_field_name(name: ZoteroFieldName) -> bool:
    if name not in FIELD_ZOTERO_CSL:
        return False
    return FIELD_ZOTERO_CSL[name] in [
        "author",
        "collection-editor",
        "composer",
        "container-author",
        "contributor",
        "director",
        "editor",
        "guest",
        "interviewer",
        "performer",
        "producer",
        "recipient",
        "reviewed-author",
        "script-writer",
        "translator",
    ]


def is_field_standard(name: ZoteroFieldName) -> bool:
    return not is_field_name(name) and not is_field_date(name)


class FieldType(Enum):
    STANDARD = "standard"
    DATE = "date"
    NAME = "name"


def get_field_type(name: ZoteroFieldName) -> FieldType:
    if is_field_date(name):
        return FieldType.DATE
    elif is_field_name(name):
        return FieldType.NAME
    elif is_field_standard(name):
        return FieldType.STANDARD
    else:
        raise ValueError(f"Unknown field type for Zotero field {name}")


FIELD_TYPES: dict[ZoteroFieldName, FieldType] = {
    f: get_field_type(f)
    for f in FIELD_ZOTERO_CSL.keys()
}
