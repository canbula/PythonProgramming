def performance(func):
    def wrapper(*args, **kwargs):
        wrapper.counter += 1

        return func(*args, **kwargs)

wrapper.counter = 0
wrapper.total_time = 0  
wrapper.total_mem = 0   

    return wrapper
    
@performance
def bilge():
    print("bilge")

bilge()
bilge()

print(bilge.counter)      
print(bilge.total_time)  
print(bilge.total_mem)   
