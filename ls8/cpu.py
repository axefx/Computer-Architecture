"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.SP = 7
        self.reg[self.SP] = 0xf4

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        if sys.argv[1]:
            program = []
            with open(sys.argv[1]) as f:
                for line in f:
                    binary_strings = line.split('#')[0].strip()
                    if binary_strings:
                        integer_values = int(binary_strings, 2)
                        program.append(integer_values)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        ADD = 0b10100000
        RET = 0b00010001

        running = True
        while running:
            # fetch instruction pointed to by the pc
            instruction_register = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(hex(instruction_register))
            if instruction_register == HLT:
                running = False
                self.pc += 1
            elif instruction_register == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction_register == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif instruction_register == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == PUSH:
                self.reg[self.SP] -= 1
                value = self.reg[operand_a]
                address = self.reg[self.SP]
                self.ram_write(address, value)
                self.pc += 2
            elif instruction_register == POP:
                address = self.reg[self.SP]
                value = self.ram_read(address)
                self.reg[operand_a] = value
                self.reg[self.SP] += 1
                self.pc += 2
            elif instruction_register == CALL:
                # Get address of the next instruction
                previous_address = self.pc + 2
                # Push that on the stack
                self.reg[self.SP] -= 1
                address = self.reg[self.SP]
                self.ram[address] = previous_address
                # Set the PC to the subroutine address
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]
                self.pc = subroutine_addr
            elif instruction_register == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif instruction_register == RET:
                # Get return address from the top of the stack
                address = self.reg[self.SP]
                ret_address = self.ram[address]
                self.reg[self.SP] += 1
                # Set the PC to the return address
                self.pc = ret_address
            else:
                print(f"Unknown instruction {instruction_register}")
                print("{0:b}".format(instruction_register))
                running = False

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
