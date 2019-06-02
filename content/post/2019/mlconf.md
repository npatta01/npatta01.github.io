---
title: Conference Notes  - MLConf 2019
date: 2019-03-31
tags: 
    - conferences
    - notes
categories:
    - conferences
---


On March, I attended the machine learning conferene [ML Conf](https://mlconf.com/blog/mlconf-nyc-2019-speaker-resources/) in NYC.


Here are links shared from the conferences:      
- [Slides](https://www.slideshare.net/SessionsEvents)       
- [Book Discount (40%)](https://mlconf.com/blog/    tweet-for-a-chance-to-win-free-books-at-mlconf-nyc-this-friday/)  ctwmlconfny19   
- [Speaker Resources](https://mlconf.com/blog/mlconf-nyc-2019-speaker-resources/)         
- [Videos](https://www.youtube.com/channel/UCjeM1xxYb_37bZfyparLS3Q/videos)     


Here are a list of my favorite talks.
<!--more-->

**Augmenting Mental Health Care in the Digital Age: Machine Learning as a Therapist Assistant (Talkspace)**     
- [Slides](https://www.slideshare.net/SessionsEvents/niels-bantilan-augmenting-mental-health-care-in-the-digital-age-machine-learning-as-a-therapist-assistant) ,   [Video](https://www.youtube.com/watch?v=aq0AhbvxBkc)    
- talked how to detect "crisis" in communications    
- trained models from proxy data and mental health subreddits ( r/mentalhealth,
r/physcology, r/bipolar)     
- Multi task learning: one model trains/predicts crisis risk label, subreddit label, primary diagnosis    
- how internal stakeholders evaluate models using Lime and ELI5   
- stack: scikit-learn, pytorch, ELi5, Lime, dash, aws, jupyterhub, redshift, sagemaker, plotly, dash    
- speakers third talk in an event; company paid for him and two other
coworkers to attend   


**Putting the Tech in Biotech: Challenges and Opportunities in Application of AI in Healthcare (Amgen)**     
- How Amgen uses ML.    
- Identify fractures use computer vision  
- using clinical icd embeddings


**Machine Learning to Detect Illegal Online Sales of Prescription Opioids (Intuit)**     
- [Slides](https://www.slideshare.net/SessionsEvents/janani-kalyanam-machine-learning-to-detect-illegal-online-sales-of-prescription-opioids) , [Video](https://www.youtube.com/watch?v=q31PvJmJxjo)     
- Detect sales of opiods from online pharmacies by using twitter's public
streaming api for 5 months.         
- Used lda to train  a topic model to identify tweets from those pharmacies
.     


**Using Network Analysis to Detect Kickback Schemes Among Medical Providers (Elder Research)**     
- [Slides](https://www.slideshare.net/SessionsEvents/leanna-kent-using-network-analysis-to-detect-kickback-schemes-among-medical-providers) , [Video](https://www.youtube.com/watch?v=G9qAbLnsMAE)     
- Framed Kickback as a graph connectivity problem.     
- 9 of the 12 doctors they identified is actively being investigated    

**Building Machine Learning Models with Strict Privacy Boundaries (Slack)**      
- [Slides](https://www.slideshare.net/SessionsEvents/renaud-bourassa-building-machine-learning-models-with-strict-privacy-boundaries) , [Videos](https://www.youtube.com/watch?v=HIKpXVc1mpo)     
- If u build a word2vec model on all slack communication, word similarity
might reveal secret project keywords.     
- Talked about how to train one model but at runtime use different params    


**Recommendations in a Marketplace: Personalizing Explainable Recommendations with Multi-objective Contextual Bandits: (Spotify)**       
- [Slides](https://www.slideshare.net/SessionsEvents/rishabh-mehrotra-recommendations-in-a-marketplace-personalizing-explainable-recommendations-with-multiobjective-contextual-bandits) ,  [Video](https://www.youtube.com/watch?v=KoMKgNeUX4k)
- Talked about training models that have different objective functions (music that user likes, promoting new artists....)      
- Very detailed slides (90+)      


**Representations from natural language data: successes and challenges: (Google)**       
- [Slides](https://www.slideshare.net/SessionsEvents/emily-pitler-representations-from-natural-language-data-successes-and-challenges-138567293) , [Video](https://www.youtube.com/watch?v=tXyEO1dFtT8)     
- Decent overview of what BERT is.      
- Before BERT , people were training different model architectures for different nlp tasks ( NER, Q/A, Intent)


**Teaching a Machine to Code (Microsoft)**    
- [Slides](https://www.slideshare.net/SessionsEvents/neel-sundaresan-teaching-a-machine-to-code) , [Video](https://www.youtube.com/watch?v=nsmhtvZquvM)     
- Some of the models that power visual studio code.     
- Method suggestion models (<5mb non dl model 50% accuracy; 78% accuracy for deep learning 40MB)    


**Increasing the Impact of AI Through Better Software (Facebook)**     
- [Slides](https://www.slideshare.net/SessionsEvents/soumith-chintala-increasing-the-impact-of-ai-through-better-software) ,  [Video](https://www.youtube.com/watch?v=uEpS9L_w6mc)    
- Where facebook uses ML. (Social recommendation, machine translation, accessibility for images, crisis text line)     
- Responses to facebook posts, include people offering to help self harm :(    
- Decent overview of pytorch   

**Reducing Operational Barriers to Model Training (Sigopt)**      
- [Slides](https://www.slideshare.net/SessionsEvents/alexandra-johnson-reducing-operational-barriers-to-model-training) , [Video](https://www.youtube.com/watch?v=NOK19qOu2_I)   
- Product seems similar to dataiku/datarobot. But uses kubernetes

**Deep Learning Applications to Online Payment Fraud Detection (Paypal)**      
- [Slides](https://www.slideshare.net/SessionsEvents/nitin-sharma-deep-learning-applications-to-online-payment-fraud-detection) , [Videos](https://www.youtube.com/watch?v=M1iKFlERRWk)    
- Didn't fully follow.     
- Seemed to use LSTMS, GANS, Auto encoders