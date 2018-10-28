from binaryninja import Architecture, InstructionInfo, BranchType, RegisterInfo, Endianness
from binaryninja import BinaryViewType, log_error
from binaryninja import InstructionTextToken, InstructionTextTokenType

import struct

from ISA_Labels import *
from Operand_Tokens import *

class Moxie(Architecture):
    name = "moxie"
    address_size = 4
    default_int_size = 4

    stack_pointer = 'sp'
    regs = {
        'sp':RegisterInfo('sp', 2),
        'fp':RegisterInfo('fp', 2),
        'r0':RegisterInfo('r0', 2),
        'r1':RegisterInfo('r1', 2),
        'r2':RegisterInfo('r2', 2),
        'r3':RegisterInfo('r3', 2),
        'r4':RegisterInfo('r4', 2),
        'r5':RegisterInfo('r5', 2),
        'r6':RegisterInfo('r6', 2),
        'r7':RegisterInfo('r7', 2),
        'r8':RegisterInfo('r8', 2),
        'r9':RegisterInfo('r9', 2),
        'r10':RegisterInfo('r10', 2),
        'r11':RegisterInfo('r11', 2),
        'r12':RegisterInfo('r12', 2),
        'r13':RegisterInfo('r13', 2),
    }

    def get_operands(self, instr, word):
        dst = None
        src = None

        if instr in NO_IMM_INSTRUCTIONS:
            return src, dst

        a = (word & 0xF0) >> 4
        b = word & 0xF

        if instr in ONE_REG_INSTRUCTIONS:
            dst = REGISTERS[a]

        elif instr in TWO_REG_INSTRUCTIONS:
            dst = REGISTERS[a]
            src = REGISTERS[b]

        return src, dst

    def decode_instruction(self, data, addr):
        instr = None
        length = 2
        extra = None
        src_value, dst_value = None, None
        dst_op, src_op = DEFAULT_MODE, DEFAULT_MODE
        src, dst = None, None

        if len(data) < 2:
            return instr, src, src_op, dst, dst_op, src_value, dst_value, length

        word = struct.unpack('>H', data[:2])[0]
        opcode_type = word >> 14

        if opcode_type == 0b11: # is branch
            branch_type = (word & 0x3c00) >> 10
            if branch_type < len(BRANCH_INSTRUCTIONS):
                instr = BRANCH_INSTRUCTIONS[branch_type]
            else:
                log_error('[%x] Bad branch opcode: %x' %(addr, branch_type))
                return instr, src, src_op, dst, dst_op, src_value, dst_value, length

            branch_offset = word & 0x3ff
            dst_value = (branch_offset << 1) + addr
            src_op = EMPTY_MODE
            dst_op = IMM_ADDRESS_MODE

        elif opcode_type == 0b10:
            instr = SPECIAL_INSTRUCTIONS[(word >> 12) & 0x3]

            dst = (word & 0xf00 >> 8)
            dst = REGISTERS[dst]
            dst_op = REGISTER_MODE

            src_value = word & 0xff
            src_op = IMM_INTEGER_MODE

        elif opcode_type == 0b00:
            opcode = word >> 8
            instr = INSTRUCTIONS[opcode]
            src, dst = self.get_operands(instr, word)

            if instr in IMM_INSTRUCTION_16:
                extra = struct.unpack('>H', data[2:4])[0]
                length += 2
            elif instr in IMM_INSTRUCTION_32:
                extra = struct.unpack('>I', data[2:6])[0]
                length += 4
            
            if instr in ONE_REG_INSTRUCTIONS: 
                dst_op = REGISTER_MODE
                src_op = EMPTY_MODE
                if extra:
                    src_value = extra
                    src_op = IMM_INTEGER_MODE
            elif instr in TWO_REG_INSTRUCTIONS:
                src_op = REGISTER_MODE
                dst_op = REGISTER_MODE

            elif instr in NO_IMM_INSTRUCTIONS and extra:
                src = None
                dst = None
                src_op = EMPTY_MODE
                dst_op = IMM_INTEGER_MODE
                dst_value = extra
            else:
                src_op = EMPTY_MODE
                dst_op = EMPTY_MODE

        return instr, src, src_op, dst, dst_op, src_value, dst_value, length


    def perform_get_instruction_info(self, data, addr):
        instr, src, src_op, dst, dst_op, src_value, dst_value, length = self.decode_instruction(data, addr)
        res = InstructionInfo()
        res.length = length

        if instr in {'ret'}:
            res.add_branch(BranchType.FunctionReturn)
        elif instr in BRANCH_INSTRUCTIONS:
            res.add_branch(BranchType.TrueBranch, dst_value)
            res.add_branch(BranchType.FalseBranch, addr + 16)
        elif instr == 'jsra':
            res.add_branch(BranchType.CallDestination, dst_value)
        elif instr == "jmpa":
            res.add_branch(BranchType.UnconditionalBranch, dst_value)

        return res

    def perform_get_instruction_text(self, data, addr):
        instr, src, src_op, dst, dst_op, src_value, dst_value, length = self.decode_instruction(data, addr)

        if instr is None:
            return None

        instruction_text = instr
        dst_token = None
        src_token = None

        tokens = [InstructionTextToken(InstructionTextTokenType.TextToken, '{:9s}'.format(instruction_text))]
        if dst_op != EMPTY_MODE:
            dst_token = OperandTokens[dst_op](dst, dst_value)
            tokens += dst_token
        if src_op != EMPTY_MODE:
            src_token = OperandTokens[src_op](src, src_value)

        if src_op != EMPTY_MODE and dst_op != EMPTY_MODE:
            tokens += [InstructionTextToken(InstructionTextTokenType.TextToken, ', ')]
        if src_token:
            tokens += src_token

        return tokens, length

    def perform_get_instruction_low_level_il(self, data, addr, il):
        instr, src, src_op, dst, dst_op, src_value, dst_value, length = self.decode_instruction(data, addr)

        if instr is None:
            return None
        il.append(il.unimplemented())
        return length

Moxie.register()

BinaryViewType['ELF'].register_arch(0xdf, Endianness.BigEndian, Architecture["moxie"])

