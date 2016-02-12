# Sexism in dictionaries

Recently a friend, and anthropologist, brought to my attention the interaction discussed [here](https://medium.com/space-anthropology/sexism-in-the-oxford-dictionary-of-english-6d335c6a77b5#.ckk4vnor6). I was immediately interested by this, and realized the need for a deeper analysis. 

While his original examples are extremely illustrative, a more data science approach would be to look at all words, or at least, a large corpus of words, and analyze their example sentences for sexism. As far as I know, there is no NLP package for detecting bigotry of a particular kind, in text. But there are some proxies for this. One such would a somewhat naive approach:
- pick out sentences where the subject is identified by a male/female pronoun
- examine the sentences for positive and negative sentiment

In some sense, this is going to return a measure of how often a particular gendered pronoun is used in the context of negative or positive words. In this case, we have a special advantage that sentiment analysis usually lacks: each sentence is tied to a unique word. To be more in the spirit of the original observation, it would make more sense to look at the sentiment of that word, rather than average the sentiment of the entire sentence. This ends up making analysis easier actually. 

## A few definitions

- `gendered pronouns` we refer to any of the pronouns listed below as gendered pronouns and we consider them to be binary: female or male. 
- `gendered sentences` we refer to any sentence that contains a gendered pronoun as a gendered sentence. If the sentence contains a female pronoun, we consider the sentence to be a "female sentence" and similarly for male pronouns and "male sentences". Note that sentences that contain female AND male pronouns we refer to as "female sentences" AND "male sentences".
- `word sentiment` we define the sentiment of a word as the value listed in the AFINN dataset corresponding to that word. If the word is not present in the AFINN dataset, we consider it to have zero sentiment. 
- `sentence sentiment` the sentiment of a sentence can be defined as the sentiment of the word for which the example sentence references, the aggregate of sentiments of words in the sentence, or the average sentiment of words in the sentence. We will be clear which we are assuming.

## AFINN

For the purpose of obtaining sentiment scores, we use the well-known AFINN dataset. Specifically we use the `AFINN-111` dataset. You can read about the dataset and this project [here](http://www2.imm.dtu.dk/pubdb/views/publication_details.php?id=6010).

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

Utilizing the output of that csv, I wrote a small python script to compute some very basic statistics related to the dataset.

We begin with extremely elementary analysis:
- `all sentiment words sum` is the sum of all sentiment values of words in AFINN, which is -1434.
- `total sentiment sum of words in gendered sentences`, we compute the sum of sentiments of words that appear in sentences with a gendered pronoun.
- `count of sentences with female pronouns` we count the number of sentences with female gendered pronouns in our corpus.
- `count of sentences with male pronouns` we count the number of sentences with male gendered pronouns in our corpus.
- `total sentiment sum of sentences with female pronouns` we compute the sum of sentiment of words that appear in sentences with female gendered pronouns. Note that this add the word's sentiment for each sentence that word appears in that also contains a female gendered pronoun.
- `total sentiment sum of sentences with male pronouns` we compute the sum of sentiment of words that appear in sentences with male gendered pronouns. Note that this add the word's sentiment for each sentence that word appears in that also contains a male gendered pronoun.
- `average sentiment of sentences with female pronouns` this is the average sentiment per sentence with female pronoun, calculated as a ratio of the sentiment sum to the count of sentences.
- `average sentiment of sentences with male pronouns` this is the average sentiment per sentence with male pronoun, calculated as a ratio of the sentiment sum to the count of sentences.

## Results by dictionary

### Merriam-Webster
------------------
```
total sentiment sum of words in gendered sentences:  -490
count of sentences with female pronouns:  1059
count of sentences with male pronouns:  1393
total sentiment sum of sentences with female pronouns:  -376
total sentiment sum of sentences with male pronouns:  -669
average sentiment of sentences with female pronouns:  -0.355051935788
average sentiment of sentences with male pronouns:  -0.480258435032
```


## Gender pronouns

Female gender pronouns used:
```
[" she ", " She ", " she'", " She'", " her ", " Her ", " her'", " Her'", " woman ", " Woman ", " woman'", " Woman'", " female ", " Female ", " female'", " Female'", " hers ", " Hers ", " hers'", " Hers'"]
```

Male gender pronouns used:
```
[" he ", " He ", " he'", " He'", " him ", " Him ", " him'", " Him'", " man ", " Man ", " man'", " Man'", " male ", " Male ", " male'", " Male'", " his ", " His ", " his'", " His'"]
```