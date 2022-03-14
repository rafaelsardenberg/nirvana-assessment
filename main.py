from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view

import requests

#By the Facade Pattern, we improve the readability and usability of the code by masking interaction with more complex components behind a single API
#Depending the type parameter, the code decides which is the best child class to invoke
@api_view(['GET'])
def facadeApi(request, member_id, type):
    response1 = requests.get('https://api1.com?member_id=' + member_id).json()
    response2 = requests.get('https://api2.com?member_id=' + member_id).json()
    response3 = requests.get('https://api3.com?member_id=' + member_id).json()

    if type=='avg': api = AvgApi(response1, response2, response3)
    elif type=='med': api = MedApi(response1, response2, response3)
    elif type=='min': api = MinApi(response1, response2, response3)
    elif type=='max': api = MaxApi(response1, response2, response3)
    else:
        return Response('Invalid type parameter.', status=HTTP_400_BAD_REQUEST)
        
    response = api.coalesce()
    return Response(response, status=HTTP_200_OK)
        
#With this kind of inheritance, we create related classes that will share a common interface that will be defined in the BaseApi class. Derived classes specialize the interface by providing a particular implementation where applies.
class BaseApi:
    def __init__(self, r1, r2, r3):
        self.response1 = r1
        self.response2 = r2
        self.response3 = r3
    
    def coalesce(self):
        return None
    
class AvgApi(BaseApi):
    def __init__(self, r1, r2, r3):
        super().__init__(r1, r2, r3)
        
    def coalesce(self):
        deductible = (self.response1.deductible + \
            self.response2.deductible + \
            self.response3.deductible)/3
            
        stop_loss = (self.response1.stop_loss + \
            self.response2.stop_loss + \
            self.response3.stop_loss)/3
            
        oop_max = (self.response1.oop_max + \
            self.response2.oop_max + \
            self.response3.oop_max)/3
            
        return {'deductible': deductible, 'stop_loss': stop_loss, 'oop_max': oop_max}
        
class MedApi(BaseApi):
    def __init__(self, r1, r2, r3):
        super().__init__(r1, r2, r3)
        
    def coalesce(self):
        arr = [self.response1.deductible, \
            self.response2.deductible, \
            self.response3.deductible]
        arr.sort()
        deductible = arr[1]
        
        arr = [self.response1.stop_loss, \
            self.response2.stop_loss, \
            self.response3.stop_loss]
        arr.sort()
        stop_loss = arr[1]
        
        arr = [self.response1.oop_max, \
            self.response2.oop_max, \
            self.response3.oop_max]
        arr.sort()
        oop_max = arr[1]
            
        return {'deductible': deductible, 'stop_loss': stop_loss, 'oop_max': oop_max}     

class MinApi(BaseApi):
    def __init__(self, r1, r2, r3):
        super().__init__(r1, r2, r3)
        
    def coalesce(self):
        arr = [self.response1.deductible, \
            self.response2.deductible, \
            self.response3.deductible]
        arr.sort()
        deductible = arr[0]
        
        arr = [self.response1.stop_loss, \
            self.response2.stop_loss, \
            self.response3.stop_loss]
        arr.sort()
        stop_loss = arr[0]
        
        arr = [self.response1.oop_max, \
            self.response2.oop_max, \
            self.response3.oop_max]
        arr.sort()
        oop_max = arr[0]
            
        return {'deductible': deductible, 'stop_loss': stop_loss, 'oop_max': oop_max}     

class MaxApi(BaseApi):
    def __init__(self, r1, r2, r3):
        super().__init__(r1, r2, r3)
        
    def coalesce(self):
        arr = [self.response1.deductible, \
            self.response2.deductible, \
            self.response3.deductible]
        arr.sort()
        deductible = arr[2]
        
        arr = [self.response1.stop_loss, \
            self.response2.stop_loss, \
            self.response3.stop_loss]
        arr.sort()
        stop_loss = arr[2]
        
        arr = [self.response1.oop_max, \
            self.response2.oop_max, \
            self.response3.oop_max]
        arr.sort()
        oop_max = arr[2]
            
        return {'deductible': deductible, 'stop_loss': stop_loss, 'oop_max': oop_max}
