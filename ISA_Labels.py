REGISTERS = ["sp", "fp"]  + [
    "r" + str(i) for i in range(14)
] 

INSTRUCTIONS = [
    None, # no opcode 0
    "ldi.l",
    "mov",
    "jsra",
    "ret",
    "add",
    "push",
    "pop",
    "lda.l",
    "sta.l",
    "ld.l",
    "st.l",
    "ldo.l",
    "sto.l",
    "cmp",
    "nop",
    "sex.b",
    "sex.s",
    "zex.b",
    "zex.s",
    "umul.x",
    "mul.x",
    None, None, None, # no opcodes 0x16 to 0x19
    "jsr",
    "jmpa",
    "ldi.b",
    "ld.b",
    "lda.b",
    "st.b",
    "sta.b",
    "ldi.s",
    "ld.s",
    "lda.s",
    "st.s",
    "sta.s",
    "jmp",
    "and",
    "lshr",
    "ashl",
    "sub",
    "neg",
    "or",
    "not",
    "ashr",
    "xor",
    "mul",
    "swi",
    "div",
    "udiv",
    "mod",
    "umod",
    "brk",
    "ldo.b"
    "sto.b",
    "ldo.s",
    "sto.s"
]

#: Special instructions for SECCON CTF
INSTRUCTIONS[0x16] = "SETRSEED"
INSTRUCTIONS[0x17] = "GETRAND"

#:    Type Address
#: 11 xxxx VVVVVVVVVV
BRANCH_INSTRUCTIONS = [
    "beq",
    "bne", 
    "blt",
    "bgt",
    "bltu",
    "bgtu", 
    "bge",
    "ble",
    "bgeu",
    "bleu",
]

SPECIAL_INSTRUCTIONS = [
    "inc",
    "dec",
    "gsr",
    "ssr"
]


#: 
#: OPCODE    Reg1  Reg2
#: oooooooo  AAAA  BBBB
TWO_REG_INSTRUCTIONS = {
    "and", "add", "ashl", "ashr", "cmp", "div", "ld.b", "ld.l", "ld.s", "ldo.b", "ldo.l", "ldo.s", "lshr", "mod", "mov", "mul", "mul.x", "neg", "not", "or", "pop", "push", "sex.b", "sex.s", "st.b", "st.l", "st.s", "sto.b", "sto.l", "sto.s", "sub", "udiv", "umod", "umul.x", "xor", "zex.b", "zex.s"
}

#: 
#: OPCODE    Reg1 Bad
#: oooooooo  AAAA xxxx
ONE_REG_INSTRUCTIONS = {
    "jmp",
    "jsr",
    "lda.b",
    "lda.l",
    "lda.s",
    "ldi.l",
    "ldi.b",
    "ldi.s",
    "sta.b",
    "sta.l",
    "sta.s",
    #: Special instructions for SECCON CTF
    "SETRSEED",
    "GETRAND"

}

#: 
#: OPCODE    Bad
#: oooooooo  xxxxxxxx
NO_IMM_INSTRUCTIONS = {
    "brk",
    "jmpa",
    "jsra",
    "nop",
    "ret",
    "swi"
}

IMM_INSTRUCTION_16 = {
    "ldo.b",
    "ldo.l",
    "ldo.s",
    "sto.b",
    "sto.l",
    "sto.s"
}

IMM_INSTRUCTION_32 = {
    "jmpa",
    "jsra",
    "lda.b",
    "lda.l",
    "lda.s",
    "ldi.l",
    "ldi.b",
    "ldi.s",
    "sta.b",
    "sta.l",
    "sta.s",
    "swi"
}

