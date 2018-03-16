# Tietovisasovellus QuizBee

QuizBee on web-sovellus, jonka valitsin harjoitustyöni aiheeksi Tietokantasovellus -kurssilla keväällä 2018.

Sovelluksessa käyttäjät voivat luoda käyttäjätilin, tehdä omia tietovisakysymyksiä ja vastata muiden käyttäjien tekemiin kysymyksiin. Lisäksi käyttäjät voivat koota omista kysymyksistään visoja, jotka ovat avoinna määritellyn ajan ja joihin muut käyttäjät voivat sinä aikana osallistua. Kysymyksille ja visoille voidaan määritellä aihepiirit ja vaikeusasteet. Käyttäjät voivat myös generoida visoja automaattisesti tiettyyn aihepiiriin liittyvistä kysymyksistä, jolloin visan tekijä ei tiedä kysymyksiä etukäteen ja saa itsekin osallistua visaan.

Oikeista vastauksista ja voitoista kertyy käyttäjille pisteitä, ja lisäksi aktiiviset käyttäjät ansaitsevat kontribuutiopisteitä järjestelmään lisäämistään kysymyksistä ja visoista. Käyttäjät voivat tarkastella  omia pistetilastojaan, kuten kuinka moneen kysymykseen he ovat vastanneet ja mikä on oikeiden vastausten osuus. Sivustolla on myös näkyvillä High Score -listoja esim. kokonaispisteiltään, viikon pistesaldoltaan ja kontribuutiopisteiltään parhaiten menestyneistä käyttäjistä. 

Jotta järjestelmä pysyy asiallisena ja laadukkaana, käyttäjien on mahdollista ilmoittaa kysymyksiä asiattomiksi tai virheellisiksi. Ilmoitus perusteluineen menee kysymyksen tekijän ja ylläpitäjän tietoon, jolloin kysymyksiä voidaan tarvittaessa muokata tai poistaa. Järjestelmän ylläpitäjä voi tarvittaessa myös poistaa käyttäjätilin.

Toimintoja: 
* Kirjautuminen
* Kysymysten ja niihin liittyvien vastausvaihtoehtojen lisääminen, muokkaaminen ja poistaminen
* Kysymysten hakeminen aihepiirin ja vaikeusasteen perusteella
* Visojen koostaminen omista kysymyksistä
* Visojen koostaminen automaattisesti aihepiirin ja vaikeusasteen perusteella
* Muiden tekemiin kysymyksiin ja visoihin vastaaminen
* Pistesaldojen tarkastelu
* Asiattomien ja virheellisten kysymysten ilmoittaminen

Valmis sovellus täyttää (onnistuessaan) seuraavat arvostelukriteerit:
* Toimiva tietokantaa käyttävä web-sovellus
* Vähintään kolme tietokohdetta (tietokantataulua) ja liitostaulut (tauluja mm. käyttäjä, kysymys, visa, ilmoitus)
* Käyttäjät voivat kirjautua ja käyttäjä on yhdistetty tietokannassa johonkin tietokohteeseen (esim. kysymyksiin)
* Täysi CRUD (luonti, lukeminen, muokkaus, poisto) toteutuu vähintään kahdella tietokohteella (peruskäyttäjän osalta omat kysymykset ja visat)
* Ainakin yksi monesta-moneen suhde tietokantataulujen välillä (esim. kysymys-visa)
* Vähintään kaksi monimutkaisempaa useampaa tietokantataulua käyttävää yhteenvetokyselyä (High Score -listat voivat yhdistää tietoja käyttäjistä, käyttäjien pisteistä, visoista ja aihepiireistä joista pisteet on ansaittu jne.)
