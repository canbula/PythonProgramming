def remove_duplicates(seq):
    sonuc = []
    for oge in seq:
        if oge not in sonuc:
            sonuc.append(oge)
    return sonuc


def list_counts(seq):
    sayimlar = {}
    for oge in seq:
        sayimlar[oge] = sayimlar.get(oge, 0) + 1
    return sayimlar


def reverse_dict(d):
    ters = {}
    for anahtar, deger in d.items():
        if deger not in ters:
            ters[deger] = [anahtar]
        else:
            ters[deger].append(anahtar)
    return ters
