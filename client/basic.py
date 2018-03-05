import dns.resolver

my_resolver = dns.resolver.Resolver()

# 8.8.8.8 is Google's public DNS server
my_resolver.nameservers = ['129.21.135.19']

answer = my_resolver.query('google.com')
print answer