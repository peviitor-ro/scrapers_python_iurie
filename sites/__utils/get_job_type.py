#
#
#
# Function to get type of job;
#
#

def get_job_type(sentence: str ,**additional_job_types) -> str:
    """
    This func return  a list of job types mentioned in the sentence;
    **args : Additional keywords arguments.
    jobs_type (list):  Additional job types to consider
    """
    jobs_type = ['hybrid', 'remote', 'on-site', 'hibrid']
    jobs_type.extend(additional_job_types)
    
    types = set([jobtype for jobtype in jobs_type if jobtype in sentence.lower()])
    
    # return by default on-site if function is called with '
    if  len(types) == 0: 
        types = ['on-site'] 
        
    #check if word hibrid is present and replace it with hybrid to solve typo 
    if 'hibrid' in types:
        types.remove('hibrid')
        types.add('hybrid')
    
    return list(types)


