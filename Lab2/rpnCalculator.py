import this


class rpnCalculator:
    
    myStack = []
    
    def pushValue(this, value):
        this.myStack.append(value)

    def popValue(this):
        return this.myStack.pop()

    def add(this):
        a = this.myStack.pop()
        b = this.myStack.pop()
        this.myStack.append( a + b)

    def sub(this):
        a = this.myStack.pop()
        b = this.myStack.pop()
        this.myStack.append( a - b)

if __name__== "__main__":
    c = rpnCalculator()
    c.pushValue(12)
    c.pushValue(2)
    c.add()
    print("\n\n")
    print(c.popValue()) # print 14!!