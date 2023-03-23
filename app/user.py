#!/usr/bin/env python3

class User:
    def __init__(self, name, address, email, password):
        self.name = name
        self.address = address
        self.email = email
        self.password = password
        self.smart_senser_measurements = []
    
    
    @property
    def measurements(self):
        return self.smart_senser_measurements

        