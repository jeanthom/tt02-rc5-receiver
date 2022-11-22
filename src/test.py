import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles


segments = [ 63, 6, 91, 79, 102, 109, 124, 7, 127, 103 ]


def forge_rc5(field, control, address, command):
    return (1 << (1+1+5+6)) | field << (5+6+1) | control << (5+6) | address << 6 | command

@cocotb.test()
async def test_7seg(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 1.778, units="ms")
    cocotb.start_soon(clock.start())
    
    dut._log.info("reset")
    dut.rst.value = 1
    dut.i_rc5.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0

    dut._log.info("assert reset state")
    await ClockCycles(dut.clk, 10)
    assert int(dut.segments.value) == segments[0]

    dut._log.info("assert first incrementation")
    rc5 = forge_rc5(1, 0, 0xA, 16)
    print(rc5)
    for i in range(14):
        if rc5 & (1 << 13):
            dut.i_rc5.value = 1
        else:
            dut.i_rc5.value = 0
        rc5 = rc5 << 1
        await Timer(1.778, units='ms')
    rc5 = forge_rc5(1, 1, 0xA, 16)
    print(rc5)
    for i in range(14):
        if rc5 & (1 << 13):
            dut.i_rc5.value = 1
        else:
            dut.i_rc5.value = 0
        rc5 = rc5 << 1
        await Timer(1.778, units='ms')
    await ClockCycles(dut.clk, 5)
    assert int(dut.segments.value) == segments[1]
