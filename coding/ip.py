MASK = (1 << 8) - 1 # 255

def _str_to_int(str):
    parts = str.split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IP address format")
    num = 0
    for part in parts:
        num = (num << 8) | (int(part) & MASK)
    return num

def _int_to_str(num):
    parts = []
    for _ in range(4):
        parts.append(str(num & MASK))
        num >>= 8
    return '.'.join(reversed(parts))

class IpIterator:
    def __init__(self, start_ip):
        self.current = _str_to_int(start_ip)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > 0xFFFFFFFF:
            raise StopIteration
        ip_str = _int_to_str(self.current)
        self.current += 1
        return ip_str
    
def test1():
    iterator = IpIterator("192.168.0.1")

    assert next(iterator) == "192.168.0.1"
    assert next(iterator) == "192.168.0.2"

def test2():
    iterator = IpIterator("192.168.0.255")
    assert next(iterator) == "192.168.0.255"
    try:
        next(iterator)
    except StopIteration:
        pass

class CidrIterator:
    def __init__(self, cidr):
        ip_str, prefix_length = cidr.split('/')
        self.prefix_length = int(prefix_length)

        # mask only keeps the network part
        mask = (1 << (32 - self.prefix_length)) - 1

        self.start_ip = _str_to_int(ip_str) & (~mask)
        self.end_ip = self.start_ip | mask

        self.current = self.start_ip

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.end_ip:
            raise StopIteration
        ip_str = _int_to_str(self.current)
        self.current += 1
        return ip_str
    
def test3():
    iterator = CidrIterator("192.168.0.0/24")
    assert next(iterator) == "192.168.0.0"
    assert next(iterator) == "192.168.0.1"

if __name__ == "__main__":
    test1()