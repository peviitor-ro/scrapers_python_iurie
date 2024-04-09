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
    jobs_type = ['hybrid', 'remote', 'on-site', 'hibrid', 'office-based']
    lower_sentance = sentence.lower()
    
    types = set([jobtype for jobtype in jobs_type if jobtype in lower_sentance])
    
    # return by default on-site if function is called with '
    if  len(types) == 0: 
        types = ['on-site'] 
        
    #check if word hibrid is present and replace it with hybrid
    if 'hibrid' in types:
        types.remove('hibrid')
        types.add('hybrid')
        
    #check if office-based then remove and add on-site
    if 'office-based' in types:
        types.remove('office-based')
        types.add('on-site')
    
    types = list(types)
    # check if aditional argument was added then add it to a list 
    if len(kwargs)>0:
        add_job_type = [''.join(map(str,kwargs))]
        types.extend(add_job_type)
        
    return types

# print(get_job_type('mama tama on-site', 'hibrid'))