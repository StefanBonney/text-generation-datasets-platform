## Developer Course Checklist

This section is a checkilst for the project developer to personally ensure that the requirements for the course have been met.

### Perusvaatimukset (arvosana 3)

#### Sovelluksen perusvaatimukset

- ✔️ Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen    
    - /register ja /login reitit, salasanan hashays werkzeug.security:llä  
- ✔️ Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tietokohteita    
    - /new_dataset luo datasettejä, /edit_dataset/<id> muokkaa, /delete_dataset/<id> poistaa  
- ✔️ Käyttäjä näkee sovellukseen lisätyt tietokohteet    
    - Etusivu (/) näyttää kaikki datasetit paginoituna, /dataset/<id> näyttää yksittäisen datasetin sisällön  
- ✔️ Käyttäjä pystyy etsimään tietokohteita hakusanalla tai muulla perusteella    
    - /search reitti hakee datasettejä otsikon ja kuvauksen perusteella SQL LIKE -kyselyllä  
- ✔️ Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät tietokohteet    
    - /user/<id> reitti näyttää käyttäjän datasetit, rivimäärät, liittymispäivän ja tilastot  
- ✔️ Käyttäjä pystyy valitsemaan tietokohteelle yhden tai useamman luokittelun    
    - Tags-taulu ja dataset_tags-liitostaulu, tagit voi lisätä/poistaa dataset-sivulla  
- ✔️ Käyttäjä pystyy lisäämään tietokohteeseen toissijaisia tietokohteita    
    - Comments-taulu sisältää kommentit, joita voi lisätä/poistaa dataset-sivulla  


#### Tekniset perusvaatimukset

- ✔️ Sovellus toteutettu kurssimateriaalin mukaisesti  
    - Noudattaa kurssimateriaalin rakennetta: Flask-sovellus, templates-kansio, SQL-tietokanta, session-hallinta  
- ✔️ Sovellus toteutettu Pythonilla käyttäen Flask-kirjastoa  
    - app.py käyttää Flask-kirjastoa, reitit määritelty @app.route-dekoraattoreilla  
- ✔️ Sovellus käyttää SQLite-tietokantaa  
    - database/db.py avaa SQLite-yhteyden (sqlite3.connect("database/database.db"))  
- ✔️ Kehitystyössä käytetty Gitiä ja GitHubia  
    - Repositorio GitHubissa, commitit näkyvissä historiassa  
- ✔️ Sovelluksen käyttöliittymä muodostuu HTML-sivuista  
    - templates/-kansio sisältää .html-tiedostot (layout.html, index.html, dataset.html jne.)  
- ✔️ Sovelluksessa ei ole käytetty JavaScript-koodia  
    - Kaikki toiminnallisuus toteutettu server-side Flaskilla, ei .js-tiedostoja tai <script>-tageja  
- ✔️ Tietokantaa käytetään suoraan SQL-komennoilla (ei ORMia)  
    - Kaikki kyselyt ovat SQL-stringejä, queries/-kansion tiedostot sisältävät raw SQL (SELECT, INSERT, UPDATE, DELETE)  
- ✔️ Flaskin lisäksi käytössä ei muita erikseen asennettavia Python-kirjastoja  
    - Käytetään vain Flaskia ja Python-standardikirjastoa (sqlite3, secrets, werkzeug tulee Flaskin mukana)  
- ✔️ Sovelluksen ulkoasu (HTML/CSS) on toteutettu itse ilman kirjastoja  
    - static/main.css sisältää kaikki tyylit, ei Bootstrap/Tailwind/muita CSS-kirjastoja  
- ✔️ Sovelluksen koodi on kirjoitettu englanniksi  
    - toteutus: Funktiot, muuttujat, kommentit englanniksi (esim. get_datasets, user_id, add_comment)  
- ✔️ Tietokannan taulut ja sarakkeet on nimetty englanniksi  
    - toteutus: schema.sql sisältää englanninkieliset taulut (users, datasets, comments) ja sarakkeet (username, title, content)  

#### Versiohallinta

- ✔️ Tiedosto README.md kertoo, millainen sovellus on ja miten sitä voi testata  
    - README sisältää kuvauksen, ominaisuudet, asennusohjeet ja testausohjeet  
- ✔️ Kehitystyön aikana on tehty commiteja säännöllisesti  
    - Commit-historiassa useita commiteja eri päiviltä ja viikoilta  
- ✔️ Commit-viestit on kirjoitettu englanniksi  
    - Commit-viestit englanniksi  

#### Sovelluksen turvallisuus

- ✔️ Salasanat tallennetaan tietokantaan asianmukaisesti  
    - werkzeug.security.generate_password_hash() hashaa salasanat, check_password_hash() tarkistaa  
- ✔️ Käyttäjän oikeus nähdä sivun sisältö tarkastetaan  
    - require_login()-funktio tarkistaa session["user_id"], template-ehdot tarkistavat omistajuuden  
- ✔️ Käyttäjän oikeus lähettää lomake tarkastetaan  
    - POST-reiteissä tarkistetaan session["user_id"] ja omistajuus ennen toimintoja  
- ✔️ Käyttäjän syötteet tarkastetaan ennen tietokantaan lisäämistä  
    - Tarkistetaan tyhjät kentät ja whitespace useissa lomakkeissa: käyttäjänimen pituus ja tyhjyys (register), salasanojen yhtäläisyys (register), datasettien kenttien tyhjyys (create_dataset), kommenttien tyhjyys (add_comment), HTML-lomakkeissa required-attribuutit  
