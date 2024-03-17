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
    
    if  len(sentence)>1:
        types =  [jobtype for jobtype in jobs_type if jobtype in sentence.lower()]
    else:
        types = ['on-site'] 
   
    return list(set(types))
