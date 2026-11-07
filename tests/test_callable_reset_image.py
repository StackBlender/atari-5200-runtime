# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 StackBlender LLC
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from emitter import AssemblyError
from cart_owned_diagnostic_image import cart_owned_diagnostic_image
from callable_reset_image import callable_reset_image,PARENT_SHA256,RESET,ENTRY,END
from export_callable_reset_candidate import candidate,verify_checkout,EXTRA_INPUTS
ROOT=Path(__file__).resolve().parents[1]
PIN='1'*40
LEN={0x78:1,0xd8:1,0xa2:2,0x9a:1,0xa9:2,0x8d:3,0x95:2,0xca:1,0x10:2,0x9d:3,0xe8:1,0xe0:2,
     0xd0:2,0x20:3,0x18:1,0xb8:1,0xa0:2,0x90:2,0xea:1,0x6c:3,0x4c:3,0x60:1}


def boundaries(code,start,stop,follow_branch=False):
    """Independent linear decode; returns instruction start offsets from start until stop."""
    out=[];at=start
    while at<stop:
        out.append(at);at+=LEN[code[at]]
    return out


def run_reinit(image,patch_rts=True,rom_start=None):
    """Independent subset interpreter. Default: the consumer procedure (copy [reset,reset+$8A) to
    $2100, patch RTS, call +$0F). With rom_start: execute in place in ROM until RTS/JMP ($BFFE)."""
    rom=lambda a:image[a-0xf800]
    ram=bytearray(65536)
    if rom_start is None:
        for i in range(END):ram[0x2100+i]=rom(RESET+i)
        if patch_rts:ram[0x2100+END]=0x60
        pc=0x2100+ENTRY
    else:
        for i in range(2048):ram[0xf800+i]=image[i]
        pc=rom_start
    a=x=y=0;carry=zero=neg=0;overflow=1;stores=[];calls=[];steps=0
    def setnz(v):
        nonlocal zero,neg;zero=int(v==0);neg=v>>7
    while True:
        steps+=1
        if steps>2000:raise AssertionError('runaway')
        op=ram[pc];imm=ram[pc+1];word=ram[pc+1]|ram[pc+2]<<8
        if op==0xa9:a=imm;setnz(a);pc+=2
        elif op==0xa2:x=imm;setnz(x);pc+=2
        elif op==0xa0:y=imm;setnz(y);pc+=2
        elif op==0x8d:stores.append((word,a));pc+=3
        elif op==0x95:stores.append((imm+x&0xff,a));pc+=2
        elif op==0x9d:stores.append((word+x&0xffff,a));pc+=3
        elif op==0xe8:x=x+1&0xff;setnz(x);pc+=1
        elif op==0xca:x=x-1&0xff;setnz(x);pc+=1
        elif op==0xe0:v=x-imm;carry=int(x>=imm);setnz(v&0xff);pc+=2
        elif op in(0x10,0xd0,0x90):
            taken={0x10:not neg,0xd0:not zero,0x90:not carry}[op]
            pc+=2
            if taken:pc+=imm-256 if imm>127 else imm
        elif op==0x20:calls.append(word);pc+=3     # external ROM routines: returned, effects not modelled
        elif op==0x18:carry=0;pc+=1
        elif op==0xb8:overflow=0;pc+=1
        elif op==0xea:pc+=1
        elif op in(0x60,0x6c):return dict(a=a,x=x,y=y,carry=carry,overflow=overflow,stores=stores,calls=calls,pc=pc)
        else:raise AssertionError('unmodelled opcode %02x at %x'%(op,pc))


