# IL BOT (E RISBOT)

- Piattaforma python

- Estrazione Fatti via LLM pubblico **(OK CIRCA)**
  - Selezionare LLM da [groq](https://groq.com/)
	- Lista fatti da [CrossJustice](https://github.com/LegalMachineLab/CrossJustice/blob/main/docs/facts.md)
	- **Task 1**: LLM conversa con l'utente e seleziona dalla lista di fatti quelli che pensa essere rilevanti per il caso
	  - Dare un recap all'utente di quel che ho capito del suo caso

- Interrogazione **CrossJustice** **(OK CIRCA)**
	- **INPUT**: lista fatti
	- **TARGET**: direttive
	- Come farlo (https://github.com/LegalMachineLab/CrossJustice/blob/main/crossjustice/python/pl_wrapper.py)
	- **OUTPUT**: lista diritti

- Domanda: *ho gli stessi diritti nel mio paese?*
	- Interrogazione **CrossJustice** base nazionale
	- Uso argomentazione per identificare la non conformità
		- Ho il diritto
		- Assenza del diritto
		- Presenza ma con requisiti differenti
		- Manca di identificare eventuali diritti nazionali che non sono dati dai fatti in kb
			- Task 2: LLM estrae da codice / transposition tables / a manina

- LLM spiega i problemi e capisce con l'utente se è risolvibile
	- introdurre nuovi fatti
  - revisionarne di vecchi
	- ...
