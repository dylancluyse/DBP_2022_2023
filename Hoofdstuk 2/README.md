# Full-Text-Search

Twee componenten:

## TS_document

Dit is de plaats waarin we gaan zoeken. Een document kan een stuk tekst zijn van meerdere kolommen.

## TS_vector

Dit is (of zijn) de zoektermen waarnaar we willen zoeken.

# SQL-queries

## Voorbeelden:

Zoek naar iemand dat een ontwikkelaar is *of* iemand met een bachelor/graduate-diploma:

```sql
select lastname, title 
from employee
where to_tsvector('english', resume)
@@ to_tsquery('english', 'developer | graduate');
```

Zoek naar iemand dat een functie als junior ontwikkelaar heeft gewerkt. De twee woorden moeten elkaar opvolgen.

```sql
select lastname, title 
from employee
where to_tsvector('english', resume)
@@ to_tsquery('english', 'junior <-> developer');
```


# Indexing

* Key-value-based: 
  * We zoeken op de index om een waarde terug te krijgen. Een kolom wordt geïndexeerd wat vasthangt aan waarden waarop je wilt gaan zoeken.
* Key-value bij FTS -> werkt omgekeerd
  * We zoeken op de value om een index terug te krijgen. De IDs zijn de documents waar het woord zich in bevindt.

## Indexering maken:

* Doe je door een extra kolom toe te voegen: (kolom1) || ' ' || (kolom2)
  * to_tsvector([de taal waarin je gaat zoeken], [twee coalesce-functies met daartussen een 'splitsing'])
  * || ' ' || ==> de splitsing of de ruimte tussen de twee variabelen
  * coalesce ==> voorkomt dat we een null-waarde gaan meegeven als waarde


```sql
ALTER TABLE employee
    ADD COLUMN ts_document ts_vector
    GENERATED ALWAYS AS
    (to_tsvector('english', coalesce(title, '') || ' ' || coalesce(resume, ''))) STORED;

```

* GIN:
  * Het standaardtype van indexering bij FTS.
  * Dit doelt zich op grote stukken tekst en maakt gebruik van omgekeerde indexering.
  * We zijn op zoek naar de index, niet de value.

