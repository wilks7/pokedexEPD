#include "esp_adc_cal.h"    // So we can read the battery voltage

#define BAT_ADC 33 //

uint32_t getBatteryVoltage(void) {
    float v = 0.0;
    int rawADC = analogRead(BAT_ADC);
    Serial.printf("Raw ADC Value: %d\n", rawADC); // Debug line
    v = (readADC_Cal(rawADC)) * 2; // Adjust this multiplier based on your setup
    Serial.printf("Calibrated Voltage: %f mV\n", v); // Debug line
    return v;
}

/**
 * @brief Get the battery voltage via the battery pin
 * 
 * @param adc_raw Raw battery voltage from an adc read.
 * @return uint32_t Battery voltage, e.g. 3999.0
 */
static uint32_t readADC_Cal(const int adc_raw)
{
    esp_adc_cal_characteristics_t adc_chars;
    esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_12, 1100, &adc_chars);
    return (esp_adc_cal_raw_to_voltage(adc_raw, &adc_chars));
}

/**
 * @brief Calculate the appromimate battery life percentage remaining. Returns a value 
 * between 0-100% rounded to the nearest integer.
 * 
 * @param v Voltage reading of the battery.
 * @return int Percentage remaining
 */

int calculateBatteryPercentage(double v)
{
    // this formula was calculated using samples collected from a lipo battery
    double y = -  144.9390 * v * v * v
             + 1655.8629 * v * v
             - 6158.8520 * v
             + 7501.3202;

    // enforce bounds, 0-100
    y = max(y, 0.0);
  
    y = min(y, 100.0);
      
    y = round(y);
     
    return static_cast<int>(y);
}