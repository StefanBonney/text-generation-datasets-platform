# Pylint-raportti

## app.py

Pylint antaa seuraavan raportin app.py tiedostosta:

```
************* Module app
app.py:82:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:135:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:159:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)   
app.py:378:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:408:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:443:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)   

------------------------------------------------------------------
Your code has been rated at 9.78/10 (previous run: 9.77/10, +0.00)
```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

#### return statements

Raportilta tule ainoastaan seuraavan tyyppisiä ilmoituksia:

```
app.py:82:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Tässä Pylint varoittaa, että jos `request.method` olisi jotain muuta kuin GET tai POST, funktio ei palauttaisi mitään arvoa. Käytännössä tällainen tilanne ei ole kuitenkaan mahdollinen.

On tehty päätös, ettei näitä ilmoituksia korjata, koska ne eivät aiheuta todellista ongelmaa sovelluksen toiminnassa ja koodi on selkeämpi nykyisessä muodossaan.


## users.py

Pylint antaa seuraavan raportin users.py tiedostosta:

```
************* Module queries.users
queries\users.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\users.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\users.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\users.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\users.py:43:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\users.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.12/10 (previous run: 7.81/10, +0.31)
```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

#### missing docstring

Raportilta tule ainoastaan seuraavan tyyppisiä ilmoituksia:

```
queries\users.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Funktioiden docstringit on jätetty pois tarkoituksella. Funktioiden nimet ovat riittävän kuvaavia (esim. `create_user`, `check_login`, `get_user_stats`), ja lisädokumentaatio olisi tarpeetonta.


## datasets.py

Pylint antaa seuraavan raportin datasets.py tiedostosta:

```
************* Module queries.datasets
queries\datasets.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:84:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:91:0: C0116: Missing function or method docstring (missing-function-docstring)
queries\datasets.py:96:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.65/10 (previous run: 7.18/10, +1.47)
```

Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

#### missing docstring

Raportilta tule ainoastaan seuraavan tyyppisiä ilmoituksia:

```
queries\datasets.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Funktioiden docstringit on jätetty pois tarkoituksella. Funktioiden nimet ovat riittävän kuvaavia (esim. `create_dataset`, `get_datasets`, `search_datasets`), ja lisädokumentaatio olisi tarpeetonta.


## comments.py

Pylint antaa seuraavan raportin comments.py tiedostosta:

```
-------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 8.82/10, +1.18)
```

Ei korjattavaa tässä.