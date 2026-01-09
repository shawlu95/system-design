
from abc import ABC, abstractmethod
from typing import Optional

class Medium(ABC):
    @abstractmethod
    def write(self, blob: bytes) -> None:
        pass

    @abstractmethod
    def read(self) -> bytes:
        pass


class InMemoryMedium(Medium):
    def __init__(self):
        self._data = b''

    def write(self, blob: bytes) -> None:
        self._data = blob

    def read(self) -> bytes:
        return self._data
    
import struct

"""
In the Python code, we use:

struct.pack('<I', value)

and

struct.unpack_from('<I', data, offset)


to serialize and deserialize 4-byte integers. Let's break down what '<I' means and why we chose it.

struct format strings tell Python how to convert between Python values (like int) and bytes.

'I' = Unsigned 4-byte Integer

'I' stands for unsigned integer (4 bytes) (i.e., uint32)

Range: 0 to 2^32 - 1 (about 4.29 billion)

Perfect for encoding lengths of strings and number of entries

'<' = Little-endian

'<' forces little-endian byte order:

Least significant byte comes first

Example: the integer 1 → b'\x01\x00\x00\x00'
"""

class KeyValueStore:
    def __init__(self, medium: Medium):
        self.store = {}
        self.medium = medium

    def set(self, key: str, value: str) -> None:
        self.store[key] = value

    def get(self, key: str) -> Optional[str]:
        return self.store.get(key)

    def delete(self, key: str) -> None:
        self.store.pop(key, None)

    def save(self) -> None:
        blob = bytearray()
        # Write number of entries as 4-byte uint32 (little-endian)
        blob.extend(struct.pack('<I', len(self.store)))

        for key, value in self.store.items():
            key_bytes = key.encode('utf-8')
            val_bytes = value.encode('utf-8')

            blob.extend(struct.pack('<I', len(key_bytes)))
            blob.extend(key_bytes)
            blob.extend(struct.pack('<I', len(val_bytes)))
            blob.extend(val_bytes)

        self.medium.write(bytes(blob))

    def load(self) -> None:
        data = self.medium.read()
        self.store.clear()

        offset = 0
        if len(data) < 4:
            return  # No entries

        entry_count, = struct.unpack_from('<I', data, offset)
        offset += 4

        for _ in range(entry_count):
            key_len, = struct.unpack_from('<I', data, offset)
            offset += 4
            key_bytes = data[offset:offset + key_len]
            offset += key_len
            key = key_bytes.decode('utf-8')

            val_len, = struct.unpack_from('<I', data, offset)
            offset += 4
            val_bytes = data[offset:offset + val_len]
            offset += val_len
            value = val_bytes.decode('utf-8')

            self.store[key] = value

if __name__ == "__main__":
    medium = InMemoryMedium()
    store1 = KeyValueStore(medium)

    store1.set("user", "alice")
    store1.set("email", "alice@example.com")
    store1.save()

    store2 = KeyValueStore(medium)
    store2.load()

    print(store2.get("user"))   # alice
    print(store2.get("email"))  # alice@example.com
