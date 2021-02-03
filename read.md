# Deep learning algorithms that find synonyms in texts

The algorithm is divided into three parts: 

- The training 
- The search for a synonym 
- Clustering

## The training 

How to start training :

```
main.py -e -t 5 --enc "utf8" --path "C:\AutomatedLanguageProcessing\Text\LesTroisMousquetairesUTF8.txt
```

- "-e" signs that this is training 

- "-t" is the size of the window

- "--enc" is the text encoding

- "--path" is the path of the text to be analyzed

  

*It's possible to train the algorithm several times.*



## The search for a synonym 

```
main.py -r -t 5
```

- "-r" means it's a search
- "t" is the size of the window

Once the dialog has appeared in the console you have to enter  : a word, the number of synonyms and the method of calculation.

Example : 

​				**bras 10 2**



## Clustering

```
main.py -c -t 5 -k 3 -n 5
```

- "-c" means that it is a clustering

- "-t" is the size of the window

- "-k" is the number of centroid

- "n" is the number of words per centroid

  