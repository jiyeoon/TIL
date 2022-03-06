class Solution:
    def calculate(self, s):
		# this is to split the input into tokens
        s = filter(None, re.split(r'([+\-*/()\$])', (s + '$').replace(' ', '')))
        return self.do_calculate(s)
    
    def do_calculate(self, s):
        stack = []
        num, sign = 0, '+'
        
        def calculate_top():
            if sign == '+':
                stack.append(num)
            if sign == '-':
                stack.append(-num)
            if sign == '*':
                stack[-1] *= num
            if sign == '/':
                stack[-1] = int(stack[-1] / num)
                
        while c := next(s):
            if c.isdigit():
                num = int(c)
            elif c == '(':
                num = self.do_calculate(s)
            elif c in ')$':
                calculate_top()
                return sum(stack)
            elif c in '+-*/':
                calculate_top()
                sign = c