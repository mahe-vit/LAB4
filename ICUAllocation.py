class ICUAllocationSystem:

    def __init__(self, icu_beds):
        if icu_beds < 0:
            raise ValueError("Invalid ICU bed availability")

        self.total_beds = icu_beds
        self.available_beds = icu_beds
        self.patients = {}
        self.waiting_list = []

    def validate_patient(self, patient_id, age, oxygen_level,
                         heart_rate, blood_pressure, temperature):

        if not patient_id:
            raise ValueError("Invalid patient ID")

        if patient_id in self.patients:
            raise ValueError("Duplicate patient ID")

        if age <= 0:
            raise ValueError("Invalid age")

        if oxygen_level < 0 or oxygen_level > 100:
            raise ValueError("Invalid oxygen level")

        if heart_rate <= 0:
            raise ValueError("Invalid heart rate")

        if temperature <= 0:
            raise ValueError("Invalid temperature")

        if not blood_pressure:
            raise ValueError("Invalid blood pressure")

    def calculate_priority(self, oxygen_level, heart_rate,
                           blood_pressure, temperature,
                           emergency=False):

        score = 0

        # Oxygen level
        if oxygen_level < 90:
            score += 4
        elif oxygen_level < 94:
            score += 3
        elif oxygen_level < 96:
            score += 2
        else:
            score += 1

        # Heart rate
        if heart_rate > 120 or heart_rate < 50:
            score += 3
        elif heart_rate > 100:
            score += 2
        else:
            score += 1

        # Temperature
        if temperature >= 39 or temperature < 35:
            score += 2
        elif temperature >= 38:
            score += 1

        # Emergency override
        if emergency:
            return score + 10

        return score

    def classify_priority(self, score, emergency=False):

        if emergency:
            return "CRITICAL"

        if score >= 8:
            return "CRITICAL"
        elif score >= 6:
            return "HIGH"
        elif score >= 4:
            return "MEDIUM"
        else:
            return "LOW"

    def admit_patient(self, patient_id, age, oxygen_level,
                      heart_rate, blood_pressure, temperature,
                      conditions=None, emergency=False):

        self.validate_patient(
            patient_id,
            age,
            oxygen_level,
            heart_rate,
            blood_pressure,
            temperature
        )

        score = self.calculate_priority(
            oxygen_level,
            heart_rate,
            blood_pressure,
            temperature,
            emergency
        )

        priority = self.classify_priority(score, emergency)

        patient = {
            "patient_id": patient_id,
            "age": age,
            "oxygen_level": oxygen_level,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "conditions": conditions or [],
            "priority_score": score,
            "priority": priority,
            "emergency": emergency
        }

        self.patients[patient_id] = patient

        # Emergency or critical patients get priority
        if self.available_beds > 0:
            self.available_beds -= 1
            patient["status"] = "ICU ALLOCATED"
        else:
            self.waiting_list.append(patient_id)
            patient["status"] = "WAITING LIST"

        return patient

    def allocate_waiting_patient(self):

        if self.available_beds <= 0 or not self.waiting_list:
            return None

        # Highest priority gets the bed
        self.waiting_list.sort(
            key=lambda pid: self.patients[pid]["priority_score"],
            reverse=True
        )

        patient_id = self.waiting_list.pop(0)

        self.available_beds -= 1
        self.patients[patient_id]["status"] = "ICU ALLOCATED"

        return self.patients[patient_id]

    def release_bed(self):

        if self.available_beds < self.total_beds:
            self.available_beds += 1

        return self.allocate_waiting_patient()


if __name__ == "__main__":

    icu = ICUAllocationSystem(2)

    patient1 = icu.admit_patient(
        "P001",
        65,
        85,
        130,
        "90/60",
        39.5,
        ["Diabetes"]
    )

    patient2 = icu.admit_patient(
        "P002",
        40,
        97,
        75,
        "120/80",
        37.0,
        []
    )

    print("Patient 1 Priority:", patient1["priority"])
    print("Patient 1 Status:", patient1["status"])

    print("Patient 2 Priority:", patient2["priority"])
    print("Patient 2 Status:", patient2["status"])

    print("Available ICU Beds:", icu.available_beds)
    print("Waiting List:", icu.waiting_list)