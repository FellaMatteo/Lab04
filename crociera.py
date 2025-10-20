class Cabina:
    def __init__(self, codice, numero_letti, ponte, prezzo_base, disponibilita=True):
        self._codice_cabina = str(codice)
        self._numero_letti = int(numero_letti)
        self._ponte = int(ponte)
        self._prezzo_base = float(prezzo_base)
        self._disponibilita = disponibilita

    def prezzo_finale(self):
        pass


class CabinaStandard(Cabina):
    def prezzo_finale(self):
        return self._prezzo_base

    def __str__(self):
        if self._disponibilita:
            stato = "Disponibile"
        else:
            stato = "Prenotata"

        return (f"{self._codice_cabina}: Standard | "
                f"{self._numero_letti} letti - Ponte {self._ponte} - "
                f"Prezzo {self.prezzo_finale():.2f}€ – {stato}")


class CabinaAnimali(Cabina):
    def __init__(self, codice, letti, ponte, prezzo_base, max_animali, disponibilita=True):
        super().__init__(codice, letti, ponte, prezzo_base, disponibilita)
        self._max_animali = int(max_animali)

    def prezzo_finale(self):
        return self._prezzo_base * (1 + 0.10 * self._max_animali)

    def __str__(self):
        stato = "Disponibile" if self._disponibilita else "Prenotata"
        return (f"{self._codice_cabina}: Animali | "
                f"{self._numero_letti} letti - Ponte {self._ponte} - "
                f"Prezzo {self.prezzo_finale():.2f}€ - "
                f"Max animali: {self._max_animali} – {stato}")


class CabinaDeluxe(Cabina):
    def __init__(self, codice, letti, ponte, prezzo_base, stile, disponibilita=True):
        super().__init__(codice, letti, ponte, prezzo_base, disponibilita)
        self._stile = stile

    def prezzo_finale(self):
        return self._prezzo_base * 1.20

    def __str__(self):
        stato = "Disponibile" if self._disponibilita else "Prenotata"
        return (f"{self._codice_cabina}: Deluxe | "
                f"{self._numero_letti} letti - Ponte {self._ponte} - "
                f"Prezzo {self.prezzo_finale():.2f}€ - "
                f"Stile: {self._stile} – {stato}")


class Passeggero:
    def __init__(self, codice, nome, cognome, documento, eta):
        self._codice = str(codice)
        self._nome = str(nome)
        self._cognome = str(cognome)
        self._documento = str(documento)
        self._eta = int(eta)
        self._cabina = None

    # Getter
    def get_nome(self):
        return self._nome

    def get_cognome(self):
        return self._cognome

    def get_eta(self):
        return self._eta

    def get_documento(self):
        return self._documento

    def get_cabina(self):
        return self._cabina

    # Metodo per prenotare una cabina
    def assegna_cabina(self, cabina):
        if cabina._disponibilita == True:
            self._cabina = cabina
            cabina._disponibilita = False
            return f"Cabina {cabina._codice_cabina} assegnata a {self._nome} {self._cognome}."
        else:
            return f"La cabina {cabina._codice_cabina} non è disponibile."

    # Rappresentazione in stringa
    def __str__(self):
        if self._cabina is not None:
            return (f"{self._codice}: {self._nome} {self._cognome}, "
                    f"{self._eta} anni – Documento: {self._documento} "
                    f"| Cabina: {self._cabina._codice_cabina}")
        else:
            return (f"{self._codice}: {self._nome} {self._cognome}, "
                    f"{self._eta} anni – Documento: {self._documento} "
                    f"| Nessuna cabina assegnata")


class Crociera:
    def __init__(self, nome, cabine=None, passeggeri=None):
        """Inizializza gli attributi e le strutture dati"""
        self._nome_crocera = nome
        self._cabine = cabine if cabine is not None else []
        self._passeggeri = passeggeri if passeggeri is not None else []

    """Aggiungere setter e getter se necessari"""

    @property
    def nome(self):
        return self._nome_crocera

    @nome.setter
    def nome(self, nuovo_nome):
        if not nuovo_nome or not nuovo_nome.strip():
            raise ValueError("Il nome della crociera non può essere vuoto")
        self._nome_crocera = nuovo_nome.strip()

    def carica_file_dati(self, file_path):
        """Carica i dati (cabine e passeggeri) dal file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for linea in file:
                    linea = linea.strip()
                    if not linea:
                        continue

                    campi = [campo.strip() for campo in linea.split(',')]

                    if campi[0].startswith('CAB'):
                        self._processa_cabina(campi)
                    elif campi[0].startswith('P'):
                        self._processa_passeggero(campi)

        except FileNotFoundError:
            raise FileNotFoundError(f"File non trovato: {file_path}")
        except Exception as e:
            raise Exception(f"Errore durante la lettura del file: {e}")

    def _processa_cabina(self, campi):
        """Processa una riga di cabina dal file"""
        codice = campi[0]
        num_letti = int(campi[1])
        ponte = int(campi[2])
        prezzo_base = float(campi[3])

        if len(campi) == 4:
            cabina = CabinaStandard(codice, num_letti, ponte, prezzo_base)
        elif len(campi) == 5:
            extra = campi[4]
            if extra.isdigit():
                cabina = CabinaAnimali(codice, num_letti, ponte, prezzo_base, extra)
            else:
                cabina = CabinaDeluxe(codice, num_letti, ponte, prezzo_base, extra)
        else:
            raise ValueError(f"Formato non valido per cabina: {campi}")

        self._cabine.append(cabina)

    def _processa_passeggero(self, campi):
        """Processa una riga di passeggero dal file"""
        if len(campi) < 3:
            raise ValueError(f"Formato non valido per passeggero: {campi}")

        codice = campi[0]
        nome = campi[1]
        cognome = campi[2]
        documento = campi[3] if len(campi) > 3 else "N/D"
        eta = int(campi[4]) if len(campi) > 4 else 0

        passeggero = Passeggero(codice, nome, cognome, documento, eta)
        self._passeggeri.append(passeggero)

    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        cabina = self._trova_cabina_per_codice(codice_cabina)
        passeggero = self._trova_passeggero_per_codice(codice_passeggero)

        if not cabina._disponibilita:
            raise ValueError(f"La cabina {codice_cabina} non è disponibile")

        if passeggero.get_cabina() is not None:
            raise ValueError(f"Il passeggero {codice_passeggero} è già assegnato a una cabina")

        passeggero.assegna_cabina(cabina)

    def _trova_cabina_per_codice(self, codice):
        """Trova una cabina per codice"""
        for cabina in self._cabine:
            if cabina._codice_cabina == codice:
                return cabina
        raise ValueError(f"Cabina non trovata: {codice}")

    def _trova_passeggero_per_codice(self, codice):
        """Trova un passeggero per codice"""
        for passeggero in self._passeggeri:
            if passeggero._codice == codice:
                return passeggero
        raise ValueError(f"Passeggero non trovato: {codice}")

    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        return sorted(self._cabine, key=lambda cabina: cabina.prezzo_finale())

    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """
        passeggeri_ordinati = sorted(self._passeggeri, key=lambda p: p._codice)
        for passeggero in passeggeri_ordinati:
            print(passeggero)