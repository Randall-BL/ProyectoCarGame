def binarioDecimal(binario):
    num= binario
    sumatoria=0
    i=0
    while num !=0:
        restante=num %10
        sumatoria=sumatoria+restante*(2**i)
        num=int(num/10)
        i=i+1
    return sumatoria

print(binarioDecimal(1001101011))

