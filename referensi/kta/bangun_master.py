"""Bangun master_nomor_kta.json dari Master_Nomor_KTA_Internal.xlsx dan berkas tambahan_nomor_kta_*.txt di folder ini.
Jalankan: python referensi/kta/bangun_master.py  (lalu nyalakan ulang server)."""
import json, re
from collections import Counter
from pathlib import Path
from openpyxl import load_workbook
D = Path(__file__).resolve().parent
wb = load_workbook(D / 'Master_Nomor_KTA_Internal.xlsx')
M = [r for r in wb['KTA Master'].iter_rows(min_row=2, values_only=True) if r[5] == 'Ketua']
P = [r for r in wb['PAC Terdata'].iter_rows(min_row=2, values_only=True) if r[6] == 'Ketua']
def kartu(tingkat, nama, prov):
    if tingkat == 'DPW': return prov
    if nama.startswith(('Kabupaten ', 'Kota ')): return nama
    return {'DPD': 'Kabupaten ', 'DPC': 'Kota '}.get(tingkat, '') + nama
def judul(s):  # RIAU -> Riau, DI YOGYAKARTA -> DI Yogyakarta
    return ' '.join(w if w == 'DI' else w.capitalize() for w in s.split())
items = []
for prov, pp, tingkat, nama, kode, _, _, status in M:
    if 'abaikan' in nama: continue                       # Kepahiang 04.010 duplikat dari 04.003
    if kode == '04.001': tingkat = 'DPC'                 # Kota Bengkulu adalah kota
    if kode == '16.038': tingkat = 'DPD'                 # Banyuwangi adalah kabupaten
    items.append(dict(kode=kode, pp=pp, provinsi=prov, tingkat=tingkat, nama=nama, kartu=kartu(tingkat, nama, prov), induk='', status=status or ''))
for kec in P:                                            # Slawi: 'Kabupaten Tegal' di sheet PAC = Tegal 14.026
    prov, pp, _, kdpd, nama, kode, _, _, status = kec
    items.append(dict(kode=kode, pp=pp, provinsi=prov, tingkat='PAC', nama=nama, kartu=nama, induk=kdpd, status=status or ''))
for f in sorted(D.glob('tambahan_nomor_kta_*.txt')):
    prov = {}
    for line in f.read_text(encoding='utf-8').splitlines():
        m = re.fullmatch(r'\s*(\d{2})(?:\.(\d{3}))?\s*-\s*(.+?)\s*', line)
        if not m: continue
        pp, no, teks = m[1], m[2], m[3]
        if no is None: prov[pp] = judul(teks); continue
        if no == '000': tingkat, nama = 'DPW', 'DPW ' + prov[pp]
        elif teks.startswith('KABUPATEN '): tingkat, nama = 'DPD', judul(teks)
        elif teks.startswith('KOTA '): tingkat, nama = 'DPC', judul(teks)
        else: raise SystemExit(f'{f.name}: tidak jelas kabupaten/kota: {line}')
        items.append(dict(kode=f'{pp}.{no}', pp=pp, provinsi=prov[pp], tingkat=tingkat, nama=nama, kartu=kartu(tingkat, nama, prov[pp]), induk='', status=f'Tambahan {f.stem[-8:]}'))
dup = [k for k, n in Counter(x['kode'] for x in items).items() if n > 1]
if dup: raise SystemExit(f'Kode ganda: {dup}')
assert all(x['induk'] in {y['kode'] for y in items} for x in items if x['induk'])
items.sort(key=lambda x: x['kode'])
(D / 'master_nomor_kta.json').write_text(json.dumps({'sumber': 'Master_Nomor_KTA_Internal.xlsx + tambahan_nomor_kta_*.txt', 'wilayah': items}, ensure_ascii=False, indent=0), encoding='utf-8')
print(len(items), dict(Counter(x['tingkat'] for x in items)), 'provinsi:', len({x['pp'] for x in items}))
