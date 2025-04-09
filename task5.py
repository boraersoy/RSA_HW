import hashlib
import random
from typing import List
import numpy as np
import sys
from cryptography.fernet import Fernet

def generate_user_ids(user_count: int) -> List[int]:
    return np.random.randint(low=sys.maxsize // 10, high=sys.maxsize, size=user_count).tolist()

# assume student keys are pre-shared
class Instructor:
    def __init__(self, pre_shared_keys):
        self.ids = None
        self.encrypted_ids = None
        self.pre_shared_keys = pre_shared_keys
        
    def generate_user_ids(self, user_count: int):
        self.ids = generate_user_ids(user_count)
        
    def _create_mapping(self):
        self.student_id_map = {key: self.ids[i] for i, key in enumerate(self.pre_shared_keys.keys())}
        self.encrypted_ids = {key: None for key in self.pre_shared_keys.keys()}
        
        
    def create_class(self, student_count: int):
        if len(self.pre_shared_keys) != student_count:
            raise ValueError("Number of pre-shared keys must match student count")
        self.generate_user_ids(student_count)
        self._create_mapping()
        for i, student in enumerate(self.pre_shared_keys.keys()):
            self.student_id_map[student] = self.ids[i]
            self.encrypted_ids[student] = self.encrypt_id(student, self.ids[i])
        
    def encrypt_id(self, student: str, anon_id: int) -> bytes:
            key = self.pre_shared_keys[student]
            fernet = Fernet(key)
            id_bytes = str(anon_id).encode('utf-8')
            encrypted_id = fernet.encrypt(id_bytes)
            return encrypted_id
            
    def verify_submission(self, submitted_id: int) -> bool:
            return submitted_id in self.ids
        
        
class Student:
    def __init__(self, name: str, key: bytes):
        self.name = name
        self.key = key
        self.anon_id = None

    def receive_encrypted_id(self, encrypted_id: bytes):
        fernet = Fernet(self.key)
        id_bytes = fernet.decrypt(encrypted_id)
        self.anon_id = int(id_bytes.decode('utf-8'))

    def submit_work(self) -> int:
        if self.anon_id is None:
            raise ValueError("Student has not received an ID yet")
        return self.anon_id


if __name__ == "__main__":
    pre_shared_keys = {
        "Alice": Fernet.generate_key(),
        "Bob": Fernet.generate_key(),
        "Charlie": Fernet.generate_key()
    }

    instructor = Instructor(pre_shared_keys)
    students = {name: Student(name, key) for name, key in pre_shared_keys.items()}

    instructor.create_class(3)

    for student_name, encrypted_id in instructor.encrypted_ids.items():
        students[student_name].receive_encrypted_id(encrypted_id)
        print(f"{student_name} received anon ID: {students[student_name].anon_id}")

    alice = students["Alice"]
    submitted_id = alice.submit_work()
    print(f"Alice submits work with ID: {submitted_id}")
    is_valid = instructor.verify_submission(submitted_id)
    print(f"Is submission valid? {is_valid}")

    fake_id = 123456789
    print(f"Testing fake ID {fake_id}: {instructor.verify_submission(fake_id)}")