class CallableResetTests(unittest.TestCase):
    def test_only_reviewed_region_changes_and_fit_symbols_vectors(self):
        parent,before=cart_owned_diagnostic_image();data,mapping=callable_reset_image()
        self.assertEqual(hashlib.sha256(parent).hexdigest(),PARENT_SHA256)
        changed=[i for i,(o,n) in enumerate(zip(parent,data)) if o!=n]
        self.assertTrue(all(0x400<=i<0x400+0x8d for i in changed))
        self.assertEqual(data[:0x400],parent[:0x400]);self.assertEqual(data[0x48d:],parent[0x48d:])
        self.assertEqual(data[0x480:0x489],parent[0x480:0x489])           # NMI/IRQ/startup fault stubs
        self.assertEqual(data[-6:],parent[-6:]);self.assertEqual(data[0x7a0:0x7fa],b'\xff'*90)
        self.assertEqual((len(data),mapping['used'],mapping['remaining']),(2048,1560,488))
        a={x['name']:x for x in mapping['allocations']}
        self.assertEqual((a['startup']['used'],a['interrupts']['used']),(111,80))
        self.assertEqual(mapping['symbols']['reset'],0xfc00);self.assertEqual(mapping['symbols']['cart_handoff'],0xfc8a)
        self.assertEqual(mapping['symbols']['reset_reinit'],0xfc0f)
        for k in ('nmi_fault','irq_fault','startup_fault','nmi_classifier','system_vbi'):
            self.assertEqual(mapping['symbols'][k],before['symbols'][k])
        self.assertIn('callable-reset-v1',mapping['authored_capabilities'])

    def test_independent_decode_boundary_at_entry_and_position_independent_body(self):
        data,_=callable_reset_image();code=data[0x400:]
        starts=boundaries(code,0,0x6f)
        self.assertIn(ENTRY,starts)                       # +$0F begins an instruction
        self.assertEqual(code[ENTRY:ENTRY+3],bytes.fromhex('8d0ee8'))
        last=[s for s in starts if s<0x6f][-1]
        self.assertEqual(code[last:last+2],bytes([0x90,END-(last+2)]))   # BCC lands exactly on +$8A
        self.assertEqual(code[END:END+3],bytes.fromhex('6cfebf'))
        for s in starts:                                   # no absolute transfer into the copied range
            if code[s] in(0x20,0x4c,0x6c):
                target=code[s+1]|code[s+2]<<8
                self.assertFalse(0xfc00<=target<0xfc8a,hex(target))

    def test_consumer_copy_patch_and_call_falls_through_to_rts_with_clean_registers(self):
        data,_=callable_reset_image();parent,_=cart_owned_diagnostic_image()
        result=run_reinit(data)
        self.assertEqual((result['a'],result['x'],result['y'],result['carry'],result['overflow']),(0,0,0,0,0))
        self.assertEqual(result['pc'],0x2100+END)
        self.assertEqual(result['calls'],[0xfedc,0xfd80])
        # Same hardware/RAM stores, same order, as the parent's initialisation (minus the
        # entry-skipped first two MMIO writes, which the consumer path does not repeat).
        full=result['stores']
        self.assertEqual(full[0],(0xe80e,0));self.assertEqual(full[-1],(0xe80b,4))
        # parent executed in place from its own STA E80E: identical stores and calls
        old=run_reinit(parent,rom_start=0xfc0d)
        self.assertEqual(full,old['stores']);self.assertEqual(result['calls'],old['calls'])
        # real reset (no copy/patch) reaches the cartridge-indirect handoff with the same registers
        real=run_reinit(data,rom_start=0xfc0f)
        self.assertEqual(real['pc'],0xfc8a);self.assertEqual((real['a'],real['x'],real['y'],real['carry'],real['overflow']),(0,0,0,0,0))

    def test_all_three_revision_byte_values_documented_and_this_layout_selects_8a(self):
        data,mapping=callable_reset_image();layout=mapping['reset_layout']
        self.assertEqual(data[0x7f8],0xff);self.assertNotIn(data[0x7f8],(0,0x32))
        self.assertEqual((layout['reinit_entry_offset'],layout['fall_through_offset'],layout['copy_length_for_revision_byte']),(15,138,138))
        self.assertFalse(layout['nmi_enabled_by_runtime'])
        self.assertEqual(mapping['nominal_startup']['numeric_normal_instructions'],260)   # native trace: parent 257 + 3

    def test_export_identity_manifest_and_input_pin_verification(self):
        data,mapping,text=candidate(PIN);manifest=json.loads(text);report=json.loads(mapping)
        self.assertEqual(report['sha256'],hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['image']['sha256'],report['sha256'])
        self.assertEqual(manifest['map_sha256'],hashlib.sha256(mapping.encode()).hexdigest())
        self.assertTrue(manifest['version'].endswith('.callable-reset-v1.candidate1'))
        self.assertEqual((manifest['timing']['base_cycles_max'],manifest['timing']['diagnostic_second_ff_base_cycles_max']),(771,752))
        self.assertFalse(manifest['provider_approved']);self.assertFalse(manifest['execution_verified'])
        with self.assertRaises(AssemblyError):candidate('e8f296d5a8fa693f13b5dd46259eafcb5567e88f')
        def pinned(cmd,**kw):
            return subprocess.CompletedProcess(cmd,0,stdout=b'different')
        with patch('subprocess.run',pinned):
            with self.assertRaises(AssemblyError):verify_checkout(ROOT,PIN)
        for relative in EXTRA_INPUTS:self.assertTrue((ROOT/relative).exists())


if __name__=='__main__':unittest.main()
