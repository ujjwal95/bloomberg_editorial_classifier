### Distribution of Named Entities in Regular and Non-Regular Articles

We will look at the distribution of different named entities in regular and non-regular articles. We would primarily be looking at the number of mentions of that entity by the document length and draw a distribution for each entity for both the regular and non-regular articles. Below are the common named entities that are referenced:

**Different Types of Named Entities**

`PERSON`:	People, including fictional.

`NORP`:	Nationalities or religious or political groups.

`ORG`:	Companies, agencies, institutions, etc.

`LOCATION`:	mountain ranges, bodies of water, counter, cities, states, buildings, airports, highways, bridges, etc.

`PRODUCT`:	Objects, vehicles, foods, etc. (Not services.)

`EVENT`:	Named hurricanes, battles, wars, sports events, etc.

`WORK_OF_ART`:	Titles of books, songs, etc.

`LAW`:	Named documents made into laws.

`LANGUAGE`:	Any named language.

`DATE`:	Absolute or relative dates or periods.

`TIME`:	Times smaller than a day.

`PERCENT`:	Percentage, including ”%“.

`MONEY`:	Monetary values, including unit.

`QUANTITY`:	Measurements, as of weight or distance.

`ORDINAL`:	“first”, “second”, etc.

`CARDINAL`:	Numerals that do not fall under another type.

![Chart](chart.jpg)

**Key Observations**

Please refer to the jupyter notebook for the charts. As we can observe from the charts, there is some striking differences in the distribution of named entities in the two classes:

* **Non-Regular Articles** have many more mentions of person names, languages and nationalities as compared to regular articles.
* **Regular Articles** on the other hand have much more mentions of locations, quantity, time and date.
* The distribution is heavily right-skewed for most of the entity types
