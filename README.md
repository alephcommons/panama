# Panama companies registry (2008)

This dataset was scraped by Dan O'Huiguinn from the Panama companies registry in 2008. See his explanation below.



## Usage

Set up a Python 3 virtual environment and have `wget` ready, then run: 

```bash
make
```

## Explanation/Blog post

(From https://ohuiginn.net/mt/2008/12/opening_up_a_tax_haven.html)

Panama is still one of the biggest and most important tax havens. As well as its absurd tax regime, its corporate disclosure regime means it is very difficult to get information about Panamanian companies.

Or rather, it was. Panama recently put online their company registry. You can now retrieve the names of the current directors of every Panamanian company, as well as all the company's filings themselves (minutes of company meetings, details of shareholdings, ownership, certificates of incorporation etc. etc.).

Nice, but you can only search by the name of the company. If you want to find somebody who is dodging tax or doing something else dubious, you really need to search by director's name.

This tool fixes that problem. I've scraped all 600,000 company records, going back 30 years, and indexed by directors.

Now you can, for instance, look up recently-arrested arms dealer Monzer al-Kassar, and you find a couple of companies. Looking through the records, you find the company's current treasurer is Hans-Ulrich Ming, chairman of Swiss firm Pax Anlage. Previous directors include Enrico Ravano, president of Contship, the Italian company that controls the Calabrian port of Gioia Tauro. A Feb 2008 report for the Italian parliament accused Ravano of complicity in cocaine smuggling by the Calabrian mafia through Gioia Tauro - the report cited Italian estimates that 80% of all Europe's cocaine is smuggled through Gioia Tauro. Ravano's connection to al Kassar could help to stand up accusations (which al Kassar has always denied) that al Kassar was involved in drug trafficking as well as weapons trafficking; and helps to undermine Ravano's recent denials that he's had anything to do with any trafficking of any sort. [This set of connections was in fact found manually, by Global Witness, and was part of the inspiration to build the search]

Or take Nadhmi Auchi: Iraqi-British billionnaire, companion of Saddam Hussein in the '50s, convicted of fraud in France (but appealing). I've not yet looked through the records of companies held by him and his friends - but there are plenty of records there, doubtless including some interesting connections.

And there are plenty more interesting names to look up. Most satisfyingly, it's already proving useful in figuring out the activities of various currently-active arms dealers...

Want the raw data? Here is a d