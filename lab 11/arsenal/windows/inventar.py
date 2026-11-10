"""Inventar de procese Windows si analiza evenimentelor de securitate."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path


CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    """Descrie un proces extras dintr-o captura Windows."""

    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        """Intoarce True daca procesul ruleaza din Temp sau Roaming."""
        cale_normalizata = self.cale.casefold()
        return any(fragment.casefold() in cale_normalizata for fragment in CAI_SUSPECTE)


@dataclass
class Eveniment:
    """Descrie un eveniment din jurnalul Windows."""

    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        """Intoarce True pentru ID-uri relevante sau nivelul critical."""
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale):
    """Citeste procesele din JSON si le transforma in obiecte Proces."""
    with open(cale, encoding="utf-8") as f:
        return [Proces(**date) for date in json.load(f)]


def evenimente_din_json(cale):
    """Citeste evenimentele din JSON si le transforma in obiecte Eveniment."""
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**date) for date in json.load(f)]


@dataclass
class Inventar:
    """Container pentru procese, cu metode de cautare si grupare."""

    procese: list

    @classmethod
    def din_json(cls, cale):
        """Construieste un Inventar direct din fisierul JSON."""
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**date) for date in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        """Intoarce procesele pentru care e_suspect() este True."""
        return [proces for proces in self.procese if proces.e_suspect()]

    def pe_user(self):
        """Grupeaza numele proceselor intr-un dictionar organizat pe user."""
        grupuri = {}
        for proces in self.procese:
            grupuri.setdefault(proces.user, []).append(proces.nume)
        return grupuri


def main():
    """Afiseaza raportul de alarme sau il exporta in format JSON."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Inventar de procese si evenimente Windows din capturi JSON."
    )
    parser.add_argument(
        "capturi",
        help="Directorul care contine procese.json si evenimente.json",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Afiseaza raportul in format JSON",
    )
    args = parser.parse_args()

    director = Path(args.capturi)
    inventar = Inventar.din_json(director / "procese.json")
    evenimente = evenimente_din_json(director / "evenimente.json")
    procese_suspecte = inventar.suspecte()
    alarme = [eveniment for eveniment in evenimente if eveniment.e_suspect()]

    if args.json:
        raport = {
            "numar_procese": len(inventar),
            "procese_suspecte": [asdict(proces) for proces in procese_suspecte],
            "numar_evenimente": len(evenimente),
            "evenimente_alarma": [asdict(eveniment) for eveniment in alarme],
        }
        print(json.dumps(raport, ensure_ascii=False, indent=2))
        return

    print(f"Procese: {len(inventar)} | suspecte: {len(procese_suspecte)}")
    for proces in procese_suspecte:
        print(f"  [{proces.pid}] {proces.nume}  ({proces.user})  {proces.cale}")

    print(f"Evenimente: {len(evenimente)} | alarma: {len(alarme)}")
    for eveniment in alarme:
        print(
            f"  {eveniment.id} [{eveniment.nivel}] "
            f"{eveniment.cont}: {eveniment.mesaj}"
        )


if __name__ == "__main__":
    main()
