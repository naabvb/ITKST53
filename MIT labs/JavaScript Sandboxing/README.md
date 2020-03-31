# ITKST53 - JavaScript Sandboxing

**Tekijä:** Lauri Pimiä (lailpimi)

**Perustelut:** Kaikki näyttäisi toimivan kuten pitää joten odottaisin saavani
täydet 3.5p. Kaikki testit menevät läpi 'make check' komennolla ja kokeilin
myös jokaisen testitapauksen selaimella ilman ongelmia.

Tehtävä itsessään osoittautui työläämmäksi kuin alunperin ajattelin ja eniten
aikaa meni varsinkin tuon visitor-mallin toiminnan ymmärtämisessä.
Tarkistuksiin ohjataan lab6visitor.py:sta neljästä kohdasta joita ovat:

- def visit_DotAccessor()

- def visit_BracketAccessor()

- def visit_FunctionCall()

- def visit_This()

Samassa tiedostossa lisätään myös 'sandbox_' etuliitteet ja poistetaan niitä
ohjeiden mukaisista kohteista.

Itse tarkistukset ja muutkin libcoden muokkaukset toteutin aikalailla ohjeita 
seuraten. Tarkistuksissa tarkistetaan mm. vaaralliset sanat, this ja onko
funktio selaimen oma (eli toisin sanoen onko funktio esim. kustomoitu toString).
Natiivin funktion tarkistin ei toimi apply() tai bind() funktioita vastaan,
mutta tehtävänannossa tämä oli sallittu.