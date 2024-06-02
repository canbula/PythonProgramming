create table item
(
    type text not null,
    field_data text not null,
    creators text not null
);

create table collection
(
    name text not null
        constraint collection_pkey
            primary key
);

create table collection_entry
(
    collection integer
        not null
        constraint collection_entry_collection_id_fkey
            references collection (rowid)
            on delete cascade,
    item integer
        not null
        constraint collection_entry_entry_id_fkey
            references item (rowid)
            on delete cascade
);
