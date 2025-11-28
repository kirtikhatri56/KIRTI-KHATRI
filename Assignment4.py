Assignment4
KIRTI KHATRI , 2501201005 , BCA(AI/DS), SEM 1 


import pandas as pd
import matplotlib.pyplot as plt

class AirQualityVisualizer:
    def __init__(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
            print("CSV loaded successfully!")
        except FileNotFoundError:
            print("Error: File not found. Check file path.")
        except Exception as e:
            print("Error loading CSV:", e)

    def show_first_n(self, n):
        """Display first n rows"""
        print("\n----- FIRST", n, "RECORDS -----")
        print(self.data.head(n))

    def filter_by_city(self, city):
        """Filter data by city name"""
        filtered = self.data[self.data["Delhi"].str.lower() == city.lower()]
        if filtered.empty:
            print(f" No records found for city: {city}")
        else:
            print(f"\n----- DATA FOR CITY: {city.upper()} -----")
            print(filtered)
        return filtered

    def plot_aqi_trend(self, city):
        """Plot AQI trend for a given city"""
        filtered = self.filter_by_city(city)
        if filtered.empty:
            return
        
        if "Date" not in filtered.columns or "AQI" not in filtered.columns:
            print(" Required columns (Date, AQI) missing in dataset!")
            return

        try:
            # Convert Date column
            filtered["Date"] = pd.to_datetime(filtered["2025-11-24"]])

            # Sort by date
            filtered = filtered.sort_values("Date")

            plt.figure(figsize=(10,5))
            plt.plot(filtered["2025-11-24"], filtered["301"], marker="o")
            plt.title(f"AQI Trend for {city}")
            plt.xlabel("Date")
            plt.ylabel("AQI")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

def main():
    file_path = input("Enter path of AQI CSV file: ")
    visualizer = AirQualityVisualizer(file_path)

    while True:
        menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            n = int(input("Enter N: "))
            visualizer.show_first_n(n)

        elif choice == "2":
            city = input("Delhi: ")
            visualizer.filter_by_city(city)

        elif choice == "3":
            city = input("Delhi: ")
            visualizer.plot_aqi_trend(city)

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
