# User storyt


## Satunnaisen käyttäjän näkökulma:
* Haluan nähdä etusivulla tietoa sovelluksesta.
* Haluan pystyä vastaamaan yksittäisiin tietovisakysymyksiin ilman kirjautumista ja näkemään, menikö vastaus oikein. Ei haittaa vaikka pisteeni eivät tällöin tallennu mihinkään.
* Haluan mahdollisuuden luoda itselleni käyttäjätilin.

## Kirjautuneen käyttäjän näkökulma:
* Haluan pystyä hallinnoimaan omia tietojani, kuten salasanaani ja käyttäjätunnustani.
* Haluan pystyä vastaamaan muiden käyttäjien tekemiin kysymyksiin ja kysymyksistä koottuihin visoihin. Joskus on kivempi vastata täysin satunnaisiin kysymyksiin, joskus taas hakea kysymyksiä aihepiirin perusteella.
* Kun pelaan kirjautuneena, haluan että ansaitsemani pisteet tallentuvat ja voin tarkastella, kuinka hyvin olen pärjännyt.
* Haluan itsekin voida tehdä omia kysymyksiä ja visoja, joihin muut käyttäjät voivat sitten vastata. Haluan myös mahdollisuuden niiden muokkaamiseen ja poistamiseen. Jos tuotan sivulle aktiivisesti uutta sisältöä, haluan että se näkyy myös pisteissäni.
* Haluan, että myös muiden kuin itseni tekemät kysymykset ovat järkeviä ja virheettömiä. Trollailumielessä tehtyihin kysymyksiin en halua vastata.

## Ylläpitäjän näkökulma:
* Haluan nähdä, kuinka paljon järjestelmällä on käyttäjiä.
* Koska en halua, että järjestelmä täyttyy asiattomasta sisällöstä, haluan muokkaus- ja poisto-oikeuden käyttäjien lisäämiin kysymyksiin.
* Koska minulla ei kuitenkaan ole aikaa lukea läpi jokaista kysymystä, haluan että käyttäjät voivat ilmoittaa minulle asiattomasta sisällöstä.
* Tarvittaessa haluan voida poistaa järjestelmästä käyttäjiä, jotka eivät noudata sääntöjä.             

## Esimerkkejä käyttötapausten SQL-kyselyistä

### Eniten kysymyksiä lisänneet käyttäjät

High Score listalle voi hakea viisi viikon aikana eniten kysymyksiä lisännyttä käyttäjää (käyttäjätunnus ja uusien kysymysten määrä) seuraavasti:

Herokussa:

SELECT Account.username, COUNT(Question.id) AS questions FROM Account, Question WHERE Question.account_id = Account.id AND Question.active = True AND Question.date_created > DATE_TRUNC('week', CURRENT_TIMESTAMP - interval '1 week') GROUP BY Account.id ORDER BY questions DESC LIMIT 5

SQLitessä:

SELECT Account.username, COUNT (Question.id) AS questions FROM Account, Question WHERE Question.account_id = Account.id AND Question.active = True AND Question.date_created >= DATE(CURRENT_TIMESTAMP, '-6 DAY') GROUP BY Account.id ORDER BY questions DESC LIMIT 5

### Parhaat tietäjät

Vastaavasti viisi viikon aikana eniten oikeita vastauksia saanutta käyttäjää (käyttäjätunnus ja vastausten määrä) voi hakea seuraavasti:

Herokussa:

SELECT Account.username, COUNT(Users_Choice.id) AS answers FROM Account, Users_Choice, Option WHERE Users_Choice.date_created > DATE_TRUNC('week', CURRENT_TIMESTAMP - interval '1 week') AND Users_Choice.account_id = Account.id AND Users_Choice.option_id = Option.id AND Option.correct = True GROUP BY Account.id ORDER BY answers DESC LIMIT 5

SQLitessä:

SELECT Account.username, COUNT(Users_Choice.id) AS answers FROM Account, Users_Choice, Option WHERE Users_Choice.date_created >= DATE(CURRENT_TIMESTAMP, '-6 DAY') AND Users_Choice.account_id = Account.id AND Users_Choice.option_id = Option.id AND Option.correct = True GROUP BY Account.id ORDER BY answers DESC LIMIT 5

### Kysymysten lisääminen visaan

Kun käyttäjä lisää visaan kysymyksiä, hän saa nähtäväkseen niistä omista kysymyksistään (id ja nimi), jotka ovat aktiivisia ja joita ei ole vielä liitetty kyseiseen visaan. Tämä onnistuu kyselyllä:

SELECT Question.id, Question.name FROM QUESTION, ACCOUNT WHERE Question.account_id = Account.id AND Account.id = ? AND Question.active = True AND Question.id NOT IN (SELECT Question.id FROM Question, Quiz, Quiz_Question Where Quiz_Question.question_id = Question.id AND Quiz_Question.quiz_id = Quiz.id AND Quiz.id = ?)

Ensimmäisen kysymysmerkin kohdalle tulee siis käyttäjän id ja toisen kysymysmerkin kohdalle visan id.

