NoSQL Baze Podataka - Drugi Kolokvijum
Miloš Gojković - 2016270969

Program se sastoji iz dva modula, fill_database i find_streets. 

Pri pokretanju, prvo treba popuniti bazu podataka koja uključuje gradove i ulice. 
Za svaku ulicu, upisuje se niz lokacija čvorova za tu ulicu. 
Nakon popunjavanja baze podataka, treba pokrenuti modul find_streets, koji će upisati ulice 3km od zadate lokacije u .json fajl.

UPOTREBA:

1.) Obezbediti PyMongo paket preko PiP - a i MongoDB konekciju na portu 27017;
2.) Pokrenuti fill_database.py;
3.) Pokrenuti find_streets.py;
4.) Rezultat pronaći u streetsWithinRadius.json fajlu.