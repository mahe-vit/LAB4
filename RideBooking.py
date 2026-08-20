import sys


class RideBookingSystem:

    VEHICLES = {
        "Bike": {"base": 30, "rate": 10, "max_passengers": 1},
        "Sedan": {"base": 60, "rate": 15, "max_passengers": 4},
        "SUV": {"base": 100, "rate": 20, "max_passengers": 6},
        "Premium": {"base": 150, "rate": 30, "max_passengers": 4}
    }

    def calculate_fare(
        self,
        customer_id,
        pickup,
        drop,
        distance,
        passengers,
        vehicle_type,
        booking_hour,
        driver_available=True,
        discount=0
    ):
        # Validate vehicle
        if vehicle_type not in self.VEHICLES:
            return {"status": "REJECTED", "reason": "Invalid vehicle type"}

        vehicle = self.VEHICLES[vehicle_type]

        # Validate distance
        if distance <= 0:
            return {"status": "REJECTED", "reason": "Invalid distance"}

        # Validate passengers
        if passengers <= 0 or passengers > vehicle["max_passengers"]:
            return {"status": "REJECTED", "reason": "Invalid passenger count"}

        # Validate booking time
        if booking_hour < 0 or booking_hour > 23:
            return {"status": "REJECTED", "reason": "Invalid booking time"}

        # Check driver
        if not driver_available:
            return {"status": "REJECTED", "reason": "Driver unavailable"}

        # Base fare
        base_fare = vehicle["base"]

        # Distance fare
        distance_fare = distance * vehicle["rate"]

        # Peak-hour surcharge: 7 AM - 10 AM and 5 PM - 9 PM
        peak_surcharge = 0
        if 7 <= booking_hour <= 10 or 17 <= booking_hour <= 21:
            peak_surcharge = (base_fare + distance_fare) * 0.20

        # Night surcharge: 10 PM - 5 AM
        night_surcharge = 0
        if booking_hour >= 22 or booking_hour <= 5:
            night_surcharge = (base_fare + distance_fare) * 0.10

        # Passenger surcharge
        passenger_surcharge = max(0, passengers - 1) * 20

        subtotal = (
            base_fare
            + distance_fare
            + peak_surcharge
            + night_surcharge
            + passenger_surcharge
        )

        # Maximum promotional discount = 20%
        discount = max(0, min(discount, 20))
        promotional_discount = subtotal * (discount / 100)

        final_fare = subtotal - promotional_discount

        return {
            "status": "SUCCESS",
            "customer_id": customer_id,
            "pickup": pickup,
            "drop": drop,
            "vehicle": vehicle_type,
            "base_fare": round(base_fare, 2),
            "distance_fare": round(distance_fare, 2),
            "peak_surcharge": round(peak_surcharge, 2),
            "night_surcharge": round(night_surcharge, 2),
            "passenger_surcharge": round(passenger_surcharge, 2),
            "discount": round(promotional_discount, 2),
            "final_fare": round(final_fare, 2),
            "driver": "Driver Assigned"
        }


def main():
    # Arguments:
    # customer pickup drop distance passengers vehicle hour driver discount

    if len(sys.argv) != 9:
        print("Usage: RideBooking.py customer pickup drop distance passengers vehicle hour driver discount")
        return

    customer_id = sys.argv[1]
    pickup = sys.argv[2]
    drop = sys.argv[3]
    distance = float(sys.argv[4])
    passengers = int(sys.argv[5])
    vehicle_type = sys.argv[6]
    booking_hour = int(sys.argv[7])
    driver_available = sys.argv[8].lower() == "true"

    # Default discount
    discount = 0

    system = RideBookingSystem()

    result = system.calculate_fare(
        customer_id,
        pickup,
        drop,
        distance,
        passengers,
        vehicle_type,
        booking_hour,
        driver_available,
        discount
    )

    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()