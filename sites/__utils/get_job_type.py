#
#
#
# Function to get type of job;
#
#

def get_job_type(sentence: str ,*kwargs) -> str:
    """
    This func return  a list of job types mentioned in the sentence;
    *kwargs : Additional keywords arguments for job type that is not mentioned.
    """
    jobs_type = ['hybrid', 'remote', 'on-site', 'hibrid']
    lower_sentance = sentence.lower()
    
    types = set([jobtype for jobtype in jobs_type if jobtype in lower_sentance])
    
    # return by default on-site if function is called with '
    if  len(types) == 0: 
        types = ['on-site'] 
        
    #check if word hibrid is present and replace it with hybrid
    if 'hibrid' in types:
        types.remove('hibrid')
        types.add('hybrid')
    
    types = list(types)
    
    if len(kwargs)>0:
        add_job_type = [''.join(map(str,kwargs))]
        types.extend(add_job_type)
        
    return types
