import java.io.BufferedReader;
import java.io.InputStreamReader;

public class RideBookingQA {

    static int passed = 0;
    static int failed = 0;

    // Change this only if your Python installation path is different.
    static String PYTHON = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe";

    static String runPython(
            String customer,
            String pickup,
            String drop,
            String distance,
            String passengers,
            String vehicle,
            String hour,
            String driver
    ) throws Exception {

        ProcessBuilder pb = new ProcessBuilder(
                PYTHON,
                "RideBooking.py",
                customer,
                pickup,
                drop,
                distance,
                passengers,
                vehicle,
                hour,
                driver
        );

        pb.redirectErrorStream(true);

        Process process = pb.start();

        BufferedReader reader =
                new BufferedReader(new InputStreamReader(process.getInputStream()));

        StringBuilder output = new StringBuilder();

        String line;

        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }

        process.waitFor();

        return output.toString();
    }


    static void check(String testName, boolean condition) {

        if (condition) {
            System.out.println("[PASS] " + testName);
            passed++;
        } else {
            System.out.println("[FAIL] " + testName);
            failed++;
        }
    }


    // 1. Normal booking
    static void testNormalBooking() throws Exception {

        String output = runPython(
                "C101",
                "Vellore",
                "Katpadi",
                "10",
                "2",
                "Sedan",
                "14",
                "true"
        );

        check(
                "Normal booking",
                output.contains("status=SUCCESS")
                        && output.contains("vehicle=Sedan")
        );
    }


    // 2. Peak-hour booking
    static void testPeakHourBooking() throws Exception {

        String output = runPython(
                "C102",
                "Vellore",
                "Chennai",
                "20",
                "2",
                "Sedan",
                "18",
                "true"
        );

        check(
                "Peak-hour booking",
                output.contains("status=SUCCESS")
                        && !output.contains("peak_surcharge=0.0")
        );
    }


    // 3. Night booking
    static void testNightBooking() throws Exception {

        String output = runPython(
                "C103",
                "Vellore",
                "Katpadi",
                "10",
                "1",
                "Bike",
                "23",
                "true"
        );

        check(
                "Night booking",
                output.contains("status=SUCCESS")
                        && !output.contains("night_surcharge=0.0")
        );
    }


    // 4. Invalid distance
    static void testInvalidDistance() throws Exception {

        String output = runPython(
                "C104",
                "Vellore",
                "Katpadi",
                "0",
                "1",
                "Bike",
                "12",
                "true"
        );

        check(
                "Invalid distance",
                output.contains("status=REJECTED")
                        && output.contains("Invalid distance")
        );
    }


    // 5. Invalid passenger count
    static void testInvalidPassengerCount() throws Exception {

        String output = runPython(
                "C105",
                "Vellore",
                "Katpadi",
                "10",
                "10",
                "Bike",
                "12",
                "true"
        );

        check(
                "Invalid passenger count",
                output.contains("status=REJECTED")
                        && output.contains("Invalid passenger count")
        );
    }


    // 6. Unavailable driver
    static void testUnavailableDriver() throws Exception {

        String output = runPython(
                "C106",
                "Vellore",
                "Katpadi",
                "10",
                "2",
                "Sedan",
                "12",
                "false"
        );

        check(
                "Unavailable driver",
                output.contains("status=REJECTED")
                        && output.contains("Driver unavailable")
        );
    }


    // 7. Maximum discount
    static void testMaximumDiscount() throws Exception {

        String output = runPython(
                "C107",
                "Vellore",
                "Chennai",
                "20",
                "2",
                "Premium",
                "14",
                "true"
        );

        check(
                "Maximum discount calculation",
                output.contains("status=SUCCESS")
                        && output.contains("discount=")
        );
    }


    // 8. Multiple vehicle types
    static void testMultipleVehicleTypes() throws Exception {

        String bike = runPython(
                "C108",
                "Vellore",
                "Katpadi",
                "10",
                "1",
                "Bike",
                "12",
                "true"
        );

        String sedan = runPython(
                "C109",
                "Vellore",
                "Katpadi",
                "10",
                "2",
                "Sedan",
                "12",
                "true"
        );

        String suv = runPython(
                "C110",
                "Vellore",
                "Katpadi",
                "10",
                "3",
                "SUV",
                "12",
                "true"
        );

        String premium = runPython(
                "C111",
                "Vellore",
                "Katpadi",
                "10",
                "2",
                "Premium",
                "12",
                "true"
        );

        check(
                "Multiple vehicle types",
                bike.contains("vehicle=Bike")
                        && sedan.contains("vehicle=Sedan")
                        && suv.contains("vehicle=SUV")
                        && premium.contains("vehicle=Premium")
        );
    }


    // 9. Boundary fare value
    static void testBoundaryFare() throws Exception {

        String output = runPython(
                "C112",
                "Vellore",
                "Katpadi",
                "1",
                "1",
                "Bike",
                "12",
                "true"
        );

        check(
                "Boundary fare value",
                output.contains("status=SUCCESS")
                        && output.contains("final_fare=40.0")
        );
    }


    // 10. Driver allocation logic
    static void testDriverAllocation() throws Exception {

        String output = runPython(
                "C113",
                "Vellore",
                "Chennai",
                "15",
                "2",
                "Sedan",
                "12",
                "true"
        );

        check(
                "Driver allocation logic",
                output.contains("status=SUCCESS")
                        && output.contains("driver=Driver Assigned")
        );
    }


    public static void main(String[] args) throws Exception {

        System.out.println("Ride Booking QA Tests");
        System.out.println("---------------------");

        testNormalBooking();
        testPeakHourBooking();
        testNightBooking();
        testInvalidDistance();
        testInvalidPassengerCount();
        testUnavailableDriver();
        testMaximumDiscount();
        testMultipleVehicleTypes();
        testBoundaryFare();
        testDriverAllocation();

        System.out.println();
        System.out.println("Tests Passed: " + passed);
        System.out.println("Tests Failed: " + failed);

        if (failed == 0) {
            System.out.println("ALL TESTS PASSED");
        } else {
            System.out.println("SOME TESTS FAILED");
        }
    }
}