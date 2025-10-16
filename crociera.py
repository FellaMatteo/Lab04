class Crociera:
    def __init__(self, nome, cabine, passeggeri):
        """Inizializza gli attributi e le strutture dati"""
        # TODO
        self._nome_crocera = nome
        self._cabine = cabine
        self._passeggeri = passeggeri

    """Aggiungere setter e getter se necessari"""
    # TODO

    def carica_file_dati(self, file_path):
        """Carica i dati (cabine e passeggeri) dal file"""
        # TODO

    def assegna_passeggero_a_cabina(self, codice_cabina, codice_passeggero):
        """Associa una cabina a un passeggero"""
        # TODO

    def cabine_ordinate_per_prezzo(self):
        """Restituisce la lista ordinata delle cabine in base al prezzo"""
        # TODO


    def elenca_passeggeri(self):
        """Stampa l'elenco dei passeggeri mostrando, per ognuno, la cabina a cui è associato, quando applicabile """
        # TODO

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

