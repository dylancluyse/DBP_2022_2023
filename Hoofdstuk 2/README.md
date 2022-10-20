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

**GIN:**
* Het standaardtype van indexering bij FTS.
* Dit doelt zich op grote stukken tekst en maakt gebruik van omgekeerde indexering.
* We zijn op zoek naar de index, niet de value -> verwijs naar de kolom dat je daarnet hebt aangemaakt.


```sql
CREATE INDEX document_index on employee 
USING GIN (ts_document)
```

# Ranking

**ts_rank:**
* De meest relevante bovenaan/onderaan
* ts_rank( ts_document, query ) as rank --> een percentage op hoe 'relevant' een resume is.
  * De relevantie is bepaalt op hoe vaak een lettergreep of deel van een woord voorkomt. 
  * Als je developers zoekt en er meermaals 'developed', 'developing', 'developer', etc. voorkomt in de tekst, dan ga je een hoog percentage hebben. 
  * 22% is in dit geval het hoogste percentage.
  * We weten niet welke woorden een match zijn, enkel het percentage.

```sql
select lastname, firstname, title, resume, ts_rank(ts_document, query) as rank
from employee, to_tsquery('english', 'developer & (java | python)') query
where query @@ ts_document
order by rank desc
limit 5;
```

# Highlighting

We willen weten **welke woorden in welke zinnen** er behoren tot onze search.
* De plaats kennen we niet bij ranking.
* Op een korte manier tonen waarom je de resultaten hebt gevonden.

```sql
select lastname, title, ts_rank(ts_document, query) as rank,
    ts_headline('english', coalesce(title, '') || ' ' || coalesce(resume, ''), query, 'MaxWords=7, MinWords=3, StartSel = [, StopSel = ], MaxFragments=7, FragmentDelimiter=...')
from employee, to_tsquery('english', 'developer & (java|python)') query
where query @@ ts_document
order by rank desc
limit 5
```

# Early & Late binding

# Early binding
--> Stored procedure of function


** Voorbeeld van een function: **

Deze functie gaat alle werknemers, met een salaris hoger dan een gegeven waarde, gaan teruggeven.
Stappenplan:
1. create function met de naam van de functie en de benodigde parameters (+ datatype).
2. de kolommen dat de functie zal teruggeven (+ datatype)
3. de taal waarin de functie is geschreven. Dit is in ons geval altijd plpgsql.
4. 

```sql
create or replace function emps(sal numeric)
returns table(emp lastname character varying, emp salary numeric)
language plpgsql
as
begin
    return query
        select lastname, salary 
        from employee 
        where salary < sal 
        order by salary desc;
end
```

** Gebruik van de function **

```sql
select * from emps(40000);
```

late --> sql-query direct invoeren