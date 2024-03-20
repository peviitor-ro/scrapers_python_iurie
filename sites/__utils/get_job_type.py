#
#
#
# Function to get type of job;
#
#

def get_job_type(sentence: str ,**additional_job_types) -> str:
    """
    This func return  a list of job types mentioned in the sentence;
    **additional_job_types : Additional keywords arguments.
    """
    jobs_type = ['hybrid', 'remote', 'on-site', 'hibrid']
    jobs_type.extend(additional_job_types)
    lower_sentance = sentence.lower()
    
    types = set([jobtype for jobtype in jobs_type if jobtype in lower_sentance])
    
    # return by default on-site if function is called with '
    if  len(types) == 0: 
        types = ['on-site'] 
        
    #check if word hibrid is present and replace it with hybrid
    if 'hibrid' in types:
        types.remove('hibrid')
        types.add('hybrid')
    
    return list(types)


