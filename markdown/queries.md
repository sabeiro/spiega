# Query collection

## SQL

Select all columns

```
SELECT * FROM table;
```
rename column variable
```
SELECT purchesed_item AS item FROM table;
```
Select first rows
```
SELECT TOP 10 FROM table;
```
subset to season spring

```
SELECT * FROM table WHERE season = 'spring';
```
double subsetting

```
SELECT * FROM table WHERE (season = 'spring' AND wind > 10);
```
order by the sun level

```
SELECT * FROM table WHERE season = 'spring' ORDER BY sun_level;
```
group by the cloud level

```
SELECT count(cloud_level), cloud_level FROM table GROUP BY cloud_level;
```
unique
```
SELECT DISTINCT ID FROM table_name;
```
functions
```
COUNT() SUM() AVG()
```
create view (table as a result of a query)
```
CREATE VIEW Failing_Students AS SELECT S_NAME, Student_ID FROM STUDENT WHERE GPA > 40;
``` 
Update a view
```
CREATE OR REPLACE VIEW [ Product List] AS SELECT ProductID, ProductName, Category FROM Products WHERE Discontinued = No;
```
drop view/table
```
DROP VIEW V1;
```
select types
```
WHERE Type='PK'
'PK' private key, 'u' user defined, 'uq' unique key, 'it' internal tables, 'p' procedures
```
swap columns 
```
UPDATE table_name SET col1=col2, col2=col1
```
wildcards
```sql
SELECT * From Customers WHERE Name LIKE 'Herb%'
```
variables
```
ALL ANY
```
between
```
SELECT ID FROM Orders WHERE Date BETWEEN ‘01/12/2018’ AND ‘01/13/2018’;
```
join 
```
SELECT ID FROM Customers INNER JOIN Orders ON Customers.ID = Orders.ID;
```
union
```
SELECT phone FROM Customers UNION SELECT item FROM Orders;
```
comments
```
/* clock comment */
-- line comment
```
create
```
CREATE DATABASE AllSales;
CREATE TABLE Customers (ID varchar(80),Name varchar(80),Phone varchar(20));
```
alter - modify
```
ALTER TABLE Customers ADD Birthday varchar(80)
```
