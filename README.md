# Sexism in dictionaries

Recently a friend, and anthropologist, brought to my attention the interaction discussed [here](https://medium.com/space-anthropology/sexism-in-the-oxford-dictionary-of-english-6d335c6a77b5#.ckk4vnor6). I was immediately interested by this, and realized the need for a deeper analysis. 

While his original examples are extremely illustrative, a more data science approach would be to look at all words, or at least, a large corpus of words, and analyze their example sentences for sexism. As far as I know, there is no NLP package for detecting bigotry of a particular kind, in text. But there are some proxies for this. One such would a somewhat naive approach:
- pick out sentences where the subject is identified by a male/female pronoun
- examine the sentences for positive and negative sentiment

In some sense, this is going to return a measure of how often a particular gendered pronoun is used in the context of negative or positive words. In this case, we have a special advantage that sentiment analysis usually lacks: each sentence is tied to a unique word. To be more in the spirit of the original observation, it would make more sense to look at the sentiment of that word, rather than average the sentiment of the entire sentence. This ends up making analysis easier actually. 

## The data set

The original goal was to use OED data, and then some other dictionaries as well. Currently, I don't have access to OED, and I haven't gotten around to other dictionaries besides Merriam-Webster(M-W henceforth), which graciously allows one to request their webpages directly. 

I grabbed the M-W dataset in a brute force way, using wget(I seem to always fall back on just scraping for these projects):
```bash
wget -q -O - "$@" http://www.merriam-webster.com/dictionary/$word | grep '<p class="definition-inner-item"' | 
	grep '<em>' | 
	grep -v "primary-content" | 
	awk '{gsub("<em>", "");print}' |
	awk '{gsub("</em>", "");print}' |
	awk '{gsub("<li>", "");print}' |
	awk '{gsub("</li>", "");print}' |
	awk '{gsub("&lt;", "");print}' |
	awk '{gsub("</p>", "");print}' |
	awk '{gsub("</ol>", "");print}' |
	awk '{gsub("<br />", "");print}' |
	awk '{gsub("<p", "");print}' |
	sed 's#class="definition-inner-item">#BEGIN #g' |
	tr BEGIN '\n' | 
	sed  '/^$/d'
```
which I put inside a shell script.

A few things that needed done from here:
- cleanup, ugh. This data was ugly. I could of probably been slicker with the wget, but this time, I did a fair amount of ad-hoc cleanup. If you try to recreate my steps, just know that "here be dragons"
- I only kept the sentences which used one of my gender-words(list below). Based on the analysis that I wanted to do, I was only going to use these anyhow, so I just tossed out the others
- Remove duplicates. M-W sometimes uses the same example sentences for different words with the same stem, so I just used a slick perl one-liner to get rid of the dupes: `perl -ne '$H{$_}++ or print'`

The data at this points looks like what is in `goodlines`

Now, I wrote a python script to take this data set, and produce the data we wish to analyze. the parsing is routine:
```
Check if the line is a new word or a sentence, if word:
	Add word to dictionary, initialize some lists, make it "current word"
If line is sentence:
	Check if the sentence contains male, female, or both kinds of pronouns if yes:
		Add to the lists corresponding to each
Print the word, its sentiment, the number of female sentences, number of male sentences as columns in a csv
```
so an example output line looks like:
```
word	sentiment	female	male
protest	-2	3	4
```
this dataset is contained in `outputData.csv`.

## Analysis

To-do!

## Gender pronouns

Female gender pronouns used:
```
[" she ", " She ", " she'", " She'", " her ", " Her ", " her'", " Her'", " woman ", " Woman ", " woman'", " Woman'", " female ", " Female ", " female'", " Female'", " hers ", " Hers ", " hers'", " Hers'"]
```

Male gender pronouns used:
```
[" he ", " He ", " he'", " He'", " him ", " Him ", " him'", " Him'", " man ", " Man ", " man'", " Man'", " male ", " Male ", " male'", " Male'", " his ", " His ", " his'", " His'"]
```