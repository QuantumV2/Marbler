import sys
import copy
def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))
class Interpreter:
    def __init__(self):
        self.register = 0
        self.stack = []
        self.ip = [0,0]
        self.dir = [0,0]
        self.grav = [0,1]
        self.is_running = False
        self.code = []
        self.in_pipe = False
        self.pipechars = "_|^v<>"
        self.commands = {
            "+": self.do_add,
            "-": self.do_sub,
            "*": self.do_mul,
            ":": self.do_div,
            "%": self.do_mod,
            "$": self.do_pop,
            "=": self.do_equ,
            "r": self.do_rev,
            "s": self.do_swp,
            "d": self.do_dup,
            "b": self.do_siz,
            "&": self.do_prg,
            "~": self.do_rrg,
            "/": self.do_slf,
            "\\":self.do_srg,
            "]": self.do_spr,
            "[": self.do_spl,
            #"A": self.do_tub,
            "_": self.do_hpi,
            "|": self.do_vpi,
            "<": self.do_lft,
            ">": self.do_rgt,
            "^": self.do_nrt,
            "v": self.do_sth,
            "\"":self.do_pst,
            "`": self.do_pnm,
            ".": self.do_inn,
            ",": self.do_ins,
            "!": self.do_jmp,
        }
    def do_slf(self):

        self.dir = [-1, 0]
    def do_srg(self):
        self.dir = [1, 0]
    def do_spr(self):
        if self.dir[0] > 0:
            self.dir[0] *= -1
    def do_spl(self):
        if self.dir[0] < 0:
            self.dir[0] *= -1
    def do_tub(self):
        if self.register == 0:
            #self.ip[1] -= 1
            #print("ENCOUNTER")
            self.dir = [0,-1]
            self.grav = [0,0]
            
        else:
            return
    def do_hpi(self):
        pass
    def do_vpi(self):
        pass
    def do_lft(self):
        self.dir = [-1,0]
    def do_rgt(self):
        self.dir = [1,0]
    def do_nrt(self):
        self.dir = [0,-1]
    def do_sth(self):
        self.dir = [0,1]

    def reverse_array_operation(self,code):
        height = len(code[0]) if code else 0
        width = len(code)
        reversed_code = [['' for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                reversed_code[y][x] = code[x][y]

        return reversed_code
    def ip_tick(self):
        
        next_pos = self.move(self.ip, self.grav)
        oor = self.out_of_range(next_pos, 0,0,len(self.code),len(self.code[0]))
        if oor:
            self.is_running = False
        #print(oor)
        #print(self.ip, self.grav, next_pos)
        if not oor:
            if not self.is_colliding(next_pos, self.code):
                self.ip = next_pos
        next_pos = self.move(self.ip, self.dir)
        oor = self.out_of_range(next_pos, 0,0,len(self.code),len(self.code[0]))
        if oor:
            self.is_running = False
        #print(next_pos)
        if not oor:
            if not self.is_colliding(next_pos, self.code):
                self.ip = next_pos
            else:
                self.dir = [0,0]
    def out_of_range(self, pos, minx,miny,maxx,maxy):
        return pos[0] < minx or pos[1] < miny or pos[0] > maxx-1 or pos[1] > maxy-1
    def print_visual(self):
        newcode = copy.deepcopy(self.code)
        newcode[self.ip[0]][self.ip[1]] = "o"
        newcode = self.reverse_array_operation(newcode)
        for row in newcode:
            print(*row, sep='')
        print("\n")
        #print(self.code)
                    
    def find_ip_start(self,code):
        for i in range(len(code)):
            for j in range(len(code[0])):
                if code[i][j] == "o":
                    self.ip = [i,j]
                    code[i][j] = " "
                    return
    def run(self, code):
        self.find_ip_start(code)
        sys.set_int_max_str_digits(0)
        self.is_running = True
        self.code = code
        while self.is_running:
            
            if self.out_of_range(self.ip, 0,0,len(code),len(code[0])):
                self.is_running = False
            inst = code[self.ip[0]][self.ip[1]]
            inst_above = code[self.ip[0]][clamp(self.ip[1]-1, 0, len(code[0]))]
            if inst.isnumeric():
                self.stack.append(int(inst))
            if inst in self.commands:
                self.commands[inst]()
            if inst_above == "A" or inst == "A":
                
                
                self.do_tub()
            if not self.in_pipe and inst in self.pipechars:
                self.in_pipe = True
                self.grav = [0,0]
                self.dir = [0,0]
            if self.in_pipe and inst in " ":
                self.in_pipe = False
                self.grav = [0,1]
                self.dir = [0,0]
            #self.print_visual()
            self.ip_tick()
            
            #print(self.code[self.ip[0]][self.ip[1]], self.ip, self.dir, self.grav, self.stack)
    def util_popstack(self, default=0):
        if len(self.stack) <= 0:
            return default
        return self.stack.pop()
    def util_peekstack(self, val):
        if len(self.stack) <= 0 or len(self.stack) < val - 1:
            return 0
        return self.stack[val]
    def is_colliding(self, pos, code ):
        return code[pos[0]][pos[1]] == "#"
    def move(self, arr1, arr2):
        return [arr1[0]+arr2[0],arr1[1]+arr2[1]]
    def do_pop(self):
        self.util_popstack()
    def do_dup(self):
        val = self.util_peekstack(-1)
        self.stack.append(val)
    def do_swp(self):
        a = self.util_popstack()
        b = self.util_popstack()
        self.stack.append(a)
        self.stack.append(b)
    def do_rev(self):
        if not self.stack:
            return
        self.stack = self.stack[::-1]
    def do_add(self):
        self.stack.append( self.util_popstack() + self.util_popstack())
    def do_sub(self):
        a = self.util_popstack()
        b = self.util_popstack()
        self.stack.append( b - a)
    def do_mul(self):
        self.stack.append(self.util_popstack() * self.util_popstack(default=1))
    def do_div(self):
        a = self.util_popstack()
        if a  == 0:
            raise ZeroDivisionError("Operand A is 0")
        b = self.util_popstack(default=1)
        self.stack.append( b // a)
    def do_mod(self):
        a = self.util_popstack()
        b = self.util_popstack()
        self.stack.append( b % a)
    def do_equ(self):
        a = self.util_popstack()
        b = self.util_popstack()
        self.stack.append( int(b == a) )
    def do_prg(self):
        val = self.util_popstack()
        self.register = val
    def do_rrg(self):
        self.stack.append(self.register)
        self.register = 0
    def do_pst(self):
        print(chr(self.util_popstack()), end='')
    def do_pnm(self):
        print(self.util_popstack(), end='')
    def do_siz(self):
        self.stack.append(len(self.stack))
    def do_jmp(self):
        if self.util_popstack() == 0:
            self.ip_tick()
        else:
            return
    def do_ins(self):
        inp = input()
        for char in inp[::-1]:
            self.stack.append(ord(char))
    def do_inn(self):
        inp = int(input())
        self.stack.append(inp)
