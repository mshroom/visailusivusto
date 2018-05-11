# Käyttöohje

Sovellus on toiminnassa [Herokussa](https://quizbee-demo.herokuapp.com). Voit myös halutessasi asentaa sen
omalle koneellesi ja käyttää paikallisen palvelimen kautta. Sovellus toimii tällöin samalla tavalla,
mutta kaikki tieto tallentuu vain omalle koneellesi.

## Sovelluksen asentaminen omalle koneelle

QuizBee -sovellus on mahdollista asentaa omalle koneelle ja käyttää paikallisen palvelimen kautta, 
mikäli käytössäsi on Linux-käyttöjärjestelmä sekä
- Tuki Python-kielisten ohjelmien suorittamiseen, [asenna Python](https://www.python.org/downloads/)
- Pythonin [pip](https://packaging.python.org/key_projects/#pip), jonka pitäisi asentua automaattisesti
edellä annetun linkin takaa löytyvistä Python-versioista
- Pythonin [venv](https://docs.python.org/3/library/venv.html), jonka pitäisi myös asentua automaattisesti

Asennus tapahtuu seuraavasti:

1. Lataa projekti zip-tiedostona itsellesi.
2. Pura zip-tiedosto koneellesi haluamaasi kansioon.
3. Mene purettuun kansioon visailusivusto-master ja luo käyttöösi Python-virtuaaliympäristö 
kirjoittamalla komentoriville _python3 -m venv venv_
4. Aktivoi virtuaaliympäristö kirjoittamalla komentoriville _source venv/bin/activate_
5. Lataa sovelluksen riippuvuudet kirjoittamalla komentoriville _pip install -r requirements.txt_
6. Sovelluksen voi nyt käynnistää kirjoittamalla komentoriville _python run.py_
7. Sovellusta voi nyt käyttää selaimen kautta osoitteessa _http://127.0.0.1:5000/_
8. Seuraavalla kerralla sovelluksen käynnistäessäsi riittää, että aktivoit virtuaaliympäristön (kohta 4) 
ja käynnistät sovelluksen (kohta 6).

Ensimmäisellä käynnistyskerralla sovellus luo kansioon _application_ tietokannan _quizdata.db_.
Kaikki tiedon tallennus tapahtuu tähän tietokantaan.

## Sovelluksen käyttö

QuizBee avautuu etusivulle, jossa voi tarkastella High Score -listoja. Sivulla on linkit sisäänkirjautumiseen
ja rekisteröitymiseen. Jos et ole kirjautunut sisään, pääset vastaamaan yksittäisiin tietokannasta löytyviin
visakysymyksiin valitsemalla ylävalikosta _Play_. Kaikkia muita toimintoja varten sinun pitää luoda käyttäjätili
ja kirjautua sisään.

Kun olet kirjautunut sisään, näet _Play_ -sivulla myös listauksen visoista ja pääset vastaamaan niihin.
Kirjautunut käyttäjä voi pelin yhteydessä myös tehdä kysymyksestä ilmoituksen ylläpidolle, 
mikäli pitää kysymystä asiattomana tai virheellisenä.

Yläpalkkiin ilmestyvät sisään kirjautuessasi myös seuraavat valikot:
- _List your questions_ -sivulla näet listauksen omista tietokantaan lisäämistäsi kysymyksistä. Voit aktivoida ja poistaa
kysymyksiä samalla sivulla. Kysymyksiä pääsee muokkaamaan listauksen kautta linkistä _Modify_. Muokkaussivulla voi myös
lisätä kysymykseen vastausvaihtoehtoja. Jos joku toinen käyttäjä on tehnyt ilmoituksen jostain kysymyksestäsi, siitä
ilmestyy huomautus listaussivun ylälaitaan. Kyseinen kysymys on muutettu automaattisesti ei-aktiivisesti ja voit
aktivoida sen uudestaan sen jälkeen, kun ylläpito on hyväksynyt kysymyksen ja/tai siihen tekemäsi muokkaukset. 
- _Add a question_ -sivulla voit lisätä tietokantaan uuden kysymyksen. Vastausvaihtoehtojen lisääminen onnistuu myöhemmin
kun menet _List your questions_ -sivun kautta muokkaamaan kysymystä.
- Kysymyksellä pitää olla oikea vastausvaihtoehto, jotta sen voi aktivoida. Ainoastaan aktiiviset kysymykset ovat
pelattavissa ja lisättävissä visoihin. Jos aktiivinen kysymys muutetaan ei-aktiiviseksi, se samalla poistetaan
kaikista visoista.
- _List your quizzes_ -sivulla näet listauksen luomistasi visoista. Voit aktivoida ja poistaa visoja samalla sivulla.
Visoja pääsee muokkaamaan listauksen kautta linkistä _Modify_. Muokkaussivulla voi myös lisätä visaan kysymyksiä.
- _Add a quiz_ -sivulla voit lisätä tietokantaan uuden visan joko omista kysymyksistäsi tai automaattisesti. Jos luot
visan omista kysymyksistäsi, voit lisätä visaan kysymyksiä myöhemmin kun menet _List your quizzes_ -sivun kautta
muokkaamaan visaa. Automaattiseen visaan kysymykset valikoituvat automaattisesti kaikkien käyttäjien kysymysten joukosta.
- Visassa pitää olla vähintään kaksi kysymystä, jotta sen voi aktivoida.
Ainoastaan aktiiviset visat näkyvät pelisivulla ja muut käyttäjät pääsevät vastaamaan niihin. 
Näet kuitenkin itse pelisivulla vain ne omat visasi, jotka on luotu automaattisesti.
- _See your statistics_ -sivulla voit tarkastella omia vastaustilastojasi.
- _Account settings_ -sivulla voit muuttaa nimeäsi, käyttäjätunnustasi ja salasanaasi sekä poistaa käyttäjätilisi.
Jos poistat käyttäjätilisi, kaikki tietokantoihin lisäämäsi data poistetaan.
- Ylläpitäjä näkee tämän lisäksi listaukset kaikista kysymyksistä, visoista, käyttäjistä ja käyttäjien tekemistä ilmoituksista.
Ylläpitäjällä on muokkausoikeudet kaikkiin kysymyksiin ja visoihin. Ylläpitäjä seuraa käyttäjien tekemiä ilmoituksia ja
voi merkitä ne kuitatuiksi, jos ilmoitus ei enää ole aiheellinen. Lisäksi ylläpitäjä voi poistaa käyttäjiä.
