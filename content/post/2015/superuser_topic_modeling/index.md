---
title: Topic Modeling on the Super User Forum

date: 2015-10-23

categories:
- nlp
tags:
- nlp
- topic modeling
- gensim

---


Lets imagine you are given a dump of a user forum , or of someone's email, how do you analyze the contents?        

One way might be to look at top words in the whole corpus.


<!--more-->

However, looking at word counts without context might not be too meaningful. Words that co-occur together might signal a theme/concept/topic.

In the world of natural language processing, there is technique called [Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation).

From a high level, LDA assumes a document contains a bunch of topics and each topic contains a bunch of words that co-occur.

Below is my analysis on the [SuperUser forum](http://superuser.com/) using the amazing python tool [gensim](https://radimrehurek.com/gensim/).


# SuperUser Analysis


I asked gensim to build a model that tried to find 8 topics. Here are the topics it learned.


## Topics
Here is are 8 topics it learned.

- file,files,text,like
- network, server,router,connection
- windows, screen , problem, time
- card, device, usb, driver
- windows user, folder, account
- drive, windows, disk, boot
- would, like, data, excel
- error, command, file, root

Looking at the list of top words, it can be difficult to assign a label.

## Labels
After looking at just the words, it can be difficult to assign a label.

One way to identify the labels, is look at documents that score the highest for a topic and assign a label.
After looking at several sample docs, here are the labels and sample question titles for the strongest docs.


- *Word Woes*
[Automatically resize picture/image in Word](http://superuser.com/questions/158626)
[Word 2010 generated PDF: corrupted copy-paste and search text](http://superuser.com/questions/654436)

- *Networking Woes*
[How can I set a static ip address on a DHCP network?](http://superuser.com/questions/493823)
[Getting LAN clients to use IPv6 tunnel of Debian router](http://superuser.com/questions/795133)

- *Display Woes*
[How can I display the Windows 8 Start Screen on a secondary monitor?](http://superuser.com/questions/491258)
[How do I force prompts to display on my primary monitor in Windows?](http://superuser.com/questions/753259)


- *Computer Concerns*
[lshw tells me my processor is a 64 bits but my motherboard has a 32 bits width](http://superuser.com/questions/490589/lshw-tells-me-my-processor-is-a-64-bits-but-my-motherboard-has-a-32-bits-width)
[Nvidia 8500GT Won't display video on Asus M2A-VM](http://superuser.com/questions/697903/nvidia-8500gt-wont-display-video-on-asus-m2a-vm)

- *Outlook/ Email Woes*
[Making MSN Explorer the default email program on Vista](http://superuser.com/questions/36907/making-msn-explorer-the-default-email-program-on-vista)
[Outlook 2010 send address not defaulting selected inbox](http://superuser.com/questions/796598/outlook-2010-send-address-not-defaulting-selected-inbox)

- *Partition Woes*
[Windows install on GPT with multiple drives](Windows install on GPT with multiple drives)
[How to remove an old windows installation that is inside the System partition?](http://superuser.com/questions/625077/how-to-remove-an-old-windows-installation-that-is-inside-the-system-partition)

- *Excel/ Word Hacks*
[Representing Specific Data from a Dynamic Database (Array) in Excel](http://superuser.com/questions/748449/representing-specific-data-from-a-dynamic-database-array-in-excel)
[http://superuser.com/questions/789091/excel-table-copy-wrong-formula-with-newly-inserted-rows](http://superuser.com/questions/789091/excel-table-copy-wrong-formula-with-newly-inserted-rows)

- *Video Woes*
[Can't get ffmpeg to use frei0r on OSX (through homebrew)](http://superuser.com/questions/396834/cant-get-ffmpeg-to-use-frei0r-on-osx-through-homebrew)
[ffmpeg: Pipe input error](http://superuser.com/questions/479063/ffmpeg-pipe-input-error)


## New instance
Now that we have a topic model, lets see how it works for identifying topics for an unseen document.

{% blockquote outlook separation of 2 email accounts http://superuser.com/questions/991960/outlook-separation-of-2-email-accounts %}
I have 2 email accounts on outlook : account A and account B.

When i send a message or receive any msg on account B, the same msg appears on account A. As far as account A is concerned, when i send any msg from this account or when i receive sth, it doesn't appear on the account B.

i would like separate these 2 accounts so that they work independently.

I was looking for an answer and i found that it shouldn't be set on outlook but on http://www.windowslive.fr/livemail/ .

If you have any suggestions how to do it or any advice, I would be very greatful!
{% endblockquote %}


Result:

Outlook/Email Woes (0.85)
Excel/Word hacks (0.08)
Video Woes (0.05)

From the result, we see that the strongest topic (Email) best describes the email.

However, we see that the two other strongest topics don't really describe the document.

This is most likely due to the model not trained enough or me coming from the label.

## Visualizations
I have deployed an instance of the site [here](https://superuser-topic-modeling.herokuapp.com/).

*Visualize all the topics and the top 4 words in them*
{% asset_img  topics.png [Topics] %}

*Visualize the words in a topic as a word cloud, and top docs for a topic*
{% asset_img  topic.png [Analysis on topic] %}

*Visualize the distribution of topics cross the corpus and similarities among topics*
{% asset_img  pca.png [Topic PCA] %}

*Analyze a new document*
{% asset_img  analyze.png [Analyze new topic] %}

# Things I need to learn more



## Evaluating Model
How to evaluate if the model has converged. How to evaluate if the number of topic is correct.
One approach seems to be [Topic perplexity](http://qpleple.com/perplexity-to-evaluate-topic-models/).

## Visualizing topics
[Ldaviz](https://github.com/benmarwick/LDAviz) implements some nice visualizations for visualizing the topic space. Need to understand that model better.

There are also other [options](https://de.dariah.eu/tatom/topic_model_visualization.html)

# Links
[Deployed Site](https://superuser-topic-modeling.herokuapp.com)
[Slide](http://www.slideshare.net/nidhinpattaniyil/topic-modelling-on-superuser-forum)
[Code](https://github.com/npatta01/superuser-topic-modeling)

{{< slideshare id="dGQh9SJb6wKIS9" >}}









# References
[gensim](https://radimrehurek.com/gensim/)
[pyLDAvis](https://github.com/bmabey/pyLDAvis)
