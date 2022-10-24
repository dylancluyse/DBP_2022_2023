**1. Hoe kunnen we volgende query sneller laten draaien?**

```sql
select u.id, u.displayname, u.Reputation, u.UpVotes 
from Users u 
order by u.Reputation desc,u.UpVotes asc;
```

*Antwoord: We gaan een index moeten schrijven. De index zal zich richten op Reputation en Upvaotes.*

```sql
create index user_idx on users (Reputation desc, UpVotes asc);
```

*De displayname blijft over. Hierop gaan we niet sorteren, maar we moeten deze kolom wel bij de query betrekken. Hiervoor gaan we een include gebruiken.*

```sql
create index user_idx on users (Reputation desc, UpVotes asc) include (displayname);
```

**2. Toon alle posts van het jaar 2010 op een efficiente manier, toon het id, titel en de viewcount.**

```sql
select id, title, viewcount 
from posts 
where CreationDate between '2010-01-01' and '2010-12-31';
```

*Hier mag je niet ```YEAR(creationdate) ``` gebruiken. Dit omdat een functie enkel een geïndexeerde query zal vertragen en zo speel je het voordeel kwijt.*

*Dit kan je oplossen door ofwel een ```WHERE ... BETWEEN ... AND ...``` te doen, ofwel door een nieuwe kolom toe te voegen aan de tabel met daarin het jaar. Het nadeel is dat je hier meer geheugen gaat voor nodig hebben, maar dit is afhankelijk voor wat je het gaat gebruiken.*

```sql
alter table posts add YearCreation as (year(creationdate));
select id, title, viewcount from posts where YearCreation = 2010;
```

**3. Tel het aantal stemmen per jaar op een efficiënte manier. Wat is het nadeel hier? Kunnen we dit aanraden?**

```sql
select year(p.CreationDate) as year_of_post, count(v.id) as number_of_posts
from Posts p 
join Votes v on p.Id = v.Id
group by year(p.CreationDate)
order by year(p.CreationDate)
```

*We hebben hier een heel lang execution plan. Dit omdat we gebruik maken van een geaggregeerde functie. We kunnen dit oplossen door een indexed view aan te maken van de gegevens.*

3.1. *Maak eerste de materialized view:*

```sql
-- eenmalig uitvoeren
create or alter view dbo.posts_per_year(creationyear, number_of_posts)
with schemabinding as
    select year(p.CreationDate) as year_of_post, count_big(v.id) as number_of_posts
    from dbo.Posts p 
    join dbo.Votes v on p.Id = v.Id
    group by year(p.CreationDate)

-- dit achteraf uitvoeren om het te testen
select * from posts_per_year
```


3.2. *Na het maken van de view moeten we een clustered index maken. Zonder de clustered index gaan we nog geen sneller systeem hebben. Als het nu sneller gaat, dan komt dit omdat het query execution plan gecached is. De clusterd index zal voor een aanzienlijk sneller systeem zorgen.*

```sql
create clustered index ci_post_per_year
on CreationDate
```

**4. De index wordt niet gebruikt wanneer het geïndexeerde veld in een functie wordt gebruikt, zoals bijvoorbeeld ```YEAR(creationdate)```. Sommige systemen voorzien function-based indexes om hiermee om te kunnen gaan. Wat kunnen we doen om dit te omzeilen?**

*Zoals hierboven gezegd, maak een nieuwe kolom aan dat gebaseerd is op een berekening met een functie.*

**X - Materialized view of indexed views**

* Data vasthouden als een tabel. De berekeningen neem je weg van de query runtime. Een heel complexe view met heel complexe aggregaties (count, sum, etc.). Je houdt de resultaten van een select-statement bij.

* Je voegt er een primary key aan toe.

* Een view wordt aangemaakt en opgeslaan als object, maar de inhoud wordt niet opgeslaan! Enkel het select-statement wordt opgeslaan.

* Virtuele tabel --> 'echte data' opgeslaan in een tabel.

**X - Schema**

* Container met alle objecten van een databank.

* Het schema moet gebonden zijn aan de tabellen in een view. De binding zorgt voor het verwijzen naar de verschillende tabellen.

*  Als je een tabel binnen een view gaat verwijderen of aanpassen, dan wordt de view onbeschikbaar.

```sql
create view ... 
with schemabinding
as select ... from ...
join by ... on .. = ..
group by ..
```

* Hierna ga je een clustered index uitvoeren op de view. 


**5. Maak een rangschikking van alle gebruikers op basis van het aantal badges op de meest efficiënte manier.**

Hoe je het niet moet doen:

```sql
select u.Id, u.DisplayName, count(*) as numberOfBadges from Users u
join Badges b on u.Id = b.UserId
group by u.Id, u.DisplayName
```

Hier volg je best hetzelfde principe. Je slaat het aantal badges op per gebruiker.


```sql

```

