from pydantic  import BaseModel, Field

from datetime import datetime
    
class IndoorSensor(BaseModel):
    '''IndoorSensor model. The range is from 06:00 of 01/01/2023 to 06:00 of 01/01/2024.'''

    TIEMSTAMP: datetime = Field(description="Timestamp of the sensor reading. This is the format: YYYY-MM-DDTHH:MM:SS+TZ")
    SENSOR_ID: int = Field(description="Sensor id. The range is from 1 to 100.")
    TEMPERATUREtemperature: int = Field(description="Indoor temperature. The range is from -20 to 70.")
    HUMIDITY: float = Field(description="Humidity. The range is from 0.0 to 1.0.")
    PIR: int = Field(description="Passive InfraRed. The range is from 0 to 65535.")
    LIGHTING: int = Field(description="Lighting. The maximum value is 60000 lux.")
    CO2: int = Field(description="C02. The range is from 400 ppm to 5000 ppm.")
    TVOC: int = Field(description="Total Volatile Organic Compounds. The range is from 0 ppb to 60000 ppb.")
    BAROMETRIC_PRESSURE: int = Field(description=" Barometric Pressure. The range is from 300 hPa to 1100 hPa.")