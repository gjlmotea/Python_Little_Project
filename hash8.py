import hashlib
import codecs
import base64

#703 45840272
#711 63195996
#710 90168086
#709 13553694
temp = base64.b64encode(bytes('711', 'utf-8'))

s_list = [str(temp), '711', '0711']
for s in s_list:
    print(int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % (10**8))
    print(int(hashlib.sha1(s.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    print(int(hashlib.md5(s.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    print(int(hashlib.sha224(s.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    print(int(hashlib.sha384(s.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    print(int(hashlib.sha512(s.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    #print(int(hashlib.new('ripemd160')(s.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
    #print(int(s)*2654435761 % (2^32))

hash = hashlib.md5()
hash.update(b"711")

print(hash.digest())
print(hash.hexdigest())
