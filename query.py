#!/usr/bin/env python3

import dns.resolver

my_resolver = dns.resolver.Resolver()

# 8.8.8.8 is Google's public DNS server
my_resolver.nameservers = ['127.0.0.1']

url = "a"
for i in range(1, 300):
    answer = my_resolver.query(url+".")
    url += "a"
    print(i)
