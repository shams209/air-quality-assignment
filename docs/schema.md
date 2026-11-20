# Raw Data Schema: Air Quality Dataset

| Column Name | Data Type | Description | Unit | Missing Count |
| :--- | :--- | :--- | :--- | :--- |
| Date | str | The date of the observation | YYYY-MM-DD | 0 |
| City | str | The city where the sensor is located | N/A | 0 |
| AQI | float64 | Air Quality Index (target variable) | Index (0-500) | 111 |
| PM2.5 | float64 | Fine particulate matter | µg/m³ | 97 |
| PM10 | float64 | Coarse particulate matter | µg/m³ | 60 |
| Ozone | float64 | Ozone concentration | ppb | 75 |
| NO2 | float64 | Nitrogen Dioxide concentration | ppb | 93 |
| CO | float64 | Carbon Monoxide concentration | ppm | 162 |
| SO2 | float64 | Sulfur Dioxide concentration | ppb | 129 |
| Temperature | float64 | Ambient temperature | °C | 148 |
| Humidity | float64 | Relative humidity | % | 104 |