- ✔️ SQL-komennoissa käytetty parametreja  
    - toteutus: Kaikki SQL-kyselyt käyttävät ?-parametreja ja params-listaa: db.query(sql, [param1, param2])  
- ✔️ Sivut muodostetaan sivupohjien kautta (render_template)  
    - Kaikki reitit palauttavat render_template("template.html"), layout.html toimii pohjana  
- ✔️ Lomakkeissa on estetty CSRF-aukko  
    - session["csrf_token"] luodaan kirjautumisen yhteydessä, tarkistetaan check_csrf()-funktiolla  

#### Vertaisarviointi ja palaute

- ✔️ Vertaisarvoinnit  
    - Molemmat vertaisarvioinnit annettu Labtool-järjestelmässä  

### Lisävaatimukset (arvosana 4)

#### Toimivuus ja käytettävyys

- ✔️ Sovellusta on helppoa ja loogista käyttää  
    - Navbar antaa selkeän navigaation, looginen sivurakenne, flash-viestit ohjaavat käyttäjää, lomakkeet selkeitä  
- ✔️ CSS:n avulla toteutettu ulkoasu (itse tehty, ei CSS-kirjastoa)  
    - static/main.css sisältää kaikki tyylit, ei Bootstrap/Tailwind tms.  

#### Versionhallinta

- ✔️ Versionhallinnassa ei ole sinne kuulumattomia tiedostoja  
    - .gitignore sisältää database.db, __pycache__, .venv jne.  
- ✔️ Commitit ovat hyviä kokonaisuuksia ja niissä on hyvät viestit  
    - Commit-viestit käsittelevät pääosin yksittäisiä pienempiä kokonaisuuksia, lyhyillä kuvauksilla muutoksista  

#### Ohjelmointityyli

- ✔️ Muuttujat ja funktiot nimetty kuvaavasti  
    - Nimet kuten get_datasets(), user_id, dataset_lines, add_comment() ovat selkeitä  
- ✔️ Sisennyksen leveys on neljä välilyöntiä  
    - Python-koodissa käytetty 4 välilyönnin sisennystä  
- ✔️ Koodissa ei ole liian pitkiä rivejä  
    - Rivit pidetty alle 100 merkissä, SQL-kyselyt jaettu usealle riville  
- ✔️ Muuttujien ja funktioiden nimet muotoa total_count (ei totalCount)  
    - Snake_case käytössä, esim: user_id, dataset_id, add_comment, get_datasets  
- ✔️ Välit oikein =- ja ,-merkkien ympärillä  
    - Python-koodissa välit oikein: def func(param1, param2), x = 5  
- ✔️ Ei ylimääräisiä sulkeita if- ja while-rakenteissa  
    - Ei ylimääräistä. If-lauseet muotoa if condition: eikä if (condition):  

#### Tietokanta-asiat

- ✔️ Taulut ja sarakkeet on nimetty kuvaavasti  
    - Taulut: users, datasets, comments; sarakkeet: username, title, content jne.  
- ✔️ Käytetty REFERENCES-määrettä, kun viittaus toiseen tauluun  
    - Esim. user_id INTEGER REFERENCES users, dataset_id INTEGER REFERENCES datasets  
- ✔️ Ei kyselyjä muotoa SELECT * (haettavat sarakkeet listattu aina)  
    - Kaikki SELECT-kyselyt listaavat sarakkeet: SELECT id, title, description FROM...  
- ✔️ Käytetty SQL:n ominaisuuksia järkevällä tavalla  
    - JOINit, aggregaatit (COUNT, AVG, MAX), ORDER BY, LIMIT, OFFSET, subqueryt käytössä  

#### Vertaisarviointi ja palaute

- ✔️ Ensimmäinen vertaisarviointi tehty kattavasti  
    - Vertaisarviointi annettu kattavasti   
- ✔️ Toinen vertaisarviointi tehty kattavasti  
    - Vertaisarviointi annettu kattavasti   
- ✔️ Kurssipalaute annettu  
    - Kurssipalaute annettu   


### Lisävaatimukset (arvosana 5)

#### Ohjelmointityyli

- ❌ Käytetty Pylint-työkalua ja raportoitu tulokset  
    - ...  
- ❌ Raportissa tulee näkyä Pylintin antama palaute sovelluksen lopullisesta versiosta  
    - ...  

#### Toimivuus ja käytettävyys

- ✔️ Käyttäjän lähettämässä tekstissä rivinvaihdot näkyvät selaimessa  
    - toteutus: show_lines-filter muuttaa \n → <br> datasettien kuvauksissa ja kommenteissa  
- ✔️ Kuvissa käytetty alt-attribuuttia (jos sovelluksessa kuvia)  
    - toteutus: Logo-kuva sisältää alt="Text Generation Datasets", käyttäjäkuvat tekstin alt="User {{ user.username }} image"  
- ✔️ Lomakkeissa käytetty label-elementtiä  
    - toteutus: Kaikki lomakkeet käyttävät <label for="..."> -elementtejä (login, register, dataset-lomakkeet)  

#### Suuren tietomäärän käsittely

- ❌ Sovellusta testattu suurella tietomäärällä ja raportoitu tulokset  
    - ...  
- ✔️ Sovelluksessa käytössä tietokohteiden sivutus  
    - toteutus: Etusivu näyttää 10 datasettiä per sivu, navigointi <<, >>, LIMIT ja OFFSET SQL:ssä  
- ✔️ Tietokantaan lisätty indeksi, joka nopeuttaa suuren tietomäärän käsittelyä  
    - Tietokannassa indeksit idx_dataset_lines ja idx_comments_dataset  