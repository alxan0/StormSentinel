from machine import Pin, ADC
import uasyncio as asyncio     
import utime     

LED_CTL = Pin(20, Pin.OUT)       # internal LED
ADC_PIN = ADC(28)                # Analog to digital converter pin
REF_V  = 3.3                     # Pico ADC reference (do not change)
CONVERSION_FACTOR = 0.000050354  # 3.3 V / 65 535 counts

# --- one dust sample ------------------------------------------------------
async def read_dust():    
    """
    Return dust concentration in µg/m³, single sample.
    Timing follows Sharp GP2Y1014AU0F datasheet.
    """
    LED_CTL.value(0)              # IR LED ON (active-LOW)
    utime.sleep_us(280)           # blocking, but only 0.28 ms
    raw = ADC_PIN.read_u16()      # 12-bit value left-aligned to 16 bits
    utime.sleep_us(40)            
    LED_CTL.value(1)              # IR LED OFF
    await asyncio.sleep_ms(10)

    v_adc = raw * CONVERSION_FACTOR  
    v_true  = v_adc * 2
    dust_ugm3 = (v_true - 0.9) / 0.005  
    return max(dust_ugm3, 0)
