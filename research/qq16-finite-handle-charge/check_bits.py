"""Independent expansion of the sequential access macro into bit instructions."""

def ensure(ok,why):
    if not ok:raise ValueError(why)


def serial_access(words,width,address,replacement=None):
    ensure(words and width>0 and 0<=address<len(words),'bit test domain')
    ensure(all(0<=x<2**width for x in words),'bit test width')
    tape=[(word>>bit)&1 for word in words for bit in range(width)]
    index=[0]*width;wanted=[(address>>i)&1 for i in range(width)]
    register=[0]*width;head=0;steps=0
    # Initialize each finite index bit explicitly.
    for bit in range(width):index[bit]=0;steps+=1
    for position in range(len(words)):
        equal=True;steps+=1
        for bit in range(width):
            test=index[bit]==wanted[bit];steps+=1
            equal=equal and test;steps+=1
        steps+=1  # Boolean branch
        if equal:
            for bit in range(width):
                if replacement is None:
                    symbol=tape[head+bit];register[bit]=symbol
                else:
                    symbol=(replacement>>bit)&1;tape[head+bit]=symbol
                steps+=2
        for bit in range(width):head+=1;steps+=1
        carry=1
        for bit in range(width):
            previous=index[bit];index[bit]=previous ^ carry;carry=previous & carry
            steps+=8  # fixed eight-bit-operation increment, including padding
        steps+=1  # bounded loop branch
    while head:head-=1;steps+=1
    steps+=1  # halt
    output=[sum(tape[j*width+i]<<i for i in range(width)) for j in range(len(words))]
    return output,sum(register[i]<<i for i in range(width)),head,steps


def verify(access_price):
    checks=0
    for length in range(1,13):
        width=max(1,length.bit_length())
        values=[(i*3+1)%(1<<width) for i in range(length)]
        for address in range(length):
            after,read,head,count=serial_access(values,width,address)
            ensure(after==values and read==values[address] and head==0,'serial read endpoint')
            ensure(count==access_price(length,width),'independent read instruction count')
            replacement=(values[address]+1)%(1<<width)
            after,_,head,count=serial_access(values,width,address,replacement)
            expected=values.copy();expected[address]=replacement
            ensure(after==expected and head==0,'serial write endpoint')
            ensure(count==access_price(length,width),'independent write instruction count')
            checks+=2
    # Address movement cannot be omitted: even address zero pays the full scan.
    _,_,_,count=serial_access([0]*8,4,0)
    ensure(count>4*8 and count!=1,'random access tariff rejected')
    return checks
