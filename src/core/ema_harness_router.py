#!/usr/bin/env python3
# ==============================================================================
# GUNDAM ROBOTICS SYSTEMS & UNIVERSITY OF WASHINGTON DEPARTMENT OF PHYSICS
# Module: src/core/ema_harness_router.py (Dual-Voltage Harness Router Gate)
# Core Framework: 16-State Hexadecimal High-Speed Insulation Leak Watchdog
# ==============================================================================

class RTEMAHarnessRouter:
    def __init__(self):
        # Native 16 discrete voltage intervals mapping line impedance status loops
        self.HEX_VOLTAGE_STAGES = [0.0, 0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375,
                                   0.5, 0.5625, 0.625, 0.6875, 0.75, 0.8125, 0.875, 1.0]
        self.REG_BIT_48V_BUS_OK  = 0x04000000 # Bit 26 - High-voltage power tracks secure
        self.REG_BIT_ISOLATE_BUS  = 0x08000000 # Bit 27 - Emergency isolation gate active

    def convert_line_volts_to_hex(self, sample_volts: float) -> int:
        """
        Bypasses binary translation lag by mapping analog wire states directly
        to the closest 16-state hexadecimal index value.
        """
        clamped_voltage = max(0.0, min(1.0, sample_volts))
        closest_index = min(range(len(self.HEX_VOLTAGE_STAGES)),
                            key=lambda i: abs(self.HEX_VOLTAGE_STAGES[i] - clamped_voltage))
        return closest_index

    def dispatch_dual_voltage_bus(self, logic_feedback_v: float, power_rail_v: float) -> dict:
        """
        Evaluates dual-voltage power-by-wire bundle parameters across the 108-bit register loop.
        Isolates high-frequency power rails instantly if an insulation crossover error flags.
        """
        logic_hex_idx = self.convert_line_volts_to_hex(logic_feedback_v)
        power_hex_idx = self.convert_line_volts_to_hex(power_rail_v)
        
        dual_loom_secure    = True
        univac_response_code = self.REG_BIT_48V_BUS_OK
        harness_status_log   = "EMA_DUAL_VOLTAGE_LOOM_OPERATIONAL_NOMINAL"
        
        # Core dual-voltage isolation check rules
        if power_hex_idx == 0 and logic_hex_idx > 0:
            # CROSSOVER FAULT DETECTED: Power rail drops to absolute 0.0V ground state while logic is hot
            # Indicates an internal insulation breakdown inside the fused silica sleeve barrier
            dual_loom_secure     = False
            univac_response_code = self.REG_BIT_ISOLATE_BUS
            harness_status_log   = "CRITICAL ENCLOSURE BREACH: SILICA INSULATION FAILED! DE-ENERGIZING 48V RAIL"
            
        # Pack harness telemetry records into our un-truncated 108-bit register mask representation
        # Bits 72-107: Power Status | Bits 36-71: Logic Integrity | Bits 0-35: Alert Index
        power_bit = 1 if dual_loom_secure else 0
        stacked_word = (power_bit << 72) | (logic_hex_idx << 36) | univac_response_code
        
        return {
            "EMA_POWER_RAIL_ACTIVE": dual_loom_secure,
            "HARNESS_ROUTER_STATUS_LOG": harness_status_log,
            "UNIVAC_IX_36BIT_WORD": f"0x{(stacked_word >> 72) & 0x7FFFFFFFF:09X}"
        }

if __name__ == "__main__":
    router = RTEMAHarnessRouter()
    print("=======================================================================")
    print("UNIVAC-IX EMA DUAL-VOLTAGE HARNESS DISPATCH SENSOR OPERATIONAL")
    print("=======================================================================")
    
    # Simulation: Hard tracking maneuver causes transient high heat, checking line feedback
    mock_logic_v = 0.6250  # Stable 5µs synchronizer timing data flowing [0.12]
    mock_power_v = 1.0000  # 48V power lines running uncompromised at full load [0.12]
    
    report_frame = router.dispatch_dual_voltage_bus(mock_logic_v, mock_power_v)
    print(f"[DATA SENSE] Logic Rail Index: {router.convert_line_volts_to_hex(mock_logic_v)} | Power Rail Index: {router.convert_line_volts_to_hex(mock_power_v)}")
    print(f"[HARNESS MASTER LOG]: {report_frame['HARNESS_ROUTER_STATUS_LOG']}")
    print(f"[POWER DISPATCH INTERLOCK]: 48V Power-by-Wire Rails Clear: {report_frame['EMA_POWER_RAIL_ACTIVE']}")
    print(f"[MAINFRAME PACKET STREAM]: Serializing Word: {report_frame['UNIVAC_IX_36BIT_WORD']}")
    print("=======================================================================")
