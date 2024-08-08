<?php
include "db_connection.php"
?>

<!DOCTYPE html>
<html>
<head>
    <title>Signup Form</title>
    <link rel="stylesheet" href="signup_css.css">
</head>
<body>
    <div class="signup-container">
        <h1>Sign Up</h1>
        <form action="signup_process.php" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>

            <label for="email">Email:</label>
            <input type="text" id="email" name="email" required>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>

            <label for="cpassword">Confirm Password:</label>
            <input type="password" id="password" name="cpassword" required>

            <button type="submit" name="submit">Sign Up</button>

            <a href="index.php" style="color: red">Already have an account? Signin</a>
            
        </form>
    </div>
</body>
</html>
