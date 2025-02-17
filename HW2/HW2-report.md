# HW2 - Ranking Webpages

### Devin Morgan

### CS 432, Spring 2025

### 02/16/2025

# Q1

How many of your 500 URIs produced useful text? If that number was less than 500, did that surprise you?

## Answer

The amount was 445. No that number did not suprise me. Since the number of uris is so high I expected some to not have text in them.

# Q2

TF = $\Large\frac{Total words in document}{Occurrences of 'Time' in document}$

IDF = log<sub>2</sub>($\Large\frac{Total number of documents}{Number of documents containing 'Time'}$)

TF-IDF = TF \* IDF

The term is "Time".

Total number of "Time"s in all files:
Total number of documents = 445
Number of documents containing "Time" = 181

Code:

Get count of how many documents have the phrase:

```bash
(Get-ChildItem processed_text/*.txt | Where-Object { Select-String -Path $_.FullName -Pattern "\bTime\b" -Quiet }).Count
```

List out all documents with the phrase:

```bash
# Define the path to the collected URIs file
$collectedUrisFile = "../HW1/collected_uris.txt"

# Create a mapping of MD5 hashes to original URIs
$uriMap = @{}
Get-Content $collectedUrisFile | ForEach-Object {
    $uri = $_.Trim()
    if ($uri -ne "") {
        $hash = [System.BitConverter]::ToString((New-Object System.Security.Cryptography.MD5CryptoServiceProvider).ComputeHash([System.Text.Encoding]::UTF8.GetBytes($uri))) -replace "-"
        $uriMap[$hash.ToLower()] = $uri
    }
}

# Find documents containing the phrase
$hashes = Select-String -Path processed_text/*.txt -Pattern "\bTime\b" | Select-Object -ExpandProperty Path | Sort -Unique | ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_) }

# Output hash and original URI
$hashes | ForEach-Object { if ($uriMap.ContainsKey($_)) { "$_ : $($uriMap[$_])" } }
```

Find the values needed to calculate TF and TF-IDF:

```bash
# Ask user for the file path
$filePath = Read-Host "Enter the full path of the .txt file"

# Read the content of the file
$content = Get-Content "processed_text\$filePath" -Raw

# Count occurrences of "Time" (case-insensitive, whole word match)
$timeCount = ([regex]::Matches($content, "\bTime\b", "IgnoreCase")).Count

# Count total words in the document
$wordCount = ($content -split "\s+").Count

# Calculate Term Frequency (TF)
$tf = if ($wordCount -gt 0) { [math]::Round($timeCount / $wordCount, 6) } else { 0 }

# Define the IDF value
$idf = 1.297

# Calculate TF-IDF
$tfidf = [math]::Round($tf * $idf, 6)

# Output results
Write-Host "File: $filePath"
Write-Host "Occurrences of 'Time': $timeCount"
Write-Host "Total words in document: $wordCount"
Write-Host "Term Frequency (TF): $tf"
Write-Host "TF-IDF: $tfidf"
```

| TF-IDF   | TF       | IDF   | "Time" Count | Word Count | Hash                             | URI                                                                                      |
| :------- | :------- | :---- | :----------- | :--------- | :------------------------------- | ---------------------------------------------------------------------------------------- |
| 0.000464 | 0.000358 | 1.297 | 7            | 19579      | fe272a3351c5123e9476ef9fd139fe4e | https://weiglemc.github.io/publications/bibtex#ruffing-milcom14                          |
| 0.002961 | 0.002283 | 1.297 | 1            | 438        | fe004e033f2c816ec0f78a15f583e601 | https://www.slideshare.net/slideshow/jcdl-howmuchisarchived/8341312                      |
| 0.034132 | 0.026316 | 1.297 | 1            | 38         | f70a40a5c075e7b4addcf8bdc9dc8324 | https://yasith.dev/                                                                      |
| 0.002259 | 0.001742 | 1.297 | 1            | 574        | ec2552781492073d6781502036f98fb4 | https://minerva.defense.gov/                                                             |
| 0.012122 | 0.009346 | 1.297 | 2            | 214        | abc4874b4179d2f199116415318af609 | https://justinfbrunelle.com/                                                             |
| 0.008547 | 0.00659  | 1.297 | 4            | 607        | df2cc69af4583c8a512e0c68b27d3ce1 | https://www.unc.edu/discover/graduate-student-discovers-youngest-transiting-planet-ever/ |
| 0.040531 | 0.03125  | 1.297 | 3            | 96         | e09aa5d7ad8169e74f18bd9532bf61d1 | https://cs531-f22.github.io/                                                             |
| 0.005127 | 0.003953 | 1.297 | 1            | 253        | c29a2af24042e73fced3295349842df8 | https://alertcarolina.unc.edu/                                                           |
| 0.004503 | 0.003472 | 1.297 | 1            | 288        | bfcbd7c748d59fdbc5577435671dc5b1 | https://www.odu.edu/                                                                     |
| 0.002235 | 0.001723 | 1.297 | 2            | 1161       | b100a58b97c7294b6f7f09a3f912a3a0 | https://www.defense.gov/Legal-Administrative/Privacy-Security/                           |

