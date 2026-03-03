
| KundenNr | Name    | Tel | Ausleihdatum | Kennzeichen | Hersteller | km-Stand | Baujahr |
| -------- | ------- | --- | ------------ | ----------- | ---------- | -------- | ------- |
| 1234     | Meier   | …   | 28.05.23     | BI-CS-123   | VW         | 20013    | 2021    |
| 1234     | Meier   | …   | 30.05.23     | BI-CS-124   | BMW        | 4021     | 2023    |
| 1235     | Neumann | …   | 01.06.23     | BI-CS-123   | VW         | 20269    | 2021    |
| …        |         |     |              |             |            |          |         |
a) Nachteil bei der Speicherung der Daten in Einer Tabelle
- Der Kundenname „Meier“ taucht hier zweimal 
- Das Kennzeichen und der Hersteller tauchen hier bereits zweimal auf 
- es fehlt die Aufteilung der Daten nach Themengebiete
- Wenn ein neues Auto hinzu kommt, müsste ein Dummy Kunde angelegtbwerde, dann könnte das Auto nicht mit aufgenommen werden. d.h. Änderungsanomalie, Löschanomalie, Einfügeanomalie

funktionale Abhängigkeiten:
- ***KundenNr*** -> Name, Tel
- ***Kennzeichen*** -> Hersteller, Baujahr
voll funktionale Abhängigkeiten:
(KundenNr, Ausleihdatum -> km-Stand)


Kunde

| KundenNr |     |
| -------- | --- |
| Name     |     |
| Tel      |     |
Auto

| Kennzeichen |     |
| ----------- | --- |
| Hersteller  |     |
| Baujahr     |     |
KundeAuto

| Kundennummer |     |
| ------------ | --- |
| Ausleihdatum |     |
| km-stand     |     |
| Kennzeichen  |     |
Es wird redundant gespeichert, dass das Fachgebiet Datenbank- und Informationssysteme dem Institut für Informatik angehört.
Mehrere Tabellen Notwendig, weil:
Mitarbeiter_id -> Fachgebiet -> Institut
