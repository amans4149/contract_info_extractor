For all errors related to NLTK, pls do the following

 echo -e "export LC_ALL=en_US.UTF-8\nexport LANG=en_US.UTF-8" >> ~/.bash_profile && source ~/.bash_profile
 
Added this:
 For AWS comprehend set-up:
 
1. -> brew install awscli
2. -> pip install boto3
3. -> aws configure - 
4. for access key (get it from AWS account),  region (choose it from available regions for Comprehend (ex: eu-west-1), 
output format: json
5. -> Copy the three lines of python code from here: https://docs.aws.amazon.com/comprehend/latest/dg/get-started-api-entities.html#get-started-api-entities-python
Remember to replace region with ‘eu-west-1’ always