## Answer

_You must discuss in your report how you computed the values (especially IDF) and provide the formulas you used for TF, IDF, and TF-IDF._

I used code to generate most of my values for me. Here are the formulas I used:

TF = $\Large\frac{Total words in document}{Occurrences of 'Time' in document}$

IDF = log<sub>2</sub>($\Large\frac{Total number of documents}{Number of documents containing 'Time'}$)

TF-IDF = TF \* IDF

# Q3

I used https://searchenginereports.net/google-pagerank-checker to check page rank.

| Page Rank | Hash                             | URI                                                                                      |
| :-------- | :------------------------------- | :--------------------------------------------------------------------------------------- |
| 0.25      | fe272a3351c5123e9476ef9fd139fe4e | https://weiglemc.github.io/publications/bibtex#ruffing-milcom14                          |
| 1         | fe004e033f2c816ec0f78a15f583e601 | https://www.slideshare.net/slideshow/jcdl-howmuchisarchived/8341312                      |
| 0.125     | f70a40a5c075e7b4addcf8bdc9dc8324 | https://yasith.dev/                                                                      |
| 0.875     | ec2552781492073d6781502036f98fb4 | https://minerva.defense.gov/                                                             |
| 0.25      | abc4874b4179d2f199116415318af609 | https://justinfbrunelle.com/                                                             |
| 1         | df2cc69af4583c8a512e0c68b27d3ce1 | https://www.unc.edu/discover/graduate-student-discovers-youngest-transiting-planet-ever/ |
| 1         | e09aa5d7ad8169e74f18bd9532bf61d1 | https://cs531-f22.github.io/                                                             |
| 0         | c29a2af24042e73fced3295349842df8 | https://alertcarolina.unc.edu/                                                           |
| 0.875     | bfcbd7c748d59fdbc5577435671dc5b1 | https://www.odu.edu/                                                                     |
| 1         | b100a58b97c7294b6f7f09a3f912a3a0 | https://www.defense.gov/Legal-Administrative/Privacy-Security/                           |

Q: Briefly compare and contrast the rankings produced in Q2 and Q3.

## Answer

### Basis of Ranking:

Q2 relies on content analysis, specifically the TF-IDF score, which measures how important a word is within a document relative to other documents in a corpus.
Q3, on the other hand, ranks pages based on PageRank, which evaluates the importance of a webpage based on its link structure.

### Value Representation:

In Q2, the TF-IDF values directly reflect the frequency of the term "Time" and its relative importance across all documents, with higher values indicating a stronger focus on the term.
In Q3, the PageRank values indicate the relative credibility and importance of a webpage in terms of its link structure, regardless of the content.

### Focus of the Rankings:

Q2 is focused on content relevance of the term "Time" within the documents, while Q3 is based on the authority of the pages in the web ecosystem.

### Conclusion:

The rankings produced in Q2 give insight into how central the term "Time" is in the context of individual documents, while those from Q3 focus on the importance of the web pages themselves based on their backlinks. These two rankings measure entirely different aspects: content relevance versus webpage authority.
