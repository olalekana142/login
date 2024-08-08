
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $username = $_POST["username"];
    $password = $_POST["password"];
    $confirmPassword = $_POST["confirm_password"];

    // Password confirmation check
    if ($password !== $confirmPassword) {
        // Handle password mismatch error
        echo "Passwords do not match";
        exit;
    }
}