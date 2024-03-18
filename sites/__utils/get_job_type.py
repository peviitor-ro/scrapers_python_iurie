#
#
#
# Function to get type of job;
#
#

def get_job_type(sentence: str ,**args) -> str:
    '''
        this func return  a list of job types mentioned in the sentence;
        **args : Additional keywords arguments.
            jobs_type (list):  Additional job types to consider
    '''
    jobs_type = ['hybrid', 'remote', 'on-site']
    jobs_type.extend(args.get('jobs_type', []))
    
    #check if word hibrid is present and replace it with hybrid to solve typo 
    if 'hibrid' in sentence.lower():
        hibrid_sentence = sentence.lower().replace('hibrid', 'hybrid')
        types =  [jobtype for jobtype in jobs_type if jobtype in hibrid_sentence.lower()]
    else:
        types =  [jobtype for jobtype in jobs_type if jobtype in sentence.lower()]
    
    # return by default on-site if function is called with ''
    if  len(types) == 0: 
        types = ['on-site'] 
   # return clean data to avoid duplicates
    return list(set(types))


