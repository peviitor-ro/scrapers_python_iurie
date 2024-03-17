#
#
#
# Function to get type of job;
#
#

def get_job_type(sentence: str ,**kwargs) -> str:
    '''
        this func return  a list of job types mentioned in the sendance;
        **kwargs : Additional keywords arguments.
            jobs_type (list):  Additional job types to consider
    '''
    jobs_type = ['hybrid', 'remote', 'on-site']#job_type.lower()
    jobs_type.extend(kwargs.get('jobs_type', []))
    
    #chec if word hibrid is present and replace it with hybrid
    if 'hibrid' in sentence.lower():
        hibrid_sentence = sentence.lower().replace('hibrid', 'hybrid')
        types =  [jobtype for jobtype in jobs_type if jobtype in hibrid_sentence.lower()]
    else:
        types =  [jobtype for jobtype in jobs_type if jobtype in sentence.lower()]
    
    if  len(types) == 0:
        types = ['on-site'] 
   
    return list(set(types))


