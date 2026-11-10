from arsenal.windows.inventar import Eveniment, Inventar, Proces


def test_proces_din_temp_e_suspect():
    proces = Proces(
        1,
        "x.exe",
        "ana",
        "C:\\Users\\ana\\AppData\\Local\\Temp\\x.exe",
    )
    assert proces.e_suspect() is True


def test_proces_din_windows_nu_e_suspect():
    proces = Proces(
        2,
        "svchost.exe",
        "SYSTEM",
        "C:\\Windows\\System32\\svchost.exe",
    )
    assert proces.e_suspect() is False


def test_eveniment_cu_id_suspect():
    eveniment = Eveniment(4625, "warning", "Security", "admin", "Logon failed")
    assert eveniment.e_suspect() is True


def test_eveniment_critical_este_suspect():
    eveniment = Eveniment(9999, "critical", "Security", "admin", "Critical event")
    assert eveniment.e_suspect() is True


def test_inventar_grupeaza_procesele_dupa_user():
    inventar = Inventar(
        [
            Proces(1, "a.exe", "ana", "C:\\Windows\\a.exe"),
            Proces(2, "b.exe", "ana", "C:\\Windows\\b.exe"),
            Proces(3, "c.exe", "SYSTEM", "C:\\Windows\\c.exe"),
        ]
    )
    assert len(inventar) == 3
    assert inventar.pe_user() == {
        "ana": ["a.exe", "b.exe"],
        "SYSTEM": ["c.exe"],
    }
