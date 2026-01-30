# 1. Mitä tekoäly teki hyvin?
Tekoäly teki projektin aloituksesta helppoa ja nopeaa.

**Nopea alustus:**Se loi toimivan FastAPI rungon, Pydantic-mallit ja CRUD-operaatiot, mitkä nopeuttivat peruskoodin kirjoittamista.

**Refaktoroinnin tekninen toteutus:** Pyysin tekoälyä jakamaan yksittäisen tiedoston (main.py) moduuleihin (schemas.py, database.py ja main.py), missä se onnistui teknisesti oikein, vaikka hukkasikin kontekstin.

**Syntaksi:** Tekoälyn tuottama koodi oli syntaksisesti oikein ja hyödynsi oikeita kirjastoja (kuten 'uuid' ja 'typing').


# 2. Mitä tekoäly teki huonosti?
Nopealla katselmuksella ja testaamisella koodi näytti toimivalta, mutta siinä oli suhteellisen vakavia loogisia ja arkkitehtuurisia puutteita, joista olisi tuotannossa seurannut virheitä.

**Kontekstin kadottaminen:** Pyydettäessäni tekoälyä refaktoroimaan koodin, se hukkasi alkuperäisen liiketoimintalogiikan ja muutti sovelluksen hotellivarausjärjestelmäksi. Tämä vaati pientä puuttumista ja logiikan palauttamista.

**Race Condition -riski:** Tekoäly teki päällekkäisyystarkistuksen ('check_overlap'), mutta se melko vajaavainen. Tämä funktio luki tietokannan tilan ja kirjoitti uuden varauksen erillisinä operaatioina, mikä jätti aikaikkunan päällekkäisille varauksille samanaikaisessa kuormituksessa.

**Puutteellinen validointi ja aikakäsittely:** Alunperin koodi salli varauksen alkamisen menneisyydessä jos loppuaika oli tulevaisuudessa. Tämän lisäksi tekoäly käytti 'datetime.now()' ilman aikavyöhykettä, mikä on riskialtista palvelinympäristössä.


# 3. Tärkeimmät parannukset ja perustelut
Seuraavat kriittiset muutokset on tehty varmistaakseni sovelluksen laadun, turvallisuuden ja ylläpidettävyyden:

## 1. Thread Safety

**Muutos:** Huomasin TOCTOU -riskin, minkä takia lisäsin 'database.py' -tiedostoon lukitusmekanismin ja yhdistin tarkistus- ja tallennuslogiikan atomiseksi operaatioksi.
**Syy:** Ilman tätä lukitusta, kaksi eri käyttäjää pystyisi varaamaan saman huoneen tismalleen samalla hetkellä. Varmistin tämän toiminnallisuuden luomalla erillisen kuormitustestin (tests/test_concurrency.py).

## 2. Validointi ja UTC-aikavyöhykkeet

**Muutos:** Tein muutoksia 'schema.py' :n validaattoreihin, jotta ne käyttäisivät 'datetime.now(timezone.utc) ja lisäsin puuttuvan tarkistuksen, joka katsoo onko varauksen aloitusaika menneisyydessä ja estää sen.
**Syy:** Yleensä palvelimet pyörivät UTC-ajassa, kun taas käyttäjät ovat paikallisajassa. Aikavyöhykkeetön vertailu johtaa ongelmiin ja tiukempi validointi parantaa datan eheyttä.

## 3. Projektirakennus ja testaus

**Muutos:** Siirsin testit erilliseen hakemistoon ja loin testitapaukset logiikalle ('test_api.py') ja kuormitukselle ('test_concurrency.py').
**Syy:** Selkeä rakenne helpottaa ylläpitoa. Automatisoidut testit helpottavat testaamista ja auttoivat tekoälyn jättämien aukkojen todennukseen ja korjaamiseen.
