def flsize(size):
    size_ = size
    
    if size[-2:] != ".5":
        size_ = size + '.0'
        
    if float(size) < 10:
        size_ = '0' + size
        
    print(size_)
        
flsize("5")
flsize("5.5")
flsize("9.5")
flsize("10")
flsize("10.5")
flsize("15")
flsize("15.5")