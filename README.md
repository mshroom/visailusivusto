# Tietovisasovellus QuizBee

QuizBee on web-sovellus, jonka valitsin harjoitustyöni aiheeksi Tietokantasovellus -kurssilla keväällä 2018.

- [Linkki sovellukseen Herokussa.](https://quizbee-demo.herokuapp.com/) Sovellusta voi kokeilla seuraavilla testikäyttäjän tunnuksilla:
  - tavallinen käyttäjä: käyttäjätunnus __hello__, salasana __world__.
  - admin: käyttäjätunnus __testadmin__, salasana __testadmin__.
  - __Huom! Kun QuizBee käynnistyy, Heroku saattaa aluksi muutaman kerran näyttää sivun "Internal server error". Näin voi käydä esimerkiksi sisään kirjautuessa. Ongelma korjaantuu päivittämällä sivu uudestaan yhden tai useamman kerran.__

- [Sovelluksen user storyt](https://github.com/mshroom/visailusivusto/blob/master/documentation/userstories.md)

- [Tietokantakaavio](https://github.com/mshroom/visailusivusto/blob/master/documentation/database_diagram.png)

- [CREATE TABLE -lauseet](https://github.com/mshroom/visailusivusto/blob/master/documentation/create_table_statements.md)

- [Käyttö- ja asennusohje](https://github.com/mshroom/visailusivusto/blob/master/documentation/usersguide.md)

## Sovelluksen kuvaus

Sovelluksessa käyttäjät voivat luoda käyttäjätilin, tehdä omia tietovisakysymyksiä ja vastata muiden käyttäjien tekemiin kysymyksiin. Kysymyksille voidaan määritellä aihepiirit ja vaikeusasteet. Lisäksi käyttäjät voivat koota omista kysymyksistään visoja, joihin muut käyttäjät voivat osallistua.  Käyttäjät voivat myös generoida visoja automaattisesti tiettyyn aihepiiriin liittyvistä kysymyksistä, jolloin visan tekijä ei tiedä kysymyksiä etukäteen ja saa itsekin osallistua visaan.

Oikeista vastauksista kertyy käyttäjille pisteitä, ja lisäksi aktiiviset käyttäjät ansaitsevat kontribuutiopisteitä järjestelmään lisäämistään kysymyksistä ja visoista. Käyttäjät voivat tarkastella  omia pistetilastojaan, kuten kuinka moneen kysymykseen he ovat vastanneet ja mikä on oikeiden vastausten osuus. Sivustolla on myös näkyvillä High Score -listoja esim. viikon pistesaldoltaan ja aktiivisuudeltaan parhaiten menestyneistä käyttäjistä. 

Jotta järjestelmä pysyy asiallisena ja laadukkaana, käyttäjien on mahdollista ilmoittaa kysymyksiä asiattomiksi tai virheellisiksi. Ilmoitus perusteluineen menee kysymyksen tekijän ja ylläpitäjän tietoon, jolloin kysymyksiä voidaan tarvittaessa muokata tai poistaa. Järjestelmän ylläpitäjä voi tarvittaessa myös poistaa käyttäjätilin.

### Toimintoja
* Kirjautuminen
* Kysymysten ja niihin liittyvien vastausvaihtoehtojen lisääminen, muokkaaminen ja poistaminen
* Kysymysten arpominen aihepiirin perusteella
* Visojen koostaminen omista kysymyksistä
* Visojen koostaminen automaattisesti aihepiirin perusteella
* Muiden tekemiin kysymyksiin ja visoihin vastaaminen
* Pistesaldojen tarkastelu
* Asiattomien ja virheellisten kysymysten ilmoittaminen

### Valmis sovellus täyttää seuraavat arvostelukriteerit:
* Toimiva tietokantaa käyttävä web-sovellus
* Vähintään kolme tietokohdetta (tietokantataulua) ja liitostaulut (tauluja mm. käyttäjä, kysymys, visa, ilmoitus)
* Käyttäjät voivat kirjautua ja käyttäjä on yhdistetty tietokannassa johonkin tietokohteeseen (esim. kysymyksiin)
* Täysi CRUD (luonti, lukeminen, muokkaus, poisto) toteutuu vähintään kahdella tietokohteella (peruskäyttäjän osalta omat kysymykset ja visat)
* Ainakin yksi monesta-moneen suhde tietokantataulujen välillä (esim. kysymys-visa)
* Vähintään kaksi monimutkaisempaa useampaa tietokantataulua käyttävää yhteenvetokyselyä (High Score -listat voivat yhdistää tietoja käyttäjistä, käyttäjien pisteistä, visoista ja aihepiireistä joista pisteet on ansaittu jne.)

## Puutteet ja kehitysideat

* Sovelluksen visuaalista ilmettä voisi kohentaa
* Sovelluksen toimintaa olisi helpompi tarkastella jos sinne lisäisi vielä enemmän dataa
* Automaattinen visojen luominen onnistuu tällä hetkellä vain joko kaikista kysymyksistä tai aihepiirin perusteella. Vaikeusasteen voisi vielä lisätä valintakriteeriksi.
* Käyttäjien saavutuksia ja pisteitä voisi vielä eritellä tarkemmin. Esim. oikeista vastauksista voisi saada pisteitä sen mukaan, kuinka vaikeita kysymykset ovat. Pisteiden laskeminen onnistuisi tässäkin tapauksessa yksinkertaisesti SQL-kyselyllä, joka laskee kuinka monta oikeaa vastausta käyttäjällä on kussakin vaikeuskategoriassa.
* High Score -listauksia voi lisätä enemmän, esim. aihepiirin mukaan, visoittain jne.
* Tällä hetkellä kun tietokannasta esimerkiksi poistaa kysymyksiä, myös kaikki niihin liittyvät vastaukset poistetaan eivätkä ne enää näy vastaajien tilastoissa. Jos käyttäjien vastauspisteet halutaan säilyttää dataa poistettaessa, voisi pisteet tallentaa erilliseen tauluun.
* Ilmoitusten käsittelyä voisi sujuvoittaa lisäämällä joitain toimintoja. Esim. käyttäjä voisi merkitä saamansa ilmoituksen hoidetuksi, jolloin järjestelmän ylläpitäjä voisi helposti tarkastella, mihin ilmoituksiin on reagoitu ja mihin ei. Ilmoituksen saanut käyttäjä voisi myös kirjoittaa vastauksen, jos ilmoitus ei hänen mielestään olisi relevantti.
